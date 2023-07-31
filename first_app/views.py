from django.shortcuts import render,redirect
from .forms import CreateUser,Bookstoreform
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout,authenticate
from .models import Books,Borrows,borrow_requests,Reservations,User
from django.contrib import messages
from django.utils import timezone
from datetime import datetime,timedelta

# Create your views here.

def home(request):
    return render(request,"base.html")

def singup(request):
    if request.method=="POST":
        frm=CreateUser(request.POST)
        if frm.is_valid():
            frm.save(commit=True)
            return redirect("profile")
    else:
        frm=CreateUser
    return render(request,"singup.html",{"form":frm})

def profile(request):
    if request.user.is_authenticated:
        return render(request,"profile.html")
    else:
        return redirect("login")
    
def show_books(request):
    if request.user.is_authenticated:
        books=Books.objects.all()
        return render(request,"show_books.html",{"books":books})
    else:
        return redirect("login")

def Login(request):
    if request.method=="POST":
        frm=AuthenticationForm(request=request,data=request.POST)
        if frm.is_valid():
            usern=frm.cleaned_data['username']
            userp=frm.cleaned_data['password']
            user=authenticate(username=usern,password=userp)
            if user is not None:
                login(request,user)
                return redirect("profile")
        else:
            return redirect("signuppage")
    else:
        frm=AuthenticationForm
    return render(request,"login.html",{"form":frm})
def Logout(reqeust):
    if reqeust.user.is_authenticated:
        logout(reqeust)
        return redirect("login")
    else:
        return redirect("login")
    
def Users(request):
    if request.user.is_superuser:
        users=User.objects.all()
        return render(request,"users.html",{"users":users})
    else:
        return redirect("login")
    
def edit_user(request,pk):
    if request.user==User.objects.get(pk=pk) or (request.user.is_authenticated and request.user.is_superuser):
        us=User.objects.get(pk=pk)
        if request.method=="POST":
            frm=CreateUser(instance=us,data=request.POST)
            if frm.is_valid():
                us.username=frm.cleaned_data["username"]
                us.first_name=frm.cleaned_data["first_name"]
                us.last_name=frm.cleaned_data['last_name']
                us.save()
                return redirect("home")
        else:
            frm=CreateUser(instance=us)
        return render(request,"update_user.html",{"form":frm})
    else:
        return redirect("login")

def delete_user(request,pk):
    if (request.user.is_superuser or request.user==User.objects.get(pk=pk)) and request.user.is_authenticated:
        User.objects.get(pk=pk).delete()
        return redirect("users")
    else:
         return redirect("login")

def store_book(request):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method=="POST":
            frm=Bookstoreform(request.POST)
            if frm.is_valid():
                print(frm.cleaned_data)
                frm.save(commit=True)
                return redirect("show_books")
        else:
            frm=Bookstoreform
        return render(request,"store_book.html",{"form":frm})
    else:
        return redirect("login")
    
def update_book(request,pk):
    if request.user.is_authenticated and request.user.is_superuser:
        book=Books.objects.get(pk=pk)
        if request.method=="POST":
            frm=Bookstoreform(instance=book,data=request.POST)
            if frm.is_valid():
                if frm.cleaned_data["number_of_copy"]>0:
                    book.is_available=True
                frm.save()
                book.save()
                return redirect("show_books")
        else:
            frm=Bookstoreform(instance=book)
        return render(request,"update_book.html",{"form":frm})
    else:
        return redirect("login")
    

def delete_book(request,pk):
    if request.user.is_authenticated and request.user.is_superuser:
        book=Books.objects.get(pk=pk).delete()
        return redirect("show_books")
    else:
        return redirect("login")
    
def book_details(request,pk):
    book=Books.objects.get(pk=pk)
    if request.user.is_authenticated:
        return render(request,"book_details.html",{"book":book})
    else:
        return redirect("login")

def my_book_list(request):
    if request.user.is_authenticated:
        borrows=Borrows.objects.filter(user=request.user)
        books=[]
        
        return render(request,"my_books.html",{"books":borrows})
    else:
         return redirect("login")
