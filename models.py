# models.py 
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class UserX(AbstractUser):
    OWNER = 'owner'
    SUPPLIER = 'supplier'

    TYPE_CHOICES = [
        (OWNER, 'Owner'),
        (SUPPLIER, 'Supplier'),
    ]

    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.username
     
class Store(models.Model):
    STORE_TYPES = [
        ('store', 'Store'),
        ('market', 'Market'),
    ]
    image = models.ImageField(upload_to='store_images/', blank=True, null=True)  
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=STORE_TYPES)
    address = models.TextField()
    phone_number = models.CharField(max_length=20)
    owner = models.ForeignKey(UserX, on_delete=models.CASCADE, related_name='stores')
    def __str__(self):
        return self.name

class Employee(models.Model):
    store = models.ForeignKey('Store', on_delete=models.CASCADE, related_name='employees')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    salary = models.PositiveIntegerField(default=2000)
    image = models.ImageField(blank=True, null=True) 
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class SalaryChange(models.Model):
    CHANGE_CHOICES = [
        ('raise', 'Raise'),
        ('deduction', 'Deduction'),
    ]
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='salary_changes')
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    change_type = models.CharField(max_length=10, choices=CHANGE_CHOICES, default='raise')
    date = models.DateField(auto_now_add=True)
    note = models.TextField(blank=True, null=True)
    manager = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name='authorized_salary_changes')

    def __str__(self):
        return f"{self.employee} - {self.change_type} on {self.date}"
    
class Supplier(models.Model):
    store = models.ManyToManyField(Store, related_name='suppliers', blank=True)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    whatsapp_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to='suppliers/', blank=True, null=True)
    def __str__(self):
        return self.name

class Customer(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='customers')
    name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField()
    business_type = models.CharField(max_length=100, choices=[('Hotel', 'Hotel'), ('Restaurant', 'Restaurant')])
    image = models.ImageField(upload_to='customer_images/', blank=True, null=True)  # Image field
    def __str__(self):
        return self.name
class Record(models.Model):
    TYPE_CHOICES = [
    ('petrol', 'Petrol'),
    ('rent', 'Rent'),
    ('electricity', 'Electricity'),
    ('water', 'Water'),
    ('equipment', 'Equipment'),
    ('facility', 'Facility'),
    ('car', 'Car'),
    ('other', 'Other'),
]
    record_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    description = models.TextField(blank=True, null=True)  # Optional description for additional details
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, blank=True, null=True)  # Optional payment method
    date = models.DateField(default=timezone.now)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='records')  # Mandatory employee link
    image = models.ImageField(upload_to='record_images/', blank=True, null=True)  # Optional image field   
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='records', null=True, blank=True)  # Optional store link

    
    def __str__(self):
        return f"{self.get_record_type_display()} - {self.date}"

class Category(models.Model):
    name = models.CharField(max_length=100)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='categories', default=0)
    suppliers = models.ManyToManyField(Supplier, related_name='categories', blank=True)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)  # Added image field
    def __str__(self):
        return self.name
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    stock_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Changed from amount to stock_quantity
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, blank=True, null=True)
    store = models.ForeignKey(Store, on_delete=models.SET_NULL, related_name='products', blank=True, null=True)
    def __str__(self):
        return self.name

class PurchaseRecord(models.Model):
    TRANSACTION_TYPES = [
        ('purchase', 'Purchase'),
        ('return', 'Return'),
        ('refund', 'Refund'),
    ]
    invoice_number = models.CharField(max_length=50, blank=True, unique=True)
    store = models.ForeignKey(Store, on_delete=models.SET_NULL, null=True, blank=True)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    payment_method = models.CharField(max_length=50, blank=True, default='')
    transaction_date = models.DateTimeField(auto_now_add=True)
    shipment_fees = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    shipment_date = models.DateField(null=True, blank=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    extra_fees = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notes = models.TextField(blank=True)
    total_amount_paid = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    def __str__(self):
        return f"Invoice {self.invoice_number} - {self.get_transaction_type_display()}"
class PurchaseItem(models.Model):
    UNIT_CHOICES = [
        ('KG', 'Kilogram'),
        ('PKT', 'Packet'),
        ('Bunch', 'Bunch'),
    ]
    store = models.ForeignKey(Store, on_delete=models.SET_NULL, null=True, blank=True)
    transaction = models.ForeignKey(PurchaseRecord, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES, default='KG')
    def __str__(self):
        return f"{self.product.name} - {self.quantity}"
    
class SalesInvoice(models.Model):
    invoice_number = models.CharField(max_length=20, unique=True, blank=True, null=True)  # Unique identifier for the invoice
    store = models.ForeignKey(Store, on_delete=models.SET_NULL, null=True, blank=True)  # Store where the sale happened
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)  # Customer receiving the invoice
    bill_date = models.DateTimeField(auto_now_add=True)  # Date and time of invoice creation
    prepared_by = models.CharField(max_length=100, blank=True, null=True)  # Person who prepared the invoice
    manager = models.CharField(max_length=100, blank=True, null=True)  # Manager responsible for the invoice
    received_by = models.CharField(max_length=100, blank=True, null=True)  # Person who received the invoice
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, blank=True, null=True)  # Total amount of the invoice

    def __str__(self):
        return f'Invoice {self.invoice_number} - {self.customer.name}'

class SalesInvoiceItem(models.Model):
    UNIT_CHOICES = [
        ('KG', 'Kilogram'),
        ('PKT', 'Packet'),
        ('Bunch', 'Bunch'),
    ]
    invoice = models.ForeignKey(SalesInvoice, related_name='items', on_delete=models.CASCADE)  # Invoice this item belongs to
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # Category of the product
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Product being sold
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES, default='KG')  # Unit of measurement for the product
    quantity = models.DecimalField(max_digits=10, decimal_places=2)  # Quantity of the product sold
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)  # Price per unit of the product
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Total price for this item
    def __str__(self):
        return f"{self.product.name} - {self.quantity}"



