
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    CustomLoginView,
    register,
    profile,
    create_store,
    store_detail,
    employee_list,
    employee_create,
    employee_update,
    employee_delete,
    home,
    manage_salary,
    salary_changes_list,
    salary_change_update,
    salary_change_delete,
    customer_create,
    customer_list,
    customer_delete,
    customer_update,
    category_create,
    category_list,
    category_update,
    category_delete,
    product_create,
    product_list,
    product_update,
    product_delete,
    supplier_create,
    supplier_list,
    supplier_update,
    supplier_delete,
    record_create,
    record_list,
    record_update,
    record_delete,
    purchase_record_list,
    purchase_record_create,
    purchase_record_update,
    purchase_record_delete,
     sales_invoice_list,
    sales_invoice_create,
    sales_invoice_update,
    sales_invoice_delete,
)

urlpatterns = [
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # Add this line for logout

    path('', home, name='home'),

    # Auth
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),

    # Store
    path('store/create/', create_store, name='create_store'),
    path('store/<int:store_id>/', store_detail, name='store_detail'),

    # Employees
    path('store/<int:store_id>/employees/', employee_list, name='employee_list'),
    path('store/<int:store_id>/employee/create/', employee_create, name='employee_create'),
    path('store/<int:store_id>/employee/<int:pk>/update/', employee_update, name='employee_update'),
    path('store/<int:store_id>/employee/<int:pk>/delete/', employee_delete, name='employee_delete'),
    
    # Salary
    path('store/<int:store_id>/employee/<int:employee_id>/manage_salary/', manage_salary, name='manage_salary'),
    path('salary_changes/', salary_changes_list, name='salary_changes_list'),
    path('employee/<int:employee_id>/salary_change/<int:pk>/update/', salary_change_update, name='salary_change_update'),
    path('employee/<int:employee_id>/salary_change/<int:pk>/delete/', salary_change_delete, name='salary_change_delete'),

    # Categories
    path('store/<int:store_id>/categories/', category_list, name='category_list'),
    path('store/<int:store_id>/category/create/', category_create, name='category_create'),
    path('store/<int:store_id>/category/<int:pk>/update/', category_update, name='category_update'),
    path('store/<int:store_id>/category/<int:pk>/delete/', category_delete, name='category_delete'),

    # Products
    path('store/<int:store_id>/products/', product_list, name='product_list'),
    path('store/<int:store_id>/product/create/', product_create, name='product_create'),
    path('store/<int:store_id>/product/<int:pk>/update/', product_update, name='product_update'),
    path('store/<int:store_id>/product/<int:pk>/delete/', product_delete, name='product_delete'),

    # Suppliers
    path('store/<int:store_id>/suppliers/', supplier_list, name='supplier_list'),
    path('store/<int:store_id>/supplier/create/', supplier_create, name='supplier_create'),
    path('store/<int:store_id>/supplier/<int:pk>/update/', supplier_update, name='supplier_update'),
    path('store/<int:store_id>/supplier/<int:pk>/delete/', supplier_delete, name='supplier_delete'),

    # Customers
    path('store/<int:store_id>/customers/', customer_list, name='customer_list'),
    path('store/<int:store_id>/customer/create/', customer_create, name='customer_create'),
    path('store/<int:store_id>/customer/<int:pk>/update/', customer_update, name='customer_update'),
    path('store/<int:store_id>/customer/<int:pk>/delete/', customer_delete, name='customer_delete'),

    # Records
    path('store/<int:store_id>/records/', record_list, name='record_list'),
    path('store/<int:store_id>/record/create/', record_create, name='record_create'),
    path('store/<int:store_id>/record/<int:pk>/update/', record_update, name='record_update'),
    path('store/<int:store_id>/record/<int:pk>/delete/', record_delete, name='record_delete'),

    # Purchase Records
    path('store/<int:store_id>/purchase_records/', purchase_record_list, name='purchase_record_list'),
    path('store/<int:store_id>/purchase_record/create/', purchase_record_create, name='purchase_record_create'),
    path('store/<int:store_id>/purchase_record/<int:pk>/update/', purchase_record_update, name='purchase_record_update'),
    path('store/<int:store_id>/purchase_record/<int:pk>/delete/', purchase_record_delete, name='purchase_record_delete'),

    # Sales Invoices
    path('store/<int:store_id>/sales_invoices/', sales_invoice_list, name='sales_invoice_list'),
    path('store/<int:store_id>/sales_invoice/create/', sales_invoice_create, name='sales_invoice_create'),
    path('store/<int:store_id>/sales_invoice/<int:pk>/update/', sales_invoice_update, name='sales_invoice_update'),
    path('store/<int:store_id>/sales_invoice/<int:pk>/delete/', sales_invoice_delete, name='sales_invoice_delete'),
]