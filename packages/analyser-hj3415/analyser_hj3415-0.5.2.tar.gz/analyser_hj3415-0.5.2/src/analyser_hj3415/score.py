import math
import numpy
import pprint
import copy
from typing import Tuple

from .db import mongo
from .eval import EXPECT_EARN, red as eval_red, mil as eval_mil, blue as eval_blue, growth as eval_growth
from util_hj3415 import utils

import logging

logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(levelname)s: [%(name)s] %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.WARNING)


def red(client, code: str) -> Tuple[int, float]:
    """red price와 최근 주가의 괴리율 파악

    양수면 주가가 고평가되어 있는 상태, 음수면 저평가
    음수가 현재 주가가 싸다는 의미

    Returns:
        tuple : 괴리율을 기반으로한 포인트, 주가와 red price 비교한 괴리율
    """
    c101 = mongo.C101(client, code)

    logger.debug(f'c101 {c101.get_recent()}')

    try:
        recent_price = utils.to_int(c101.get_recent()['주가'])
    except KeyError:
        recent_price = float('nan')
    red_price = eval_red(client, code)['red_price']

    logger.debug(f"recent_price : {recent_price}\tred_price : {red_price}")

    try:
        # 괴리율 구하는 공식이 두가지임. 어떤걸 사용해도 동일함
        f1 = round((recent_price / red_price - 1) * 100, 2)
        f2 = round((recent_price - red_price) / red_price * 100, 2)
        logger.debug(f'f1 : {f1}, f2 : {f2}')
        괴리율 = round((recent_price / red_price - 1) * 100, 2)
    except ZeroDivisionError:
        괴리율 = float('nan')

    logger.debug(f'괴리율 : {괴리율}')

    if math.isnan(괴리율) or red_price <= 0:
        return 0, float('nan')
    else:
        try:
            p = round(100*math.log10(-괴리율+31.622777)-150)
            return p if p > 0 else 0, 괴리율
        except ValueError:
            # 괴리율+31.622777이 0이하인 경우 ValueError 발생함.
            return 0, 괴리율


def mil(client, code: str) -> Tuple[int, int, int, int]:
    """
    - 재무활동현금흐름이 마이너스라는 것은 배당급 지급했거나, 자사주 매입했거나, 부채를 상환한 상태임.
    - 반대는 채권자로 자금을 조달했거나 신주를 발행했다는 의미
    <주주수익률> - 재무활동현금흐름/시가총액 => 5%이상인가?

    투하자본수익률(ROIC)가 30%이상인가
    ROE(자기자본이익률) 20%이상이면 아주 우수 다른 투자이익률과 비교해볼것 10%미만이면 별로...단, 부채비율을 확인해야함.

    이익지표 ...영업현금흐름이 순이익보다 많은가 - 결과값이 음수인가..

    FCF는 영업현금흐름에서 자본적 지출(유·무형투자 비용)을 차감한 순수한 현금력이라 할 수 있다.
    말 그대로 자유롭게(Free) 사용할 수 있는 여윳돈을 뜻한다.
    잉여현금흐름이 플러스라면 미래의 투자나 채무상환에 쓸 재원이 늘어난 것이다.
    CAPEX(Capital expenditures)는 미래의 이윤을 창출하기 위해 지출된 비용을 말한다.
    이는 기업이 고정자산을 구매하거나, 유효수명이 당회계년도를 초과하는 기존의 고정자산에 대한 투자에 돈이 사용될 때 발생한다.

    잉여현금흐름이 마이너스일때는 설비투자가 많은 시기라 주가가 약세이며 이후 설비투자 마무리되면서 주가가 상승할수 있다.
    주가는 잉여현금흐름이 증가할때 상승하는 경향이 있다.
    fcf = 영업현금흐름 - capex

    가치지표평가
    price to fcf 계산
    https://www.investopedia.com/terms/p/pricetofreecashflow.asp
    pcr보다 정확하게 주식의 가치를 평가할수 있음. 10배이하 추천

    Returns:
        tuple: 주주수익률, 이익지표, 투자수익률, PFCF포인트
    """
    mil_dict = eval_mil(client, code)

    logger.debug(pprint.pformat(mil_dict, width=200))

    # 주주수익률 평가
    if math.isnan(mil_dict['주주수익률']):
        p1 = 0
    else:
        주주수익률평가 = math.ceil(mil_dict['주주수익률'] - (EXPECT_EARN * 100))
        p1 = 0 if 0 > 주주수익률평가 else 주주수익률평가

    # 이익지표 평가
    p2 = 10 if mil_dict['이익지표'] < 0 else 0

    # 투자수익률 평가
    MAX3 = 20
    p3 = 0
    roic = mil_dict['투자수익률']['ROIC']
    roe = mil_dict['투자수익률']['ROE']
    if math.isnan(roic) or roic <= 0:
        # roic 가 비정상이라 평가할 수 없는 경우
        if 10 < roe <= 20:
            p3 += round(MAX3 * 0.333)
        elif 20 < roe:
            p3 += round(MAX3 * 0.666)
    elif 0 < roic:
        # roic 로 평가할 수 있는 경우
        if 0 < roic <= 15:
            p3 += round(MAX3 * 0.333)
        elif 15 < roic <= 30:
            p3 += round(MAX3 * 0.666)
        elif 30 < roic:
            p3 += MAX3

    # PFCF 평가
    pfcf_dict = mil_dict['가치지표']['PFCF']
    _, pfcf = mongo.Corps.latest_value(pfcf_dict)

    logger.debug(f'recent pfcf {_}, {pfcf}')
    try:
        p = round(-40 * math.log10(pfcf) + 40)
    except ValueError:
        p = 0
    p4 = 0 if 0 > p else p

    return p1, p2, p3, p4


