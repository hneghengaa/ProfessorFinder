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
            mail = self._get_mail(link, 'slxbgs@tsinghua.edu.cn')
            self.append_info(name, mail, link)


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


class TsinghuaMe(TsinghuaCrawler):

    def __init__(self):
        url = 'http://me.tsinghua.edu.cn/szdw/ys.htm'
        super().__init__(url, '机械工程学院机械工程系')

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
            link = self._internal_link_convert(link)
            all_professors[name] = link

        for name, link in all_professors.items():
            email = self._get_mail(link, 'mayue@tsinghua.edu.cn')
            self.append_info(name, email, link)


class TsinghuaDpi(TsinghuaCrawler):

    def __init__(self):
        url = 'http://faculty.dpi.tsinghua.edu.cn/index.html'
        super().__init__(url, '机械工程学院精密仪器系')

    def handler(self):
        for bs in self.bs.find_all('div', {'class': 'third'}):
            for professor in bs.ul.find_all('li'):
                name = professor.h6.get_text()
                link = professor.a.attrs['href']
                link = self._internal_link_convert(link)
                email = self._get_email(link)
                self.append_info(name, email, link)


class TsinghuaTe(TsinghuaCrawler):

    def __init__(self):
        url = 'http://www.te.tsinghua.edu.cn/szdw/szxx1.htm'
        super().__init__(url, '机械工程学院能源与动力工程系')

    def handler(self):
        bs = self.bs.find('div', {'id': 'vsb_content'})
        for table in bs.find_all('table'):
            for professor in table.find_all('td'):
                try:
                    name = professor.a.get_text()
                    name = name.encode('iso8859-1').decode('utf-8')
                    name = name.strip().replace(' ', '')
                    link = professor.a.attrs['href']
                    email = self._get_email(link)
                    self.append_info(name, email, link)
                except AttributeError:
                    continue


class TsinghuaSvm(TsinghuaCrawler):

    def __init__(self):
        url = 'http://www.svm.tsinghua.edu.cn/column/26_1.html'
        super().__init__(url, '机械工程学院车辆与运载学院')

    def handler(self):
        bs = self.bs.find('div', {'class': 'teacher-list'})
        for professor in bs.find_all('a'):
            name = professor.get_text()
            name = name.encode('iso8859-1').decode('utf-8')
            link = professor.attrs['href']
            link = self._internal_link_convert(link)
            email = self._get_email(link, 'qcxbgs@tsinghua.edu.cn')
            self.append_info(name, email, link)


class TsinghuaIe(TsinghuaCrawler):

    def __init__(self):
        url = 'http://www.ie.tsinghua.edu.cn/List/index/cid/29.html'
        super().__init__(url, '机械工程学院工业工程系')

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
        super().__init__(url, '机械工程学院基础工业训练中心')

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
                pass
            else:
                link = self._internal_link_convert(link)
            email = self._get_email(link, 'saturn@tsinghua.edu.cn')
            self.append_info(name, email, link)

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


class TsinghuaHy(TsinghuaCrawler):

    def __init__(self):
        url = 'http://www.hy.tsinghua.edu.cn/szqk/szxx.htm'
        super().__init__(url, '航天航空学院')

    def handler(self):
        bs = self.bs.find('div', {'id': 'vsb_content'})
        for professor in bs.find_all('a'):
            name = professor.get_text()
            try:
                name = name.encode('iso8859-1').decode('utf-8')
            except UnicodeDecodeError:
                pass
            name = ''.join(name.split())
            link = professor.attrs['href']
            link = self._internal_link_convert(link)
            email = self._get_email(link)
            self.append_info(name, email, link)