def request_borrow_from_book_list(request,pk):
    if request.user.is_authenticated:
        obj=borrow_requests()
        obj.user=request.user
        obj.book=Books.objects.get(pk=pk)
        requests=borrow_requests.objects.all()
        if borrow_requests.objects.filter(user=obj.user,book=obj.book).exists() or Borrows.objects.filter(user=obj.user,book=obj.book):
            warning=messages.warning(request,"This borrow reqeust is already exists. ")
            return render(request,"book_details.html",{"book":obj.book,"warnings":warning})
        if obj.book.number_of_copy>0:
            obj.book.number_of_copy-=1
            if Reservations.objects.filter(user=request.user,book=obj.book).exists():
                Reservations.objects.filter(user=request.user,book=obj.book).delete()
            if obj.book.number_of_copy==0:
                obj.book.is_available=False
            obj.book.save()
            obj.save()
            success=messages.success(request,"This borrow request is placed. After the admin's approval the book will be added to your book list.")
            return render(request,"book_details.html",{"book":obj.book,"messege":success})
        else:
            obj.book.is_available=False
            messages.warning(request,"Sorry! The book is not availeble.")
            obj.book.save()
            return render(request,"book_details.html",{"book":obj.book})
    else:
        return redirect("login")
    
def show_borrow_reqeusts(request):
    if request.user.is_superuser:
        requests=borrow_requests.objects.all()
        return render(request,"borrow_requests.html",{"requests":requests})
    else:
        return redirect("login")

def approve_borrow_request(request,pk):
    if request.user.is_superuser:
        req=borrow_requests.objects.get(pk=pk)
        req.approved=True
        req.save()
        new_borrow=Borrows()
        new_borrow.user=req.user
        new_borrow.book=req.book

        new_borrow.save() 
        return redirect("show_borrow_requests")
    else:
        return redirect("login")
    
def reserving_book_from_book_details(request,pk):
    if request.user.is_authenticated:
        reservation=Reservations()
        reservation.user=request.user
        reservation.book=Books.objects.get(pk=pk)
        if Reservations.objects.filter(user=request.user,book=reservation.book).exists() or Borrows.objects.filter(user=request.user,book=reservation.book).exists() or borrow_requests.objects.filter(user=request.user,book=reservation.book).exists():
            messages.error(request,"This reservation request is already exists.")
            return render(request,"book_details.html",{"book":reservation.book})
        reservation.is_reserved=True
        reservation.save()
        return render(request,"book_details.html",{"book":reservation.book})
    
def reserv_book(request,pk):
    if request.user.is_authenticated:
        reservation=Reservations()
        reservation.user=request.user
        reservation.book=Books.objects.get(pk=pk)
        if Reservations.objects.filter(user=request.user,book=reservation.book).exists():
            messages.error(request,"This reservation request is already exists.")
            return redirect("unavailable_books")
        reservation.is_reserved=True
        reservation.save()
        return redirect("unavailable_books")
    
def unavailable_books(request):
    if request.user.is_authenticated:
        un_books=Books.objects.filter(number_of_copy=0)
        for un_book in un_books:
            un_book.is_available=False
        return render(request,"unavailable_books.html",{"books":un_books})
    
def my_reserved_list(request):
    if request.user.is_authenticated:
        reserved_books=Reservations.objects.filter(user=request.user,is_reserved=True)
        for reserved_book in reserved_books:
            if Borrows.objects.filter(user=request.user,book=reserved_book.book).exists() or borrow_requests.objects.filter(user=request.user,book=reserved_book.book).exists():
                reserved_book.delete()

        return render(request,"reserved_books.html",{"books":reserved_books})
    
def fine_calculate(due_time):
    now=timezone.now()
    if now>due_time:
        return (now-due_time)*5
    else:
        return 0

def return_book(request,pk):
    if request.user.is_authenticated:
        book=Books.objects.get(pk=pk)

        borrow=Borrows.objects.get(user=request.user,book=book)
        borrow.fine=fine_calculate(borrow.expiry)
        borrow.save()
        if borrow.fine==0:
            borrow.delete()
            borrow_requests.objects.filter(user=request.user,book=book).delete()
            book.number_of_copy+=1
            book.is_available=True
            book.save()
            return redirect("my_books")
        else:
            messages.warning(request,f"Please pay {borrow.fine} taka as fine to return {borrow.book.name} book.")
            return redirect("my_books")
    else:
        return redirect("login")
