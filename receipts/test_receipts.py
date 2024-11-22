from rest_framework.test import APITestCase, APIRequestFactory
from receipts.views import ReceiptViewSet


class TestReceipts(APITestCase):

    def setUp(self) -> None:
        self.receipts_view = ReceiptViewSet.as_view(
            {"post": "process", "get": "points"}
        )
        self.request_factory: APIRequestFactory = APIRequestFactory()
        self.simple_receipt_data = {
            "retailer": "Target",
            "purchaseDate": "2022-01-02",
            "purchaseTime": "13:13",
            "total": "1.25",
            "items": [{"shortDescription": "Pepsi - 12-oz", "price": "1.25"}],
        }
        self.morning_receipt_data = {
            "retailer": "Walgreens",
            "purchaseDate": "2022-01-02",
            "purchaseTime": "08:13",
            "total": "2.65",
            "items": [
                {"shortDescription": "Pepsi - 12-oz", "price": "1.25"},
                {"shortDescription": "Dasani", "price": "1.40"},
            ],
        }
        self.example_1_receipt_data = {
            "retailer": "Target",
            "purchaseDate": "2022-01-01",
            "purchaseTime": "13:01",
            "items": [
                {"shortDescription": "Mountain Dew 12PK", "price": "6.49"},
                {"shortDescription": "Emils Cheese Pizza", "price": "12.25"},
                {"shortDescription": "Knorr Creamy Chicken", "price": "1.26"},
                {"shortDescription": "Doritos Nacho Cheese", "price": "3.35"},
                {"shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ", "price": "12.00"},
            ],
            "total": "35.35",
        }
        self.example_2_receipt_data = {
            "retailer": "M&M Corner Market",
            "purchaseDate": "2022-03-20",
            "purchaseTime": "14:33",
            "items": [
                {"shortDescription": "Gatorade", "price": "2.25"},
                {"shortDescription": "Gatorade", "price": "2.25"},
                {"shortDescription": "Gatorade", "price": "2.25"},
                {"shortDescription": "Gatorade", "price": "2.25"},
            ],
            "total": "9.00",
        }

    def test_process_simple_receipt(self):
        request = self.request_factory.post(
            path="/receipts/process", data=self.simple_receipt_data, format="json"
        )
        response = self.receipts_view(request)
        self.assertEqual(response.status_code, 200)
        request = self.request_factory.get(
            path="/receipts/" + response.data["id"] + "/points"
        )
        response = self.receipts_view(request, pk=response.data["id"])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["points"], 31)

    def test_process_morning_receipt(self):
        request = self.request_factory.post(
            path="/receipts/process", data=self.morning_receipt_data, format="json"
        )
        response = self.receipts_view(request)
        self.assertEqual(response.status_code, 200)
        request = self.request_factory.get(
            path="/receipts/" + response.data["id"] + "/points"
        )
        response = self.receipts_view(request, pk=response.data["id"])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["points"], 15)

    def test_process_example_1_receipt_data(self):
        request = self.request_factory.post(
            path="/receipts/process", data=self.example_1_receipt_data, format="json"
        )
        response = self.receipts_view(request)
        self.assertEqual(response.status_code, 200)
        request = self.request_factory.get(
            path="/receipts/" + response.data["id"] + "/points"
        )
        response = self.receipts_view(request, pk=response.data["id"])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["points"], 28)

    def test_process_example_2_receipt_data(self):
        request = self.request_factory.post(
            path="/receipts/process", data=self.example_2_receipt_data, format="json"
        )
        response = self.receipts_view(request)
        self.assertEqual(response.status_code, 200)
        request = self.request_factory.get(
            path="/receipts/" + response.data["id"] + "/points"
        )
        response = self.receipts_view(request, pk=response.data["id"])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["points"], 109)

    def test_process_receipt_bad_request(self):
        data = {}
        request = self.request_factory.post(
            path="/receipts/process", data=data, format="json"
        )
        response = self.receipts_view(request)
        self.assertEqual(response.status_code, 400)

    def test_process_simple_receipt_not_found(self):
        request = self.request_factory.post(
            path="/receipts/process", data=self.simple_receipt_data, format="json"
        )
        response = self.receipts_view(request)
        self.assertEqual(response.status_code, 200)
        request = self.request_factory.get(path="/receipts/" + "123456" + "/points")
        response = self.receipts_view(request, pk="123456")
        self.assertEqual(response.status_code, 404)
