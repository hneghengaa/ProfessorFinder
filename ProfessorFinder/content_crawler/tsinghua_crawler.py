from urllib.parse import urlparse
from ProfessorFinder.content_crawler.base_crawler import WebCrawler


class TsinghuaArch(WebCrawler):
    def __init__(self):
        super().__init__('http://www.arch.tsinghua.edu.cn/column/rw')

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


all_pack = [TsinghuaArch()]


def main():
    pass


if __name__ == '__main__':
    main()
