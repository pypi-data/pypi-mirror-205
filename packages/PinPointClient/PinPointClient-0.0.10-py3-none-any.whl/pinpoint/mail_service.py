import json
import os

import boto3
from botocore.exceptions import ClientError
from pinpoint.exception import PinPointException, ErrorCodes


class EMailService:
    region = "eu-central-1"
    channel_type = "EMAIL"
    aws_access_key_id = None
    aws_secret_access_key = None
    response = None
    sender = None

    def __init__(self, region='eu-central-1', channel_type='EMAIL', sender=None, aws_access=None, aws_secret=None):
        self.region = os.environ.get('REGION', region)
        self.aws_access_key_id = os.environ.get('AWS_ACCESS', aws_access)
        if self.aws_access_key_id is None:
            raise ValueError(ErrorCodes.AWS_ACCESS_KEY_ERROR)
        self.aws_secret_access_key = os.environ.get('AWS_SECRET', aws_secret)
        if self.aws_secret_access_key is None:
            raise ValueError(ErrorCodes.AWS_SECRET_KEY_ERROR)
        self.sender = os.environ.get('EMAIL_SENDER', sender)
        if self.sender is None:
            raise ValueError(ErrorCodes.MAIL_SENDER_ERROR)
        self.channel_type = os.environ.get('CHANNEL_TYPE', channel_type)
        self.client = boto3.client('pinpoint-email', region_name=self.region, aws_access_key_id=self.aws_access_key_id,
                                   aws_secret_access_key=self.aws_secret_access_key)

    def send_via_template(self, to_addresses=None, template_arn=None, data=None):
        try:
            if to_addresses is None or not isinstance(to_addresses, list) or len(to_addresses) == 0:
                raise ValueError(ErrorCodes.DESTINATION_ADDRESS_ERROR)
            if data is None:
                raise ValueError(ErrorCodes.MESSAGE_ERROR)
            destination = {'ToAddresses': to_addresses}
            content = {'Template': {'TemplateArn': template_arn, 'TemplateData': json.dumps(data)}}
            self.response = self.client.send_email(FromEmailAddress=self.sender, Destination=destination,
                                                   Content=content)
            if self.check_send_via_template_status() is False:
                raise PinPointException(ErrorCodes.MAIL_SEND_ERROR)
        except ClientError as e:
            raise PinPointException(e.response['Error']['Message'])

    def check_send_via_template_status(self):
        return self.response is not None and 'MessageId' in self.response
