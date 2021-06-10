import unittest
from ProfessorFinder.content_crawler.base_crawler import WebCrawler


class BaseCrawlerTestCase(unittest.TestCase):

    def setUp(self):
        self.test_crawler1 = WebCrawler('https://www.sem.tsinghua.edu.cn/tesearch/jssearch.html', test=True)
        self.test_crawler2 = WebCrawler('http://www.arch.tsinghua.edu.cn/column/rw', test=True)

    def test_urlparse(self):
        pass

    def test_internal_convert(self):
        self.assertEqual(self.test_crawler1._internal_link_convert('/upload_files/image/1572091053113_0B.png'),
                         'https://www.sem.tsinghua.edu.cn/upload_files/image/1572091053113_0B.png')
        self.assertEqual(self.test_crawler1._internal_link_convert(
            'www.sem.tsinghua.edu.cn/upload_files/image/1572091053113_0B.png'),
            'https://www.sem.tsinghua.edu.cn/upload_files/image/1572091053113_0B.png')
        self.assertEqual(self.test_crawler1._internal_link_convert(
            'https://www.sem.tsinghua.edu.cn/upload_files/image/1572091053113_0B.png'),
            'https://www.sem.tsinghua.edu.cn/upload_files/image/1572091053113_0B.png')
        self.assertEqual(self.test_crawler2._internal_link_convert('/upload_files/image/1572091053113_0B.png'),
                         'http://www.arch.tsinghua.edu.cn/upload_files/image/1572091053113_0B.png')
        self.assertEqual(self.test_crawler2._internal_link_convert(
            'www.arch.tsinghua.edu.cn/upload_files/image/1572091053113_0B.png'),
            'http://www.arch.tsinghua.edu.cn/upload_files/image/1572091053113_0B.png')
        self.assertEqual(self.test_crawler2._internal_link_convert(
            'http://www.arch.tsinghua.edu.cn/upload_files/image/1572091053113_0B.png'),
                         'http://www.arch.tsinghua.edu.cn/upload_files/image/1572091053113_0B.png')

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
