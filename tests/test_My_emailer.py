import unittest
from model.emailer import Emailer

class TestEmailer(unittest.TestCase):
    def test_SendingEmail(self):
        recipients= ['ofamous1@gmail.com']
        Emailer.send_plain_email(self, recipients,'This is a test email','hello world')

if __name__ == '__main__':
    unittest.main()
