import re
import json
import requests
from bs4 import BeautifulSoup
from ProfessorFinder.content_crawler.base_crawler import WebCrawler


class TsinghuaArch(WebCrawler):

    def __init__(self):
        url = 'http://www.arch.tsinghua.edu.cn/column/rw'
        super().__init__(url, '建筑学院')

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
                self.all_info.append(('清华大学', '建筑学院',
                                      name, email, url_tab))
            except AttributeError:
                pass
        return self.all_info


class TsinghuaSem(WebCrawler):

    def __init__(self):
        url = 'http://www.sem.tsinghua.edu.cn/tesearch/jssearch.html'
        super().__init__(url, '经济学院')

    def handler(self):
        self._url = 'http://mis.sem.tsinghua.edu.cn/psc/CRMPRD/EM' \
                    'PLOYEE/CRM/s/WEBLIB_TZ_ISRPT.TZ_WEB_JSWW2_FL' \
                    'D.FieldFormula.IScript_LoadTeaTeam?language=' \
                    'ZHS'
        self._page = self._get_page()
        data_list = json.loads(self._page.text)
        for each in data_list:
            self.all_info.append(('清华大学', '经济学院', each['name'],
                                  each['email'], each['detailurl']))
        return self.all_info


class TsinghuaCivil(WebCrawler):  # something to solve?

    def __init__(self):
        url = 'http://www.civil.tsinghua.edu.cn/20.html'
        super().__init__(url, '土木水利学院')

    def handler(self):
        data_link = {}
        pattern = re.compile('.*text-decoration: underline;')
        peoples = self.bs.find_all('a', {'style': pattern})
        for people in peoples:
            name = people.get_text()
            name = name.encode('iso8859-1').decode('utf-8')  # solve encoding problem
            link = people.attrs['href']
            data_link[name] = link
        for name, link in data_link.items():
            mail = self._get_mail(link)
            self.all_info.append(('清华大学', '土木水利学院',
                                  name, mail, link))
        return self.all_info

    @classmethod
    def _get_mail(cls, link):
        response = requests.get(link)
        bs = BeautifulSoup(response.text, 'lxml')
        bs = bs.find('div', {'class': 'essay_field'})
        bs = bs.find('div', {'class': 'content'})
        mail = re.search(cls.mail_re, bs.get_text())
        try:
            return mail.group(0)
        except AttributeError:
            return None


class TsinghuaEnv(WebCrawler):

    def __init__(self):
        url = 'http://www.env.tsinghua.edu.cn/szdw/jyjs/ys.htm'
        super().__init__(url, '环境学院')

    def handler(self):
        all_professors = []  # each element is a bs object
        bs = self.bs.find('div', {'class': 'box_detail'}).p
        bs = bs.find_all('a')
        all_professors.extend(bs)

        resp = requests.get('http://www.env.tsinghua.edu.cn/szdw/jyjs/jyssz.htm')
        bs = BeautifulSoup(resp.text, 'lxml')
        bs = bs.find_all('p', {'style': 'text-indent: 0em;'})
        for group in bs:
            t = group.find_all('a')
            all_professors.extend(t)

        professors = {}
        for professor in all_professors:
            name = professor.get_text()
            name = name.encode('iso8859-1').decode('utf-8')
            name = name.replace(' ', '')
            link = professor.attrs['href'][5:]
            link = self._internal_link_convert(link)
            professors[name] = link
        for professor, link in professors.items():
            mail = self._get_mail(link)
            self.all_info.append(('清华大学', '环境学院',
                                  professor, mail, link))
        return self.all_info

    @classmethod
    def _get_mail(cls, url):
        resp = requests.get(url)
        bs = BeautifulSoup(resp.text, 'lxml')
        pattern = re.compile(r'vsb_content.*')
        try:
            bs = bs.find('div', {'id': pattern}).table
        except AttributeError:
            return None
        info = bs.get_text()
        mail = re.search(cls.mail_re, info)
        try:
            return mail.group(0)
        except AttributeError:
            return None


def get_pack():
    all_pack = ['清华大学', TsinghuaArch(), TsinghuaSem(),
                TsinghuaCivil(), TsinghuaEnv()]
    return all_pack


def main():
    print(TsinghuaEnv().run())


if __name__ == '__main__':
    main()
