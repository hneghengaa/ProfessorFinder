"""
    北大
"""
import re
import json
import requests
from bs4 import BeautifulSoup
from requests.api import request
from  ProfessorFinder.content_crawler.base_crawler import WebCrawler


class PKUCrawler(WebCrawler):

    def __init__(self, url, name):
        super().__init__(url, name)

    def append_info(self, name, email, url):
        self.all_info.append(('北京大学', self.name, name, email, url))

    def get_info(self):
        return self.all_info


class PKUPhy(PKUCrawler):

    def __init__(self):
        url = 'https://www.phy.pku.edu.cn/system/resource/tsites/portal/queryteacher.jsp?collegeid=1520&isshowpage=false&postdutyid=0&postdutyname=%E6%95%99%E7%A0%94%E4%BA%BA%E5%91%98&facultyid=&disciplineid=0&rankcode=0&jobtypecode=JOB_TYPE_ID927559,JOB_TYPE_ID024588,JOB_TYPE_ID056883,JOB_TYPE_ID984595,JOB_TYPE_ID959332,JOB_TYPE_ID091962,JOB_TYPE_ID945233,01114,JOB_TYPE_ID280117,01110,00319,01106,01120,01112,01119,00318,00305,00315,01113,01108,01103,01102,00311,00303,01104,00107,JOB_TYPE_ID069686,JOB_TYPE_ID011361,&enrollid=0&pageindex=1&pagesize=220&login=false&profilelen=10&honorid=0&pinyin=&teacherName=&searchDirection=&viewmode=10&viewOwner=1539754034&viewid=275976&siteOwner=1539754034&viewUniqueId=u12&showlang=zh_CN&actiontype='
        super().__init__(url, '物理学院')

    def handler(self):
        r = requests.get('https://www.phy.pku.edu.cn/system/resource/tsites/portal/queryteacher.jsp?collegeid=1520&isshowpage=false&postdutyid=0&postdutyname=%E6%95%99%E7%A0%94%E4%BA%BA%E5%91%98&facultyid=&disciplineid=0&rankcode=0&jobtypecode=JOB_TYPE_ID927559,JOB_TYPE_ID024588,JOB_TYPE_ID056883,JOB_TYPE_ID984595,JOB_TYPE_ID959332,JOB_TYPE_ID091962,JOB_TYPE_ID945233,01114,JOB_TYPE_ID280117,01110,00319,01106,01120,01112,01119,00318,00305,00315,01113,01108,01103,01102,00311,00303,01104,00107,JOB_TYPE_ID069686,JOB_TYPE_ID011361,&enrollid=0&pageindex=1&pagesize=220&login=false&profilelen=10&honorid=0&pinyin=&teacherName=&searchDirection=&viewmode=10&viewOwner=1539754034&viewid=275976&siteOwner=1539754034&viewUniqueId=u12&showlang=zh_CN&actiontype=')
        professor=json.loads(r.text)
        for teacher in professor['teacherData']:
            name = teacher['name']
            email = teacher['email']
            link = teacher['url']
            if link== 'javascript:void(0)':
                link = None
            self.append_info(name, email, link)
        
        
def get_pack():
    all_pack = {
        '北京大学': 0, PKUPhy: 1
    }
    return all_pack


uncrawled = ['数学学院']


def main():
    PKUPhy().run()


if __name__ == '__main__':
    main()
