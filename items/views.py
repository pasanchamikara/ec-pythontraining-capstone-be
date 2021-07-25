from django.shortcuts import render
from rest_framework.views import APIView

from django.http import HttpResponse, JsonResponse
import json
import requests

from .models import Item
from .serializers import ItemSerializer

# def user_authenticated():
#     return

class AuthRegisterView(APIView):
    def post(self, request):
        user_data = {"email": request.data["email"], "name": request.data["name"], "password": request.data["password"]}
        res = requests.post('http://localhost/auth/signup', user_data)
        if res.status_code == 200:
            return
        else:
            return

class AuthLoginView(APIView):
    def post(self, request):
        user_data = {"email": request.data["email"], "password": request.data["password"]}
        res = request.post('http://localhost/auth/signin', user_data)
        if res.status_code == 200:
            return
        else:
            return


# Create your views here.
@method_decorator()
class ItemView(APIView):
    def get(self, request):
        try:
            items = list(Item.objects.values())
            # print(json.dumps(items))
            items_json = json.dumps(items)
            print(type(items_json))
            # items_serializer = ItemSerializer(items)
            # return JsonResponse({"data": json.loads(items_json)} ,  safe=False)
            return JsonResponse(json.loads(items_json) ,  safe=False)

        except Exception as e:
            print(str(e))
            return HttpResponse(json.dumps({"message": "error while retrieving data"}), headers = {'Content-Type': 'application/json'})
    def post(self, request):
        item = Item(name=request.data["name"], price=request.data["price"], description=request.data["description"])
        try:
            item.save()
            return HttpResponse(json.dumps({"itemId": item.id }), headers = {'Content-Type': 'application/json'})
        except:
            return HttpResponse(json.dumps({"message" : "error while creating the object" }), headers = {'Content-Type': 'application/json'})
    

@method_decorator()    
class ItemParameterView(APIView):
    def get(self, request, itemId):
        try:
            items = Item.objects.filter(id=itemId).values()

            items_dict = list(items)[0]
        
            return HttpResponse(json.dumps(items_dict), status = 200, headers = {"Content-Type": "application/json"})
        except IndexError:
             return HttpResponse(json.dumps({"message": "item not found"}), status = 404, headers = {"Content-Type": "application/json"})
        except(e):
            return HttpResponse(json.dumps({"itemId": itemId}), headers = { "Content-Type": "application/json"})
    def put(self, request, itemId):
        try:
            items = Item.objects.filter(id=itemId)
            if not items:
                return HttpResponse(json.dumps({"message": "item not found"}), status = 404, headers = {"Content-Type": "application/json"})
            else:
                if request.data["name"]:
                    items.name = request.data["name"]
                if request.data["price"]:
                    items.price = request.data["price"]
                if request.data["description"]:
                    items.description = request.data["description"]
                items.save()
                return HttpResponse(json.dumps({
                    "message": "content updated",
                    "itemId" : itemId
                }), status=200, headers= {"Content-Type": "application/json"})
        except:
            return HttpResponse(json.dumps({
                "message": "error while updating the content"
            }), headers={"Content-Type": "application/json"})
                
    def delete(self, request, itemId):
        try:
            items = Item.objects.filter(id=itemId)
            if not items:
                return HttpResponse(json.dumps({"message": "item not found"}), status = 404, headers = {"Content-Type": "application/json"})
            else:
                items.delete()
                return HttpResponse(json.dumps({"message":"record deleted successfully", "itemId": itemId}), status = 200, headers = {"Content-Type": "application/json"})
        except:
            return HttpResponse(json.dumps({"message": "error while deleting the record"}), status=404)