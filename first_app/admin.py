from django.contrib import admin
from .models import Books,Borrows,borrow_requests,Reservations
# Register your models here.
@admin.register(Books)
class BookAdmin(admin.ModelAdmin):
    readonly_fields=("author",)
    list_display=["id","name","catagory"]
@admin.register(Borrows)
class BorrowsAdmin(admin.ModelAdmin):
    list_display=["user","book","expiry"]
@admin.register(borrow_requests)
class BorroRequestsAdmin(admin.ModelAdmin):
    list_display=["id","user","book","approved"]
@admin.register(Reservations)
class ReservationAdmin(admin.ModelAdmin):
    list_display=["id","user","book","reserved_date"]

