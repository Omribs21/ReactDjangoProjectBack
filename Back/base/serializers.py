from dataclasses import fields
from operator import imod
from pyexpat import model
from sre_parse import CATEGORIES
from rest_framework.serializers import ModelSerializer
from base.models import Categories,Products,Orders,Wishlist


class CategorySerializer(ModelSerializer):
    class Meta:
        model= Categories
        fields ='__all__'


class ProductSerializer(ModelSerializer):
    class Meta:
        model= Products
        fields ='__all__'

class OrderSerializer(ModelSerializer):
    class Meta:
        model= Orders
        fields ='__all__'


class WishlistSerializer(ModelSerializer):
    class Meta:
        model= Wishlist
        fields ='__all__'