import re
import json
import requests
from bs4 import BeautifulSoup
from ProfessorFinder.content_crawler.base_crawler import WebCrawler


class TsinghuaCrawler(WebCrawler):

    def __init__(self, url, name):
        super().__init__(url, name)

    def append_info(self, name, email, url):
        self.all_info.append(('清华大学', self.name, name, email, url))

    def get_info(self):
        return self.all_info


class TsinghuaArch(TsinghuaCrawler):

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
                self.append_info(name, url_tab, email)
            except AttributeError:
                pass
        return self.get_info()


class TsinghuaSem(TsinghuaCrawler):

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
            self.append_info(each['name'], each['email'],
                             each['detailurl'])
        return self.get_info()


class TsinghuaCivil(TsinghuaCrawler):  # something to solve?

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
            self.append_info(name, mail, link)
        return self.get_info()

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


class TsinghuaEnv(TsinghuaCrawler):

    def __init__(self):
        url = 'http://www.env.tsinghua.edu.cn/szdw/jyjs/ys.htm'
        super().__init__(url, '环境学院')

    def handler(self):
        all_professors = []  # each element is a bs object
        bs = self.bs.find('div', {'class': 'box_detail'}).p
        bs = bs.find_all('a')
        all_professors.extend(bs)

        resp = requests.get('http://www.env.tsinghua.edu.cn/szdw/'
                            'jyjs/jyssz.htm')
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
            self.append_info(professor, mail, link)
        return self.get_info()

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


class TsinghuaSppm(TsinghuaCrawler):

    def __init__(self):
        url = 'http://www.sppm.tsinghua.edu.cn/szdw/qzjs/'
        super().__init__(url, '公共管理学院')

    def handler(self):
        bs = self.bs.find('div', {'id': 'xp_zw'}).table
        tabs = bs.find_all('tr')
        for tab in tabs:
            name_tab = tab.find('td', {'width': '91'})
            email_tab = tab.find('td', {'width': '164'})
            try:
                name = name_tab.get_text()
                name = name.encode('iso8859-1').decode('gbk')
            except AttributeError:
                continue
            link = name_tab.a.attrs['href']
            link = self._internal_link_convert(link)
            email = None if email_tab.get_text().isspace() \
                else email_tab.get_text()
            self.append_info(name, email, link)
        return self.get_info()


class TsinghuaMe(TsinghuaCrawler):

    def __init__(self):
        url = 'http://me.tsinghua.edu.cn/szdw/ys.htm'
        super().__init__(url, '信息科学技术学院机械工程系')

    def handler(self):
        all_professors = {}
        bs = self.bs.find('div', {'class': 'ys-con'})
        for professor in bs.div.find_all('a'):
            name = professor.attrs['title'] \
                .encode('iso8859-1').decode('utf-8')
            link = professor.attrs['href']
            link = self._internal_link_convert(link[2:])
            all_professors[name] = link
        r = requests.get('http://me.tsinghua.edu.cn/szdw/zzjs.htm')
        bs = BeautifulSoup(r.text, 'lxml')
        bs = bs.find('div', {'class': 'tea-text'})
        for professor in bs.find_all('a'):
            name = professor.attrs['title'] \
                .encode('iso8859-1').decode('utf-8')
            link = professor.attrs['href']
            link = self._internal_link_convert(link[2:])
            all_professors[name] = link

        for name, link in all_professors.items():
            email = self._get_mail(link)
            self.append_info(name, email, link)
        return self.get_info()

    @classmethod
    def _get_mail(cls, url):
        r = requests.get(url)
        bs = BeautifulSoup(r.text, 'lxml')
        tab = bs.find('div', {'class': 't-info-text fl'})
        email = re.search(cls.mail_re, tab.get_text())
        try:
            return email.group(0)
        except AttributeError:
            return None


class TsinghuaDpi(TsinghuaCrawler):

    def __init__(self):
        url = 'http://faculty.dpi.tsinghua.edu.cn/index.html'
        super().__init__(url, '信息科学技术学院精密仪器系')

    def handler(self):
        for bs in self.bs.find_all('div', {'class': 'third'}):
            for professor in bs.ul.find_all('li'):
                name = professor.h6.get_text()
                link = professor.a.attrs['href']
                link = self._internal_link_convert(link)
                email = self._get_email(link)
                self.append_info(name, email, link)
        return self.get_info()

    @classmethod
    def _get_email(cls, url):
        r = requests.get(url)
        bs = BeautifulSoup(r.text, 'lxml')
        bs = bs.find('div', {'class': 'information'})
        email = re.search(cls.mail_re, bs.get_text())
        try:
            return email.group(0)
        except AttributeError:
            return None


