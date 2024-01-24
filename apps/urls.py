from django.urls import path

from .views import (
    apps_ecommerce_add_product_view,
    apps_ecommerce_cart_view,
    apps_ecommerce_checkout_view,
    apps_ecommerce_customers_view,
    apps_ecommerce_orders_view,
    apps_ecommerce_product_detail_view,
    apps_ecommerce_products_view,
    apps_ecommerce_shops_view,
    apps_ecommerce_seller_view,
    apps_ecommerce_seller_details_view,
    apps_calendar_calendar_view,
    apps_chat_chat_view,
    apps_email_inbox_view,
    apps_email_read_view,
    apps_tasks_create_view,
    apps_tasks_kanban_view,
    apps_tasks_list_view,
    # apps_invoice_list_view,
    # apps_invoice_details_view,
    # apps_contacts_usergrid_view,
    # apps_contacts_userlist_view,
    # apps_contacts_profile_view,
    apps_users_employees_view,
    apps_users_employee_view,
    apps_users_profile_view,
    apps_horizontal_horizontal_view,
)

app_name = "apps"
urlpatterns = [
    # Ecommerce
    path(
        "ecommerce/add-product",
        view=apps_ecommerce_add_product_view,
        name="ecommerce.add_product",
    ),
    path("ecommerce/cart", view=apps_ecommerce_cart_view, name="ecommerce.cart"),
    path(
        "ecommerce/checkout",
        view=apps_ecommerce_checkout_view,
        name="ecommerce.checkout",
    ),
    path(
        "ecommerce/customers",
        view=apps_ecommerce_customers_view,
        name="ecommerce.customers",
    ),
    path("ecommerce/orders", view=apps_ecommerce_orders_view,
         name="ecommerce.orders"),
    path(
        "ecommerce/product-detail",
        view=apps_ecommerce_product_detail_view,
        name="ecommerce.product_detail",
    ),
    path(
        "ecommerce/products",
        view=apps_ecommerce_products_view,
        name="ecommerce.products",
    ),
    path("ecommerce/shops", view=apps_ecommerce_shops_view, name="ecommerce.shops"),
    path("ecommerce/seller", view=apps_ecommerce_seller_view,name="ecommerce.seller"),
    path("ecommerce/seller_details", view=apps_ecommerce_seller_details_view,name="ecommerce.seller_details"),
    # calendar
    path("calendar", view=apps_calendar_calendar_view, name="calendar"),
    # chat
    path("chat", view=apps_chat_chat_view, name="chat"),
    # Email
    path("email/inbox", view=apps_email_inbox_view, name="email.inbox"),
    path("email/read_email", view=apps_email_read_view, name="email.read"),
    # Tasks
    path("tasks/create-task", view=apps_tasks_create_view, name="tasks.create"),
    path("tasks/kanban", view=apps_tasks_kanban_view, name="tasks.kanban"),
    path("tasks/list", view=apps_tasks_list_view, name="tasks.list"),
    # Users
    # path("users/user_grid", view=apps_contacts_usergrid_view, name="users.usergrid"),
    path("users/employees", view=apps_users_employees_view, name="users.employees"),
    path("users/employee/<int:id>", view=apps_users_employee_view, name="users.employee"),
    path("users/profile", view=apps_users_profile_view,name="users.profile"),
    # Horizontal
    path("horizontal", view=apps_horizontal_horizontal_view, name="horizontal"),
]
