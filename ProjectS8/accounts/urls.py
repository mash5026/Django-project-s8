from django.urls import path
from . import views

urlpatterns = [
    path("", views.index , name = 'index'),
    path("get-accounts",views.get_account,name="accounts"),
    path("create-accounts",views.create_accounts,name="create-accounts"),
    path("mobile-verify",views.mobile_verify,name="mobile-verify"),
    path("login",views.login,name="login"),
    path("edit-profile",views.edit_profile,name="edit_profile"),
    path("order",views.order,name="order"),
    path("get-order",views.get_order,name="get_order")

]
