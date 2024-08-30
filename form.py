#/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.forms import inlineformset_factory
from django.forms import modelformset_factory

class UserRegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = UserX
        fields = ('username', 'type', 'company_name', 'phone_number', 'address' )
        
class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['image', 'name', 'type', 'address', 'phone_number']

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['store', 'first_name', 'last_name', 'position', 'email', 'phone_number', 'salary', 'image']

class SalaryChangeForm(forms.ModelForm):
    CHANGE_CHOICES = [
        ('raise', 'Raise'),
        ('deduction', 'Deduction'),
    ]
    
    class Meta:
        model = SalaryChange
        fields = ['change_type', 'amount', 'note', 'manager']
        widgets = {
            'change_type': forms.RadioSelect(choices='CHANGE_CHOICES'),
            'amount': forms.NumberInput(attrs={'step': '0.01'}),
        }
    
    def __init__(self, *args, **kwargs):
        store_id = kwargs.pop('store_id', None)
        super().__init__(*args, **kwargs)
        if store_id:
            self.fields['manager'].queryset = Employee.objects.filter(store_id=store_id)

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'phone_number', 'whatsapp_number', 'email', 'address', 'website', 'image', 'store']
        widgets = {
            'store': forms.CheckboxSelectMultiple,  # or forms.SelectMultiple
        }
        
class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['store', 'name', 'contact_person', 'phone_number', 'email', 'address', 'business_type', 'image']

class RecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ['record_type', 'description', 'cost', 'payment_method', 'date', 'employee', 'image']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'store', 'suppliers', 'image']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'name', 'image', 'stock_quantity', 'supplier', 'store']  

class PurchaseRecordForm(forms.ModelForm):
    class Meta:
        model = PurchaseRecord
        fields = ['invoice_number', 'store', 'transaction_type', 'payment_method',  'shipment_fees', 'shipment_date', 'supplier', 'extra_fees', 'notes', 'total_amount_paid']

class PurchaseItemForm(forms.ModelForm):
    class Meta:
        model = PurchaseItem
        fields = ['store', 'transaction', 'product', 'category', 'quantity', 'price', 'unit']

class SalesInvoiceForm(forms.ModelForm):
    class Meta:
        model = SalesInvoice
        fields = ['invoice_number', 'store', 'customer', 'prepared_by', 'manager', 'received_by', 'total_amount']

class SalesInvoiceItemForm(forms.ModelForm):
    class Meta:
        model = SalesInvoiceItem
        fields = ['invoice', 'category', 'product', 'unit', 'quantity', 'unit_price', 'total_price']

PurchaseItemFormSet = inlineformset_factory(
    PurchaseRecord,
    PurchaseItem,
    form=PurchaseItemForm,
    fields='__all__',  # Include all fields from PurchaseItem model
    extra=1,  # Number of extra forms to display
    can_delete=True,  # Allow deletion of existing items
)

SalesInvoiceItemFormSet = inlineformset_factory(
    SalesInvoice,
    SalesInvoiceItem,
    form=SalesInvoiceItemForm,
    fields='__all__',  # Include all fields from SalesInvoiceItem model
    extra=1,  # Number of extra forms to display
    can_delete=True,  # Allow deletion of existing items
)
