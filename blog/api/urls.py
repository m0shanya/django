from django.urls import include, path
from rest_framework import routers

from api.homework.views import ProfileViewSet
from api.posts.views import PostViewSet
from api.shop.views import PurchaseViewSet, PurchaseCreateView
from api.users.views import UserViewSet, UserCreateView, UserLoginView, UserLogoutView

app_name = "api"

router = routers.DefaultRouter()
router.register(r"posts", PostViewSet)
router.register(r"shop_list", PurchaseViewSet, basename="shop")
router.register(r"users", UserViewSet, basename="users")
router.register(r"profiles", ProfileViewSet, basename="profiles")


urlpatterns = [
    path("", include(router.urls)),
    path("register/", UserCreateView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("purchases/", PurchaseViewSet.as_view({'get': 'list'}), name="purchase_list"),
    path("add_p/", PurchaseCreateView.as_view(), name="add_purchase"),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
