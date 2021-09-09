import os
from io import StringIO, BytesIO
from bs4 import BeautifulSoup, SoupStrainer
from lxml import etree

FILE_NAME = 'full.html'


def read_file():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, 'r', encoding='windows-1251') as dump:
            file_content = dump.read()

        parser = etree.HTMLParser()
        tree = etree.parse(
            StringIO(file_content), parser)

        tables = []

        for child in tree.getroot().iterchildren():
            if 'body' == child.tag:
                for t in child.iterchildren():
                    tables.append(t)
                    print('\n\r' + ("-"*60) + '\n\r')

                    for tbody in t.iter('tbody'):
                        # print('- TBODY')
                        for tr in tbody.iterchildren('tr'):
                            # print('-- TR')
                            txt = ''
                            for td in tr.iterchildren():
                                # print('--- TD')
                                if len(td):
                                    for f in td.iterchildren('font'):
                                        print(
                                            " ".join(''.join(f.itertext()).split()))

        print('Reading completed. Number of records: %d' % (len(tables)))

    else:
        print('No file found')


if __name__ == '__main__':
    read_file()
