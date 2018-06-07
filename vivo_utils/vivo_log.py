import datetime
import sqlite3

from vivo_utils.queries import get_person_list
from vivo_utils.queries import get_journal_list
from vivo_utils.queries import get_publisher_list
from vivo_utils.queries import get_article_list

def update_db(connection, db_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    prep_tables(c)

    authors = get_person_list.run(connection, **{})
    journals = get_journal_list.run(connection, **{})
    publishers = get_publisher_list.run(connection, **{})
    publications = get_article_list.run(connection, **{})

    add_authors(c, authors)
    add_journals(c, journals)
    add_publishers(c, publishers)
    add_publications(c, publications)

    conn.commit()
    conn.close()

def prep_tables(c):
    c.execute('''create table if not exists authors
                (n_num text unique, last text, first text, middle text, display text, date_added text)''')
    c.execute('''create table if not exists journals
                (n_num text unique, name text, issn text, date_added text)''')
    c.execute('''create table if not exists publishers
                (n_num text unique, name text, date_added text)''')
    c.execute('''create table if not exists publications
                (n_num text unique, title text, doi text, pmid text, type text, date_added text)''')

def add_authors(c, authors):
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d")
    for nnum, author in authors.items():
        try:
            c.execute('INSERT INTO authors (n_num, last, first, middle, display, date_added) VALUES(?, ?, ?, ?, ?, ?)', (((nnum,) + author + (timestamp,))))
        except sqlite3.IntegrityError as e:
            continue

def add_journals(c, journals):
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d")
    for nnum, journal in journals.items():
        try:
            c.execute('INSERT or REPLACE INTO journals (n_num, name, issn, date_added) VALUES(?, ?, ?, ?)', (nnum, journal[0], journal[1], timestamp))
        except sqlite3.IntegrityError as e:
            continue

def add_publishers(c, publishers):
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d")
    for nnum, publisher in publishers.items():
        try:
            c.execute('INSERT or REPLACE INTO publishers (n_num, name, date_added) VALUES(?, ?, ?)', (nnum, publisher, timestamp))
        except sqlite3.IntegrityError as e:
            continue

def add_publications(c, publications):
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d")
    for nnum, publication in publications.items():
        try:
            c.execute('INSERT or REPLACE INTO publications (n_num, title, doi, pmid, type, date_added) VALUES(?, ?, ?, ?, ?, ?)', (((nnum,) + publication + (timestamp,))))
        except sqlite3.IntegrityError as e:
            continue

def lookup(db_name, table, search, term, lenient=False):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    if lenient:
        search = '%' + search + '%'
    query = '''SELECT * FROM {} WHERE {} like ? '''.format(table, term)
    c.execute(query, (search,))
    rows = c.fetchall()
    conn.close()
    return rows
