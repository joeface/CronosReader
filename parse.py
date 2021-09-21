import os
from io import StringIO, BytesIO
from bs4 import BeautifulSoup, SoupStrainer
from lxml import etree

# Tuple with relative filenames to parse
FILES = ('full.html',)


def read_file(file_name):

    if os.path.exists(file_name):
        try:
            with open(file_name, 'r', encoding='windows-1251') as dump:
                file_content = dump.read()
        except:
            print('! Error reading file %s' % (file_name))
            return False

        print('Reading file %s' % (file_name))

        file_content = file_content.replace('<BR>', ' ')

        parser = etree.HTMLParser()
        tree = etree.parse(
            StringIO(file_content), parser)

        tables = []
        records = []

        counter_date = 0
        counter_doc = 0

        is_date = False
        is_doc = False

        rec = None

        for child in tree.getroot().iterchildren():
            if 'body' == child.tag:
                for t in child.iterchildren():
                    tables.append(t)
                    # print('\n\r' + ("-"*60) + '\n\r')

                    for tbody in t.iter('tbody'):
                        # print('- TBODY')
                        for tr in tbody.iterchildren('tr'):
                            # print('-- TR')
                            txt = ''
                            for td in tr.iterchildren():
                                # print('--- TD')
                                if len(td):
                                    for f in td.iterchildren('font'):
                                        txt = " ".join(
                                            ''.join(f.itertext()).split())

                                        if not rec:
                                            rec = {
                                                'date': None,
                                                'doc': '',
                                            }

                                        if is_date:
                                            rec['date'] = txt
                                            is_date = False

                                        if is_doc:
                                            rec['doc'] = txt
                                            is_doc = False

                                        if txt == 'Дата поступ.инф. :':
                                            is_date = True
                                            counter_date += 1

                                        elif txt == 'Полный документ :':
                                            is_doc = True
                                            counter_doc += 1

                                        # print(txt)
                    if rec:
                        records.append(rec)
                        rec = None
                        is_date = False
                        is_doc = False

        # print('Reading completed. Number of tables: %d, records: %d, dates: %d docs: %d' %
        #      (len(tables), len(records), counter_date, counter_doc))

        for r in records:
            print(r['date'])
            print(r['doc'], '\n\n')

    else:
        print('File %s not found' % (file_name))


def run():
    for f in FILES:
        read_file(f)


if __name__ == '__main__':
    run()