class TsinghuaSss(TsinghuaCrawler):

    def __init__(self):
        url = 'http://www.sss.tsinghua.edu.cn/szll.htm'
        super().__init__(url, '社会科学学院')

    def handler(self):
        teacher_list = \
            self.bs.find_all('div', {'class': 'teacher_list'})
        for a_list in teacher_list:
            for professor in a_list.find_all('li'):
                name = professor.get_text()
                name = name.encode('iso8859-1').decode('utf-8')
                name = name.strip()
                link = professor.a.attrs['href']
                link = self._internal_link_convert('/' + link)
                email = self._get_email(link, 'skxy@tsinghua.edu.cn')
                self.append_info(name, email, link)


class TsinghuaCs(TsinghuaCrawler):

    def __init__(self):
        url = 'http://www.cs.tsinghua.edu.cn/szzk/jzgml.htm'
        super().__init__(url, '信息科学技术学院电子工程系')

    def handler(self):
        bs = self.bs.find('div', {'class': 'people01-nr'})
        for dl in bs.find_all('dl'):
            for professor in dl.find_all('li'):
                tar = professor.find('div', {'class': 'text'})
                name = tar.h2.get_text()
                name = name.encode('iso8859-1').decode('utf-8')
                link = tar.a.attrs['href'][2:]
                link = self._internal_link_convert(link)
                try:
                    email = re.search(self.mail_re, tar.get_text())
                    email = email.group(0)
                except AttributeError:
                    email = None
                self.append_info(name, email, link)


class TsinghuaAu(TsinghuaCrawler):

    def __init__(self):
        url = 'http://www.au.tsinghua.edu.cn/szdw/jsdw1/ayjscz.htm'
        super().__init__(url, '信息科学技术学院自动化系')

    def handler(self):
        teacher_list = \
            self.bs.find_all('div', {'class': 'teacher-list'})
        for li in teacher_list:
            for professor in li.find_all('a'):
                name = professor.get_text()
                name = name.encode('iso8859-1').decode('utf-8')
                link = professor.attrs['href']
                if link == 'javascript:;':
                    link = None
                else:
                    link = self._internal_link_convert(link[5:])
                email = self._get_email(link)
                self.append_info(name, email, link)

    @classmethod
    def _get_email(cls, url):
        try:
            r = requests.get(url)
        except requests.exceptions.MissingSchema:
            return None
        bs = BeautifulSoup(r.text, 'lxml')
        info_tab = bs.find('div', {'class': 'basic'})
        email = re.search(cls.mail_re, info_tab.get_text())
        try:
            return email.group(0)
        except AttributeError:
            return None


class TsinghuaSic(TsinghuaCrawler):

    def __init__(self):
        url = 'https://www.sic.tsinghua.edu.cn/szdw/rygc/szxx.htm'
        super().__init__(url, '信息科学技术学院集成电路')

    def handler(self):
        bs = self.bs.find('div', {'class': 'clearfloat list_zhy'})
        for professor in bs.find_all('a'):
            name = professor.get_text()
            name = name.encode('iso8859-1').decode('utf-8')
            link = professor.attrs['href'][5:]
            link = self._internal_link_convert(link)
            email = self._get_email(link)
            self.append_info(name, email, link)


class TsinghuaInsc(TsinghuaCrawler):

    def __init__(self):
        url = 'https://www.insc.tsinghua.edu.cn/szdw/zzjs.htm'
        super().__init__(url, '信息科学技术学院网络研究院')

    def handler(self):
        bs = self.bs.find('div', {'id': 'vsb_content'})
        for professor in bs.find_all('a'):
            name = professor.get_text()
            name = name.encode('iso8859-1').decode('utf-8')
            link = professor.attrs['href'][2:]
            link = self._internal_link_convert(link)
            email = self._get_email(link)
            self.append_info(name, email, link)


class TsinghuaThss(TsinghuaCrawler):
    pass


