from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.info_page, {'slug': 'about'}, name='about'),
    path('how-to-order/', views.info_page, {'slug': 'how-to-order'}, name='how_to_order'),
    path('faq/', views.faq_list, name='faq'),
    path('contacts/', views.info_page, {'slug': 'contacts'}, name='contacts'),
    path('page/<slug:slug>/', views.info_page, name='info_page'),
]