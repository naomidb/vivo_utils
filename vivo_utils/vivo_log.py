import datetime
import sqlite3

from vivo_utils.queries import get_person_list
from vivo_utils.queries import get_journal_list
from vivo_utils.queries import get_publisher_list
from vivo_utils.queries import get_article_list

def update_db(connection):
    conn = sqlite3.connect('fake_vivo_log.db')
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
        c.execute('INSERT or REPLACE INTO authors (n_num, last, first, middle, display) VALUES(?, ?, ?, ?, ?, ?)', (((nnum,) + author + (timestamp,))))

def add_journals(c, journals):
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d")
    for nnum, journal in journals.items():
        c.execute('INSERT or REPLACE INTO journals (n_num, name, issn) VALUES(?, ?, ?, ?)', (nnum, journal[0], journal[1], timestamp))

def add_publishers(c, publishers):
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d")
    for nnum, publisher in publishers.items():
        c.execute('INSERT or REPLACE INTO publishers (n_num, name) VALUES(?, ?, ?)', (nnum, publisher, timestamp))

def add_publications(c, publications):
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d")
    for nnum, publication in publications.items():
        dataset = ()
        c.execute('INSERT or REPLACE INTO publications (n_num, title, doi, pmid, type) VALUES(?, ?, ?, ?, ?, ?)', (((nnum,) + publication + (timestamp,))))

def lookup(table, search, term, lenient=False):
    conn = sqlite3.connect('fake_vivo_log.db')
    c = conn.cursor()
    if lenient:
        query = '''SELECT * FROM {} WHERE {} like '%{}%' '''.format(table, term, search)
    else:
        query = '''SELECT * FROM {} WHERE {}='{}' '''.format(table, term, search)
    c.execute(query)
    rows = c.fetchall()
    conn.close()
    return rows
