# -*- coding: utf-8 -*-
"""
@summary: 股票概念 行情
同花顺概念更及时和完整，所以目前暂只基于同花顺的股票概念抓取,网页数据中心和手机概念板块
http://d.10jqka.com.cn/v6/line/48_885772/01/last1800.js
http://search.10jqka.com.cn/gateway/urp/v7/landing/getDataList?query=%E6%89%80%E6%9C%89%E6%A6%82%E5%BF%B5&condition=%5B%7B%22indexName%22%3A%22%E6%8C%87%E6%95%B0%40%E5%90%8C%E8%8A%B1%E9%A1%BA%E6%A6%82%E5%BF%B5%E6%8C%87%E6%95%B0%22%2C%22indexProperties%22%3A%5B%5D%2C%22source%22%3A%22new_parser%22%2C%22type%22%3A%22index%22%2C%22indexPropertiesMap%22%3A%7B%7D%2C%22reportType%22%3A%22null%22%2C%22chunkedResult%22%3A%22%E6%89%80%E6%9C%89%E6%A6%82%E5%BF%B5%22%2C%22valueType%22%3A%22_%E6%8C%87%E6%95%B0%E7%B1%BB%E5%9E%8B%22%2C%22domain%22%3A%22abs_a%E6%8C%87%E9%A2%86%E5%9F%9F%22%2C%22uiText%22%3A%22%E5%90%8C%E8%8A%B1%E9%A1%BA%E6%A6%82%E5%BF%B5%E6%8C%87%E6%95%B0%22%2C%22sonSize%22%3A0%2C%22queryText%22%3A%22%E5%90%8C%E8%8A%B1%E9%A1%BA%E6%A6%82%E5%BF%B5%E6%8C%87%E6%95%B0%22%2C%22relatedSize%22%3A0%7D%5D&urp_sort_index=%E6%8C%87%E6%95%B0%E4%BB%A3%E7%A0%81&source=Ths_iwencai_Xuangu&perpage=500&page=1&urp_sort_way=desc&codelist=&page_id=&logid=35df00ee5ae706d0dfcd0dbfdb846e0c&ret=json_all&sessionid=35df00ee5ae706d0dfcd0dbfdb846e0c&iwc_token=0ac9667016801698001765831&user_id=Ths_iwencai_Xuangu_7fahywzhbkrh4lwwkwfw936njqbjzsly&uuids%5B0%5D=23119&query_type=zhishu&comp_id=6367801&business_cat=soniu&uuid=23119
885772 表示手机端的概念代码
@author: 1nchaos
@date: 2023/3/30 16:17
"""
import copy
import json
import time

import pandas as pd

from adata.common.headers import ths_headers
from adata.common.utils import requests


