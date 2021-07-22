"""
    人大
"""
from ProfessorFinder.content_crawler.base_crawler import WebCrawler


class RUCCrawler(WebCrawler):

    def __init__(self, url, name):
        super().__init__(url, name)

    def append_info(self, name, email, url):
        self.all_info.append(('中国人民大学', self.name, name, email, url))

    def get_info(self):
        return self.all_info


class RUCSomeDepartment(RUCCrawler):

    def __init__(self):
        url = 'some url'
        super().__init__(url, 'department name')

    def handler(self):
        pass


def get_pack():
    all_pack = {
        '北京大学': 0, RUCSomeDepartment: 0
    }
    return all_pack


uncrawled = []


def main():
    RUCSomeDepartment().run()


if __name__ == '__main__':
    main()
