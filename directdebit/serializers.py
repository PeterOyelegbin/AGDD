from rest_framework import serializers
from utils import MANDATE_TYPE, FREQUENCY, MANDATE_STATUS


class CreateMandateSerializer(serializers.Serializer):
    productId = serializers.IntegerField(help_text='This is a system generated unique ID of the product')
    accountNumber = serializers.CharField(min_length=10, max_length=10)
    bankCode = serializers.CharField(min_length=3, max_length=3, help_text='3-digit CBN assigned code of the bank', default='032') #, read_only=True)
    payerName = serializers.CharField(max_length=255)
    payerEmail = serializers.EmailField()
    payerAddress = serializers.CharField(max_length=255)
    accountName = serializers.CharField(max_length=255)
    amount = serializers.CharField(help_text="The amount to be debited in Naira and Kobo.")
    narration = serializers.CharField(help_text='AMFB/customer_name/account_number',)
    phoneNumber = serializers.CharField(max_length=11)
    subscriberCode = serializers.CharField(max_length=255, help_text='Unique ID assigned to the Payer by the Payee.',)
    startDate = serializers.DateTimeField(input_formats=['%Y-%m-%d'], help_text='Start Date (YYYY-MM-DD)')
    endDate = serializers.DateTimeField(input_formats=['%Y-%m-%d'], help_text='End Date (YYYY-MM-DD)')
    mandateImageFile = serializers.FileField(help_text='Upload Mandate File (jpeg, png & pdf)')
    billerId = serializers.IntegerField(help_text='ID for a biller.')


class MandateStatusSerializer(serializers.Serializer):
    mandate_code = serializers.CharField(max_length=255)


class EMandateSerializer(serializers.Serializer):
    productId = serializers.IntegerField(help_text='This is a system generated unique ID of the product')
    billerId = serializers.IntegerField(help_text='ID for a biller.')
    accountNumber = serializers.CharField(min_length=10, max_length=10)
    bankCode = serializers.CharField(min_length=3, max_length=3, help_text='3-digit CBN assigned code of the bank', default='032') #, read_only=True)
    payerName = serializers.CharField(max_length=255)
    payerEmail = serializers.EmailField(max_length=255)
    mandateType = serializers.ChoiceField(choices=MANDATE_TYPE, help_text='(Mandate Type, {1=Direct Debit, 2=Balance Enquiry})')
    payerAddress = serializers.CharField(max_length=255)
    accountName = serializers.CharField(max_length=255)
    amount = serializers.IntegerField(help_text="The amount to be debited in Naira and Kobo.")
    frequency = serializers.ChoiceField(choices=FREQUENCY, help_text='(Rate at which a customer is debited, {1=weekly, 2=2weeks, 4=monthly}):')
    narration = serializers.CharField(max_length=255, help_text='AMFB-customer_name-account_number',)
    phoneNumber = serializers.CharField(max_length=11)
    subscriberCode = serializers.CharField(max_length=255, help_text='Unique ID assigned to the Payer by the Payee.',)
    startDate = serializers.DateTimeField(input_formats=['%Y-%m-%d'], help_text='Start Date (YYYY-MM-DD)')
    endDate = serializers.DateTimeField(input_formats=['%Y-%m-%d'], help_text='End Date (YYYY-MM-DD)')


class FetchMandateSerializer(serializers.Serializer):
    billerId = serializers.CharField(max_length=255)
    accountNumber = serializers.CharField(min_length=10, max_length=10)


class UpdateMandateStatus(serializers.Serializer):
    mandateCode = serializers.CharField(max_length=255)
    billerId = serializers.IntegerField(help_text='ID for a biller.')
    productId = serializers.IntegerField(help_text='This is a system generated unique ID of the product')
    accountNumber = serializers.CharField(min_length=10, max_length=10)
    mandateStatus = serializers.ChoiceField(choices=MANDATE_STATUS, help_text='(Mandate Status, {1=Active, 2=Suspend}):')


class GetProductSerializer(serializers.Serializer):
    billerId = serializers.CharField(max_length=255)