class StockMarketConcept(object):
    """
    股票概念 行情
    """
    COLUMNS = ['trade_date', 'open', 'high', 'low', 'close', 'volume', 'amount']

    def __init__(self) -> None:
        super().__init__()

    def get_market_concept_ths(self, concept_code: str = '886013', k_type: int = 1, adjust_type: int = 1):
        """
        获取同花顺的概率的行情
        web: http://q.10jqka.com.cn/gn/
        pc: http://d.10jqka.com.cn/v4/line/bk_885772/21/last.js
        app: http://d.10jqka.com.cn/v6/line/48_886013/01/last1800.js
        00 日k不复权；01日k前复权；02日k后复权；11周k前复权；21月k前复权
        :param concept_code: 同花顺概念代码
        :param k_type: k线类型：1.日；2.周；3.月 默认：1 日k
        :param adjust_type: k线复权类型：0.不复权；1.前复权；2.后复权 默认：1 前复权
        :return: k线行情数据 [日期，开，高，低，收,成交量，成交额]
        ;20230419,958.901,981.118,958.449,961.107,521143220,20442229000.000
        成交量：股 820953530  821万手
        成交额：元 16959251000.000 169.6亿
        """
        # 1.接口 url
        api_url = f"http://d.10jqka.com.cn/v6/line/48_{concept_code}/{k_type - 1}{adjust_type}/last1800.js"
        # 同花顺可能ip限制，降低请求次数
        text = self.__get_text(api_url, concept_code)
        result_text = text[text.index('{'):-1]
        data_list = json.loads(result_text)['data'].split(';')
        data = []
        for d in data_list:
            data.append(str(d).split(',')[0:7])
        result_df = pd.DataFrame(data=data, columns=self.COLUMNS)
        result_df['concept_code'] = concept_code
        result_df['trade_time'] = pd.to_datetime(result_df['trade_date']).dt.strftime('%Y-%m-%d %H:%M:%S')
        result_df['trade_date'] = pd.to_datetime(result_df['trade_date'], format='%Y%m%d').dt.strftime('%Y-%m-%d')
        return result_df

    def get_market_concept_min_ths(self, concept_code):
        """
        获取概念行情当日分时
        web： http://d.10jqka.com.cn/v6/time/48_886013/last.js
        0930,958.901,74456973,36.807,2022925;  "pre": "960.374",
        :param concept_code: 概念代码
        :return 时间，现价，成交额（元），均价，成交量（股） 涨跌额，涨跌幅
        'concept_code', 'trade_time', 'price', 'change', 'change_pct', 'volume', 'avg_price', 'amount'
        """
        # 1.接口 url
        api_url = f"http://d.10jqka.com.cn/v6/time/48_{concept_code}/last.js"
        text = self.__get_text(api_url, concept_code)
        # 2. 解析数据
        result_json = json.loads(text[text.index('{'):-1])[f"48_{concept_code}"]
        pre_price = result_json['pre']
        trade_date = result_json['date']
        data_list = result_json['data'].split(';')
        data = []
        for d in data_list:
            data.append(str(d).split(','))
        # 3. 封装数据
        result_df = pd.DataFrame(data=data, columns=['trade_time', 'price', 'amount', 'avg_price', 'volume'])
        result_df['concept_code'] = concept_code
        result_df['trade_time'] = trade_date + result_df['trade_time']
        result_df['trade_date'] = pd.to_datetime(trade_date, format='%Y%m%d').strftime('%Y-%m-%d')
        result_df['trade_time'] = pd.to_datetime(result_df['trade_time'], format='%Y%m%d%H%M').dt.strftime(
            '%Y-%m-%d %H:%M:%S')
        result_df['change'] = result_df['price'].astype(float) - float(pre_price)
        result_df['change_pct'] = result_df['change'].astype(float) / float(pre_price) * 100
        return result_df

    def get_market_concept_today_ths(self, concept_code: str = '886013', k_type: int = 1, adjust_type: int = 1):
        """
        获取同花顺当前的概念行情
        web: http://q.10jqka.com.cn/gn/
        pc: http://d.10jqka.com.cn/v6/line/48_886042/01/today.js
        quotebridge_v6_line_48_886042_01_today({"48_886042":{"1":"20230425","7":"891.344","8":"892.350","9":"853.800",
        "11":"860.076","13":491708080,"19":"17647511000.000","74":"","1968584":"","66":"","open":1,"dt":"2244",
        "name":"\u5b58\u50a8\u82af\u7247","marketType":""}})

        :param concept_code: 同花顺概念代码
        :param k_type: k线类型：1.日；2.周；3.月 默认：1 日k
        :param adjust_type: k线复权类型：0.不复权；1.前复权；2.后复权 默认：1 前复权
        :return: k线行情数据 [概念代码,概念名称,日期，开，高，低，收,成交量，成交额]
        ;20230419,958.901,981.118,958.449,961.107,521143220,20442229000.000,存储芯片
        k:   1,      7,      8,       9,      11,      13,         19,        name
        成交量：股 820953530  821万手
        成交额：元 16959251000.000 169.6亿
        """
        # 1.接口 url
        api_url = f"http://d.10jqka.com.cn/v6/line/48_{concept_code}/{k_type - 1}{adjust_type}/today.js"
        headers = copy.deepcopy(ths_headers.text_headers)
        headers['Host'] = 'd.10jqka.com.cn'
        # 同花顺可能ip限制，降低请求次数
        text = self.__get_text(api_url, concept_code)
        result_text = text[text.index('{'):-1]
        data_list = [json.loads(result_text)[f"48_{concept_code}"]]
        rename = {'1': 'trade_date', '7': 'open', '8': 'high', '9': 'low', '11': 'close', '13': 'volume',
                  '19': 'amount'}
        result_df = pd.DataFrame(data=data_list).rename(columns=rename)[self.COLUMNS]
        result_df['concept_code'] = concept_code
        result_df['trade_date'] = pd.to_datetime(result_df['trade_date'], format='%Y%m%d').dt.strftime('%Y-%m-%d')
        return result_df

    def __get_text(self, api_url, concept_code):
        """
        获取同花顺的请求 text
        :param api_url: url
        :param concept_code: 概念代码
        :return:
        """
        headers = copy.deepcopy(ths_headers.text_headers)
        headers['Host'] = 'd.10jqka.com.cn'
        text = ''
        for i in range(3):
            res = requests.request('get', api_url, headers=headers, proxies={})
            text = res.text
            if concept_code in text:
                break
            time.sleep(2)
        return text


if __name__ == '__main__':
    print(StockMarketConcept().get_market_concept_ths(concept_code='886042'))
    print(StockMarketConcept().get_market_concept_min_ths(concept_code='886041'))
    print(StockMarketConcept().get_market_concept_today_ths(concept_code='886041'))
