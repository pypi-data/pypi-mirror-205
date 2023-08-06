class ErrorCodes:
    MAIL_SEND_ERROR = 'Email couldn\'t send'
    SMS_SEND_ERROR = 'Sms couldn\'t send!'
    APPLICATION_ID_ERROR = 'You must set application id!'
    AWS_ACCESS_KEY_ERROR = 'You must set aws access key id!'
    AWS_SECRET_KEY_ERROR = 'You must set aws secret access key!'
    MAIL_SENDER_ERROR = 'You must set mail sender!'
    DESTINATION_NUMBER_ERROR = 'You must set phone number to send sms!'
    DESTINATION_ADDRESS_ERROR = 'You must set one email address to send email!'
    MESSAGE_ERROR = 'You must set message which you want to send as sms!'


class PinPointException(Exception):
    def __init__(self, message):
        Exception.__init__(self)
        self.message = message
