from content_crawler import __all__ as ap
from content_crawler import *
from content_handler import excel_writer


def main():
    excel_writer.check()
    for each in ap:
        eval('excel_writer.write_excel({}.get_pack())'.format(each))


if __name__ == '__main__':
    main()
