import os

import boto3
from botocore.exceptions import ClientError
from pinpoint.exception import PinPointException, ErrorCodes


class GsmService:
    region = "eu-central-1"
    message_type = "TRANSACTIONAL"
    channel_type = "SMS"
    applicationId = None
    aws_access_key_id = None
    aws_secret_access_key = None
    address_dict = dict()
    message_configuration = dict()
    message_request = dict()
    response = None
    destinationNumber = None
    message = None

    def __init__(self, region='eu-central-1', message_type='TRANSACTIONAL', channel_type='SMS',
                 applicationId=None, aws_access=None, aws_secret=None):
        self.region = os.environ.get('REGION', region)
        self.message_type = os.environ.get('PINPOINT_MESSAGE_TYPE', message_type)
        self.applicationId = os.environ.get('PINPOINT_APPLICATION_ID', applicationId)
        if self.applicationId is None:
            raise ValueError(ErrorCodes.APPLICATION_ID_ERROR)
        self.aws_access_key_id = os.environ.get('AWS_ACCESS', aws_access)
        if self.aws_access_key_id is None:
            raise ValueError(ErrorCodes.AWS_ACCESS_KEY_ERROR)
        self.aws_secret_access_key = os.environ.get('AWS_SECRET', aws_secret)
        if self.aws_secret_access_key is None:
            raise ValueError(ErrorCodes.AWS_SECRET_KEY_ERROR)
        self.channel_type = os.environ.get('CHANNEL_TYPE', channel_type)
        self.is_sms_send = False
        self.error_message = ErrorCodes.SMS_SEND_ERROR
        self.client = boto3.client('pinpoint', region_name=self.region, aws_access_key_id=self.aws_access_key_id,
                                   aws_secret_access_key=self.aws_secret_access_key)

    def send(self, phone, message):
        try:
            self.destinationNumber = phone
            if self.destinationNumber is None:
                raise ValueError(ErrorCodes.DESTINATION_NUMBER_ERROR)
            self.message = message
            if self.message is None:
                raise ValueError(ErrorCodes.MESSAGE_ERROR)
            self.address_dict = {self.destinationNumber: {'ChannelType': self.channel_type}}
            self.message_configuration = {'SMSMessage': {'Body': self.message, 'MessageType': self.message_type}}
            self.message_request = {'Addresses': self.address_dict, 'MessageConfiguration': self.message_configuration}
            self.response = self.client.send_messages(ApplicationId=self.applicationId,
                                                      MessageRequest=self.message_request)
            self.is_sms_send = self.check_sms_status()
            if self.is_sms_send is False:
                self.error_message = self.get_error_message()
                raise PinPointException(self.error_message)
        except ClientError as e:
            raise PinPointException(e.response['Error']['Message'])

    def check_sms_status(self):
        return self.response is not None and 'MessageResponse' in self.response and 'Result' in self.response[
            'MessageResponse'] and self.destinationNumber in self.response['MessageResponse'][
                   'Result'] and 'DeliveryStatus' in self.response['MessageResponse']['Result'][
                   self.destinationNumber] and \
               self.response['MessageResponse']['Result'][self.destinationNumber][
                   'DeliveryStatus'] == 'SUCCESSFUL'

    def get_error_message(self):
        return self.response['MessageResponse']['Result'][self.destinationNumber]['StatusMessage']
