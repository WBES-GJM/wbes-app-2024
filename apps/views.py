from django.http import request
from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.views.generic import TemplateView
from .models import Employee


# ---------------- Users views ----------------

class UserView(LoginRequiredMixin, TemplateView):
    
    @staticmethod
    def get_employee_list(template_name):
        def get(request):
            
            form = None
            context = {
                "employees": Employee.objects.all()
            }
            
            return render(request, template_name, context)
        return get
    
    @staticmethod
    def get_current_user(template_name):
        def get(request):
            
            form = None
            try:
                emp = Employee.objects.filter(user=request.user)[0]
                context = {
                    "user_details": emp,
                    "options": {
                        "disable_message": True
                    }
                }
                return render(request, template_name, context)
            except (Employee.DoesNotExist, IndexError):
                return render(request, template_name, {}) # should raise employee profile not found
            
        return get
    
    def get(self, request, id):
        try:
            emp = Employee.objects.filter(id=id)[0]
            context = {
                "user_details": emp
            }
            if emp.user == request.user:
                context['options'] = {"disable_message": True}
            return render(request, self.template_name, context)
        except (Employee.DoesNotExist, IndexError):
            return render(request, self.template_name, {}) # should raise 404

apps_users_employees_view = UserView.get_employee_list(template_name="apps/users/apps-users-employees.html")
apps_users_employee_view = UserView.as_view(template_name="apps/users/apps-users-profile.html")
apps_users_profile_view = UserView.get_current_user(template_name="apps/users/apps-users-profile.html")


# ---------------- Sample view ----------------
class AppsView(LoginRequiredMixin, TemplateView):
    pass


# Ecommerce
apps_ecommerce_add_product_view = AppsView.as_view(
    template_name="apps/ecommerce/ecommerce-add-product.html"
)
apps_ecommerce_cart_view = AppsView.as_view(
    template_name="apps/ecommerce/ecommerce-cart.html"
)
apps_ecommerce_checkout_view = AppsView.as_view(
    template_name="apps/ecommerce/ecommerce-checkout.html"
)
apps_ecommerce_customers_view = AppsView.as_view(
    template_name="apps/ecommerce/ecommerce-customers.html"
)
apps_ecommerce_orders_view = AppsView.as_view(
    template_name="apps/ecommerce/ecommerce-orders.html"
)
apps_ecommerce_product_detail_view = AppsView.as_view(
    template_name="apps/ecommerce/ecommerce-product-detail.html"
)
apps_ecommerce_products_view = AppsView.as_view(
    template_name="apps/ecommerce/ecommerce-products.html"
)
apps_ecommerce_shops_view = AppsView.as_view(
    template_name="apps/ecommerce/ecommerce-shops.html"
)
apps_ecommerce_seller_view = AppsView.as_view(
    template_name="apps/ecommerce/ecommerce-seller.html"
)
apps_ecommerce_seller_details_view = AppsView.as_view(
    template_name="apps/ecommerce/ecommerce-sale-details.html"
)

apps_calendar_calendar_view = AppsView.as_view(template_name="apps/apps-calendar.html")
apps_chat_chat_view = AppsView.as_view(template_name="apps/apps-chat.html")

# Email
apps_email_inbox_view = AppsView.as_view(template_name="apps/email/apps-email-inbox.html")
apps_email_read_view = AppsView.as_view(template_name="apps/email/apps-email-read.html")

# # Invoices
# apps_invoice_list_view = AppsView.as_view(
#     template_name="apps/invoices/invoice_list.html"
# )
# apps_invoice_details_view = AppsView.as_view(
#     template_name="apps/invoices/invoice_details.html"
# )

# Tasks
apps_tasks_create_view = AppsView.as_view(template_name="apps/tasks/tasks-create.html")
apps_tasks_kanban_view = AppsView.as_view(template_name="apps/tasks/tasks-kanban.html")
apps_tasks_list_view = AppsView.as_view(template_name="apps/tasks/tasks-list.html")


# Contacts
# apps_contacts_usergrid_view = AppsView.as_view(
#     template_name="apps/contacts/apps-contacts-grid.html"
# )


# horizontal
apps_horizontal_horizontal_view = AppsView.as_view(
    template_name="apps/horizontal/horizontal.html"
)
