from django.urls import path
from . import views
from .views import UpdateUser,CleanWishlist,GetWishlist,DeleteFromWishlist,Wishlist,AddOrder,GetProducts,UpdatePriceToProduct,AddCategory,GetProductsByCategory, MyTokenObtainPairView,AddProduct


urlpatterns = [
     path('test/', views.get_data),
     path('register/', views.register),# Register to the website.
     path('updateProd/',views.UpdatePriceToProduct), # Update Product price.
     path('products/<id>/',views.GetProducts),# Get Product by his category id
     path('products/',views.GetProducts), # Get all Products
     path("addProduct/", views.AddProduct), # Add new Product to DB
     path("getprodbycat/",views.GetProductsByCategory),
     # path('mycartprods/',views.GetCartProdsbyidw),
     path('addOrder/',views.AddOrder),
     path("addCategory/",views.AddCategory),
     path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),# log in
     path('logout/',views.myLogout), # Logout of the website.
     path('AddToWishlist/',views.AddToWishlist), # Add an item to the user Wishlist 
     path('RemoveFromWishlist/', views.DeleteFromWishlist), # Remove specific item from Wishlist
     path('GetWishlist/',views.GetWishlist), # Get all of the user items in his Wishlist
     path('CleanWishlist/', views.CleanWishlist), # Clean the user Wishlist.
     path('UpdateUser/',views.UpdateUser),
]