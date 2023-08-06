from django.urls import path

from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "orders"

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_request, name="login"),
    path("register/", views.register, name="register"),
    path("logout", views.logout_request, name="logout"),
    path("pizza", views.pizza, name="pizza"),
    path("SufiNight", views.SufiNight, name="SufiNight"),
    path("TheatreAct", views.TheatreAct, name="TheatreAct"),
    path("sunburn", views.sunburn, name="sunburn"),
    path("Pasta", views.pasta, name="pasta"),
    path("Salad", views.salad, name="salad"),
    path("Concert", views.Concert, name="Concert"),
    path("Subs", views.subs, name="subs"),
    path("ComedyNight", views.ComedyNight, name="ComedyNight"),
    path("Platters", views.dinner_platters, name="dinner_platters"),
    path("DJshow", views.DJshow, name="DJshow"),
    path("directions", views.directions, name="directions"),
    path("hours", views.hours, name="hours"),
    path("contact", views.contact, name="contact"),
    path("cart", views.cart, name="cart"),
    path("checkout", views.checkout, name="checkout"),
    path("view-orders", views.view_orders, name="view_orders"),
    path("mark_order_as_delivered", views.mark_order_as_delivered, name="mark_order_as_delivered"),
    path("save_cart", views.save_cart, name="save_cart"),
    path("retrieve_saved_cart", views.retrieve_saved_cart, name="retrieve_saved_cart"),
    path("check_superuser", views.check_superuser, name="check_superuser"),
    path('delete_item', views.delete_item, name='delete_item'),
    path('delete_order', views.delete_order, name='delete_order'),


]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

