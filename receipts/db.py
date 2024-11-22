import os
import string
import random
import csv
from receipt_processor_challenge.settings import BASE_DIR

FILES = ["data.csv", "test_data.csv"]


class DBStore:

    def __init__(self):
        self.DATA_FILE = (
            "test_data.csv" if os.getenv("UNIT_TEST") == "True" else "data.csv"
        )
        self.clear()

    def save(self, points):
        id = DBStore.generate_id()
        row = [id, str(points)]
        with open(
            str(BASE_DIR) + "/data/" + self.DATA_FILE, "a", newline=""
        ) as csv_file:
            writer = csv.writer(csv_file, delimiter=",")
            writer.writerow(row)
        csv_file.close()
        return id

    def get(self, id):
        with open(
            str(BASE_DIR) + "/data/" + self.DATA_FILE, "r", newline=""
        ) as csv_file:
            file_reader = csv.reader(csv_file, delimiter=",")

            for row in file_reader:
                curr_id = row[0]
                if curr_id == id:
                    return int(row[1])
        csv_file.close()
        return -1

    def clear(self):
        for file in FILES:
            f = open(str(BASE_DIR) + "/data/" + file, "w+")
            f.close()

    @staticmethod
    def generate_id():
        key_values = [9, 4, 4, 4, 12]
        id_values = []
        for key in key_values:
            id_values.append(
                "".join(random.choices(string.ascii_lowercase + string.digits, k=key))
            )
        return "-".join(id_values)
