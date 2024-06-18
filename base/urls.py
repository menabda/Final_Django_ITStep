from django.urls import path
from . import views
from .views import LibraryList, BookDetail, BookCreate, BookUpdate, BookDelete, BorrowedBooksPage, BurrowBookView, ReturnBookView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', LibraryList.as_view(), name = 'books'),
    path('book/<int:pk>', BookDetail.as_view(), name = 'book'),
    path('book_add/', BookCreate.as_view(), name = 'book_add'),
    path('book_update/<int:pk>', BookUpdate.as_view(), name = 'book_update'),
    path('book_delete/<int:pk>', BookDelete.as_view(), name = 'book_delete'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.RegisterPage.as_view(), name='register'),
    path('my_books/', BorrowedBooksPage.as_view(), name='my_books'),
    path('borrow/', BurrowBookView.as_view(), name='book_borrow'),
    path('return/', ReturnBookView.as_view(), name='book_return'),


]