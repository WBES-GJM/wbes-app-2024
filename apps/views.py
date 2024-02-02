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
    
    def post(self, request, room_id=None):
        # Parameters
        client_id = request.POST.get('new_booking_client_id')
        start_date = request.POST.get('newbooking_start_date_input')
        start_time = request.POST.get('newbooking_start_time_input')
        end_date = request.POST.get('newbooking_end_date_input')
        end_time = request.POST.get('newbooking_end_time_input')
        duration_hours = request.POST.get('newbooking_duration_hours_input')
        use_end_datetime = request.POST.get('newbooking_check_use_end')
        
        
        
        # booking case where user is submitting time and info to book a conference room
        if request.POST.get("start_time"):
            # retrieve and assign variables from form inputs
            client_name = request.POST.get("client_name")
            conference_room = request.POST.get("conference_room")
            start_time_str = request.POST.get("start_time")
            start_time:datetime = datetime.strptime(start_time_str, '%Y-%m-%dT%H:%M')
            day = start_time.day
            month = start_time.month
            year = start_time.year
            duration = int(request.POST.get("duration"))
            
            print('conference_room should be here:', conference_room)
            print('client name should be here', client_name)
            
            # Calculate the day of the week (0 = Monday, 1 = Tuesday, ...)
            date = datetime(year, month, day)
            day_of_week = date.weekday()

            # Convert the day of the week to the name
            day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            day_name = day_names[day_of_week]

            try:
                # Try to find the client and room by name
                selected_client = Client.objects.get(name=client_name)
                name = selected_client.name
                selected_room = ConferenceRoom.objects.get(room=conference_room)
                print('selected_room=', selected_room)

            except (Client.DoesNotExist, ConferenceRoom.DoesNotExist):
                print('either no client object or no conferenceroom object exists maybe')
                return HttpResponseRedirect(reverse('calendar'))
            
            print('for sure went here')
            clients = Client.objects.all()
            
            this_client = Client.objects.get(name=name)
            phones = this_client.list_of_phone.split('\n')
            emails = this_client.list_of_email.split('\n')

            # Convert start_time_str to a datetime object
            start_time = timezone.make_aware(datetime.strptime(start_time_str, '%Y-%m-%dT%H:%M'))
            dt = start_time.replace(minute=0, second=0)

            # Calculate the end time by adding the duration as a timedelta
            end_time = dt + timedelta(hours=duration)
            bookings = Booking.objects.filter(day=day, month=month, year=year).order_by('start_time')

            # Case when booking during a booked timeframe
            for booking in bookings:
                if start_time >= booking.start_time and start_time < booking.end_time:
                    bookings = Booking.objects.filter(day=day, month=month, year=year).order_by('start_time')
                    clients = Client.objects.all()
                    context = {
                        'day_name': day_name,
                        'day': day,
                        'month': month,
                        'year': year,
                        'bookings': bookings,
                        'clients': clients,
                        'error_message': 'This time slot is already booked.',
                        'phones': phones,
                        'emails': emails,
                        'conference_room': conference_room
                    }
                    return render(request, 'commerce/calendar.html', context)
                
            # Case when booking is during open timeframe
            booking = Booking(name=this_client, room=selected_room, start_time=dt, duration=duration, end_time=end_time)

            booking.save()
            bookings = Booking.objects.filter(day=day, month=month, year=year).order_by('start_time')
            clients = Client.objects.all()
            context = {
                'day_name': day_name,
                'day': day,
                'month': month,
                'year': year,
                'bookings': bookings,
                'clients': clients,
                'phones': phones,
                'emails': emails,
                'conference_room': selected_room
            }
            
            return render(request, 'commerce/calendar.html', context)
        


    def get(self, request, room_id=None):
        
        # Fetch all buildings
        buildings = Building.objects.all()
        
        # Set context
        context = {
            # 'day_name': day_name,
            # 'day': day,
            # 'month': month,
            # 'year': year,
            'buildings': buildings,
            # 'clients': clients,
            # 'phones': phones,
            # 'emails': emails,
            # 'conference_room_options': conference_room_options,
        }
        
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
