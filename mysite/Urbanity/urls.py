from django.urls import path
from . import views

urlpatterns = [
	#Leave as empty string for base url
	path('products', views.StoreListView.as_view(), name="products"),
	path('main/', views.main, name="main"),
	path('', views.main, name="main"),
    path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.updateitem, name="updateitem"),
    path('process_order/', views.processOrder, name="processOrder"),
	path('login/', views.login, name="login"),
	path('logoutUser/', views.logoutUser, name="logoutUser"),
	path('verify/', views.verify_user, name="verify"),
	path('<int:id>',views.show , name='show'),
	path('search/',views.search , name='search'),
	path('showSearchedProduct/', views.showSearchedProduct, name='showSearchedProduct')
]
