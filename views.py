# adc/views.py
from django.shortcuts import render, redirect
from django.views import View
from .form import *
from django.contrib.auth.decorators import login_required
from .models import *  # Import your Owner model
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .form import *
from django.utils import timezone
from django.contrib import messages
from django.db import transaction
from django.urls import reverse_lazy


class CustomLoginView(LoginView):
    template_name = 'login.html'
    success_url = reverse_lazy('profile')

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Redirect to a success page or login page
            return redirect('login')  # Assuming 'login' is your login URL name
    else:
        form = UserRegistrationForm()
    
    return render(request, 'register.html', {'form': form})

@login_required
def profile(request):
    owner = request.user
    stores = owner.stores.all()  # Fetch stores related to the logged-in user
    context = {
        'owner': owner,
        'stores': stores,
    }
    return render(request, 'profile.html', context)

#store 
def create_store(request):
    if request.method == 'POST':
        form = StoreForm(request.POST, request.FILES)
        if form.is_valid():
            store = form.save(commit=False)
            store.owner = request.user  # Assign the current user as the store owner
            store.save()
            return redirect('profile')  # Redirect to profile or any other page after successful creation
    else:
        form = StoreForm()
    
    return render(request, 'create_store.html', {'form': form})


def store_detail(request, store_id):
    store = get_object_or_404(Store, id=store_id)
    context = {
        'store': store,
    }
    return render(request, 'store_detail.html', context)




#employee
@login_required
def employee_list(request, store_id):
    store = get_object_or_404(Store, id=store_id)
    employees = Employee.objects.filter(store=store)
    context = {
        'store': store,
        'employees': employees,
    }
    return render(request, 'employee_list.html', context)

