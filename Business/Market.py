import uuid

import zope

from Business.StorePackage.Store import Store
from Exceptions.CustomExceptions import NotOnlineException, ProductException, QuantityException, \
    EmptyCartException, PaymentException, NoSuchStoreException
from interfaces.IMarket import IMarket
from interfaces.IStore import IStore
from interfaces.IMember import IMember
from interfaces.IUser import IUser
from Payment.PaymentStatus import PaymentStatus
from Payment.PaymentDetails import PaymentDetails
from Payment.paymentlmpl import Paymentlmpl
from Business.Transactions.StoreTransaction import StoreTransaction
from Business.Transactions.UserTransaction import UserTransaction
from zope.interface import implements
from typing import Dict
import threading


@zope.interface.implementer(IMarket)
class Market:
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if Market.__instance is None:
            Market()
        return Market.__instance

    def __init__(self):
        """ Virtually private constructor. """
        self.__stores: Dict[int, IStore] = {}  # <id,Store> should check how to initial all the stores into dictionary
        self.__globalStore = 0
        self._transactionIdCounter = 0
        self.__storeId_lock = threading.Lock()
        self.__transactionId_lock = threading.Lock()
        if Market.__instance is None:
            Market.__instance = self

    def createStore(self, storeName, user, bank, address):  # change test!
        storeID = self.__getGlobalStoreId()
        newStore = Store(storeID, storeName, user, bank, address)
        self.__stores[storeID] = newStore
        return newStore.getStoreId()

    def addProductToCart(self, user, storeID, productID, quantity):  # Tested
        try:
            if self.__stores.get(storeID).hasProduct(productID) is None:
                raise ProductException("The product id " + productID + " not in market!")
            if self.__stores.get(storeID).addProductToBag(productID, quantity):
                product = self.__stores.get(storeID).getProduct(productID)
                user.getCart().addProduct(storeID, product, quantity)
                return True
            else:
                raise QuantityException("The quantity " + quantity + " is not available")
        except Exception as e:
            raise Exception(e)

    def removeProductFromCart(self, storeID, user, productId):  # Tested
        try:
            quantity = user.getCart().removeProduct(storeID, productId)
            self.__stores.get(storeID).removeProductFromBag(productId, quantity)
            return True
        except Exception as e:
            raise Exception(e)

    def updateProductFromCart(self, user, storeID, productId, quantity):  # UnTested
        try:
            if self.__stores.get(storeID).hasProduct(productId):
                raise ProductException("The product id " + productId + " not in market!")
            if quantity > 0:
                return self.addProductToCart(user, storeID, productId, quantity)
            else:
                return self.removeProductFromBag(productId, quantity)
        except Exception as e:
            return e

    def getProductByCategory(self, category):
        productsInStores = []
        keys = self.__stores.keys()
        for i in keys:
            products_list_per_Store = self.__stores.get(i).getProductsByCategory(category)
            if products_list_per_Store is not None:
                productsInStores += products_list_per_Store
        return productsInStores

    def getProductsByName(self, nameProduct):
        productsInStores = []
        keys = self.__stores.keys()
        for i in keys:
            products_list_per_Store = self.__stores.get(i).getProductsByName(nameProduct)
            if products_list_per_Store is not None:
                productsInStores += products_list_per_Store
        return productsInStores

    def getProductByKeyWord(self, keyword):
        productsInStores = []
        keys = self.__stores.keys()
        for i in keys:
            products_list_per_Store = self.__stores.get(i).getProductsByKeyword(keyword)
            if products_list_per_Store is not None:
                productsInStores += products_list_per_Store
        return productsInStores

    def getProductByPriceRange(self, minPrice, highPrice):
        productsInStores = []
        keys = self.__stores.keys()
        for i in keys:
            products_list_per_Store = self.__stores.get(i).getProductsByPriceRange(minPrice, highPrice)
            if products_list_per_Store is not None:
                productsInStores += products_list_per_Store
        return productsInStores

    def addTransaction(self, storeID, transaction):
        try:
            self.__stores.get(storeID).addTransaction(transaction)
        except Exception as e:
            raise Exception(e)

    def removeTransaction(self, storeID, transactionId):
        try:
            self.__stores.get(storeID).removeTransaction(transactionId)
        except Exception as e:
            raise Exception(e)

    def purchaseCart(self, user, bank):
        try:
            cart = user.getCart()
            if cart.isEmpty():
                raise EmptyCartException("cannot purchase an empty cart")

            storeFailed = []
            storeTransactions: Dict[int: StoreTransaction] = {}
            totalAmount = 0.0
            paymentStatuses: Dict[int: PaymentStatus] = {}

            for storeId in cart.getAllProductsByStore().keys():  # pay for each store
                storeName = self.__stores.get(storeId).getStoreName()
                storeBank = self.__stores.get(storeId).getStoreBankAccount()
                storeAmount = cart.calcSumOfBag(storeId)
                totalAmount += storeAmount
                paymentDetails = PaymentDetails(user.getUserID(), bank, storeBank, storeAmount)
                paymentStatus = Paymentlmpl.getInstance().createPayment(paymentDetails)
                user.addPaymentStatus(paymentStatus)
                paymentStatuses[paymentStatus.getPaymentId()] = paymentStatus

                if paymentStatus.getStatus() == "payment succeeded":
                    productsInStore = cart.getAllProductsByStore()[storeId]

                    user.addPaymentStatus(paymentStatus)
                    transactionId = self.__getTransactionId()
                    storeTransaction: StoreTransaction = StoreTransaction(storeId, storeName, transactionId,
                                                                          paymentStatus.getPaymentId(), productsInStore,
                                                                          storeAmount)
                    self.__stores.get(storeId).addTransaction(storeTransaction)
                    storeTransactions[storeId] = storeTransaction
                else:
                    storeFailed.append(storeId)

            userPaymentId = Paymentlmpl.getInstance().getPaymentId()
            user.addTransaction(UserTransaction(user.getUserID(), self.__getTransactionId(), storeTransactions, userPaymentId))
            if len(storeFailed) == 0:
                return True
            else:
                raise PaymentException("failed to pay in stores: " + str(storeFailed))

            # here need to add delivary
        except Exception as e:
            raise Exception(e)

    # need to delete that function
    def cancelPurchaseCart(self, user, transactionId):
        try:
            userTransaction = user.getTransaction(transactionId)

            for storeId in userTransaction.getStoreTransactions().keys():
                store: Store = self.__stores.get(storeId)
                storeTransaction: StoreTransaction = userTransaction.getStoreTransactions()[storeId]

                for product in storeTransaction.getProduts().keys():
                    quantity = storeTransaction.getProduts()[product]
                    store.addProductQuantityToStore(user.getUserID(), product.getProductId(), quantity)

                store.removeTransaction(storeTransaction.getTransactionID())

            for paymentStatus in userTransaction.getPaymentStatus():
                user.removePaymentStatus(paymentStatus)

        except Exception as e:
            raise Exception(e)

    #  actions of roles - role managment
    def appointManagerToStore(self, storeID, assigner, assignee):  # Tested
        try:
            self.__stores.get(storeID).appointManagerToStore(assigner, assignee)
            return True
        except Exception as e:
            raise Exception(e)

    def appointOwnerToStore(self, storeID, assigner, assignee):  # unTested
        try:
            self.__stores.get(storeID).appointOwnerToStore(assigner, assignee)
            return True
        except Exception as e:
            raise Exception(e)

    def setStockManagerPermission(self, storeID, assigner, assignee):  # Tested
        try:
            self.__stores.get(storeID).setStockManagementPermission(assigner, assignee)
            return True
        except Exception as e:
            raise Exception(e)

    def setAppointOwnerPermission(self, storeID, assigner, assignee):  # Tested
        try:
            self.__stores.get(storeID).setAppointOwnerPermission(assigner, assignee)
            return True
        except Exception as e:
            raise Exception(e)

    def setChangePermission(self, storeID, assigner, assignee):
        try:
            self.__stores.get(storeID).setChangePermission(assigner, assignee)
        except Exception as e:
            raise Exception(e)

    def setRolesInformationPermission(self, storeID, assigner, assignee):
        try:
            self.__stores.get(storeID).setRolesInformationPermission(assigner, assignee)
        except Exception as e:
            raise Exception(e)

    def setPurchaseHistoryInformationPermission(self, storeID, assigner, assignee):
        try:
            self.__stores.get(storeID).setPurchaseHistoryInformationPermission(assigner, assignee)
        except Exception as e:
            raise Exception(e)

    def addProductToStore(self, storeID, user, product):  # Tested
        try:
            self.__stores.get(storeID).addProductToStore(user, product)
            return True
        except Exception as e:
            raise Exception(e)

    def updateProductPrice(self, storeID, user, productId, mewPrice):
        try:
            self.__stores.get(storeID).updateProductPrice(user, productId, mewPrice)
        except Exception as e:
            raise Exception(e)

    def addProductQuantityToStore(self, storeID, user, productId, quantity):
        try:
            self.__stores.get(storeID).addProductQuantityToStore(user, productId, quantity)
        except Exception as e:
            raise Exception(e)

    def removeProductFromStore(self, storeID, user, productId):
        try:
            self.__stores.get(storeID).removeProductFromStore(user, productId)
        except Exception as e:
            raise Exception(e)

    def printRolesInformation(self, storeID, user):
        try:
            return self.__stores.get(storeID).PrintRolesInformation(user)
        except Exception as e:
            raise Exception(e)

    def printPurchaseHistoryInformation(self, storeID, user):
        try:
            self.__stores.get(storeID).printPurchaseHistoryInformation(user)
        except Exception as e:
            raise Exception(e)

    def getStoreByName(self, store_name):
        store_collection = []
        store_names = self.__stores.keys()
        for s in store_names:
            if self.__stores.get(s).getName() == store_name:
                store_collection.append(self.__stores.get(s))
        return store_collection

    def getStoreById(self, id_store):  # maybe should be private
        return self.__stores.get(id_store)

    def getUserByName(self, userName):
        return self.__activeUsers.get(userName)

    def getStores(self):
        return self.__stores

    # need to add to the service
    def removeStore(self, storeID, user):
        try:
            if self.__stores.get(storeID) is None:
                raise NoSuchStoreException("Store " + str(storeID) + " is not exist in system!")
            # for user in self.__activeUsers.values():
            #    user.getCart().removeBag(storeID)
            self.__stores.pop(storeID)
            return "Store removed successfully!"
        except Exception as e:
            return e

    def loginUpdates(self, user):  # we need to check if all the store exist if not we remove all the products from
        # the user that get in the system!
        for storeID in user.getCart().getAllBags().keys():
            if self.__stores.get(storeID) is None:
                user.getCart().removeBag(storeID)

    def updateProductName(self, user, storeID, productID, newName):
        try:
            self.__stores.get(storeID).updateProductName(user, productID, newName)
        except Exception as e:
            raise Exception(e)

    def updateProductCategory(self, user, storeID, productID, newCategory):
        try:
            self.__stores.get(storeID).updateProductCategory(user, productID, newCategory)
        except Exception as e:
            raise Exception(e)

    def __getGlobalStoreId(self):
        with self.__storeId_lock:
            storeId = self.__globalStore
            self.__globalStore += 1
            return storeId

    def __getTransactionId(self):
        with self.__transactionId_lock:
            transactionId = self._transactionIdCounter
            self._transactionIdCounter += 1
            return transactionId
