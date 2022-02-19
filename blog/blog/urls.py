"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from blog.views import register
from homework.views import homework_index, profile_index
from posts.views import posts_index, posts_index_user, add_post, user_login, logout_view
from shop.views import prod_list, product_details_view, currency_converter

urlpatterns = [
    path("admin/django-rq/", include("django_rq.urls")),
    path('admin/', admin.site.urls),
    path('', posts_index, name="home"),
    path('homework/', homework_index),
    path('profile/', profile_index),
    path('posts_index_user/', posts_index_user),
    path('register/', register),
    path('add/', add_post),
    path('shop/', prod_list, name="product_list"),
    path(
        "product/<int:product_id>/", product_details_view, name="product_details_view"
    ),
    path('login/', user_login, name='login'),
    path('logout/', logout_view, name='logout'),
    path("api/", include("api.urls", namespace="api")),
    path("currencyconverter/", currency_converter),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
