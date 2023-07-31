from django.db import models
from django import forms
from django.contrib.auth.models import User
from datetime import datetime,timedelta
from django.utils import timezone
# Create your models here.
class Books(models.Model):
    CATAGORY=(
        ("Mystery","Mystery"),
        ("Thrill","Thriller"),
        ("Sci-fi","Sci-fi"),
        ("Horror","Horror"),
        ("Humor","Humor")
    )
    name=models.CharField(max_length=50)
    number_of_copy=models.IntegerField()
    is_available=models.BooleanField(default=True)
    catagory=models.CharField(max_length=30,choices=CATAGORY)
    author=models.CharField(max_length=30)
    first_pub=models.DateTimeField(auto_now_add=True)
    last_pub=models.DateTimeField(auto_now=True)
    description=models.TextField()
    def __str__(self) -> str:
        return f"{self.name}"
def expiry():
    return datetime.today()+timedelta(days=1)
class Borrows(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    book=models.ForeignKey(Books,on_delete=models.CASCADE)
    fine=models.DecimalField(max_digits=5,decimal_places=3,default=0)
    expiry=models.DateTimeField(default= timezone.now() + timedelta(days=14))
    class Meta:
        unique_together=('user',"book")
class borrow_requests(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    book=models.ForeignKey(Books,on_delete=models.CASCADE)
    approved=models.BooleanField(default=False)
    class Meta:
        unique_together=('user',"book")
class Reservations(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    book=models.ForeignKey(Books,on_delete=models.CASCADE)
    is_reserved=models.BooleanField(default=False)
    reserved_date=models.DateField(auto_now_add=True)
    class Meta:
        unique_together=('user','book')

