from django.contrib.auth.forms import  UserCreationForm,AuthenticationForm,PasswordChangeForm
from django.contrib.auth.models import User
from django import forms
from .models import ItemModel

class SignUpForm(UserCreationForm):
    class Meta:
        model=User    
        fields=['username','first_name','last_name','email']
 
class LoginForm(AuthenticationForm):
    pass 

class ChangePwd(PasswordChangeForm):
    pass


class PaymentForm(forms.ModelForm):
    class Meta:
        model = ItemModel
        fields = ['name']