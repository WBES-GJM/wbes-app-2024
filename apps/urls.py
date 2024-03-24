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
    
    # calendar
    apps_booking_calendar_view, 
    apps_ajax_get_rooms, 
    apps_ajax_get_client,
    
    apps_chat_chat_view,
    apps_email_inbox_view,
    apps_email_read_view,
    apps_tasks_create_view,
    apps_tasks_kanban_view,
    apps_tasks_list_view,
    # apps_invoice_list_view,
    # apps_invoice_details_view,
    apps_users_view,
    # apps_horizontal_horizontal_view,
)

app_name = "apps"
urlpatterns = [
    # Ecommerce
    
    # ------------------------ BOOKING ------------------------
    path("ecommerce/booking/", view=apps_booking_calendar_view, name="ecommerce.booking"),
    path("ecommerce/booking/<int:room_id>", view=apps_booking_calendar_view, name="ecommerce.booking"),
    path("ecommerce/booking/get_rooms/", view=apps_ajax_get_rooms, name="ecommerce.booking.get.rooms"),
    path("ecommerce/booking/get_client/", view=apps_ajax_get_client, name="ecommerce.booking.get.client"),
    # ---------------------------------------------------------
    
    #  ----------------------- PROFILES -----------------------
    # path("users/myprofile", view=apps_users_myprofile_view, name="users.myprofile"),
    path("profiles/<str:profile>", view=apps_users_view, name="profiles.list"),
    path("profiles/<str:profile>/<int:id>", view=apps_users_view, name="profiles.profile"),
    # ---------------------------------------------------------
    
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
    
    # ------------------------ OLD CALENDAR ------------------------
    # path("calendar/", view=apps_calendar_calendar_view, name="calendar"),
    # path("calendar/<int:room_id>", view=apps_calendar_calendar_view, name="calendar"),
    # path("calendar/get_rooms/", view=apps_ajax_get_rooms, name="calendar.get.rooms"),
    # path("calendar/get_client/", view=apps_ajax_get_client, name="calendar.get.client"),
    # path("calendar/delete/<int:booking_id>", view=apps_ajax_get_client, name="calendar.get.client"),
    # ----------------------------------------------------------
    
    # chat
    path("chat", view=apps_chat_chat_view, name="chat"),
    # Email
    path("email/inbox", view=apps_email_inbox_view, name="email.inbox"),
    path("email/read_email", view=apps_email_read_view, name="email.read"),
    # Tasks
    path("tasks/create-task", view=apps_tasks_create_view, name="tasks.create"),
    path("tasks/kanban", view=apps_tasks_kanban_view, name="tasks.kanban"),
    path("tasks/list", view=apps_tasks_list_view, name="tasks.list"),
    # Horizontal
    # path("horizontal", view=apps_horizontal_horizontal_view, name="horizontal"),
]
