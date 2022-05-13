from Business.Managment.UserManagment import UserManagment
from Business.UserPackage.Member import Member
from Business.Managment.MemberManagment import MemberManagment
from Exceptions.CustomExceptions import NoSuchMemberException, NoSuchStoreException
from Business.StorePackage.Product import Product
import threading


class RoleManagment:
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if RoleManagment.__instance is None:
            RoleManagment()
        return RoleManagment.__instance

    def __init__(self):
        """ Virtually private constructor. """
        super().__init__()
        self.__memberManagement = MemberManagment.getInstance()
        self.__productId = 0
        self.__productId_lock = threading.Lock()
        if RoleManagment.__instance is None:
            RoleManagment.__instance = self

    def appointManagerToStore(self, storeID, assignerID, assigneeName):  # check if the asssignee he member and assignerID!!
        try:
            self.__memberManagement.checkOnlineUserFromUser(assignerID)
            assigner = self.__memberManagement.getMembersFromUser().get(assignerID)
            assignee = self.__memberManagement.getMemberByName(assigneeName)
            if assignerID not in self.__memberManagement.getMembers().keys():
                raise NoSuchMemberException("user: " + str(assignerID) + "is not a member")
            return assigner.appointManagerToStore(storeID, assignee)
        except Exception as e:
            raise Exception(e)

    def appointOwnerToStore(self, storeID, assignerID, assigneeName):  # check if the assignee he member and assignerID!!
        try:
            self.__memberManagement.checkOnlineUserFromUser(assignerID)
            assigner = self.__memberManagement.getMembersFromUser().get(assignerID)
            assignee = self.__memberManagement.getMemberByName(assigneeName)
            if assignerID not in self.__memberManagement.getMembersFromUser().keys():
                raise NoSuchMemberException("user: " + str(assignerID) + "is not a member")
            return assigner.appointOwnerToStore(storeID, assignee)
        except Exception as e:
            raise Exception(e)

    def setStockManagerPermission(self, storeID, assignerID, assigneeName):
        try:
            self.__memberManagement.checkOnlineUserFromUser(assignerID)
            assigner = self.__memberManagement.getMembersFromUser().get(assignerID)
            assignee = self.__memberManagement.getMemberByName(assigneeName)
            if assignerID not in self.__memberManagement.getMembersFromUser().keys():
                raise NoSuchMemberException("user: " + str(assignerID) + "is not a member")
            return assigner.setStockManagerPermission(storeID, assignee)
        except Exception as e:
            return e

    def setAppointOwnerPermission(self, storeID, assignerID, assigneeName):
        try:
            self.__memberManagement.checkOnlineUserFromUser(assignerID)
            assigner = self.__memberManagement.getMembersFromUser().get(assignerID)
            assignee = self.__memberManagement.getMemberByName(assigneeName)
            if assignerID not in self.__memberManagement.getMembersFromUser().keys():
                raise NoSuchMemberException("user: " + str(assignerID) + "is not a member")
            return assigner.setAppointOwnerPermission(storeID, assignee)
        except Exception as e:
            raise Exception(e)

    def setChangePermission(self, storeID, assignerID, assigneeName):
        try:
            self.__memberManagement.checkOnlineUserFromUser(assignerID)
            assigner = self.__memberManagement.getMembersFromUser().get(assignerID)
            assignee = self.__memberManagement.getMemberByName(assigneeName)
            if assignerID not in self.__memberManagement.getMembersFromUser().keys():
                raise NoSuchMemberException("user: " + str(assignerID) + "is not a member")
            return assigner.setChangePermission(storeID, assignee)
        except Exception as e:
            raise Exception(e)

    def setRolesInformationPermission(self, storeID, assignerID, assigneeName):
        try:
            self.__memberManagement.checkOnlineUserFromUser(assignerID)
            assigner = self.__memberManagement.getMembersFromUser().get(assignerID)
            assignee = self.__memberManagement.getMemberByName(assigneeName)
            if assignerID not in self.__memberManagement.getMembersFromUser().keys():
                raise NoSuchMemberException("user: " + str(assignerID) + "is not a member")
            return assigner.setRolesInformationPermission(storeID, assignee)
        except Exception as e:
            raise Exception(e)

    def setPurchaseHistoryInformationPermission(self, storeID, assignerID, assigneeName):
        try:
            self.__memberManagement.checkOnlineUserFromUser(assignerID)
            assigner = self.__memberManagement.getMembersFromUser().get(assignerID)
            assignee = self.__memberManagement.getMemberByName(assigneeName)
            if assignerID not in self.__memberManagement.getMembersFromUser().keys():
                raise NoSuchMemberException("user: " + str(assignerID) + "is not a member")
            return assigner.setRolesInformationPermission(storeID, assignee)
        except Exception as e:
            raise Exception(e)

    def addProductToStore(self, storeID, userID, product):
        try:
            self.__memberManagement.checkOnlineUserFromUser(userID)
            member = self.__memberManagement.getMembersFromUser().get(userID)
            if storeID < 0:
                raise NoSuchStoreException("The store id " + storeID + " is not illegal!")
            if userID not in self.__memberManagement.getMembersFromUser().keys():
                raise NoSuchMemberException("user: " + str(userID) + "is not a member")
            member.addProductToStore(storeID, product)
            return product.getProductId()
        except Exception as e:
            raise Exception(e)

    def addProductQuantityToStore(self, storeID, userID, productId, quantity):
        try:
            self.__memberManagement.checkOnlineUserFromUser(userID)
            member = self.__memberManagement.getMembersFromUser().get(userID)
            if userID not in self.__memberManagement.getMembersFromUser().keys():
                raise NoSuchMemberException("user: " + str(userID) + "is not a member")
            return member.addProductQuantityToStore(storeID, productId, quantity)
        except Exception as e:
            raise Exception(e)

    def removeProductFromStore(self, storeID, userID, product):
        try:
            self.__memberManagement.checkOnlineUserFromUser(userID)
            member = self.__memberManagement.getMembersFromUser().get(userID)
            if userID not in self.__memberManagement.getMembersFromUser().keys():
                raise NoSuchMemberException("user: " + str(userID) + "is not a member")
            return member.removeProductFromStore(storeID, product)
        except Exception as e:
            raise Exception(e)

    def updateProductPrice(self, storeID, userID, productId, newPrice):
        try:
            self.__memberManagement.checkOnlineUserFromUser(userID)
            member = self.__memberManagement.getMembersFromUser().get(userID)
            if userID not in self.__memberManagement.getMembersFromUser().keys():
                raise NoSuchMemberException("user: " + str(userID) + "is not a member")
            return member.updateProductPrice(storeID, productId, newPrice)
        except Exception as e:
            raise Exception(e)

    def updateProductName(self, userID, storeID, productID, newName):
        try:
            self.__memberManagement.checkOnlineUserFromUser(userID)
            member = self.__memberManagement.getMembersFromUser().get(userID)
            if userID not in self.__memberManagement.getMembersFromUser().keys():
                raise NoSuchMemberException("user: " + str(userID) + "is not a member")
            return member.updateProductPrice(storeID, productID, newName)
        except Exception as e:
            raise Exception(e)

    def updateProductCategory(self, userID, storeID, productID, newCategory):
        try:
            self.__memberManagement.checkOnlineUserFromUser(userID)
            member = self.__memberManagement.getMembersFromUser().get(userID)
            if userID not in self.__memberManagement.getMembersFromUser().keys():
                raise NoSuchMemberException("user: " + str(userID) + "is not a member")
            return member.updateProductPrice(storeID, productID, newCategory)
        except Exception as e:
            raise Exception(e)

    def getRolesInformation(self, storeID, userID):
        try:
            self.__memberManagement.checkOnlineUserFromUser(userID)
            member = self.__memberManagement.getMembersFromUser().get(userID)
            if userID not in self.__memberManagement.getMembersFromUser().keys():
                raise NoSuchMemberException("user: " + str(userID) + "is not a member")
            return member.getRolesInformation(storeID)
        except Exception as e:
            raise Exception(e)

    def getPurchaseHistoryInformation(self, storeID, userID):
        try:
            self.__memberManagement.checkOnlineUserFromUser(userID)
            member = self.__memberManagement.getMembersFromUser().get(userID)
            if userID not in self.__memberManagement.getMembersFromUser().keys():
                raise NoSuchMemberException("user: " + str(userID) + "is not a member")
            return member.getPurchaseHistoryInformation(storeID)
        except Exception as e:
            raise Exception(e)

    def createProduct(self, userId, storeId, name, price, category, keywords):
        self.__memberManagement.checkOnlineUserFromUser(userId)
        member = self.__memberManagement.getMembersFromUser().get(userId)
        if userId not in self.__memberManagement.getMembersFromUser().keys():
            raise NoSuchMemberException("user: " + str(userId) + "is not a member")
        if not member.isStoreExists(storeId):
            raise NoSuchStoreException("store: " + str(storeId) + "is not exists in the market")
        if name is None:
            raise Exception("product name cannot be None")
        if price <= 0:
            raise Exception("product cannot have negative price")
        if category is None:
            raise Exception("product category cannot be None")
        return Product(self.__getProductId(), storeId, name, price, category, keywords)

    def getUserStores(self, userId):
        self.__memberManagement.checkOnlineUserFromUser(userId)
        member = self.__memberManagement.getMembersFromUser().get(userId)
        if userId not in self.__memberManagement.getMembersFromUser().keys():
            raise NoSuchMemberException("user: " + str(userId) + "is not a member")
        try:
            return member.getUserStores()
        except Exception as e:
            raise Exception(e)

    def removeStoreOwner(self, storeId, assignerId, assigneeName):
        try:
            self.__memberManagement.checkOnlineUserFromUser(assignerId)
            assigner = self.__memberManagement.getMembersFromUser().get(assignerId)
            assignee = self.__memberManagement.getMemberByName(assigneeName)
            if assignerId not in self.__memberManagement.getMembers().keys():
                raise NoSuchMemberException("user: " + str(assignerId) + "is not a member")
            return assigner.removeStoreOwner(storeId, assignee)
        except Exception as e:
            raise Exception(e)

    def removeMember(self, systemManagerName, memberName):
        try:
            system_manager = self.__memberManagement.getSystemManagers().get(systemManagerName)
            self.__memberManagement.checkOnlineUserFromUser(system_manager.getUserID())
            member = self.__memberManagement.getMemberByName(memberName)
            if member not in self.__memberManagement.getMembers().values():
                raise NoSuchMemberException("user: " + str(member.getUserID()) + "is not a member")
            if member.hasRole():
                raise Exception("cannot remove member with a role")
            if system_manager is None:
                raise Exception("user: " + str(systemManagerName) + " is not a system manager")

            if self.__memberManagement.checkOnlineUserFromUser(system_manager.getUserID()):
                self.__memberManagement.removeFromMembers(member.getUserID())
            return True
        except Exception as e:
            raise Exception(e)

    def getAllStoreTransactions(self, systemManagerName):
        try:
            system_manager = self.__memberManagement.getSystemManagers().get(systemManagerName)
            self.__memberManagement.checkOnlineUserFromUser(system_manager.getUserID())
            if system_manager is None:
                raise Exception("user: " + str(systemManagerName) + " is not a system manager")
            return system_manager.getAllStoreTransactions()
        except Exception as e:
            raise Exception(e)

    def getAllUserTransactions(self, systemManagerName):
        try:
            system_manager = self.__memberManagement.getSystemManagers().get(systemManagerName)
            self.__memberManagement.checkOnlineUserFromUser(system_manager.getUserID())
            if system_manager is None:
                raise Exception("user: " + str(systemManagerName) + " is not a system manager")
            return system_manager.getAllUserTransactions()
        except Exception as e:
            raise Exception(e)

    def getStoreTransaction(self, systemManagerName, transactionId):
        try:
            system_manager = self.__memberManagement.getSystemManagers().get(systemManagerName)
            self.__memberManagement.checkOnlineUserFromUser(system_manager.getUserID())
            if system_manager is None:
                raise Exception("user: " + str(systemManagerName) + " is not a system manager")
            return system_manager.getStoreTransaction(transactionId)
        except Exception as e:
            raise Exception(e)

    def getUserTransaction(self, systemManagerName, transactionId):
        try:
            system_manager = self.__memberManagement.getSystemManagers().get(systemManagerName)
            self.__memberManagement.checkOnlineUserFromUser(system_manager.getUserID())
            if system_manager is None:
                raise Exception("user: " + str(systemManagerName) + " is not a system manager")
            return system_manager.getUserTransaction(transactionId)
        except Exception as e:
            raise Exception(e)

    def getStoreTransactionByStoreId(self, systemManagerName, storeId):
        try:
            system_manager = self.__memberManagement.getSystemManagers().get(systemManagerName)
            self.__memberManagement.checkOnlineUserFromUser(system_manager.getUserID())
            if system_manager is None:
                raise Exception("user: " + str(systemManagerName) + " is not a system manager")
            return system_manager.getStoreTransactionByStoreId(storeId)
        except Exception as e:
            raise Exception(e)

    def __getProductId(self):
        with self.__productId_lock:
            pId = self.__productId
            self.__productId += 1
            return pId

