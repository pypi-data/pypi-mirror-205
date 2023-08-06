"""다양한 문자열 출력 형식에 맞춘 함수들
"""
from .db import mongo
from .eval import red as eval_red, mil as eval_mil, blue as eval_blue, growth as eval_growth
from .score import red as score_red, mil as score_mil, blue as score_blue, growth as score_growth
from util_hj3415 import utils
import textwrap

import logging
logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(levelname)s: [%(name)s] %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.WARNING)


class Report:
    separate_line = '\n' + ('-' * 65) + '\n'

    def __init__(self, client, code: str):
        self.client = client
        self.code = code
        self.name = mongo.Corps.get_name(client, code)

    def __str__(self):
        return (self.c101() + self.separate_line
                + self.red() + self.separate_line
                + self.mil() + self.separate_line
                + self.blue() + self.separate_line
                + self.growth())
        # + make_str.c108())

    def c101(self, full=True):
        c101 = mongo.C101(self.client, self.code).get_recent(merge_intro=True)
        logger.info(c101)

        title = '=' * 35 + f"\t{c101['코드']}\t\t{c101['종목명']}\t\t{c101['업종']}\t" + '=' * 35
        intro = textwrap.fill(f"{c101['intro']}", width=70)

        if full:
            price = (f"{c101['date']}\t\t"
                     f"주가: {utils.deco_num(c101['주가'])}원\t\t"
                     f"52주최고: {utils.deco_num(c101['최고52주'])}원\t"
                     f"52주최저: {utils.deco_num(c101['최저52주'])}원")
            info = (f"PER: {c101['PER']}\t\t"
                    f"PBR: {c101['PBR']}\t\t\t"
                    f"배당수익률: {c101['배당수익률']}%\t\t"
                    f"시가총액: {utils.get_kor_amount(utils.to_int(c101['시가총액']), omit='억')}\n"
                    f"업종PER: {c101['업종PER']}\t"
                    f"유통비율: {c101['유통비율']}%\t\t"
                    f"거래대금: {utils.to_억(c101['거래대금'])}원\t\t"
                    f"발행주식: {utils.to_만(c101['발행주식'])}주")
        else:
            price = (f"<< {c101['date']} >>\n"
                     f"주가: {utils.deco_num(c101['주가'])}원")
            info = (f"PER: {c101['PER']}\n"
                    f"업종PER: {c101['업종PER']}\n"
                    f"PBR: {c101['PBR']}\n"
                    f"배당수익률: {c101['배당수익률']}%\n"
                    f"유통비율: {c101['유통비율']}%\n"
                    f"발행주식: {utils.to_만(c101['발행주식'])}주\n"
                    f"시가총액: {utils.get_kor_amount(utils.to_int(c101['시가총액']), omit='억')}")

        return title + '\n' + intro + self.separate_line + price + '\n' + info

    def red(self, full=True) -> str:
        red_dict = eval_red(self.client, self.code)
        p, 괴리율 = score_red(self.client, self.code)
        logger.info(red_dict)

        title = f"Red\tPoint({p})\t괴리율({괴리율}%)\t{red_dict['date']}\n"
        if full:
            contents = (f"사업가치({utils.deco_num(red_dict['사업가치'])}억) "
                        f"+ 재산가치({utils.deco_num(red_dict['재산가치'])}억) "
                        f"- 부채({utils.deco_num(red_dict['부채평가'])}억) "
                        f"/ 발행주식({utils.to_만(red_dict['발행주식수'])}주) "
                        f"= {utils.deco_num(red_dict['red_price'])}원")
        else:
            contents = f"{utils.deco_num(red_dict['red_price'])}원"
        return title + contents

    def mil(self, full=True) -> str:
        mil_dict = eval_mil(self.client, self.code)
        p1, p2, p3, p4 = score_mil(self.client, self.code)
        logger.info(mil_dict)

        title = f"Millenial\tPoint({p1+p2+p3+p4})\t{mil_dict['date']}\n"
        if full:
            contents = (f"1. 주주수익률({p1}): {mil_dict['주주수익률']} %\n"
                        f"2. 이익지표({p2}): {mil_dict['이익지표']}\n"
                        f"3. 투자수익률({p3}): ROIC 4분기합: {mil_dict['투자수익률']['ROIC']}%, "
                        f"최근 ROE: {mil_dict['투자수익률']['ROE']}%\n"
                        f"4. 가치지표\n"
                        f"\tFCF: {mil_dict['가치지표']['FCF']}\n"
                        f"\tPFCF({p4}) : {mil_dict['가치지표']['PFCF']}\n"
                        f"\tPCR: {mil_dict['가치지표']['PCR']}")
        else:
            contents = (f"1. 주주수익률({p1}): {mil_dict['주주수익률']} %\n"
                        f"2. 이익지표({p2}): {mil_dict['이익지표']}\n"
                        f"3. 투자수익률({p3}): ROIC 4분기합: {mil_dict['투자수익률']['ROIC']}%, "
                        f"최근 ROE: {mil_dict['투자수익률']['ROE']}%\n"
                        f"4. 가치지표\tPFCF({p4}) : {mongo.EvalTools.get_recent(mil_dict['가치지표']['PFCF'])}")
        return title + contents

    def blue(self, full=True) -> str:
        blue_dict = eval_blue(self.client, self.code)
        p1, p2, p3, p4, p5 = score_blue(self.client, self.code)
        logger.info(blue_dict)

        title = f"Blue\tPoint({p1+p2+p3+p4+p5})\t{blue_dict['date']}\n"
        if full:
            contents = (f"1. 유동비율({p1}): {blue_dict['유동비율']}(100이하 위험)\n"
                        f"2. 이자보상배율({p2}): {blue_dict['이자보상배율']}(1이하 위험 5이상 양호)\n"
                        f"3. 순부채비율({p3}): {blue_dict['순부채비율']}(30이상 not good)\n"
                        f"4. 순운전자본회전율({p4}): {blue_dict['순운전자본회전율']}\n"
                        f"5. 재고자산회전율({p5}): {blue_dict['재고자산회전율']}")

        else:
            contents = ''
        return title + contents

    def growth(self, full=True) -> str:
        growth_dict = eval_growth(self.client, self.code)
        p1, p2 = score_growth(self.client, self.code)
        logger.info(growth_dict)

        title = f"Growth\tPoint({p1 + p2})\t{growth_dict['date']}\n"
        if full:
            contents = (f"1. 매출액증가율({p1}): {growth_dict['매출액증가율']}\n"
                        f"2. 영업이익률({p2}): {growth_dict['영업이익률']}")
        else:
            contents = (f"1. 매출액증가율({p1}): {growth_dict['매출액증가율'][0]}\n"
                        f"2. 영업이익률({p2}): {growth_dict['영업이익률'].get(self.name)}")
        return title + contents

    def for_django(self) -> dict:
        """
        장고에서 report 페이지에서 사용될 eval & score data 를 반환

        장고의 view context는 딕셔너리 형식이기 때문에 딕셔너리 모음으로 반환한다.

        리턴값
        {'blue': {'date': ['2022/12'],
        '순부채비율': (-29.57, {'2018/12': -34.82,...'2023/12': -27.54}),
        '순운전자본회전율': (1.59, {'2018/12': 12.3,...'2023/12': nan}),
        '유동비율': 278.86,
        '이자보상배율': (15.7, {'2018/12': 87.29,...'2023/12': nan}),
        '재고자산회전율': (1.29, {'2018/12': 9.03,...'2023/12': nan})},
        'blue_s': (0, 0, 0, -1, 0),
        'c101': {'BPS': 50817.0, 'EPS': 8057.0, 'PBR': 1.28, 'PER': 8.08, 'date': '2023.04.14', 'intro': '...',
        '거래대금': '1062800000000', '거래량': '16176500', '발행주식': '5969782550', '배당수익률': '2.22', '베타52주': '0.95',
        '시가총액': '388632800000000', '업종': '반도체와반도체장비', '업종PER': '8.36', '유통비율': '75.82', '종목명': '삼성전자',
        '주가': '65100', '최고52주': '68800', '최저52주': '51800', '코드': '005930'},
        'growth': {'date': ['2022/12'],
        '매출액증가율': (-8.23, {'2018/12': 1.75,...'2023/12': -10.5}),
        '영업이익률': {'LG디스플레이': '3.61', 'LG전자': '42.38', 'SK하이닉스': '15.26', '삼성전자': '14.35', '에스에프에이': '45.89'}},
        'growth_s': (-2, 1),
        'mil': {'date': ['2022/12'],
        '가치지표': {'FCF': {'2018/12': 374754.5,...'2023/12': 24605.8},
                  'PCR': {'2021/12': 8.17,...'2022/12': 6.04},
                  'PFCF': {'2018/12': 10.37,...'2023/12': 157.94}},
        '이익지표': -0.01917,
        '주주수익률': 4.99,
        '투자수익률': {'ROE': 17.07, 'ROIC': 13.41}},
        'mil_s': (1, 10, 7, 0),
        'red': {'date': ['2022/12'], 'red_price': 264881, '발행주식수': 6792669000.0, '부채평가': 1257599.6,
        '사업가치': 13682505.0, '재산가치': 5567563.52},
        'red_s': (53, -75.42)}
        """
        return {
            'c101': mongo.C101(self.client, self.code).get_recent(merge_intro=True),
            'red': eval_red(self.client, self.code),
            'mil': eval_mil(self.client, self.code),
            'blue': eval_blue(self.client, self.code),
            'growth': eval_growth(self.client, self.code),
            # 'c108': mongo.C108(self.client, self.code).get_recent(),
            'red_s': score_red(self.client, self.code),
            'mil_s': score_mil(self.client, self.code),
            'blue_s': score_blue(self.client, self.code),
            'growth_s': score_growth(self.client, self.code),
        }


    """
    def c108(self, full=True) -> str:
        if full:
            c108_list = mongo.C108(self.client, self.code).get_all()
        else:
            c108_list = mongo.C108(self.client, self.code).get_recent()
        s = ''
        logger.info(c108_list)
        for i, c108_dict in enumerate(c108_list):
            logger.info(c108_dict)
            if i == 0:
                pass
            else:
                s += '\n'
            header = f"{c108_dict['날짜']}\thprice : {c108_dict['목표가']} 원\n"
            title = f"<<{c108_dict['제목']}>>\n"
            contents = ''
            for line in c108_dict['내용'].split('▶'):
                contents += line.strip()
            s += header + title + textwrap.fill(contents, width=70) + self.separate_line
        return s
    """



def for_telegram(client, code: str) -> str:
    make_str = MakeStr(client, code)

    return (make_str.c101(full=False) + make_str.separate_line
            + make_str.red(full=False) + make_str.separate_line
            + make_str.mil(full=False) + make_str.separate_line
            + make_str.blue(full=False) + make_str.separate_line
            + make_str.growth(full=False))
            # + make_str.c108(full=False))