def blue(client, code: str) -> Tuple[int, int, int, int, int]:
    """회사의 안정성을 보는 지표들

    0을 기준으로 상태가 좋치 않을 수록 마이너스 값을 가진다.

    Returns:
        tuple : 유동비율, 이자보상배율, 순부채비율, 순운전자본회전율, 재고자산회전율 평가 포인트

    Notes:
        <유동비율>
        100미만이면 주의하나 현금흐름창출력이 좋으면 괜찮을수 있다.
        만약 100%이하면 유동자산에 추정영업현금흐름을 더해서 다시계산해보아 기회를 준다.
        <이자보상배율>
        이자보상배율 영업이익/이자비용으로 1이면 자금사정빡빡 5이상이면 양호
        <순운전자금회전율>
        순운전자금 => 기업활동을 하기 위해 필요한 자금 (매출채권 + 재고자산 - 매입채무)
        순운전자본회전율은 매출액/순운전자본으로 일정비율이 유지되는것이 좋으며 너무 작아지면 순운전자본이 많아졌다는 의미로 재고나 외상이 쌓인다는 뜻
        <재고자산회전율>
        재고자산회전율은 매출액/재고자산으로 회전율이 낮을수록 재고가 많다는 이야기이므로 불리 전년도등과 비교해서 큰차이 발생하면 알람.
        재고자산회전율이 작아지면 재고가 쌓인다는뜻
        <순부채비율>
        부채비율은 업종마다 달라 일괄비교 어려우나 순부채 비율이 20%이하인것이 좋고 꾸준히 늘어나지 않는것이 좋다.
        순부채 비율이 30%이상이면 좋치 않다.
    """
    def _calc_point_with_std(data: dict) -> int:
        """표준편차를 통해 점수를 계산하는 내부 함수

        Args:
            data(dict): 재무재표상의 연/분기 딕셔너리 데이터
        """
        NEG_MAX = -5
        d_values = [i for i in data.values() if not math.isnan(i)]
        logger.debug(f'd_values : {d_values}')
        if len(d_values) == 0:
            p = NEG_MAX
        else:
            std = numpy.std(d_values)
            # 표준편차가 작을수록 데이터의 변환가 적다는 의미임.
            logger.debug(f'표준편차 : {std}')
            p = NEG_MAX if float(std) > -NEG_MAX else -math.floor(float(std))

        return int(p)

    c104y = mongo.C104(client, code, 'c104y')

    blue_dict = eval_blue(client, code)

    logger.debug(pprint.pformat(blue_dict, width=200))

    def 유동비율평가(유동비율: float) -> int:
        # 채점은 0을 기준으로 마이너스 해간다. 즉 0이 제일 좋은 상태임.
        # 유동비율 평가 - 100 이하는 문제 있음
        NEG_MAX = -10
        if math.isnan(유동비율) or 유동비율 <= 0:
            p = NEG_MAX
        elif math.isinf(유동비율):
            p = 0
        else:
            p = 0 if 100 < round(유동비율) else NEG_MAX + round(유동비율/10)
        logger.debug(f'유동비율평가 point : {p}')
        return int(p)

    p1 = 유동비율평가(blue_dict['유동비율'])

    def 이자보상배율평가(이자보상배율: tuple) -> int:
        # 이자보상배율평가 : 1이면 자금사정 빡빡 5이상이면 양호
        NEG_MAX = -5
        최근이자보상배율q, dict_y = 이자보상배율

        if math.isnan(최근이자보상배율q) or 최근이자보상배율q <= 1:
            # 최근 분기의 값이 비정상이면 최근 년도를 한번 더 비교해 보지만 좀더 엄격하게 전년대비도 비교한다.

            _, 최근이자보상배율y = mongo.Corps.latest_value(dict_y)
            c104y.page = 'c104y'
            _, 전년대비 = c104y.find_증감율(title='이자보상배율').popitem()

            if math.isnan(최근이자보상배율y) or 최근이자보상배율y <= 1 or math.isnan(전년대비) or 전년대비 < 0:
                p = NEG_MAX
            else:
                p = 0 if 5 < 최근이자보상배율y else NEG_MAX + round(최근이자보상배율y)
        else:
            p = 0 if 5 < 최근이자보상배율q else NEG_MAX + round(최근이자보상배율q)
        logger.debug(f'이자보상배율평가 point : {p}')
        return int(p)

    p2 = 이자보상배율평가(blue_dict['이자보상배율'])

    def 순부채비율평가(순부채비율: tuple) -> int:
        # 부채비율은 업종마다 달라 일괄비교 어려우나 순부채 비율이 20%이하인것이 좋고 꾸준히 늘어나지 않는것이 좋다.
        # 순부채 비율이 30%이상이면 좋치 않다.
        NEG_MAX = -5
        최근순부채비율q, dict_y = 순부채비율

        if math.isnan(최근순부채비율q) or 최근순부채비율q >= 80:
            # 최근 분기의 값이 비정상이면 최근 년도를 한번 더 비교해 보지만 좀더 엄격하게 전년대비도 비교한다.
            _, 최근순부채비율y = mongo.Corps.latest_value(dict_y)
            c104y.page = 'c104y'
            _, 전년대비 = c104y.find_증감율(title='순부채비율').popitem()
            if math.isnan(최근순부채비율y) or 최근순부채비율y >= 80 or math.isnan(전년대비) or 전년대비 > 0:
                p = NEG_MAX
            else:
                p = 0 if 최근순부채비율y < 30 else round((30 - 최근순부채비율y) / 10)
        else:
            p = 0 if 최근순부채비율q < 30 else round((30 - 최근순부채비율q) / 10)
        logger.debug(f'순부채비율평가 point : {p}')
        return int(p)

    p3 = 순부채비율평가(blue_dict['순부채비율'])

    def 순운전자본회전율평가(순운전자본회전율: tuple) -> int:
        # 순운전자본회전율은 매출액/순운전자본으로 일정비율이 유지되는것이 좋으며 너무 작아지면 순운전자본이 많아졌다는 의미로 재고나 외상이 쌓인다는 뜻
        _, dict_y = 순운전자본회전율
        p = _calc_point_with_std(data=dict_y)
        logger.debug(f'순운전자본회전율평가 point : {p}')
        return p

    p4 = 순운전자본회전율평가(blue_dict['순운전자본회전율'])

    def 재고자산회전율평가(재고자산회전율: tuple) -> int:
        # 재고자산회전율은 매출액/재고자산으로 회전율이 낮을수록 재고가 많다는 이야기이므로 불리 전년도등과 비교해서 큰차이 발생하면 알람.
        # 재고자산회전율이 작아지면 재고가 쌓인다는뜻
        _, dict_y = 재고자산회전율
        p = _calc_point_with_std(data=dict_y)
        logger.debug(f'재고자산회전율평가 point : {p}')
        return p

    p5 = 재고자산회전율평가(blue_dict['재고자산회전율'])

    return p1, p2, p3, p4, p5