class TsinghuaBnrist(TsinghuaCrawler):

    def __init__(self):
        url = 'https://www.bnrist.tsinghua.edu.cn/rcdw/jsml.htm'
        super().__init__(url, '信息技术学院信息国家研究中心')

    def handler(self):
        bs = self.bs.find('div', {'id': 'vsb_content'})
        for professor in bs.find_all('a'):
            name = professor.get_text()
            name = name.encode('iso8859-1').decode('utf-8')
            link = professor.attrs['href']
            if link == '#':
                link = None
                email = None
            else:
                link = self._internal_link_convert(link)
                email = self._get_email(link)
            print(name, link, email)
            self.append_info(name, email, link)


class TsinghuaLaw(TsinghuaCrawler):

    def __init__(self):
        url = 'https://www.law.tsinghua.edu.cn/szll/byjs/zzjs.htm'
        super().__init__(url, '法学院')

    def handler(self):
        bs = self.bs.find_all('div', {'class': 'side-name'})
        for professor in bs:
            name = professor.get_text()
            name = name.encode('iso8859-1').decode('utf-8')
            link = professor.a.attrs['href']
            link = self._internal_link_convert(link)
            email = self._get_email(link)
            self.append_info(name, email, link)


class TsinghuaTsjc(TsinghuaCrawler):

    def __init__(self):
        url = 'https://www.tsjc.tsinghua.edu.cn/xysz/jszy.htm'
        super().__init__(url, '新闻与传播学院')

    def handler(self):
        for professor in self.bs.find_all('td'):
            tab = professor.a
            try:
                name = tab.get_text()
                try:
                    name = ''.join(name.split())
                    name = name.encode('iso8859-1').decode('utf-8')
                except UnicodeDecodeError:
                    pass
                link = tab.attrs['href']
            except AttributeError:
                continue
            email = self._get_email(link)
            self.append_info(name, email, link)


class TsinghuaPbcsf(TsinghuaCrawler):

    def __init__(self):
        url = 'http://www.pbcsf.tsinghua.edu.cn/portal/list/index/id/10.html'
        super().__init__(url, '五道口金融学院')

    def handler(self):
        with open('content_crawler/content_data/tsinghuaPbcsf.json', 'r') as f:
            data = json.load(f)
        for professor in data:
            name = professor['title']
            link = professor['url']
            link = self._internal_link_convert(link)
            email = self._get_email(link)
            self.append_info(name, email, link)


class TsinghuaMse(TsinghuaCrawler):

    def __init__(self):
        url = 'https://www.mse.tsinghua.edu.cn/szqk/jsdw1.htm'
        super().__init__(url, '材料学院')

    def handler(self):
        bs = self.bs.find('div', {'class': 'szdw-list'})
        table = bs.ul
        for professor in table.find_all('li'):
            name = professor.a.get_text()
            name = name.encode('iso8859-1').decode('utf-8')
            m = map(lambda x: '' if x == '　' or x == ' ' else x, name)
            name = ''.join(m)
            link = professor.a.attrs['href']
            link = self._internal_link_convert(link)
            email = self._get_email(link, 'CLX@TSINGHUA.EDU.CN')
            self.append_info(name, email, link)


class TsinghuaAd(TsinghuaCrawler):

    def __init__(self):
        url = 'https://www.ad.tsinghua.edu.cn/jsdw/jsml.htm'
        super().__init__(url, '美术学院')

    def handler(self):
        bs = self.bs.find('div', {'id': 'vsb_content'})
        for professor in bs.find_all('td'):
            tab = professor.a
            try:
                name = tab.get_text()
                name = name.encode('iso8859-1').decode('utf-8')
                link = tab.attrs['href']
                link = self._internal_link_convert(link)
                email = self._get_email(link)
                self.append_info(name, email, link)
            except (AttributeError, UnicodeDecodeError):
                pass


