from content_crawler import *
from content_handler import excel_writer

excel_writer.write_excel(tsinghua_crawler.get_pack())
