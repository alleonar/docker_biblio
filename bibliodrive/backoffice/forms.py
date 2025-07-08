from django import forms
from .models import Reservation

# Password for tests user john_doe (admin) and jane_smith is test
# Hash with django shell
class LoginForm(forms.Form):
    username = forms.CharField(min_length=1)
    password = forms.CharField(widget=forms.PasswordInput)

# class ReservationForm(forms.Form):
#     user = forms.IntegerField(widget=forms.HiddenInput(attrs={'readonly': 'readonly'}))
#     title = forms.IntegerField(widget=forms.HiddenInput(attrs={'readonly': 'readonly'}))
#     start_date = forms.DateField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
#     end_date = forms.DateField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
#     close = forms.BooleanField(widget=forms.HiddenInput(attrs={'readonly': 'readonly'}))

class ReservationForm(forms.ModelForm):
   class Meta:
        model = Reservation
        fields = ['user', 'title', 'start', 'end', 'close']
        widgets = {
            'user': forms.HiddenInput(),
            'title': forms.HiddenInput(),
            'start': forms.TextInput(attrs={'readonly': 'readonly', 'id': 'start_date'}),
            'end': forms.TextInput(attrs={'readonly': 'readonly', 'id': 'end_date'}),
            'close': forms.HiddenInput(),
        }