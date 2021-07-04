from django.shortcuts import render
from rest_framework import APIView
from django.http import HttpResponse

from .models import Item

# Create your views here.
class ItemView(APIView):
    def get(self, request):
        return
    def post(self, request):
        item = Item(name=request.data["name"], price=request.data["price"], description=request.data["description"])
        try:
            item.save()
            return HttpResponse(json.dumps({"itemId": item.id }), headers = {'Content-Type': 'application/json'})
        except as e:
            return HttpResponse(json.dumps({"message" : item.id }), headers = {'Content-Type': 'application/json'})
    def put(self, request):
        return
    def delete(self, request):
        return
    
class ItemParameterView(APIView):
    def get(self, request):
        items = Item.objects.filter()
        return
    def post(self, request):
        return