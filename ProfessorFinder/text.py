import re
import requests
from bs4 import BeautifulSoup


class WebHandler(object):
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
        print(self)
        return self.handler()

    def _get_page(self):
        try:
            response = requests.get(self._url)
        except requests.exceptions.HTTPError:
            response = None
        return response


class TsinghuaArch(WebHandler):
    def __init__(self, url):
        super().__init__(url)

    def handler(self):
        all_info = []
        bs = self.bs.find('div', {'class': 'tabContent'})
        peoples = bs.find_all('li')
        for people in peoples:
            name_tab = people.find('div', {'class': 'name'}).a.div
            info_tab = people.find('div', {'class': 'info'})
            try:
                name = name_tab.get_text()
                info = info_tab.get_text()
                all_info.append(('tsinghua', 'Arch', name, info))
            except AttributeError:
                pass
        return all_info


def main():
    url = 'http://www.arch.tsinghua.edu.cn/column/rw'
    print(TsinghuaArch(url).run(), file=open('data.txt', 'w'))


if __name__ == '__main__':
    main()
