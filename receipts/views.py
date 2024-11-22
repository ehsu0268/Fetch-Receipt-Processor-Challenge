import os

from django.http import HttpResponseBadRequest, HttpResponseNotFound
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializer import ReceiptSerializer
from .points import PointsCalculator
from .db import DBStore


class ReceiptViewSet(viewsets.ViewSet):
    db_store = DBStore()

    @action(methods=['GET'], detail=True)
    def points(self, request, pk):
        points = self.db_store.get(pk)
        if points == -1:
            return HttpResponseNotFound()
        return Response({"points": points})

    @action(methods=['POST'], detail=False)
    def process(self, request):
        receipt_serializer = ReceiptSerializer(data=request.data)
        if not receipt_serializer.is_valid():
            return HttpResponseBadRequest()
        input_data = receipt_serializer.data
        points = PointsCalculator.determine_points(input_data)

        print("Total points: " + str(points))

        id = self.db_store.save(points)
        return Response({"id": id})
