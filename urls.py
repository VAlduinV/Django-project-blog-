from django.urls import path
from . import views
from .views import mainHome, mainCategory, ShowPost, AddPage, RegisterUser, LoginUser, ContactFormView
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', (mainHome.as_view()), name='home'),
    path('home/', mainHome.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout', views.logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('contact/', ContactFormView.as_view(), name='contact'),
    path('addpage/', AddPage.as_view(), name='add_page'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    path('Category/<slug:tech_slug>/', mainCategory.as_view(), name='Category'),
]
