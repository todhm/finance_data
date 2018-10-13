import requests
import json
from collections import defaultdict
from multiprocessing.dummy import Pool as ThreadPool
from multiprocessing import Queue
from threading import Thread, active_count
from settings import KOREAN_BANK_SECRET_KEY
from utils.data_utils import daterange, exception_handler
import sys
import os
import socket
import ssl
import grequests
import time
from imp import reload


class BankHandler(object):
    def __init__(self, MAX_THREAD=40):
        self.api_key = KOREAN_BANK_SECRET_KEY
        self.max_thread = MAX_THREAD

    def exception_handler(self, request, exception):
        for i in range(10):
            try:
                response = requests.get(request.url)
                return response
            except requests.exceptions.ConnectionError:
                time.sleep(3)
        return request.url

    def make_requests(self, url_list):
        response_list = []
        for url in url_list:
            response_list.append(url)
        return response_list
        # response_list = (grequests.get(u) for u in url_list)
        # response_list = grequests.map(
        #     response_list, exception_handler=self.exception_handler)
        # return response_list

    def get_daily_stats(self, startdate, enddate, statcode, itemcode):
        data_list = defaultdict(list)
        data_list['date'] = []
        url_list = []
        for start_date_str, end_date_str in daterange(startdate, enddate, 10):
            url = 'http://ecos.bok.or.kr/api/StatisticSearch/{}/json/kr/0/10/{}/DD/{}/{}/{}/'.format(
                self.api_key, statcode, start_date_str, end_date_str, itemcode
            )
            url_list.append(url)
        reload(sys)
        reload(os)
        reload(socket)
        reload(ssl)
        chunks = [url_list[x:x+100] for x in range(0, len(url_list), 100)]
        pool = ThreadPool(self.max_thread)
        results = pool.map(self.make_requests, chunks)
        pool.close()
        pool.join()
        response_list = [i for j in results for i in j]
        for response in response_list:
            try:
                data = json.loads(response.text)
            except:
                new_response = requests.get(response)
                data = json.loads(new_response.text)

            item_name = data['StatisticSearch']['row'][0]['ITEM_NAME1']
            if item_name not in data_list.keys():
                data_list[item_name] = []
            data_list[item_name].extend(
                map(lambda x: float(x['DATA_VALUE']),
                    data['StatisticSearch']['row'])
            )
            data_list['date'].extend(
                map(lambda x: x['TIME'],
                    data['StatisticSearch']['row'])
            )
        return data_list
