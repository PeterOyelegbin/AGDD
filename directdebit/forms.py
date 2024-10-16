from django.forms import *
from utils import MANDATE_TYPE, FREQUENCY


class CreateProductForm(Form):
    billerId = CharField(label='Biller ID',
        help_text='This represents the ID for a biller.',
        widget=NumberInput(attrs={'class':'form-control', 'placeholder': 'Enter biller ID'}),
    )
    
    productName = CharField(label='Product Name', min_length=5, max_length=100,
        widget=TextInput(attrs={'class':'form-control', 'placeholder': 'Enter product name'}),
    )


class CreateMandateForm(Form):
    accountNumber = CharField(label='Account Number', min_length=10, max_length=10,
        widget=NumberInput(attrs={'class':'form-control', 'placeholder': 'Enter 10-digit NUBAN'}),
    )
    bankCode = CharField(label='Bank Code', min_length=3, max_length=3,
        help_text='3-digit CBN assigned code of the bank where the account on which a mandate is being created.',
        widget=NumberInput(attrs={'class':'form-control', 'value':'032'}),
        disabled=True
    )
    payerName = CharField(label='Payer Name', max_length=255,
        widget=TextInput(attrs={'class':'form-control'}),
    )
    payerEmail = EmailField(label='Payer Email',
        widget=TextInput(attrs={'class':'form-control'}),
    )
    payerAddress = CharField(label='Payer Address', max_length=255,
        widget=TextInput(attrs={'class':'form-control'}),
    )
    accountName = CharField(label='Account Name', max_length=255,
        widget=TextInput(attrs={'class':'form-control'}),
    )
    amount = DecimalField(label='Amount', max_digits=10, decimal_places=2,
        widget=NumberInput(attrs={'class':'form-control'}),
    )
    narration = CharField(label='Narration', max_length=255,
        widget=TextInput(attrs={'class':'form-control', 'value':'AMFB-cusstomer_name-account_number'}),
        required=False,
    )
    phoneNumber = CharField(label='Phone Number', max_length=15,
        widget=NumberInput(attrs={'class':'form-control'}),
    )
    subscriberCode = CharField(label='Subscriber Code', max_length=255,
        help_text='Unique ID assigned to the Payer by the Payee.',
        widget=TextInput(attrs={'class':'form-control'}),
    )
    startDate = DateField(label='Start Date', input_formats=['%Y-%m-%d'],
        label_suffix=' (YYYY-MM-DD):',
        widget=DateInput(attrs={'class':'form-control', "placeholder":"2023-05-15"}),
    )
    endDate = DateField(label='End Date', input_formats=['%Y-%m-%d'],
        label_suffix=' (YYYY-MM-DD):',
        widget=DateInput(attrs={'class':'form-control', "placeholder":"2024-12-25"}),
    )
    mandateFile = FileField(label='Upload Mandate File',
        label_suffix=' (jpeg, png & pdf):',
        widget=FileInput(attrs={'class':'form-control'}), required=False,
    )
    billerId = CharField(label='Biller ID',
        help_text='ID for a biller.',
        widget=NumberInput(attrs={'class':'form-control'}),
    )


class EMandateForm(Form):
    accountNumber = CharField(label='Account Number', min_length=10, max_length=10,
        widget=NumberInput(attrs={'class':'form-control', 'placeholder': 'Enter 10-digit NUBAN'}),
    )
    bankCode = CharField(label='Bank Code', min_length=3, max_length=3,
        help_text='3-digit CBN assigned code of the bank where the account on which a mandate is being created.',
        widget=NumberInput(attrs={'class':'form-control', 'value':'032'}),
        disabled=True
    )
    payerName = CharField(label='Payer Name', max_length=255,
        widget=TextInput(attrs={'class':'form-control'}),
    )
    payerEmail = EmailField(label='Payer Email',
        widget=TextInput(attrs={'class':'form-control'}),
    )
    payerAddress = CharField(label='Payer Address', max_length=255,
        widget=TextInput(attrs={'class':'form-control'}),
    )
    accountName = CharField(label='Account Name', max_length=255,
        widget=TextInput(attrs={'class':'form-control'}),
    )
    amount = DecimalField(label='Amount', max_digits=10, decimal_places=2,
        widget=NumberInput(attrs={'class':'form-control'}),
    )
    narration = CharField(label='Narration', max_length=255,
        widget=TextInput(attrs={'class':'form-control', 'value':'AMFB-cusstomer_name-account_number'}),
        required=False,
    )
    phoneNumber = CharField(label='Phone Number', max_length=15,
        widget=NumberInput(attrs={'class':'form-control'}),
    )
    subscriberCode = CharField(label='Subscriber Code', max_length=255,
        help_text='Unique ID assigned to the Payer by the Payee.',
        widget=TextInput(attrs={'class':'form-control'}),
    )
    startDate = DateField(label='Start Date', input_formats=['%Y-%m-%d'],
        label_suffix=' (YYYY-MM-DD):',
        widget=DateInput(attrs={'class':'form-control', "placeholder":"2023-05-15"}),
    )
    endDate = DateField(label='End Date', input_formats=['%Y-%m-%d'],
        label_suffix=' (YYYY-MM-DD):',
        widget=DateInput(attrs={'class':'form-control', "placeholder":"2024-12-25"}),
    )
    billerId = CharField(label='Biller ID',
        help_text='ID for a biller.',
        widget=NumberInput(attrs={'class':'form-control'}),
    )
    mandateType = ChoiceField(label='Mandate Type', choices=MANDATE_TYPE,
        help_text='ID for the type of mandate.',
        widget=Select(attrs={'class':'form-control'}),
    )
    frequency = ChoiceField(label='Frequency', choices=FREQUENCY,
        label_suffix=' (Rate at which a customer is debited):',
        widget=Select(attrs={'class':'form-control'}),
    )


class FetchMandateForm(Form):
    billerId = CharField(label='Biller ID',
        help_text='This is the unique ID generated when a biller is created.',
        widget=NumberInput(attrs={'class':'form-control', 'placeholder': 'Enter biller ID'}),
    )
    accountNumber = CharField(label='Account Number', min_length=10, max_length=10,
        widget=NumberInput(attrs={'class':'form-control', 'placeholder': 'Enter 10-digit NUBAN'}),
    )
