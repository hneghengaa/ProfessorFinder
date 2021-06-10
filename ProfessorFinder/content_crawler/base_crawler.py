import requests
from bs4 import BeautifulSoup


class WebCrawler(object):
    def __init__(self, url):
        self._url = url
        self._page = self._get_page()
        if self._page is None:
            print('error')
        self.bs = BeautifulSoup(self._page.text, 'lxml')

    def handler(self):
        """
        needs to be overwritten,
        return school, department, name, email, bio of teacher.
        :return:
        """
        pass

    def run(self):
        return self.handler()

    def _get_page(self):
        try:
            response = requests.get(self._url)
        except requests.exceptions.HTTPError:
            response = None
        return response
