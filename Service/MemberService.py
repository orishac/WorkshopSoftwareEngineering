from Business.Managment.MemberManagment import MemberManagment
from Business.Managment.RoleManagment import RoleManagment
from Service.Response import Response
from Service.DTO.storeDTO import storeDTO
from Service.DTO.bankDTO import bankDTO
from Service.DTO.adressDTO import adressDTO
from Service.DTO.userTransactionDTO import userTransactionDTO
from Service.DTO.productDTO import productDTO
import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')


class MemberService:

    def __init__(self):
        self.__memberManage = MemberManagment.getInstance()
        self.__roleManagment = RoleManagment.getInstance()

    def createStore(self, storeName, founderId, accountNumber, brunch, country, city, street, apartmentNum, zipCode):
        try:
            bank = self.__memberManage.createBankAcount(accountNumber, brunch)
            address = self.__memberManage.createAddress(country, city, street, apartmentNum, zipCode)
            storeId = self.__memberManage.createStore(storeName, founderId, bank, address)

            dtoBank = bankDTO(accountNumber, brunch)
            dtoAddress = adressDTO(country, city, street, apartmentNum, zipCode)

            logging.info("succeeded create store " + storeName)
            return Response(storeDTO(storeId, storeName, founderId, dtoBank, dtoAddress))

        except Exception as e:
            logging.error("Failed opening a new store")
            return Response(e.__str__())

    def logoutMember(self, userName):
        try:
            isLoggedOut = self.__memberManage.logoutMember(userName)
            logging.info("logout member: " + userName)
            return Response(isLoggedOut)
        except Exception as e:
            logging.error("Failed opening a new store")
            return Response(e.__str__())

    def getMemberTransactions(self, userID):
        try:
            transactions = self.__memberManage.getMemberTransactions(userID)
            logging.info("")
            return Response(self.__makeDtoTransaction(transactions))
        except Exception as e:
            logging.error("Failed opening a new store")
            return Response(e.__str__())

    def __makeDtoTransaction(self, userTransactions):
        transactionList = []
        for ut in userTransactions:
            transactionId = ut.getUserTransactionId()

            storeTransactions = ut.getStoreTransactions()
            storeTransactionsDtoList = []
            for st in storeTransactions.keys():
                storeId = st.getStoreId()
                storeName = st.getStoreName()
                tId = st.getTransactionID()
                pId = st.getPaymentId()
                amount = st.getAmount()
                products = st.getProducts()

                productDTOList = []
                for product in products:
                    productId = product.getProductId()
                    productName = product.getProductName()
                    productPrice = product.getProductPrice()
                    productCategory = product.getProductCategory()
                    productKeywords = product.getProductKeywords()

                    dtoProduct = productDTO(productId, productName, productPrice, productCategory, productKeywords)
                    productDTOList.append(dtoProduct)

                dtoStore = storeDTO(storeId, storeName, )




            paymentStatuses = ut.getPaymentStatus()





            transactionList.append(userTransactionDTO(transactionId, ))