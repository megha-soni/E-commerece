from django.urls import path
from . import views

urlpatterns=[
path('',views.home,name='home'),
path('signup/',views.Signup,name="signup"),
path('login/',views.Login,name="login"),
path('logout/',views.Logout,name="logout"),
path("dress/",views.Dress,name='dress'),
path("jeans/",views.Jeans,name='jeans'),
path("jacket/",views.Jacket,name='jacket'),
path("shirt/",views.Shirt,name='shirt'),
path("watch/",views.Watch,name='watch'),
path("sunglass/",views.Sunglass,name='sunglass'),
path("candle/",views.Candle,name='candle'),
path("tee/",views.Tee,name='tee'),
path("search/",views.Search,name="search"),
path("men/",views.Men,name="men"),
path("women/",views.Women,name="women"),
path("productdetail/<int:id>/",views.ProductDetail,name="productdetail"),
path('filter/',views.filterprice,name='filter'),
path('changepassword/',views.Changepwd,name="changepwd"),
path('addtocart/',views.AddToCart,name="addtocart"),
path('showcart/',views.ShowCart,name="showcart"),
path("RemoveItem/<int:id>/",views.RemoveItems,name="remove"),
path("itpay/",views.item_payment,name='item_payment'),
path("payment-Status/",views.payment_status,name='payment-status')

]