def growth(client, code: str) -> Tuple[int, int]:
    """회사의 성장성을 보는 지표들

    <매출액>
    매출액은 어떤경우에도 성장하는 기업이 좋다.매출이 20%씩 늘어나는 종목은 유망한 종목
    <영업이익률>
    영업이익률은 기업의 경쟁력척도로 경쟁사에 비해 높으면 경제적해자를 갖춘셈

    Returns:
        tuple : 매출액증가율, 영업이익률 평가 포인트
    """
    growth_dict = eval_growth(client, code)

    logger.debug(pprint.pformat(growth_dict, width=200))

    def 매출액증가율평가(매출액증가율: tuple) -> int:
        # 매출액은 어떤경우에도 성장하는 기업이 좋다.매출이 20%씩 늘어나는 종목은 유망한 종목
        MAX = 20
        최근매출액증가율q, dict_y = 매출액증가율
        _, 최근매출액증가율y = mongo.Corps.latest_value(dict_y)

        # 최근 자료가 성장하는 중인지 판단
        if math.isnan(최근매출액증가율q):
            최근매출액증가율q = 최근매출액증가율y

        sp1 = 0
        if math.isnan(최근매출액증가율y):
            pass
        elif 0 < 최근매출액증가율y and 0 < 최근매출액증가율q:
            # 최근에 마이너스 성장이 아닌경우 MAX/10점 보너스
            sp1 += MAX / 10
            if 최근매출액증가율y < 최근매출액증가율q:
                # 최근에 이전보다 더 성장중이면 MAX/10점 보너스
                sp1 += MAX / 10
            # 나머지는 성장률 기반 점수 배정
            sp1 += MAX / 2 if 최근매출액증가율q > MAX else 최근매출액증가율q / 2
        elif 최근매출액증가율y <= 0 < 최근매출액증가율q:
            # 직전에 마이너스였다가 최근에 회복된 경우 MAX/10점 보너스
            sp1 += MAX / 10
            # 나머지는 성장률 기반 점수 배정
            sp1 += MAX / 2 if 최근매출액증가율q > MAX else 최근매출액증가율q / 2
        else:
            # 최근 자료가 마이너스인 경우 마이너스만큼 점수를 차감한다.
            sp1 += -(MAX / 2) if 최근매출액증가율q < -MAX else 최근매출액증가율q / 2

        # 평균매출액증가율 구하기
        d_values = [i for i in dict_y.values() if not math.isnan(i)]
        logger.debug(f'평균매출액증가율 d_values : {d_values}')

        if len(d_values) == 0:
            평균매출액증가율 = float('nan')
        else:
            평균매출액증가율 = float(numpy.mean(d_values))
        logger.debug(f'평균 : {평균매출액증가율}')

        sp2 = 0
        if math.isnan(평균매출액증가율):
            sp2 += -(MAX/2)
        elif 평균매출액증가율 <= 0:
            # 평균매출액증가율이 마이너스인 경우 마이너스만큼 점수를 차감한다.
            sp2 += -(MAX / 2) if 평균매출액증가율 < -MAX else 평균매출액증가율 / 2
        else:
            sp2 = MAX / 2 if 평균매출액증가율 > MAX else 평균매출액증가율 / 2

        logger.debug(f'매출액증가율평가 point : {sp1 + sp2}')

        return int(sp1 + sp2)

    p1 = 매출액증가율평가(growth_dict['매출액증가율'])

    def 영업이익률평가(영업이익률: dict) -> int:
        # 영업이익률은 기업의 경쟁력척도로 경쟁사에 비해 높으면 경제적해자를 갖춘셈
        영업이익률 = copy.deepcopy(영업이익률)
        name = mongo.Corps.get_name(client, code)

        p = 0
        try:
            myprofit = utils.to_float(영업이익률.pop(name))
        except KeyError:
            logger.warning(f'{name} 영업이익률 does not exist.')
            return 0
        logger.debug(f'종목영업이익률 : {myprofit}')

        for profit in 영업이익률.values():
            profit = utils.to_float(profit)
            if math.isnan(profit):
                continue
            elif myprofit > profit:
                p += 1
            else:
                continue

        logger.debug(f'영업이익률평가 point : {p}')
        return p

    p2 = 영업이익률평가(growth_dict['영업이익률'])

    return p1, p2
