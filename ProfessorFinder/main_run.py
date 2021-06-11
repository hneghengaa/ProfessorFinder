from content_crawler import *
from content_handler import excel_writer


def main():
    excel_writer.check()
    excel_writer.write_excel(tsinghua_crawler.get_pack())


if __name__ == '__main__':
    main()
