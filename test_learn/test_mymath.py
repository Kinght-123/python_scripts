import unittest
from mymath import BankAccount


class TestBankAccount(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("开始银行账户测试")

    @classmethod
    def tearDownClass(cls):
        print("结束银行账户测试")

    def setUp(self):
        # 每个测试前创建一个新的银行账户实例
        self.account = BankAccount("Alice", balance=100)

    def tearDown(self):
        self.account = None

    def test_deposit(self):
        new_balance = self.account.deposit(50)
        self.assertEqual(new_balance, 150)
        # 检验存款后的余额
        self.assertEqual(self.account.balance, 150)

    def test_withdraw(self):
        new_balance = self.account.withdraw(30)
        self.assertEqual(new_balance, 70)
        # 收取全部存款时，余额应为0
        self.assertEqual(self.account.balance, 70)

    def test_invalid_deposit(self):
        with self.assertRaises(ValueError):
            self.account.deposit(-20)

    def test_invalid_withdraw(self):
        with self.assertRaises(ValueError):
            self.account.withdraw(200)


if __name__ == '__main__':
    unittest.main()
