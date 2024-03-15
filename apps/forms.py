from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from .models import Booking, Client

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