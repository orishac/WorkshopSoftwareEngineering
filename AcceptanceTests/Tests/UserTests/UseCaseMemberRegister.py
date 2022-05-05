import unittest

from AcceptanceTests.Bridges.UserBridge.UserProxyBridge import UserProxyBridge
from AcceptanceTests.Bridges.UserBridge.UserRealBridge import UserRealBridge
from Service.MemberService import MemberService
from Service.UserService import UserService
from Service.Response import Response


class UseCaseMemberRegister(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.proxy = UserProxyBridge(UserRealBridge())

    def test_register_positive(self):
        try:
            member = self.proxy.register("user1", "1234", "0500000000", "500", "20", "Israel", "Beer Sheva",
                                             "Ben Gurion", 0, "HaPoalim")
            print(member.getData())
            self.assertTrue(True)
        except:
            self.assertTrue(False)

    def test_register_negative(self):
        self.proxy.register("user2", "1234", "0500000000", "500", "20", "Israel", "Beer Sheva", "Ben Gurion", 0,
                            "HaPoalim")
        self.assertTrue(self.proxy.register("user2", "1234", "0500000000", "500", "20", "Israel", "Beer Sheva",
                                             "Ben Gurion", 0, "HaPoalim").isError())

    # def test_register_negative2(self):
    #     self.assertEqual(self.proxy.register("user2", "", "0500000000", "500", "20", "Israel", "Beer Sheva",
    #                                          "Ben Gurion", 0, "HaPoalim", None), None)


if __name__ == '__main__':
    unittest.main()
