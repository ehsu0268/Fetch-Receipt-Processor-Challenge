import mock
from rest_framework.test import APITestCase, APIRequestFactory
from receipts.views import ReceiptViewSet
from django.db.backends.utils import CursorWrapper

disabled_cursor = mock.Mock()
disabled_cursor.side_effect = RuntimeError("db access disabled")
disabled_cursor.WRAP_ERROR_ATTRS = CursorWrapper.WRAP_ERROR_ATTRS


@mock.patch("django.db.backends.utils.CursorWrapper", disabled_cursor)
@mock.patch("django.db.backends.utils.CursorDebugWrapper", disabled_cursor)
class TestReceipts(APITestCase):

    def setUp(self) -> None:
        self.receipts_view = ReceiptViewSet.as_view({"post": "process", "get": "points"})
        self.request_factory: APIRequestFactory = APIRequestFactory()

    def test_process_simple_receipt(self):
        input_data = {
            "retailer": "Target",
            "purchaseDate": "2022-01-02",
            "purchaseTime": "13:13",
            "total": "1.25",
            "items": [
                {"shortDescription": "Pepsi - 12-oz", "price": "1.25"}
            ]
        }
        request = self.request_factory.post(path="/receipts/process", data=input_data, format="json")
        response = self.receipts_view(request)
        self.assertEqual(response.status_code, 200)
        request = self.request_factory.get(path="/receipts/" + response.data['id'] + "/points")
        response = self.receipts_view(request, pk=response.data['id'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['points'], 31)

    def test_process_morning_receipt(self):
        input_data = {
            "retailer": "Walgreens",
            "purchaseDate": "2022-01-02",
            "purchaseTime": "08:13",
            "total": "2.65",
            "items": [
                {"shortDescription": "Pepsi - 12-oz", "price": "1.25"},
                {"shortDescription": "Dasani", "price": "1.40"}
            ]
        }
        request = self.request_factory.post(path="/receipts/process", data=input_data, format="json")
        response = self.receipts_view(request)
        self.assertEqual(response.status_code, 200)
        request = self.request_factory.get(path="/receipts/" + response.data['id'] + "/points")
        response = self.receipts_view(request, pk=response.data['id'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['points'], 15)

    def test_process_receipt_bad_request(self):
        input_data = {
            "retail": "Target",
            "purchaseDate": "2022-01-02",
            "purchaseTime": "13:13",
            "total": "1.25",
            "items": [
                {"shortDescription": "Pepsi - 12-oz", "price": "1.25"}
            ]
        }
        request = self.request_factory.post(path="/receipts/process", data=input_data, format="json")
        response = self.receipts_view(request)
        self.assertEqual(response.status_code, 400)

    def test_process_simple_receipt_not_found(self):
        input_data = {
            "retailer": "Target",
            "purchaseDate": "2022-01-02",
            "purchaseTime": "13:13",
            "total": "1.25",
            "items": [
                {"shortDescription": "Pepsi - 12-oz", "price": "1.25"}
            ]
        }
        request = self.request_factory.post(path="/receipts/process", data=input_data, format="json")
        response = self.receipts_view(request)
        self.assertEqual(response.status_code, 200)
        request = self.request_factory.get(path="/receipts/" + "123456" + "/points")
        response = self.receipts_view(request, pk="123456")
        self.assertEqual(response.status_code, 404)
