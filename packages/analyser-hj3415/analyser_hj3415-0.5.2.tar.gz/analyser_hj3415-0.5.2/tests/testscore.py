import unittest
import random

from src.analyser_hj3415.db import mongo
from src.analyser_hj3415.score import red, mil, blue, growth

addr = "mongodb://192.168.0.173:27017"
client = mongo.connect_mongo(addr)
all_codes = mongo.Corps.get_all_codes(client)


class ScoreTest(unittest.TestCase):
    def setUp(self):
        self.rndcode = random.choice(all_codes)
        self.rndname = mongo.Corps.get_name(client, self.rndcode)

        self.code_one = '005930'
        self.code_one_name = mongo.Corps.get_name(client, self.code_one)

    def test_red_one(self):
        print("양수면 주가가 고평가되어 있는 상태, 음수면 저평가. 음수가 현재 주가가 싸다는 의미")

        # 랜덤 종목 테스트
        p, q = red(client, self.rndcode)
        print(self.rndcode, self.rndname, p, q)

        # 원하는 종목 테스트
        p, q = red(client, self.code_one)
        print(self.code_one, self.code_one_name, p, q)

    def test_red_all(self):
        for i, code in enumerate(all_codes):
            name = mongo.Corps.get_name(client, code)
            p, q = red(client, code)
            print(i+1, name, p, q)

    def test_mil_one(self):
        # 랜덤 종목 테스트
        p1, p2, p3, p4 = mil(client, self.rndcode)
        print(self.rndcode, self.rndname, "주주수익률", p1, "이익지표", p2, "투자수익률", p3, "PFCF포인트", p4)

        # 원하는 종목 테스트
        p1, p2, p3, p4 = mil(client, self.code_one)
        print(self.code_one, self.code_one_name, "주주수익률", p1, "이익지표", p2, "투자수익률", p3, "PFCF포인트", p4)

    def test_mil_all(self):
        for i, code in enumerate(all_codes):
            name = mongo.Corps.get_name(client, code)
            p1, p2, p3, p4 = mil(client, code)
            print(i+1, code, name, "주주수익률", p1, "이익지표", p2, "투자수익률", p3, "PFCF포인트", p4)

    def test_blue_one(self):
        # 랜덤 종목 테스트
        p1, p2, p3, p4, p5 = blue(client, self.rndcode)
        print(self.rndcode, self.rndname, "유동비율", p1, "이자보상배율", p2, "순부채비율", p3, "순운전자본회전율", p4, "재고자산회전율", p5)

    def test_blue_all(self):
        for i, code in enumerate(all_codes):
            name = mongo.Corps.get_name(client, code)
            p1, p2, p3, p4, p5 = blue(client, code)
            print(i+1, code, name, "유동비율", p1, "이자보상배율", p2, "순부채비율", p3, "순운전자본회전율", p4, "재고자산회전율", p5)

    def test_growth_one(self):
        # 랜덤 종목 테스트
        p1, p2 = growth(client, self.rndcode)
        print(self.rndcode, self.rndname, "매출액증가율", p1, "영업이익률", p2)

    def test_growth_all(self):
        for i, code in enumerate(all_codes):
            name = mongo.Corps.get_name(client, code)
            p1, p2 = growth(client, self.rndcode)
            print(i+1, code, name, "매출액증가율", p1, "영업이익률", p2)

    def test_one(self):
        code = '352700'
        name = mongo.Corps.get_name(client, code)
        print('/'.join([str(1), str(code), str(name)]))
        print('red', red(client, code))
        print('mil', mil(client, code))
        print('blue', blue(client, code))
        print('growth', growth(client, code))

    def test_all(self):
        for i, code in enumerate(all_codes):
            name = mongo.Corps.get_name(client, code)
            print('/'.join([str(i+1), str(code), str(name)]))
            print('red', red(client, code))
            print('mil', mil(client, code))
            print('blue', blue(client, code))
            print('growth', growth(client, code))
