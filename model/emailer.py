import keyring
import yagmail


class Emailer:
    sender_address = 'jimkowalski70@gmail.com'
    _sole_instance = None  # the only instance of this class

    @classmethod
    def configure(cls, sender_address):
        # sets the class variable as specified
        cls.sender_address = sender_address

    @classmethod
    def instance(cls):
        # return the only instance of this class
        return cls._sole_instance

    def send_plain_email(self, recipients, subject, message):
        # Note: this is an instance method.
        # recipients must be a collection of email addresses (not TeamMembers!).  
        # subject and message are strings.  
        # Just have this method print f"Sending mail to: {recipient}" for each recipient in the recipients list.  
        # We'll cover sending e-mail from Python later.

        password = keyring.get_password('yagmail_service', Emailer.sender_address)
        if password is None:
            print("Please register your credentials .")
            exit()
        yag = yagmail.SMTP(Emailer.sender_address, password)
        for recipient in recipients:
            try:
                yag.send(to=recipient, subject=subject, contents=message)
                print(f"Email sent to: {recipient}")
            except Exception as e:
                print(f"Failed to send email to {recipient}: {str(e)}")
