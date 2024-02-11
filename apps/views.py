import calendar, json
from typing import Any
from django.db.models import Q
from django.core.serializers.json import DjangoJSONEncoder
from datetime import datetime, timedelta
from django.http.response import HttpResponse
from django.utils import timezone
from django.http import HttpRequest, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.views.generic import TemplateView
from .models import (
    Employee, Client, Company, Owner, 
    ConferenceRoom, Booking, Building
)
from .forms import BookingForm
from .helper import ModelInstanceGetter, JsonResponseHelper

# ---------------------------------------------
#             AJAX functions 
# ---------------------------------------------

class AjaxFunctionsView(LoginRequiredMixin, TemplateView):
    '''
    This purpose class-based view is only to return JsonResponse.
    All static methods from this class will be called by ajax functions from the JS files. 
    '''
    
    # -------------------------------------
    #           Fetching Data
    # -------------------------------------
    
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
    def get_client(request):
        
        # Inner methods
        def _get_client_with_booking(booking_id:int):
            booking:Booking = ModelInstanceGetter.get_instance(Booking, booking_id)
            assert booking
            
            return booking.client
            
        # Parameters
        booking_id = request.GET.get('booking_id')
        # ... 
        # ...
        # probably more parameters in the future
        
        if booking_id:
            client = _get_client_with_booking(int(booking_id))
            client = JsonResponseHelper.serialize(client)
        
        # Return response
        response = {
            'client': client
        } if client else {}
        return JsonResponse(response)
    
    @staticmethod
    def get_booking(request):
        pass
        # try:
        #     if not booking_id:
        #         booking_id = request.GET.get('booking_id')
        #     if not booking_id:
        #         raise ValueError('No booking_id provided')
            
        #     query = ModelInstanceGetter.get_instance(Booking, int(booking_id))
        
        # except ValueError:
        #     pass
        
        # response = {
        #     'clients': json.dumps(query, cls=DjangoJSONEncoder)
        # } if query else {}
        # return JsonResponse(response)
    
    ''' This method is currently not being used '''
    @staticmethod
    def search_clients(request):
        # Parameters
        search = request.GET.get('search_query')
        
        # Fetch all clients
        clients_query = Client.objects.all()
        if search:
            clients_query = clients_query.filter(Q(name__icontains=search)) # filter by search here
        clients = [JsonResponseHelper.serialize(obj) for obj in clients_query]
        
        # Return response
        response = {
            'clients': json.dumps(clients, cls=DjangoJSONEncoder)
        } if clients_query else {}
        return JsonResponse(response)
    


apps_ajax_get_rooms = AjaxFunctionsView.get_rooms
apps_ajax_get_client = AjaxFunctionsView.get_client


# ---------------------------------------------
#               Booking views 
# ---------------------------------------------

