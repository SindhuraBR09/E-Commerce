from django.urls import path
from . import views

urlpatterns = [
	#Leave as empty string for base url
	path('', views.StoreListView.as_view(), name="store"),
	path('main/', views.main, name="main"),
    path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.updateitem, name="updateitem"),
    path('process_order/', views.processOrder, name="processOrder"),
]
