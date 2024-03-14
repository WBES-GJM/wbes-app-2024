from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from .models import Booking, Client

class BookingForm(forms.ModelForm):
    
    client = forms.ModelMultipleChoiceField(queryset=Client.objects.all())
    
    class Meta:
        model = Booking
        fields = ['client', 'room']
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('current_user', None)
        
        super(BookingForm, self).__init__(*args, **kwargs)
        
        if not user: return
        
        client_query = Client.objects.all()
        include_id = []
        
        for client in client_query:
            if user.id in client.users.all().values_list('id', flat=True):
                include_id.append(client.pk)
                
        self.fields['client'].queryset = client_query.filter(id__in=include_id)
        
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