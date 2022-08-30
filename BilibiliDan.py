#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
from wordcloud import WordCloud as wc
from dm.dm_pb2 import DmSegMobileReply
from google.protobuf.json_format import MessageToJson, Parse
import xlwt
import json
import jieba
import random
from threading import Thread
from sys import argv

class BilibiliDan():
    THREAD_NUM = 20
    GET_CID_URL = "https://api.bilibili.com/x/player/pagelist"
    DIRECT_DAN_URL = "https://comment.bilibili.com/"
    DAN_URL_DATE = "https://api.bilibili.com/x/v2/dm/history?type=1&oid={cid}&date={date}"
    DIRECT_DAN_LIST = []
    DAN_DATE_DICT = {}
    # 传入url和相关的meta参数-->包括pattern，开始和结束日期以及cookie，为dict类型
    def __init__(self,input_url,meta):
        self.input_url = input_url
        self.meta = meta
    # 获取视频的cid，来自于BV号
    def getVideoCid(self):
        # 与match不同点在于match是从头开始匹配的，若一开始就不匹配，返回none
        bv_id = re.search(r'(?<=video/).+(?=\?)', self.input_url).group()
        # 用get可以传入params参数，参数值用如{param1}代替
        params={"bvid":bv_id,"jsonp":"jsonp"}
        res = requests.get(self.GET_CID_URL,params=params).text
        # 与loads不同点在于load接受的是json文件作为参数
        json_data = json.loads(res)
        self.cid = json_data["data"][0]["cid"]
    # 直接获取弹幕文件 xml
    def getDirectDan(self):
        url = self.DIRECT_DAN_URL + str(self.cid) + ".xml"
        res = requests.get(url)
        res.encoding = "utf-8"
        xml = BeautifulSoup(res.text, 'xml')
        el_list = xml.find_all("d")
        self.DIRECT_DAN_LIST = []
        for item in el_list:
            self.DIRECT_DAN_LIST.append(item.get_text())

    def generateUrlList(self,startDate,endDate):
        url_list = []
        date = pd.date_range(start=startDate, end=endDate).strftime('%Y-%m-%d')
        # print(date)
        for i in date:
            url = "https://api.bilibili.com/x/v2/dm/web/history/seg.so?type=1&oid=" + str(self.cid) + "&date=" + i
            url_list.append(url)
        return url_list
    # 根据日期查询
    def getDanByDate(self,startDate,endDate,cookie):
        print(2222)
        url_list = self.generateUrlList(startDate,endDate)
        user_list = [
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"

            ]

        t_user = random.choice(user_list)

        headers = {
            "cookie": cookie,
            'origin': 'https://www.bilibili.com',
            'referer': 'https://www.bilibili.com/video/BV15E411a77a?p=4&spm_id_from=pageDriver&vd_source=5ee90ee987353c0a0414b14767c52720',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': t_user
        }
        self.DAN_DATE_DICT = {}
        for s_url in url_list:
            # print(s_url)
            date = re.search(r'(?<=&date=).+$',s_url).group()
            response = requests.get(url=s_url, headers=headers)
            # response.encoding = 'utf-8'
            # html = BeautifulSoup(response.text, 'html.parser')
            dm = DmSegMobileReply()
            dm.ParseFromString(response.content)
            data_dict = json.loads(MessageToJson(dm))
            # print(data_dict)
            # print(html)
            # danmu = html.find_all('d')
            Dam_list = []
            for item in data_dict["elems"]:
                # print(item)
                Dam_list.append(item["content"])
            # for text in danmu:
            #     t_danmu = text.get_text()
            #     Dam_list.append(t_danmu)
            self.DAN_DATE_DICT[date] = Dam_list

    # 从Qfiledialog的getsavefilename获取数据（类型为元组，元组第一项为你的文件路径（包括你给的文件名），第二项为该文件的类型）
    def exportExcel(self,file_info,dan_list):
        record = xlwt.Workbook(file_info)
        sheet1 = record.add_sheet('工作表1')
        sheet1.write(0, 0, '弹幕信息')
        num = 1
        for dan in dan_list:
            sheet1.write(num, 0, dan)
            num = num + 1
        record.save(file_info)

    # 默认导出文本文件
    def exportTxt(self,file_info):
        with open(file_info,'a',encoding='utf-8') as f:
            for dan in self.DIRECT_DAN_LIST:
                f.write(dan)

    def cutWord(self,dan_list):
        list_wait_for_cut = dan_list
        # print(dan_list)
        # try:
        #     file = open('stop_words.txt','r')
        #     print(file.readlines())
        # except Exception as e:
        #     print(f'Cause:{e}')
        with open('stop_words.txt','r',encoding='utf-8') as f:
            lines = f.readlines()
            # print(lines)
            for i in range(len(list_wait_for_cut)):
                if list_wait_for_cut[i] in lines:
                    list_wait_for_cut.pop(i)
        all_txt = " ".join(list_wait_for_cut)

        word_list = jieba.lcut(all_txt)
        return word_list

    def generateWordCloud(self,file_info,dan_list):
        word_list = self.cutWord(dan_list)
        text = " ".join(word_list)
        d_wd = wc(font_path='./static/HYTangMeiRenW.ttf', background_color='black', height=1200,
                  width=1000).generate(text)
        d_wd.to_file(file_info)

    def genrateThread(self,target_method,args):
        thread_list = []
        for i in range(self.THREAD_NUM):
            thread = Thread(target=target_method,args=args)
            # 守护线程
            thread.setDaemon(True)
            thread.start()
            # 线程启动后
            thread_list.append(thread)

        for thread in thread_list:
            # 主线程等待子线程执行完毕
            thread.join()

    def start(self):
        if self.meta["pattern"]=="direct":
            self.genrateThread(self.getDirectDan,())
        elif self.meta["pattern"]=="date":
            startDate = self.meta["startDate"]
            endDate = self.meta["endDate"]
            cookie = self.meta["cookie"]
            self.genrateThread(self.getDanByDate,(startDate,endDate,cookie))

if __name__=='__main__':
    try:
        bilibiliDan = BilibiliDan(argv[1], argv[2])
        bilibiliDan.getVideoCid()
        bilibiliDan.start()
    except Exception as e:
        print(f'程序出错,Cause:{e}')






