from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Books,borrow_requests

class CreateUser(UserCreationForm): 
    class Meta:
        model=User
        fields=['username','first_name','last_name','email',]

class Bookstoreform(forms.ModelForm):
    number_of_copy=forms.IntegerField(min_value=1)
    class Meta:
        model=Books
        exclude=["first_pub","last_pub"]

class ReqeustForm(forms.ModelForm):
    class Meta:
        model=borrow_requests
        exclude=["approved","user"]
