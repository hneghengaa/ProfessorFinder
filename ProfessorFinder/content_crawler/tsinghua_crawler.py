import json
import requests
from urllib.parse import urlparse
from ProfessorFinder.content_crawler.base_crawler import WebCrawler


class TsinghuaArch(WebCrawler):
    def __init__(self):
        super().__init__('http://www.arch.tsinghua.edu.cn/column/rw')

    def handler(self):
        bs = self.bs.find('div', {'class': 'tabContent'})
        peoples = bs.find_all('li')
        for people in peoples:
            url_tab = self._internal_link_convert(people.find(
                'div', {'class': 'name'}).a.attrs['href'])
            name_tab = people.find('div', {'class': 'name'}).a.div
            email_tab = people.find('div', {'class': 'info'})
            try:
                name = name_tab.get_text()
                email = email_tab.get_text()
                self.all_info.append(('tsinghua', 'Arch', name, email, url_tab))
            except AttributeError:
                pass
        return self.all_info


class TsinghuaSem(WebCrawler):
    def __init__(self):
        super().__init__('http://www.sem.tsinghua.edu.cn/tesearch/jssearch.html')

    def handler(self):
        self._url = 'http://mis.sem.tsinghua.edu.cn/psc/CRMPRD/EMPLOYEE/CRM/s/WEBLIB_TZ_ISRPT.TZ_WEB_JSWW2_FLD.FieldFormula.IScript_LoadTeaTeam?language=ZHS&_=1623331525098'
        self._page = self._get_page()
        data_list = json.loads(self._page.text)
        for each in data_list:
            self.all_info.append(('tsinghua', 'Sem', each['name'], each['email'], each['detailurl']))
        return self.all_info


all_pack = [TsinghuaArch(), TsinghuaSem()]


def main():
    print(TsinghuaSem().run())


if __name__ == '__main__':
    main()