class TsinghuaEea(TsinghuaCrawler):

    def __init__(self):
        url = 'https://www.eea.tsinghua.edu.cn/szdw/zzjs1.htm'
        super().__init__(url, '电机工程与应用电子技术系')

    def handler(self):
        ul = self.bs.find('ul', {'id': 'list'})
        for li in ul.find_all('li'):
            for professor in li.find_all('a'):
                name = professor.attrs['title']
                name = name.encode('iso8859-1').decode('utf-8')
                link = professor.attrs['href']
                link = self._internal_link_convert(link)
                email = self._get_email(link, 'ee@tsinghua.edu.cn')
                self.append_info(name, email, link)


class TsinghuaEp(TsinghuaCrawler):

    def __init__(self):
        url = 'http://www.ep.tsinghua.edu.cn/column/32_1.html'
        super().__init__(url, '工程物理')

    def handler(self):
        bs = self.bs.find('div', {'class': 'right-main-box'})
        for professor in bs.find_all('li'):
            name = professor.get_text()
            name = name.encode('iso8859-1').decode('utf-8')
            try:
                link = professor.a.attrs['href']
                link = self._internal_link_convert(link)
                email = self._get_email(link, 'ioe@tsinghua.edu.cn')
            except AttributeError:
                link = None
                email = None
            self.append_info(name, email, link)


class TsinghuaIoe(TsinghuaCrawler):

    def __init__(self):
        url = 'https://www.ioe.tsinghua.edu.cn/szdw/gdjyyjs.htm'
        super().__init__(url, '高等教育研究所')

    def handler(self):
        navs = self.bs.find('ul', {'class': 'left-nav'})
        for nav in navs.find_all('li'):
            sub_link = '/szdw/' + nav.a.attrs['href']
            sub_link = self._internal_link_convert(sub_link)
            r = requests.get(sub_link)
            print(sub_link)
            bs = BeautifulSoup(r.text, 'lxml')
            ul = bs.find('ul', {'class': 'teacher-list '
                                         'clearfix text-center'})
            try:
                for professor in ul.find_all('li'):
                    t = professor.find('div', {'class':
                                                   'teacher-name'})
                    name = t.get_text()
                    name = name.encode('iso8859-1').decode('utf-8')
                    link = t.a.attrs['href']
                    link = self._internal_link_convert(link)
                    email = self._get_email(link,
                                            'ioe@tsinghua.edu.cn')
                    self.append_info(name, email, link)
            except AttributeError:
                pass


class TsinghuaMath(TsinghuaCrawler):

    def __init__(self):
        url = 'https://www.math.tsinghua.edu.cn/szdw1/zzjs.htm'
        super().__init__(url, '数学系')

    def handler(self):
        pass


class TsinghuaPhys(TsinghuaCrawler):

    def __init__(self):
        url = 'https://www.phys.tsinghua.edu.cn/ry/jsfc/apysx.htm'
        super().__init__(url, '物理系')

    def handler(self):
        bs = self.bs.find('div', {'class': 'pull-right right-width'})
        for professor in bs.find_all('li'):
            tab = professor.a
            name = tab.attrs['title']
            name = name.encode('iso8859-1').decode('utf-8')
            m = map(lambda x: '' if x == '　' or x == ' ' else x, name)
            name = ''.join(m)
            link = tab.attrs['href']
            link = self._internal_link_convert(link)
            email = self._get_email(link, 'wlx@tsinghua.edu.cn')
            self.append_info(name, email, link)


class TsinghuaChem(TsinghuaCrawler):

    def __init__(self):
        url = 'https://www.chem.tsinghua.edu.cn/szdw/zzjg/apypx1.htm'
        super().__init__(url, '化学系')

    def handler(self):
        p = self.bs.find_all('a', {'class': 'zhy_tittle'})
        for professor in p:
            try:
                name = professor.attrs['title']
                name = name.encode('iso8859-1').decode('utf-8')
                link = professor.attrs['href']
                link = self._internal_link_convert(link)
            except KeyError:
                continue
            email = self._get_email(link)
            self.append_info(name, email, link)


