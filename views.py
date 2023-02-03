from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
from .models import *
from .utils import *
# Create your views here.


def base(request):
    return render(request, 'main/base.html')


class mainHome(DataMixin, ListView):
    model = main
    template_name = "main/index.html"
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        t_def = self.get_user_context(title='Головна сторінка')
        return dict(list(context.items()) + list(t_def.items()))

    def get_queryset(self):
        return main.objects.filter(is_published=True).select_related('tech')


# @login_required
def about(request):
    return render(request, 'main/about.html')


class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'main/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        t_def = self.get_user_context(title="Контакти")
        return dict(list(context.items()) + list(t_def.items()))

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')



class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class =AddPostForm
    template_name = 'main/addpage.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        t_def = self.get_user_context(title='Додати статтю')
        return dict(list(context.items()) + list(t_def.items()))


class ShowPost(DataMixin, DetailView):
    model = main
    template_name = 'main/post.html'
    slug_url_kwarg = 'post_slug'
    #pk_url_kwarg = 'post_pk' or 'pk'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        t_def = self.get_user_context(title=context['post'])
        return dict(list(context.items()) + list(t_def.items()))


class mainCategory(DataMixin, ListView):
    model = main
    template_name = 'main/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return main.objects.filter(tech__slug=self.kwargs['tech_slug'], is_published=True).selected_related('tech')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['tech_slug'])
        t_def = self.get_user_context(title='Категория - ' + str(c.name),
                                      tech_selected=c.pk)
        return dict(list(context.items()) + list(t_def.items()))


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'main/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        t_def = self.get_user_context(title="Реєстрація")
        return dict(list(context.items()) + list(t_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'main/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        t_def = self.get_user_context()
        return dict(list(context.items()) + list(t_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Сторінка не знайдена</h1>')
