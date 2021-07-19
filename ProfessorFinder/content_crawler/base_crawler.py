import re
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup


class WebCrawler(object):

    mail_re = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')

    def __init__(self, url, name='', test=False):
        self.name = name
        self._url = url
        self._internal_link_parse()     # parse link
        self.all_info = []
        if not test:
            self._page = self._get_page()
            if self._page is None:
                print('error')
            self.bs = self._get_bs()

    def handler(self):
        """
        needs to be overwritten,
        return school, department, name, email, bio of teacher.
        :return:
        """
        # return self.all_info

    def return_data(self):
        self.handler()
        return self.all_info

    def run(self):
        return self.return_data()

    def _internal_link_convert(self, raw_link: str):
        while raw_link.startswith('../'):
            raw_link = raw_link[2:]
        if raw_link.startswith('/'):
            return self._scheme + '://' + self._netloc + raw_link
        elif re.match('^http(s)?://.+', raw_link):
            return raw_link
        else:
            return self._scheme + '://' + raw_link

    def _internal_link_parse(self):
        o = urlparse(self._url)
        self._scheme = o.scheme
        self._netloc = o.netloc
        self._path = o.path

    def _get_page(self):
        try:
            response = requests.get(self._url)
        except requests.exceptions.HTTPError:
            response = None
        return response

    def _get_bs(self):
        return BeautifulSoup(self._page.text, 'lxml')

    @classmethod
    def _get_email(cls, url):
        """
        needs to be overwritten
        receive a url then parse the page
        and return email if possible.
        """
        return ''
