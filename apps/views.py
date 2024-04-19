import json
from datetime import datetime, timedelta

from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.http.response import HttpResponse
from django.http import HttpRequest, HttpResponseRedirect, JsonResponse
from django.views import View
from django.views.generic import TemplateView

from django.core.serializers.json import DjangoJSONEncoder
from django.utils import timezone
from django.db import models
from django.db.models import Q
from django import forms

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

from .helper import *
from .models import *
from .forms import *


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
        ''' This method is currently not being used '''
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

    @staticmethod
    def search_clients(request):
        ''' This method is currently not being used '''
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

    def format_time(self, hour: int, full: bool=True, min: bool=False) -> str:
        tm = hour if hour <= 12 else hour-12
        if full:
            return f'{tm:02d}:00 ' + ('AM' if hour<12 else 'PM')
        else:
            return str(tm) + ('a' if hour<12 else 'p')


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
        building_id = room.building.pk
        rooms_query = ConferenceRoom.objects.filter(building__id=building_id)
        context['rooms'] = rooms_query
        context['selected_room'] = {
            'building_id': building_id,
            'room_id': room_id
        }

        # Set form
        context['form'] = BookingForm(initial={'room': room})

        # Fetch all the bookings on the specified room
        bookings_query = Booking.objects.filter(room__id=room_id)
        bookings_list = [
            {
                'id': bk.pk,
                'title':
                    # f'{self.format_time(bk.start_datetime.hour, full=False)}-' \
                    # + f'{self.format_time(bk.end_datetime.hour, full=False)} | ' \
                     bk.client.name, # \
                    # if request.user.id in \
                    # list(bk.client.users.all().values_list('id', flat=True)) \
                    # else '',
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
                # 'duration': bk.duration_hours,
                # 'allDay': bk.all_day,
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

        # Business hours of calendar
        business_hours_dict = Booking.BUSINESS_HOURS

        # Transform into JSON objects
        bookings = json.dumps(bookings_list, cls=DjangoJSONEncoder)
        business_hours = json.dumps(business_hours_dict, cls=DjangoJSONEncoder)

        # Return with context
        context['bookings'] = bookings
        context['business_hours'] = business_hours
        context['business_hours_clock'] = [
            (hr, self.format_time(hr))
            for hr in range(business_hours_dict['start'], business_hours_dict['end']+1)
        ]

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

class UserView(LoginRequiredMixin, TemplateView):
    
    def get_template(self, model_str, display_as_profile) -> str:
        list_templates = {
            "client": "apps/profiles/apps-users-list-client.html",
            "company": "apps/profiles/apps-users-list-company.html",
            "employee": "apps/profiles/apps-users-list-employee.html",
            "owner": "apps/profiles/apps-users-list-owner.html",
            "user": "apps/profiles/apps-users-list-user.html",
        }
        
        profile_templates = {
            "client": "apps/profiles/apps-users-profile-client.html",
            "company": "apps/profiles/apps-users-profile-company.html",
            "employee": "apps/profiles/apps-users-profile-employee.html",
            "owner": "apps/profiles/apps-users-profile-owner.html",
            "user": "apps/profiles/apps-users-profile-user.html",
        }
    
        if display_as_profile:
            return profile_templates.get(model_str)
        else:
            return list_templates.get(model_str)
 
    def get_model(self, model_str):
        forms = {
            'user': User,
            'client': Client,
            'company': Company,
            'owner': Owner,
            'employee': Employee,
        }
        return forms[model_str]
    
    def get_form(self, model, post_request=None, id=None):
        new_obj_forms = {
            User: NewUserForm,
            Client: ClientForm,
            Company: CompanyForm,
            Owner: OwnerForm,
            Employee: EmployeeForm,
        }
        edit_obj_forms = {
            User: EditUserForm,
            Client: ClientForm,
            Company: CompanyForm,
            Owner: OwnerForm,
            Employee: EmployeeForm,
        }
        
        # Post request form (for saving data)
        if post_request:
            # Edit object form
            if bool(id):
                form = edit_obj_forms[model]
                model_instance = get_object_or_404(model, pk=id)
                return form(post_request, instance=model_instance)
            # New object form
            else:
                form = new_obj_forms[model]
                return form(post_request)
        
        # Get request form (for fetching data)
        else:
            # Edit object form
            if bool(id):
                form = edit_obj_forms[model]
                obj = ModelInstanceGetter.get_instance(model, id)
                return form(instance=obj)
            else:
                form = new_obj_forms[model]
                return form()

    def post(self, request, *args, **kwargs):
        # Always Initial Step, get variables
        context: dict = kwargs.get('context', {})
        id = kwargs.get('id')
        model_str = context['profile'] = kwargs.get('profile')
        display_as_profile = bool(id)
        
        # Set the model and form
        model = self.get_model(model_str=model_str)
        form = self.get_form(model=model, post_request=request.POST, id=id)

        # Process form
        if form.is_valid():
            # Save the data
            if model == User: 
                form.save()
            else:
                form.save(user=request.user)

            # If already using profile template, redirect to the same URL
            if display_as_profile: 
                HttpResponseRedirect(request.path)
                
            # Else, new object was created 
            # so redirect to the new page with the profile template
            else:
                return redirect('apps:profiles.profile', 
                                profile=model_str, id=form.instance.pk)
        
        # If the form is not valid, re-render the form with error messages
        context['form'] = form
        
        return self.get(request, context=context, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        # Always Initial Step, get variables
        context: dict = kwargs.get('context', {})
        id = kwargs.get('id')
        model_str = context['profile'] = kwargs.get('profile')
        display_as_profile = bool(id)
        
        # Set the model and template as "profile"
        model = self.get_model(model_str=model_str)
        template_name = self.get_template(model_str=model_str, 
                                          display_as_profile=display_as_profile)

        if display_as_profile:
            context = self.context_for_object(context, model_str, model, id)
        else:
            context = self.context_for_list(context, model_str, model)

        return render(request, template_name, context)

    def context_for_object(self, context, model_str, model, id) -> HttpResponse:
        
        obj = ModelInstanceGetter.get_instance(model, id)
        # Access "object" in view and get details such as object.id, object.name, etc.
        if obj:
            context['object'] = obj
        else:
            context['error'] = 'No instance found'
                
        form = context.get('form')
        if not form:
            form = self.get_form(model=model, id=id)
        context['form'] = form
        context['form_title'] = 'Editing ' + model_str.title()
        context['form_url'] = 'apps:profiles.profile'
        context['form_obj_id'] = obj.pk

        return context

    def context_for_list(self, context, model_str, model) -> HttpResponse:
        objs = model.objects.all()
        context['list'] = objs
        
        form = context.get('form')
        if not form:
            form = self.get_form(model=model)
        context['form'] = form
        context['form_title'] = 'New ' + model_str.title()
        context['form_url'] = 'apps:profiles.list'
        
        # NOT YET IMPLEMENTED PROPERLY
        # form_depends = self.form_dependencies.get(self.model_str)
        # if form_depends:
        #     context['form_depends']
        
        return context

apps_users_view = UserView.as_view()


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