class TsinghuaDess(TsinghuaCrawler):

    def __init__(self):
        url = 'https://www.dess.tsinghua.edu.cn/sz/qzjs.htm'
        super().__init__(url, '地球系统科学系')

    def handler(self):
        v_links = [
            'https://www.dess.tsinghua.edu.cn/sz/qzjs.htm',
            'https://www.dess.tsinghua.edu.cn/sz/qzjs/2.htm',
            'https://www.dess.tsinghua.edu.cn/sz/qzjs/1.htm'
        ]
        for each_link in v_links:
            r = requests.get(each_link)
            bs = BeautifulSoup(r.text, 'lxml')
            bs = bs.find('section', {'class': 'n_renwu'})
            for professor in bs.find_all('li'):
                tab = professor.a
                name = tab.attrs['title']
                name = name.encode('iso8859-1').decode('utf-8')
                link = tab.attrs['href']
                link = self._internal_link_convert(link)
                email = self._get_email(link,
                                        'dess@mail.tsinghua.edu.cn')
                print(name, link, email)
                self.append_info(name, email, link)


class TsinghuaAstro(TsinghuaCrawler):

    def __init__(self):
        url = 'http://astro.tsinghua.edu.cn/index.php' \
              '/zh/people-faculty'
        super().__init__(url, '天文系')

    def handler(self):
        bs = self.bs.find('div', {'id': 'ce-category-88'})
        for tabs in bs.find_all('tbody'):
            for professor in tabs.find_all('tr'):
                name = professor.find('td', {'class': 'item-title'})
                link = name.a.attrs['href']
                link = self._internal_link_convert(link)
                name = name.get_text()
                email = self._get_email(link)
                print(name, link, email)
                self.append_info(name, email, link)


class TsinghuaLife(TsinghuaCrawler):

    def __init__(self):
        url = 'https://life.tsinghua.edu.cn/szdw/jzyg1.htm'
        super().__init__(url, '生命科学学院')

    def handler(self):
        pls = self.bs.find_all('div', {'class': 'pepolelist'})
        for pl in pls:
            bs = pl.find_all('ul', {'class': 'clearfix'})
            for professors in bs:
                for professor in professors.find_all('li'):
                    name = professor.a.attrs['title']
                    name = name.encode('iso8859-1').decode('utf-8')
                    link = professor.a.attrs['href']
                    link = self._internal_link_convert(link)
                    email = self._get_email(link, 'admin-life@tsinghua.edu.cn')
                    if link == 'https://javascript:;':
                        link = None
                    self.append_info(name, email, link)


def get_pack():
    all_pack = {
        '清华大学': 0, TsinghuaArch: 0, TsinghuaSem: 0,
        TsinghuaCivil: 0, TsinghuaEnv: 0, TsinghuaSppm: 0,
        TsinghuaMe: 0, TsinghuaDpi: 0, TsinghuaTe: 0,
        TsinghuaSvm: 0, TsinghuaIe: 0, TsinghuaIcenter: 0,
        TsinghuaHy: 0, TsinghuaSss: 0, TsinghuaCs: 0,
        TsinghuaAu: 0, TsinghuaSic: 0, TsinghuaInsc: 0,
        TsinghuaBnrist: 0, TsinghuaLaw: 0, TsinghuaTsjc: 0,
        TsinghuaPbcsf: 0, TsinghuaMse: 0, TsinghuaAd: 0,
        TsinghuaEea: 0, TsinghuaEp: 0, TsinghuaIoe: 0,
        TsinghuaPhys: 0, TsinghuaChem: 0, TsinghuaDess: 0,
        TsinghuaAstro: 0, TsinghuaLife: 1
    }
    return all_pack


uncrawled = ['马克思主义学院', '人文学院', '信息技术学院软件学院',
             '化学工程系', '核能与新能源技术研究院']


def main():
    TsinghuaLife().run()


if __name__ == '__main__':
    main()
