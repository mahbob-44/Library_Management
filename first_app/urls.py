from django.urls import path
from .views import home,singup,profile,Login,store_book,show_books,Logout,update_book,delete_book,book_details,my_book_list,request_borrow_from_book_list,show_borrow_reqeusts,approve_borrow_request,reserving_book_from_book_details,unavailable_books,reserv_book,my_reserved_list,return_book,Users,edit_user,delete_user
urlpatterns = [
    path("",home,name="home"),
    path("signup/",singup,name="signuppage"),
    path("profile/",profile,name="profile"),
    path("login/",Login,name="login"),
    path("store_book/",store_book,name="store_book"),
    path("show_books/",show_books,name="show_books"),
    path("logout/",Logout,name="logout"),
    path("update_book/<int:pk>",update_book,name="update_book"),
    path("delete_book/<int:pk>",delete_book,name="delete_book"),
    path("book_details/<int:pk>",book_details,name="book_details"),
    path("my_book_list/",my_book_list,name="my_books"),
    path("borrow_request_from_list/<int:pk>",request_borrow_from_book_list,name="borrow_request_from_list"),
    path("show_borrow_requests/",show_borrow_reqeusts,name="show_borrow_requests"),
    path("approve_borrow_request/<int:pk>",approve_borrow_request,name="approve_request"),
    path("reserv_book_from_book_details/<int:pk>",reserving_book_from_book_details,name='reserve_book_from_book_details'),
    path("reserve_book/<int:pk>",reserv_book,name="reserve_book"),
    path("unavailable_books",unavailable_books,name="unavailable_books"),
    path("my_reserved_list/",my_reserved_list,name="my_reserved_list"),
    path("return_book/<int:pk>",return_book,name="return_book"),
    path("users/",Users,name="users"),
    path("edit_user/<int:pk>",edit_user,name="edit_user"),
    path("delete_user/<int:pk>",delete_user,name="delete_user")
]
