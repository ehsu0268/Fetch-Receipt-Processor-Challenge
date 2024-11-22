from decimal import Decimal
import math


class PointsCalculator:

    @staticmethod
    def determine_points(receipt):
        print("Retail: " + str(RetailProcessor.calculate(receipt['retailer'])) + "\n" +
              "Total: " + str(TotalProcessor.calculate(receipt['total'])) + "\n" +
              "Items: " + str(ItemsProcessor.calculate(receipt['items'])) + "\n" +
              "Day: " + str(DayProcessor.calculate(receipt['purchaseDate']))  + "\n" +
              "Time: " + str(TimeProcessor.calculate(receipt['purchaseTime'])))
        return RetailProcessor.calculate(receipt['retailer']) + TotalProcessor.calculate(receipt['total']) + \
        ItemsProcessor.calculate(receipt['items']) + DayProcessor.calculate(receipt['purchaseDate']) + \
        TimeProcessor.calculate(receipt['purchaseTime'])


class RetailProcessor:

    @staticmethod
    def calculate(input: str):
        return len([c for c in input if c.isalnum()])


class TotalProcessor:

    @staticmethod
    def calculate(input: str):
        return TotalProcessor.round_dollar_amount(input) + TotalProcessor.multiple_of_quarter(input)

    @staticmethod
    def round_dollar_amount(input):
        return 50 if int(input.split('.')[-1]) == 0 else 0

    @staticmethod
    def multiple_of_quarter(input):
        values = input.split('.')
        curr_total = int(values[0]) * 100 + int(values[1])
        return 25 if curr_total % 25 == 0 else 0


class ItemsProcessor:

    @staticmethod
    def calculate(items):
        return ItemsProcessor.number_of_items(items) + ItemsProcessor.item_description(items)

    @staticmethod
    def number_of_items(items):
        return int(len(items) / 2) * 5

    @staticmethod
    def item_description(items):
        curr_total = 0
        for item in items:
            if len(item['shortDescription'].strip()) % 3 == 0:
                price = math.ceil(Decimal(item['price']) * Decimal(0.2))
                curr_total += price
        return curr_total


class DayProcessor:

    @staticmethod
    def calculate(input: str):
        return 6 if int(input.split('-')[-1]) % 2 != 0 else 0


class TimeProcessor:

    @staticmethod
    def calculate(input: str):
        return 10 if "14:00" < input < "16:00" else 0
