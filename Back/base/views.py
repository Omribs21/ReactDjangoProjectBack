from ast import Return
from unicodedata import category
from urllib import response
from django.http import JsonResponse
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
import json
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
from base.serializers import OrderSerializer,CategorySerializer,ProductSerializer,WishlistSerializer
from base.models import Profile,Categories,Products,Orders,Orders_details,Wishlist
from django.contrib.auth import logout

def index(req):
    return JsonResponse('hello', safe=False)


@api_view(['GET'])
def get_data(request):
    if request.method == 'GET':
        return JsonResponse({"test":"test"} , safe=False)
    

@api_view(["POST"])
def register(request):
    Username = request.data["username"]
    Password = request.data["password"]
    Email = request.data["email"]
    First_name = request.data["first_name"]
    Last_name = request.data["last_name"]
    print(Username, Password, Email,)
    user = User.objects.create_user(
        username=Username, password=Password, email=Email,first_name= First_name, last_name= Last_name)
    return Response({"first name": First_name, "last name": Last_name})


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    # classmethod (static method) method we can use with out creating an object
    @classmethod
    def get_token(cls, user):
        # super -> the class we inherit
        token = super().get_token(user)
        # select one row from Profile table (where user = given user)
        token['username'] = user.username
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name  
        token['email'] = user.email   
                # from here it's our code
        # pro = Profile.objects.get(user=user)
        # print(pro)
        # our code done
        print("logged")
        return token
    
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def UpdateUser(request):
    user_id = request.user.id 
    city = request.data["city"]
    temp_user =  User.objects.get(id = user_id)
    temp_user.city =city
    return JsonResponse({"updated"})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def myLogout(request):
    logout(request)
    return Response("logged out")
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(["POST"])
def AddCategory(request):
    serializer = CategorySerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
    else:
        return Response("data was not saved")
    return Response({'new category':"added"})

@api_view(["POST"])
def AddProduct(request):
    serializer = ProductSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
    else:
        return Response("data was not saved")
    return Response({"new product":"Added"})

@api_view(["GET"])
def GetProductsByCategory(request):
    products = Products.objects.filter(category = request.data["catId"])
    serializer = ProductSerializer(products,many = True)
    return Response(serializer.data)

@api_view(["PUT"])
def UpdatePriceToProduct(request):
    id = request.data["_id"]
    temp=Products.objects.get(_id = id)
    temp.price =request.data['price']
    temp.save()
    return Response({"new price":"Updated"})

@api_view(["GET"])
def GetProducts(request, id = 0):
    if int(id) > 0:
        products = Products.objects.filter(_id = int(id))
    else:
        products = Products.objects.all()
    serializer = ProductSerializer(products,many =True)
    return Response(serializer.data)

    



@api_view(["POST"])
@permission_classes([IsAuthenticated])
def AddOrder(request):
    # User_id = request.user.id

    # details for the order.
    myCart = (request.data["cartItems"])["CartItems"]
    city = request.data["city"]
    district = request.data["district"]
    phone =request.data["phone"]
    postalCode = request.data["postalCode"]
    totalCart = request.data["total"]

    # create new order with the values above.
    newOrder = Orders.objects.create(user = request.user,city= city,district=district,phone_num = phone, postal_code = postalCode,Total = totalCart)
    
    # add every item of the order to the DB with the order Id
    for item in myCart:
        print(item)
        Orders_details.objects.create(
            order_id = newOrder, 
            desc = item["desc"],
            back_name = item["back_name"],
            price = item["price"],
            quantity = item["quantity"],
            total = item["total"],
            patch = item["patch"],
            size = item["size"])
    return Response({"order saved, cost:":totalCart})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def AddToWishlist(request):
    user_id = request.user.id # returnes the user id.
    user = request.user # returnes the user as an Object.
    prod_id = request.data["prod_id"] # returnes the id of the product
    product_id = Products.objects.get(_id = request.data["prod_id"])
    count = Wishlist.objects.filter(prod_id = prod_id, user_id= user_id).count()
    if count >= 1: # checks if the product id and the same user id is already in db.
        return Response("item already in wishlist") # if so notify.
    else: # otherwise add the new item to the user wishlist
        Wishlist.objects.create(user = user, prod_id = product_id)
        return Response("item added to wishlist.")

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def DeleteFromWishlist(request):
    # DELETE the item from the Wishlist by its ID and the user ID.
    Wishlist.objects.filter(prod_id=request.data["prod_id"],user_id = request.data["user_id"]).delete()
    return JsonResponse({"item ID that deleted":request.data["prod_id"]})

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def CleanWishlist(request):
    # DELETE the whole user's wishlist --> Clean it.
    user_id = request.data["user_id"]
    all_products = Wishlist.objects.filter(user_id= user_id)
    for prod in all_products:  
        prod.delete()
    return JsonResponse({"Your wishlist is empty!":user_id})
        


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetWishlist(request):
    user_id = request.user.id # returnes the user id as int.
    all_products = Wishlist.objects.filter(user_id = user_id) # returnes all the product of the user 
    serializer = WishlistSerializer(all_products,many =True)
    return Response(serializer.data) # returnes the data in JSON format.