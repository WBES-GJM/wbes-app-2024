import calendar, json
from django.db.models import Q
from django.core.serializers.json import DjangoJSONEncoder
from datetime import datetime, timedelta
from django.utils import timezone
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.views.generic import TemplateView
from .models import (
    Employee, Client, 
    ConferenceRoom, Booking, Building
)

# ---------------------------------------------
#             AJAX functions 
# ---------------------------------------------

class AjaxFunctionsView(LoginRequiredMixin, TemplateView):
    
    '''
    This purpose class-based view is only to return JsonResponse.
    All static methods from this class will be called by ajax functions from the JS files. 
    '''
    
    @staticmethod
    def get_rooms(request):
        # Parameters
        building_id = request.GET.get('building_id')
        
        # Check if building exists
        try:
            Building.objects.get(id=building_id)
        except Building.DoesNotExist:
            return JsonResponse({'building_nonexistent': True})
        
        # Fetch all rooms of the building
        rooms_query = ConferenceRoom.objects.filter(building__id=building_id)
        
        # Return response
        rooms = [
            {'id': rm.pk, 'name': rm.__str__()}
            for rm in rooms_query
        ]
        return JsonResponse({'rooms': json.dumps(rooms, cls=DjangoJSONEncoder)})
    
    @staticmethod
    def get_clients(request):
        # Parameters
        search = request.GET.get('search_query')
        
        # Fetch all clients
        clients_query = Client.objects.all()
        if search:
            clients_query = clients_query.filter(Q(name__icontains=search)) # filter by search here
        clients = [
            {'id': obj.pk, 'name': obj.name}
            for obj in clients_query
        ]
        
        # Return response
        response = {
            'clients': json.dumps(clients, cls=DjangoJSONEncoder)
        } if clients_query else {}
        return JsonResponse(response)


# ---------------------------------------------
#               Users views 
# ---------------------------------------------

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


# ---------------------------------------------
#               Calendar views 
# ---------------------------------------------

class EcommerceCalendarView(LoginRequiredMixin, TemplateView):
    
    def post(self, request, room_id):
        # Parameters
        client_id = request.POST.get('new_booking_client_id')
        start_date = request.POST.get('newbooking_start_date_input')
        start_time = request.POST.get('newbooking_start_time_input')
        end_date = request.POST.get('newbooking_end_date_input')
        end_time = request.POST.get('newbooking_end_time_input')
        duration_hours = request.POST.get('newbooking_duration_hours_input')
        use_end_datetime = request.POST.get('newbooking_check_use_end')
        
        
        context = {}
        
        
        
        return self.get(request, room_id, context)
    

    def get(self, request, room_id=None, context={}):
        
        # Fetch all buildings
        buildings = Building.objects.all()
        
        # Set context
        context = {
            'buildings': buildings,
        }.update(context)
        
        # Return guard if theres no room id
        if room_id is None:
            context['no_room_selected'] = True
            return render(request, self.template_name, context)
        
        # Set values of rooms if existing
        try:
            room = ConferenceRoom.objects.get(id=room_id)
            building_id = room.building.all()[0].id
            rooms_query = ConferenceRoom.objects.filter(building__id=building_id)
            context['rooms'] = rooms_query
            context['selected_room'] = {
                'building_id': building_id, 
                'room_id': room_id
            }
        except ConferenceRoom.DoesNotExist:
            context['room_nonexistent'] = True
            return render(request, self.template_name, context)
        
        # Fetch all the bookings on the specified room
        bookings_query = Booking.objects.filter(room__id=room_id)
        bookings_list = [
            {
                'id': bk.pk,
                'title': bk.client.name \
                    if (request.user.id,) in \
                    list(bk.client.users.all().values_list('id')) \
                    else '',
                'start': [
                    bk.start_datetime.year,
                    bk.start_datetime.month-1,
                    bk.start_datetime.day,
                    bk.start_datetime.hour, 0
                ],
                'end': [
                    bk.end_datetime.year,
                    bk.end_datetime.month-1,
                    bk.end_datetime.day,
                    bk.end_datetime.hour, 0
                ],
                # 'allDay': False,
                # 'url': '',
                # 'className': 'bg-info',
            } for bk in bookings_query
        ]
        '''
        Format in calendars.init.js
        {
            id: 999,
            title: 'Repeating Event',
            start: new Date(y, m, d - 3, 16, 0),
            end: new Date(y, m, d - 2),
            allDay: false,
            url: 'http://google.com/',
            className: 'bg-info'
        }
        '''
    
        
        # Transform into JSON objects
        bookings = json.dumps(bookings_list, cls=DjangoJSONEncoder)
        
        # Return with context
        context['bookings'] = bookings

        return render(request, self.template_name, context)

apps_calendar_calendar_view = EcommerceCalendarView.as_view(template_name="apps/apps-calendar.html")
apps_calendar_get_rooms = AjaxFunctionsView.get_rooms
apps_calendar_get_clients = AjaxFunctionsView.get_clients

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