class TsinghuaTe(TsinghuaCrawler):

    def __init__(self):
        url = 'http://www.te.tsinghua.edu.cn/szdw/szxx1.htm'
        super().__init__(url, '信息科学技术学院能源与动力工程系')

    def handler(self):
        bs = self.bs.find('div', {'id': 'vsb_content'})
        for table in bs.find_all('table'):
            for professor in table.find_all('td'):
                try:
                    name = professor.a.get_text()
                    name = name.encode('iso8859-1').decode('utf-8')
                    name = name.strip().replace(' ', '')
                    link = professor.a.attrs['href']
                    if link.startswith('../'):
                        link = self._internal_link_convert(link[2:])
                    email = self._get_email(link)
                    self.append_info(name, email, link)
                except AttributeError:
                    continue
        return self.get_info()

    @classmethod
    def _get_email(cls, url):
        r = requests.get(url)
        bs = BeautifulSoup(r.text, 'lxml')
        t = bs.find('div', {'class': 'teacher-p'}).get_text()
        email = re.search(cls.mail_re, t)
        try:
            return email.group(0)
        except AttributeError:
            return None


class TsinghuaSvm(TsinghuaCrawler):

    def __init__(self):
        url = 'http://www.svm.tsinghua.edu.cn/column/26_1.html'
        super().__init__(url, '信息科学技术学院车辆与运载学院')

    def handler(self):
        bs = self.bs.find('div', {'class': 'teacher-list'})
        for professor in bs.find_all('a'):
            name = professor.get_text()
            name = name.encode('iso8859-1').decode('utf-8')
            link = professor.attrs['href']
            link = self._internal_link_convert(link[2:])
            email = self._get_email(link)
            self.append_info(name, email, link)
        return self.get_info()

    @classmethod
    def _get_email(cls, url):
        r = requests.get(url)
        bs = BeautifulSoup(r.text, 'lxml')
        bs = bs.find('div', {'class': 'desc'})
        email = re.search(cls.mail_re, bs.get_text())
        try:
            return email.group(0)
        except AttributeError:
            return None


class TsinghuaIe(TsinghuaCrawler):

    def __init__(self):
        url = 'http://www.ie.tsinghua.edu.cn/List/index/cid/29.html'
        super().__init__(url, '信息科学技术学院工业工程系')

    def handler(self):
        i = 0
        for bs in self.bs.find_all('ul', {'class': 'teacher'}):
            i += 1
            for professor in bs.find_all('li'):
                name = professor.h2.get_text().strip()
                link = professor.a.attrs['href']
                link = self._internal_link_convert(link)
                email = self._get_email(link, i)
                self.append_info(name, email, link)
        return self.get_info()

    @classmethod
    def _get_email(cls, url, i):
        r = requests.get(url)
        bs = BeautifulSoup(r.text, 'lxml')
        if i == 1:
            bs = bs.find('span', {'class': 'mail'})
            raw = bs.a.attrs['onclick']
            pattern = re.compile(r'sendEmail\(\'(.+?)\',\'(.+?)\'\)')
            ma = re.search(pattern, raw)
            email = ma.group(2).strip() + ma.group(1).strip()
            return email
        elif i == 2:
            bs = bs.find('div', {'class': 'educaz-team-item'})
        email = re.search(cls.mail_re, bs.get_text())
        try:
            return email.group(0)
        except AttributeError:
            return None


class TsinghuaIcenter(TsinghuaCrawler):

    def __init__(self):
        url = 'http://www.icenter.tsinghua.edu.cn/szdw/zzjs.htm'
        super().__init__(url, '信息科学技术学院基础工业训练中心')

    def handler(self):
        bs = self.bs.find('div', {'class': 'entry-content font-mid'})
        for professor in bs.find_all('td'):
            try:
                name = professor.a.attrs['title']
                name = name.encode('iso8859-1').decode('utf-8')
                link = professor.a.attrs['href']
            except KeyError:
                node = professor.find('a', {'target': '_blank'})
                name = node.attrs['title']
                name = name.encode('iso8859-1').decode('utf-8')
                link = node.attrs['href']
            if link == 'javascript:;':
                link = None
            else:
                link = self._internal_link_convert(link[2:])
            email = self._get_email(link)
            self.append_info(name, email, link)
        return self.get_info()

    @classmethod
    def _get_email(cls, url):
        if url is None:
            return None
        r = requests.get(url)
        bs = BeautifulSoup(r.text, 'lxml')
        bs = bs.find('div', {'id': 'vsb_content'})
        email = re.search(cls.mail_re, bs.get_text())
        try:
            return email.group(0)
        except AttributeError:
            return None


def get_pack():
    all_pack = {
        '清华大学': 0, TsinghuaArch: 0, TsinghuaSem: 0,
        TsinghuaCivil: 0, TsinghuaEnv: 0, TsinghuaSppm: 0,
        TsinghuaMe: 0, TsinghuaDpi: 0, TsinghuaTe: 0,
        TsinghuaSvm: 0, TsinghuaIe: 0, TsinghuaIcenter: 1
    }
    return all_pack


def main():
    print(TsinghuaIcenter().run())


if __name__ == '__main__':
    main()
