import json
import unittest
from utils.data_utils import *


class TestUtils(unittest.TestCase):

    def setUp(self):
        self.searchTableList = {'StatisticTableList':
                                {'list_total_count': 2,
                                 'row': [{'SRCH_YN': 'N',
                                          'ORG_NAME': '',
                                          'CYCLE': '',
                                          'STAT_NAME': '1.통화 및 유동성지표',
                                          'STAT_CODE': '000Y005',
                                          'P_STAT_CODE': '*'},
                                         {'SRCH_YN': 'Y',
                                          'ORG_NAME': '',
                                          'CYCLE': 'MM',
                                          'STAT_NAME': '1.1.주요 통화금융지표',
                                          'STAT_CODE': '010Y002',
                                          'P_STAT_CODE': '000Y005'},
                                         {'SRCH_YN': 'N',
                                          'ORG_NAME': '',
                                          'CYCLE': '',
                                          'STAT_NAME': '1.2.본원통화',
                                          'STAT_CODE': '000Y074',
                                          'P_STAT_CODE': '000Y005'}, ]}}
        self.detailTableList = {
            'StatisticItemList': {'list_total_count': 29,
                                  'row': [{'END_TIME': '201808',
                                           'DATA_CNT': 96,
                                           'GRP_NAME': 'Group1',
                                           'CYCLE': 'MM',
                                           'STAT_NAME': '4.1.2 시장금리(월,분기,년)',
                                           'ITEM_NAME': '무담보콜금리(1일, 중개거래,투신사연계콜제외)',
                                           'STAT_CODE': '028Y001',
                                           'ITEM_CODE': 'BEEA131',
                                           'START_TIME': '197601'},
                                          {'END_TIME': '201808',
                                           'DATA_CNT': 332,
                                           'GRP_NAME': 'Group1',
                                           'CYCLE': 'MM',
                                           'STAT_NAME': '4.1.2 시장금리(월,분기,년)',
                                           'ITEM_NAME': '무담보콜금리 전체',
                                           'STAT_CODE': '028Y001',
                                           'ITEM_CODE': 'BEEA14',
                                           'START_TIME': '197601'},
                                          {'END_TIME': '201808',
                                           'DATA_CNT': 140,
                                           'GRP_NAME': 'Group1',
                                           'CYCLE': 'MM',
                                           'STAT_NAME': '4.1.2 시장금리(월,분기,년)',
                                           'ITEM_NAME': 'KORIBOR(12M)',
                                           'STAT_CODE': '028Y001',
                                           'ITEM_CODE': 'BEEA220',
                                           'START_TIME': '197601'},
                                          {'END_TIME': '201808',
                                           'DATA_CNT': 215,
                                           'GRP_NAME': 'Group1',
                                           'CYCLE': 'MM',
                                           'STAT_NAME': '4.1.2 시장금리(월,분기,년)',
                                           'ITEM_NAME': '국고채(10년)',
                                           'STAT_CODE': '028Y001',
                                           'ITEM_CODE': 'BEEA422',
                                           'START_TIME': '197601'},
                                          {'END_TIME': '201808',
                                           'DATA_CNT': 152,
                                           'GRP_NAME': 'Group1',
                                           'CYCLE': 'MM',
                                           'STAT_NAME': '4.1.2 시장금리(월,분기,년)',
                                           'ITEM_NAME': '국고채(20년)',
                                           'STAT_CODE': '028Y001',
                                           'ITEM_CODE': 'BEEA423',
                                           'START_TIME': '197601'},
                                          {'END_TIME': '201808',
                                           'DATA_CNT': 144,
                                           'GRP_NAME': 'Group1',
                                           'CYCLE': 'MM',
                                           'STAT_NAME': '4.1.2 시장금리(월,분기,년)',
                                           'ITEM_NAME': '통안증권(91일)',
                                           'STAT_CODE': '028Y001',
                                           'ITEM_CODE': 'BEEA431',
                                           'START_TIME': '197601'},
                                          {'END_TIME': '201808',
                                           'DATA_CNT': 330,
                                           'GRP_NAME': 'Group1',
                                           'CYCLE': 'MM',
                                           'STAT_NAME': '4.1.2 시장금리(월,분기,년)',
                                           'ITEM_NAME': '산금채(1년)',
                                           'STAT_CODE': '028Y001',
                                           'ITEM_CODE': 'BEEA45',
                                           'START_TIME': '197601'},
                                          {'END_TIME': '201808',
                                           'DATA_CNT': 56,
                                           'GRP_NAME': 'Group1',
                                           'CYCLE': 'MM',
                                           'STAT_NAME': '4.1.2 시장금리(월,분기,년)',
                                           'ITEM_NAME': '카드채(A+)수익률',
                                           'STAT_CODE': '028Y001',
                                           'ITEM_CODE': 'BEEA54',
                                           'START_TIME': '197601'}]}
        }
        self.industList = [
            {'name': '통신업', 'site': '/quote/upjong_detail.daum?stype=P&seccode=020'}
        ]
        self.paginationIndust = [
            {'name': '금융업', 'site': '/quote/upjong_detail.daum?stype=P&seccode=021'}
        ]

    def test_searchcode_properly(self):
        code = search_stats_code(self.searchTableList, '본원통화')
        self.assertEqual(code['data'][0]['STAT_NAME'], '1.2.본원통화')
        self.assertEqual(code['data'][0]['STAT_CODE'], '000Y074')
        self.assertEqual(code['data'][0]['P_STAT_CODE'], '000Y005')
        self.assertEqual(code['status'], 'SUCCESS')
        # invalid keyword
        code = search_stats_code(self.searchTableList, '브라질')
        self.assertEqual(code['status'], 'FAIL')
        self.assertEqual(code['message'], '해당 통계를 찾을 수 없습니다.')

        # invalid input
        code = search_stats_code([], '본원통화')
        self.assertEqual(code['status'], 'FAIL')
        self.assertEqual(code['message'], '잘못된 형식의 데이터입니다.')

    def test_detailcode_properly(self):
        code = search_stats_code(self.detailTableList, '국고채', 'ITEM_NAME')
        self.assertEqual(code['data'][0]['ITEM_NAME'], '국고채(10년)')
        self.assertEqual(code['data'][0]['ITEM_CODE'], 'BEEA422')
        self.assertEqual(code['data'][0]['START_TIME'], '197601')
        self.assertEqual(code['status'], 'SUCCESS')

    def test_get_industries_sites(self):
        data = get_all_industries_sites()
        self.assertTrue(len(data) > 5)
        for key in data:
            self.assertTrue('site' in key.keys())
            self.assertTrue('name' in key.keys())

    def test_get_company_list(self):
        companyList = getAllCompanyList(self.industList)
        self.assertTrue(len(companyList) == 4)
        for key in companyList:
            self.assertTrue('code' in key.keys())
            self.assertTrue('name' in key.keys())
            self.assertTrue('industry' in key.keys())

    def test_check_company_list_with_pagination(self):
        companyList = getAllCompanyList(self.paginationIndust)
        self.assertTrue(len(companyList) > 120)
        for data in companyList:
            self.assertTrue('code' in data.keys())
            self.assertTrue('name' in data.keys())
            self.assertTrue('industry' in data.keys())


if __name__ == "__main__":
    unittest.main()
