from rest_framework import serializers

class ItemSerializer(serializers.ModelSerizer):
    class Meta:
        model = Item
        fields = '__all__'