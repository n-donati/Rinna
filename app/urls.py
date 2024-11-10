from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'app'  # Add namespace to avoid URL naming conflicts

urlpatterns = [
    path('', views.home, name='home'),
    path('market/', views.market, name='market'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login_c/', views.login_c, name='login_c'),
    path('login_f/', views.login_f, name='login_f'),
    path('pool/<str:store_name>/', views.pool, name='pool'),
    path('upload_xml/', views.upload_xml, name='upload_xml'),
]

# Only add static/media serving if in debug mode
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    if settings.MEDIA_URL and settings.MEDIA_ROOT:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)