@login_required
def employee_create(request, store_id):
    store = get_object_or_404(Store, id=store_id)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            employee = form.save(commit=False)
            employee.store = store
            employee.save()
            messages.success(request, 'Employee created successfully!')
            return redirect('employee_list', store_id=store_id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = EmployeeForm()

    return render(request, 'employee_form.html', {'form': form, 'store_id': store_id})

@login_required
def employee_update(request, store_id, pk):
    employee = get_object_or_404(Employee, id=pk, store__id=store_id)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employee updated successfully!')
            return redirect('employee_list', store_id=store_id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = EmployeeForm(instance=employee)

    return render(request, 'employee_form.html', {'form': form, 'store_id': store_id})

@login_required
def employee_delete(request, store_id, pk):
    employee = get_object_or_404(Employee, id=pk, store__id=store_id)
    if request.method == 'POST':
        employee.delete()
        messages.success(request, 'Employee deleted successfully!')
        return redirect('employee_list', store_id=store_id)
    return render(request, 'employee_confirm_delete.html', {'employee': employee})


@login_required
def employee_salary_manage(request, store_id, pk):
    employee = get_object_or_404(Employee, id=pk, store__id=store_id)
    
    if request.method == 'POST':
        form = SalaryChangeForm(request.POST)
        if form.is_valid():
            change_type = form.cleaned_data['change_type']
            amount = form.cleaned_data['amount']
            
            if change_type == 'raise':
                employee.salary += amount
            elif change_type == 'deduction':
                employee.salary -= amount
            
            employee.save()
            messages.success(request, 'Salary updated successfully!')
            return redirect('employee_list', store_id=store_id)
    else:
        form = SalaryChangeForm()

    context = {
        'employee': employee,
        'form': form,
        'store_id': store_id,
    }
    return render(request, 'employee_salary_manage.html', context)

@login_required
def manage_salary(request, store_id, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    if request.method == 'POST':
        form = SalaryChangeForm(request.POST, store_id=store_id)
        if form.is_valid():
            salary_change = form.save(commit=False)
            salary_change.employee = employee
            salary_change.save()
            messages.success(request, 'Salary change recorded successfully!')
            return redirect('employee_list', store_id=store_id)
    else:
        form = SalaryChangeForm(store_id=store_id)

    return render(request, 'manage_salary.html', {'form': form, 'employee': employee})


@login_required
def salary_changes_list(request):
    salary_changes = SalaryChange.objects.all().order_by('-date')
    return render(request, 'salary_changes_list.html', {'salary_changes': salary_changes})

@login_required
def salary_change_update(request, employee_id, pk):
    salary_change = get_object_or_404(SalaryChange, id=pk, employee__id=employee_id)
    if request.method == 'POST':
        form = SalaryChangeForm(request.POST, instance=salary_change)
        if form.is_valid():
            form.save()
            messages.success(request, 'Salary change updated successfully!')
            return redirect('salary_changes_list')
    else:
        form = SalaryChangeForm(instance=salary_change)

    return render(request, 'manage_salary.html', {'form': form, 'employee': salary_change.employee})

@login_required
def salary_change_delete(request, employee_id, pk):
    salary_change = get_object_or_404(SalaryChange, id=pk, employee__id=employee_id)
    if request.method == 'POST':
        salary_change.delete()
        messages.success(request, 'Salary change deleted successfully!')
        return redirect('salary_changes_list')
    return render(request, 'salary_change_confirm_delete.html', {'salary_change': salary_change})

# Categories
@login_required
def category_list(request, store_id):
    store = get_object_or_404(Store, id=store_id)
    categories = Category.objects.filter(store=store)
    context = {
        'store': store,
        'categories': categories,
    }
    return render(request, 'category_list.html', context)

@login_required
def category_create(request, store_id):
    store = get_object_or_404(Store, id=store_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.store = store
            category.save()
            messages.success(request, 'Category created successfully!')
            return redirect('category_list', store_id=store_id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CategoryForm()

    return render(request, 'category_form.html', {'form': form, 'store_id': store_id})

@login_required
def category_update(request, store_id, pk):
    category = get_object_or_404(Category, id=pk, store__id=store_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('category_list', store_id=store_id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CategoryForm(instance=category)

    return render(request, 'category_form.html', {'form': form, 'store_id': store_id})

@login_required
def category_delete(request, store_id, pk):
    category = get_object_or_404(Category, id=pk, store__id=store_id)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully!')
        return redirect('category_list', store_id=store_id)
    return render(request, 'category_confirm_delete.html', {'category': category})

# Products
@login_required
def product_list(request, store_id):
    store = get_object_or_404(Store, id=store_id)
    products = Product.objects.filter(store=store)
    context = {
        'store': store,
        'products': products,
    }
    return render(request, 'product_list.html', context)

@login_required
def product_create(request, store_id):
    store = get_object_or_404(Store, id=store_id)
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.store = store
            product.save()
            messages.success(request, 'Product created successfully!')
            return redirect('product_list', store_id=store_id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProductForm()

    return render(request, 'product_form.html', {'form': form, 'store_id': store_id})

@login_required
def product_update(request, store_id, pk):
    product = get_object_or_404(Product, id=pk, store__id=store_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('product_list', store_id=store_id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProductForm(instance=product)

    return render(request, 'product_form.html', {'form': form, 'store_id': store_id})

@login_required
def product_delete(request, store_id, pk):
    product = get_object_or_404(Product, id=pk, store__id=store_id)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('product_list', store_id=store_id)
    return render(request, 'product_confirm_delete.html', {'product': product})

# Suppliers
@login_required
def supplier_list(request, store_id):
    store = get_object_or_404(Store, id=store_id)
    suppliers = Supplier.objects.filter(store=store)
    context = {
        'store': store,
        'suppliers': suppliers,
    }
    return render(request, 'supplier_list.html', context)

@login_required
def supplier_create(request, store_id):
    store = get_object_or_404(Store, id=store_id)
    if request.method == 'POST':
        form = SupplierForm(request.POST, request.FILES)
        if form.is_valid():
            supplier = form.save(commit=False)
            supplier.save()
            # Assign the store(s) to the supplier
            # Make sure to set the correct stores
            supplier.store.set(form.cleaned_data['stores'])  # Correct way to set many-to-many relationships
            messages.success(request, 'Supplier created successfully!')
            return redirect('supplier_list', store_id=store_id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SupplierForm()

    return render(request, 'supplier_form.html', {'form': form, 'store_id': store_id})

@login_required
def supplier_update(request, store_id, pk):
    supplier = get_object_or_404(Supplier, id=pk, store__id=store_id)
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            messages.success(request, 'Supplier updated successfully!')
            return redirect('supplier_list', store_id=store_id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SupplierForm(instance=supplier)

    return render(request, 'supplier_form.html', {'form': form, 'store_id': store_id})

@login_required
def supplier_delete(request, store_id, pk):
    supplier = get_object_or_404(Supplier, id=pk, store__id=store_id)
    if request.method == 'POST':
        supplier.delete()
        messages.success(request, 'Supplier deleted successfully!')
        return redirect('supplier_list', store_id=store_id)
    return render(request, 'supplier_confirm_delete.html', {'supplier': supplier})

# Customers
@login_required
def customer_list(request, store_id):
    store = get_object_or_404(Store, id=store_id)
    customers = Customer.objects.filter(store=store)
    context = {
        'store': store,
        'customers': customers,
    }
    return render(request, 'customer_list.html', context)

@login_required
def customer_create(request, store_id):
    store = get_object_or_404(Store, id=store_id)
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.store = store
            customer.save()
            messages.success(request, 'Customer created successfully!')
            return redirect('customer_list', store_id=store_id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomerForm()

    return render(request, 'customer_form.html', {'form': form, 'store_id': store_id})

@login_required
def customer_update(request, store_id, pk):
    customer = get_object_or_404(Customer, id=pk, store__id=store_id)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer updated successfully!')
            return redirect('customer_list', store_id=store_id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomerForm(instance=customer)

    return render(request, 'customer_form.html', {'form': form, 'store_id': store_id})

@login_required
def customer_delete(request, store_id, pk):
    customer = get_object_or_404(Customer, id=pk, store__id=store_id)
    if request.method == 'POST':
        customer.delete()
        messages.success(request, 'Customer deleted successfully!')
        return redirect('customer_list', store_id=store_id)
    return render(request, 'customer_confirm_delete.html', {'customer': customer})

# Records
@login_required
def record_list(request, store_id):
    store = get_object_or_404(Store, id=store_id)
    records = Record.objects.filter(store=store)
    context = {
        'store': store,
        'records': records,
    }
    return render(request, 'record_list.html', context)

@login_required
def record_create(request, store_id):
    store = get_object_or_404(Store, id=store_id)
    if request.method == 'POST':
        form = RecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.store = store
            record.save()
            messages.success(request, 'Record created successfully!')
            return redirect('record_list', store_id=store_id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RecordForm()

    return render(request, 'record_form.html', {'form': form, 'store_id': store_id})

@login_required
def record_update(request, store_id, pk):
    record = get_object_or_404(Record, id=pk, store__id=store_id)
    if request.method == 'POST':
        form = RecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, 'Record updated successfully!')
            return redirect('record_list', store_id=store_id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RecordForm(instance=record)

    return render(request, 'record_form.html', {'form': form, 'store_id': store_id})

@login_required
def record_delete(request, store_id, pk):
    record = get_object_or_404(Record, id=pk, store__id=store_id)
    if request.method == 'POST':
        record.delete()
        messages.success(request, 'Record deleted successfully!')
        return redirect('record_list', store_id=store_id)
    return render(request, 'record_confirm_delete.html', {'record': record})


@login_required
def purchase_record_list(request, store_id):
    store = get_object_or_404(Store, id=store_id)
    records = PurchaseRecord.objects.filter(store=store)
    return render(request, 'purchase_record_list.html', {'store': store, 'records': records})

@login_required
def purchase_record_create(request, store_id):
    store = get_object_or_404(Store, id=store_id)
    if request.method == 'POST':
        record_form = PurchaseRecordForm(request.POST)
        item_formset = PurchaseItemFormSet(request.POST, request.FILES)
        if record_form.is_valid() and item_formset.is_valid():
            record = record_form.save(commit=False)
            record.store = store
            record.save()
            item_formset.instance = record
            item_formset.save()
            messages.success(request, 'Purchase record created successfully!')
            return redirect('purchase_record_list', store_id=store_id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        record_form = PurchaseRecordForm()
        item_formset = PurchaseItemFormSet()

    return render(request, 'purchase_record_form.html', {
        'transaction_form': record_form,
        'product_formset': item_formset
    })

@login_required
def purchase_record_update(request, store_id, pk):
    store = get_object_or_404(Store, id=store_id)
    record = get_object_or_404(PurchaseRecord, id=pk, store=store)
    if request.method == 'POST':
        record_form = PurchaseRecordForm(request.POST, instance=record)
        item_formset = PurchaseItemFormSet(request.POST, request.FILES, instance=record)
        if record_form.is_valid() and item_formset.is_valid():
            record = record_form.save()
            item_formset.save()
            messages.success(request, 'Purchase record updated successfully!')
            return redirect('purchase_record_list', store_id=store_id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        record_form = PurchaseRecordForm(instance=record)
        item_formset = PurchaseItemFormSet(instance=record)

    return render(request, 'purchase_record_form.html', {
        'transaction_form': record_form,
        'product_formset': item_formset
    })

@login_required
def purchase_record_delete(request, store_id, pk):
    store = get_object_or_404(Store, id=store_id)
    record = get_object_or_404(PurchaseRecord, id=pk, store=store)
    if request.method == 'POST':
        record.delete()
        messages.success(request, 'Purchase record deleted successfully!')
        return redirect('purchase_record_list', store_id=store_id)
    return render(request, 'purchase_record_confirm_delete.html', {'record': record})
SalesInvoiceItemFormSet = inlineformset_factory(
    SalesInvoice,
    SalesInvoiceItem,
    form=SalesInvoiceItemForm,
    extra=1,
    can_delete=True
)


@login_required
def sales_invoice_list(request, store_id):
    store = get_object_or_404(Store, id=store_id)
    invoices = SalesInvoice.objects.filter(store=store)
    return render(request, 'sales_invoice_list.html', {'store': store, 'invoices': invoices})

@login_required
def sales_invoice_create(request, store_id):
    store = get_object_or_404(Store, id=store_id)
    if request.method == 'POST':
        invoice_form = SalesInvoiceForm(request.POST)
        item_formset = SalesInvoiceItemFormSet(request.POST, request.FILES)
        if invoice_form.is_valid() and item_formset.is_valid():
            invoice = invoice_form.save(commit=False)
            invoice.store = store
            invoice.save()
            item_formset.instance = invoice
            item_formset.save()
            messages.success(request, 'Sales invoice created successfully!')
            return redirect('sales_invoice_list', store_id=store_id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        invoice_form = SalesInvoiceForm()
        item_formset = SalesInvoiceItemFormSet()

    return render(request, 'sales_invoice_form.html', {
        'invoice_form': invoice_form,
        'item_formset': item_formset
    })

@login_required
def sales_invoice_update(request, store_id, pk):
    store = get_object_or_404(Store, id=store_id)
    invoice = get_object_or_404(SalesInvoice, id=pk, store=store)
    if request.method == 'POST':
        invoice_form = SalesInvoiceForm(request.POST, instance=invoice)
        item_formset = SalesInvoiceItemFormSet(request.POST, request.FILES, instance=invoice)
        if invoice_form.is_valid() and item_formset.is_valid():
            invoice = invoice_form.save()
            item_formset.save()
            messages.success(request, 'Sales invoice updated successfully!')
            return redirect('sales_invoice_list', store_id=store_id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        invoice_form = SalesInvoiceForm(instance=invoice)
        item_formset = SalesInvoiceItemFormSet(instance=invoice)

    return render(request, 'sales_invoice_form.html', {
        'invoice_form': invoice_form,
        'item_formset': item_formset
    })

@login_required
def sales_invoice_delete(request, store_id, pk):
    store = get_object_or_404(Store, id=store_id)
    invoice = get_object_or_404(SalesInvoice, id=pk, store=store)
    if request.method == 'POST':
        invoice.delete()
        messages.success(request, 'Sales invoice deleted successfully!')
        return redirect('sales_invoice_list', store_id=store_id)
    return render(request, 'sales_invoice_confirm_delete.html', {'invoice': invoice})