from django.shortcuts import render
from rest_framework.views import APIView
from django.http import HttpResponse
import json

from .models import Item
from .serializers import ItemSerializer

# def user_authenticated():
#     return

# Create your views here.
class ItemView(APIView):
    def get(self, request):
        try:
            items = Item.objects.all()
            items_serializer = ItemSerializer(items)
            return HttpResponse(json.dumps(items_serializer), headers = {'Content-Type': 'application/json'})
        except(e):
            print(e)
            return HttpResponse(json.dumps({"message": "error while retrieving data"}), headers = {'Content-Type': 'application/json'})
    def post(self, request):
        item = Item(name=request.data["name"], price=request.data["price"], description=request.data["description"])
        try:
            item.save()
            return HttpResponse(json.dumps({"itemId": item.id }), headers = {'Content-Type': 'application/json'})
        except:
            return HttpResponse(json.dumps({"message" : "error while creating the object" }), headers = {'Content-Type': 'application/json'})
    
    
class ItemParameterView(APIView):
    def get(self, request):
        try:
            items = Item.objects.filter(id=request.data['itemId'])
            if not items:
                return HttpResponse(json.dumps({"message": "item not found"}), status = 404, headers = {"Content-Type": "application/json"})
            else:
                item_serializer = ItemSerializer(items)
                return HttpResponse(json.dumps(item_serializer), status = 200, headers = {"Content-Type": "application/json"})
        except:
            return HttpResponse(json.dumps({"itemId"}))
    def put(self, request):
        try:
            items = Item.objects.filter(id=request.data['itemId'])
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
                    "itemId" : request.data['itemId']
                }), status=200, headers= {"Content-Type": "application/json"})
        except:
            return HttpResponse(json.dumps({
                "message": "error while updating the content"
            }), headers={"Content-Type": "application/json"})
                
    def delete(self, request):
        try:
            items = Item.objects.filter(id=request.data['itemId'])
            if not items:
                return HttpResponse(json.dumps({"message": "item not found"}), status = 404, headers = {"Content-Type": "application/json"})
            else:
                items.delete()
                return HttpResponse(json.dumps({"message":"record deleted successfully", "itemId": request.data['itemId']}), status = 200, headers = {"Content-Type": "application/json"})
        except:
            return HttpResponse(json.dumps({"itemId"}))