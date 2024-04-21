from django import forms
from django.db.models import Model
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from .models import *

class BookingForm(forms.ModelForm):

    client = forms.ModelMultipleChoiceField(queryset=Client.objects.all())

    class Meta:
        model = Booking
        fields = ['client', 'room']

    # Override
    def clean_client(self):
        return self.cleaned_data["client"].first()

    # Override
    def clean_start_datetime(self):
        start_datetime = self.cleaned_data["start_datetime"]

        # Ensure that start_time only contains the hour with zero minutes and zero seconds
        if start_datetime.second % 60 != 0 or start_datetime.second % 60 != 0:
            raise forms.ValidationError(
                'Start time should only have the hour with zero minutes and zero seconds.',
                code="invalid",
            )

        return start_datetime


# ---------------------------------------------
#             New Profiles Forms
# ---------------------------------------------

PROFILE_EXCLUDED_FIELDS = ['user', 'list_of_phone', 'list_of_email']

class BaseProfileForm(forms.ModelForm):
    def save(self, commit=True, **kwargs):
        instance = super(BaseProfileForm, self).save(commit=False)
        instance.user = kwargs.pop('user')
        if commit:
            instance.save()
        return instance

class ClientForm(BaseProfileForm):
    class Meta:
        model = Client
        exclude = PROFILE_EXCLUDED_FIELDS

class CompanyForm(BaseProfileForm):
    class Meta:
        model = Company
        exclude = PROFILE_EXCLUDED_FIELDS

class OwnerForm(BaseProfileForm):
    class Meta:
        model = Owner
        exclude = PROFILE_EXCLUDED_FIELDS

class EmployeeForm(BaseProfileForm):
    class Meta:
        model = Employee
        exclude = PROFILE_EXCLUDED_FIELDS

class NewUserForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

class EditUserForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    class Meta:
        model = User
        fields = ('first_name', 'last_name','email', )