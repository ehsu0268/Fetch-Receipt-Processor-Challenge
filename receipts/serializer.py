from rest_framework import serializers


class ItemSerializer(serializers.Serializer):
    shortDescription = serializers.CharField(max_length=100)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)


class ReceiptSerializer(serializers.Serializer):
    retailer = serializers.CharField(max_length=100)
    purchaseDate = serializers.DateField(format="%Y-%m-%d")
    purchaseTime = serializers.TimeField(format="%H:%M")
    items = ItemSerializer(many=True)
    total = serializers.DecimalField(max_digits=100, decimal_places=2)
