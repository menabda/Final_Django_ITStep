from urllib import request
from django.conf import LazySettings
from django.shortcuts import redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views import View
from django.urls import reverse_lazy
from .models import Book 
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin,AccessMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, QueryDict
from django.shortcuts import resolve_url
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.http import url_has_allowed_host_and_scheme, urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

class AdminRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

class LibraryList(LoginRequiredMixin, ListView):

    model = Book
    context_object_name = 'books'   
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Book.objects.filter(title__icontains=query)
        else:
           return Book.objects.all()
        
    def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      for book in context['books']:
         book.borrowed = book.belongs_to_user(self.request.user)
      return context
    
class BookDetail(LoginRequiredMixin, DetailView):
    model = Book
    context_object_name = 'book'   

class BookCreate(AdminRequiredMixin, 
LoginRequiredMixin, CreateView):
    model = Book
    fields = '__all__'
    success_url = reverse_lazy('books')
    context_object_name = 'book_add'  
    template_name = 'base/book_add.html'

class BookUpdate(AdminRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Book
    fields = '__all__'
    success_url = reverse_lazy('books')
    context_object_name = 'book_update'  
    template_name = 'base/book_update.html'

class BookDelete(AdminRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Book
    context_object_name = 'book'
    success_url = reverse_lazy('books')
    template_name = 'base/book_delete.html'

    

class CustomLoginView(LoginView):
  template_name = 'base/login.html'
  fields = '__all__'


  def get_success_url(self):
    return reverse_lazy ('books')
  

  def get(self, *args, **kwargs):
    if self.request.user.is_authenticated:
      return redirect('books')

    return super(CustomLoginView, self).get(*args, **kwargs)
  
class RegisterPage(FormView):
  template_name = 'base/register.html'
  form_class = UserCreationForm
  success_url = reverse_lazy('books')


  def form_valid(self, form):
    user = form.save()

    if user is not None:
      login(self.request, user)

    return super(RegisterPage, self).form_valid(form)
  

  def get(self, *args, **kwargs):
    if self.request.user.is_authenticated:
      return redirect('books')

    return super(RegisterPage, self).get(*args, **kwargs)


class BorrowedBooksPage(LoginRequiredMixin, ListView):

  model = Book
  context_object_name = 'books'   
  template_name = 'base/book_borrowed.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['books'] = Book.objects.filter(user__id=self.request.user.id)
    
    return context
  
  
class BurrowBookView(LoginRequiredMixin, View):
  def post(self, request):
    book_id = request.POST.get('book_id')
    book = Book.objects.get(pk=book_id)
    if book.quantity and request.user not in book.user.all():
       book.user.add(request.user)
       book.quantity -= 1
       book.save()
    return redirect(reverse_lazy('my_books'))
  

class ReturnBookView(LoginRequiredMixin, View):
  def post(self, request):
    book_id = request.POST.get('book_id')
    book = Book.objects.get(pk=book_id)
    if request.user in book.user.all():
       book.user.remove(request.user)
       book.quantity += 1
       book.save()
    return redirect(reverse_lazy('my_books'))
     

  
