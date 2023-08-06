import pprint
import unittest
import random

from src.analyser_hj3415.db import mongo
from src.analyser_hj3415.report import Report

addr = "mongodb://192.168.0.173:27017"
client = mongo.connect_mongo(addr)
all_codes = mongo.Corps.get_all_codes(client)


class ReportTest(unittest.TestCase):
    def setUp(self):
        self.rndcode = random.choice(all_codes)

    def test_Report(self):
        print(Report(client, self.rndcode))

    def test_Report_for_django(self):
        self.rndcode = '005930'
        pprint.pprint(Report(client, self.rndcode).for_django())