class EcommerceBookingView(LoginRequiredMixin, TemplateView, View):
    
    reverse_url = "apps:ecommerce.booking"
    template_name = "apps/ecommerce/ecommerce-booking.html"
    
    
    def format_datetime(self, date: str, hour: int) -> datetime:
        datetime_str = f'{date} {hour}:00:00'
        return datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
    
    
    def get(self, request,  *args, **kwargs):
        # Get parameters
        room_id = kwargs.get('room_id', None)
        context = kwargs.get('context', {})
        
        # Fetch all buildings
        buildings = Building.objects.all()
        
        # Set context
        context['buildings'] = buildings
        
        # Return guard if theres no room id
        if room_id is None:
            context['no_room_selected'] = True
            return render(request, self.template_name, context)
        
        # See if room is existing
        try:
            room = ConferenceRoom.objects.get(id=room_id)
        except ConferenceRoom.DoesNotExist:
            context['room_nonexistent'] = True
            return render(request, self.template_name, context)
        
        # Set objects
        building_id = room.building.all()[0].id
        rooms_query = ConferenceRoom.objects.filter(building__id=building_id)
        context['rooms'] = rooms_query
        context['selected_room'] = {
            'building_id': building_id, 
            'room_id': room_id
        }
        
        # Set form
        context['form'] = BookingForm(current_user=request.user, initial={'room': room})
        
        # Fetch all the bookings on the specified room
        bookings_query = Booking.objects.filter(room__id=room_id)
        bookings_list = [
            {
                'id': bk.pk,
                'title': bk.client.name \
                    if request.user.id in \
                    list(bk.client.users.all().values_list('id', flat=True)) \
                    else '',
                'start': [
                    bk.start_datetime.year,
                    bk.start_datetime.month-1,
                    bk.start_datetime.day,
                    bk.start_datetime.hour,
                ],
                'end': [
                    bk.end_datetime.year,
                    bk.end_datetime.month-1,
                    bk.end_datetime.day,
                    bk.end_datetime.hour,
                ],
                'duration': bk.duration_hours,
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
    
    
    def post(self, request, *args, **kwargs):
        
        # Check if edit or delete
        what_to_do = str(request.POST.get('booking_method'))
        if what_to_do.lower() == 'put':
            return self._put(request, *args, **kwargs)
        elif what_to_do.lower() == 'delete':
            return self._delete(request, *args, **kwargs)
            
        # Parameters
        start_date = request.POST.get('newbooking_start_date_input')
        start_time = request.POST.get('newbooking_start_time_input')
        end_date = request.POST.get('newbooking_end_date_input')
        end_time = request.POST.get('newbooking_end_time_input')
        duration_hours = int(request.POST.get('newbooking_duration_hours_input'))
        use_end_datetime = request.POST.get('newbooking_check_use_end')
        
        # Set the values
        start_datetime = self.format_datetime(start_date, start_time)
        if use_end_datetime:
            end_datetime = self.format_datetime(end_date, end_time)
            duration_hours = None
        else:
            end_datetime = None

        # Create new entry with form and save it
        booking_form = BookingForm(request.POST)
        if booking_form.is_valid():
            booking = booking_form.save(commit=False)
            booking.start_datetime = start_datetime
            booking.end_datetime = end_datetime
            booking.duration_hours = duration_hours
            booking.save()
            return HttpResponseRedirect(reverse(self.reverse_url, kwargs=kwargs))
        
        # Set context if there are any errors
        if booking_form.errors:
            kwargs['context']['error'] = booking_form.errors
        
        return self.get(request, *args, **kwargs)
    
    
    def _put(self, request, *args, **kwargs):
        # Parameters
        booking_id = request.POST.get('opened_booking_id')
        start_date = request.POST.get('newbooking_start_date_input')
        start_time = request.POST.get('newbooking_start_time_input')
        end_date = request.POST.get('newbooking_end_date_input')
        end_time = request.POST.get('newbooking_end_time_input')
        
        # Set the values
        start_datetime = self.format_datetime(start_date, start_time)
        end_datetime = self.format_datetime(end_date, end_time)

        # Save the values
        booking = ModelInstanceGetter.get_instance(Booking, int(booking_id))
        booking_form = BookingForm(instance=booking)
        booking = booking_form.save(commit=False)
        booking.start_datetime = start_datetime
        booking.end_datetime = end_datetime
        booking.save()
        
        return HttpResponseRedirect(reverse(self.reverse_url, kwargs=kwargs))
    
    
    def _delete(self, request, *args, **kwargs):
        # Parameters
        booking_id = request.POST.get('opened_booking_id')
        
        # Delete the instance
        booking = ModelInstanceGetter.get_instance(Booking, int(booking_id))
        booking.delete()
        
        return HttpResponseRedirect(reverse(self.reverse_url, kwargs=kwargs))

apps_booking_calendar_view = EcommerceBookingView.as_view()


# ---------------------------------------------
#               Users views 
# ---------------------------------------------

class UserListView(LoginRequiredMixin, TemplateView):
    
    template_name = "apps/users/apps-users-employees.html"
    
    @staticmethod
    def get_client_list():
        pass
    
    
    @staticmethod
    def get_employee_list():
        
        
        def get(request):
            
            form = None
            context = {
                "employees": Employee.objects.all()
            }
            
            # return render(request, self.list_template_name, context)
        return get
    
    
    def get(self, request,  *args, **kwargs):
        
        context = kwargs.get('context', {})
        account = kwargs.get('account')
        id = kwargs.get('id')
        
        if account == 'clients':
            pass
        # elif account == 'companies'
        
        
        return render(request, self.template_name, context)
    
class UserView(LoginRequiredMixin, TemplateView):
    
    profile_template_name = "apps/users/apps-users-profile.html"
    profile_model_templates = {
        'client': (Client, "apps/users/apps-users-profile-client.html"),
        'company': (Company, "apps/users/apps-users-profile-company.html"),
        'owner': (Owner, "apps/users/apps-users-profile-owner.html"),
        'employee': (Employee, "apps/users/apps-users-profile-employee.html"),
    }
    list_model_templates = {
        'client': (Client, "apps/users/apps-users-list-client.html"),
        'company': (Company, "apps/users/apps-users-list-company.html"),
        'owner': (Owner, "apps/users/apps-users-list-owner.html"),
        'employee': (Employee, "apps/users/apps-users-list-employee.html"),
    }
    
    @staticmethod
    def get_current_user():
        
        template_name="apps/users/apps-users-profile.html"
        
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

    
    def get(self, request, *args, **kwargs):
        context = kwargs.get('context', {})
        context['profile'] = profile = kwargs.get('profile')
        id = kwargs.get('id')
        
        # Set model and template to use
        model, self.template_name = self.list_model_templates.get(profile, (None, None))
        assert model
        
        # Get objects
        if id:
            obj = ModelInstanceGetter.get_instance(model, id)
            if not obj:
                context['error'] = 'No instance found'
            else:
                context['object'] = obj
        else:
            objs = model.objects.all()
            context['list'] = objs
        
        return render(request, self.template_name, context)

apps_users_profile_view = UserView.as_view()
apps_users_myprofile_view = UserView.get_current_user()
apps_users_list_view = UserListView.as_view()


# ---------------------------------------------
#             Placeholder views 
# ---------------------------------------------
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
