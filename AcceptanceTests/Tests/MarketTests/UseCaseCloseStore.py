import unittest
from AcceptanceTests.Bridges.MarketBridge.MarketProxyBridge import MarketProxyBridge
from AcceptanceTests.Bridges.MarketBridge.MarketRealBridge import MarketRealBridge
from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge
from AcceptanceTests.Bridges.UserBridge.UserRealBridge import UserRealBridge


class UseCaseCloseStore(unittest.TestCase):
    # use-case 4.9
    proxy_market = MarketProxyBridge(MarketRealBridge())
    proxy_user = UserProxyBridge(UserRealBridge())


    def setUp(self):

        self.proxy_user.appoint_system_manager("Manager", "1234", "0500000000", 1, 1, "Israel", "Beer Sheva",
                                               "Ben Gurion", 1, 1)
        # username, password, phone, account_number, branch, country, city, street, apartment_num, bank, ICart
        self.__guestId1 = self.proxy_user.login_guest().getData().getUserID()
        self.proxy_user.register("testUser", "1243", "0540000000", 123, 0, "Israel", "Beer Sheva",
                                                "Rager", 1, 0)
        # store_name, founder_id, account_num, branch, country, city, street, apartment_num, zip_code
        self.user_id = self.proxy_user.login_member(self.__guestId1, "testUser", "1243").getData().getUserID()
        self.store_id = self.proxy_user.open_store("testStore", self.user_id, 123, 1, "Israel", "Beer Sheva",
                                                   "Rager", 1, 0).getData().getStoreId()

    def tearDown(self) -> None:
        self.proxy_market.removeStoreForGood(self.user_id, self.store_id)
        self.proxy_user.removeMember("Manager", "testUser")
        self.proxy_user.removeSystemManger_forTests("Manager")

    def test_closeStorePositive(self):
        self.assertTrue(self.proxy_market.close_store(self.store_id, self.user_id).getData())
        self.store_id1 = self.proxy_user.open_store("testStore", self.user_id, 123, 1, "Israel", "Beer Sheva",
                                                    "Rager", 1, 0).getData().getStoreId()
        self.assertTrue(self.proxy_market.close_store(self.store_id1, self.user_id).getData())
        self.assertIsNone(self.proxy_market.get_store_by_ID(self.store_id1).getData())

    def test_closeStorePositive_afterLogOut(self):
        self.proxy_user.logout_member(self.user_id)
        self.__guestId2 = self.proxy_user.login_guest().getData().getUserID()
        self.proxy_user.login_member(self.__guestId2, "testUser", "1243")
        self.assertTrue(self.proxy_market.close_store(self.store_id, self.user_id).getData())
        self.assertIsNone(self.proxy_market.get_store_by_ID(self.store_id).getData())

    def test_closeStoreNegative(self):
        # store doesn't exist
        self.assertTrue(self.proxy_market.close_store(-1, self.user_id).isError())
        self.assertTrue(self.proxy_market.close_store(7, self.user_id).isError())

    def test_closeStore_CloseTwice(self):
        self.assertTrue(self.proxy_market.close_store(self.store_id, self.user_id).getData())
        self.assertTrue(self.proxy_market.close_store(self.store_id, self.user_id).isError())


if __name__ == '__main__':
    unittest.main()
