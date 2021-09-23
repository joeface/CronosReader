import os
import re
import json
from io import StringIO, BytesIO
from bs4 import BeautifulSoup, SoupStrainer
from lxml import etree

# Tuple with relative filenames to parse
FILES = ('full.html',)

# Global record storage
RECORDS = []

# Global surnames storage
SURNAMES = []


def read_file(file_name):

    global RECORDS

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

                    if rec:
                        RECORDS.append(rec)
                        rec = None
                        is_date = False
                        is_doc = False

    else:
        print('File %s not found' % (file_name))


def parse():

    global RECORDS

    # Read data from files
    for f in FILES:
        read_file(f)

    # Output records
    for rec in RECORDS:
        print(rec['date'])
        print(replace_names(rec['doc']), '\n\n')


def search_names():
    try:
        with open('dump.txt', 'r', encoding='utf-8') as dump:
            file_content = dump.read()
    except:
        print('! Error reading dump file')
        return False

    names = re.findall(
        r'([а-я]+ [а-я]{1}\.[а-я]{1}\.)[\W]+', file_content, re.I)

    for n in names:
        print(n)

    print('Total number of names found: %d' % (len(names)))


def index_surnames():

    global SURNAMES

    try:
        with open('surnames.json') as json_file:
            file_content = json.load(json_file)
    except:
        print('! Error reading surnames file')
        return False

    min_len = 20

    for surname in file_content:
        SURNAMES.append(surname['Surname'])
        if len(surname['Surname']) < min_len:
            min_len = len(surname['Surname'])

    print('Total number of surnames found: %d' % (len(SURNAMES)))
    print('Mininal surname length: %d' % (min_len))


def replace_names(text):
    return re.sub(r'([а-я]+ [а-я]{1}\.[а-я]{1}\.)[\W]+', '--- ', text, flags=re.I)


if __name__ == '__main__':
    index_surnames()
