import datetime
import sqlite3

from vivo_utils.queries import get_person_list
from vivo_utils.queries import get_journal_list
from vivo_utils.queries import get_publisher_list
from vivo_utils.queries import get_article_list
from vivo_utils.queries import get_grant_list
from vivo_utils.queries import get_organization_list

def update_db(connection, db_name, selections):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    prep_tables(c)

    if 'authors' in selections:
        authors = get_person_list.run(connection, **{})
        add_authors(c, authors)
    if 'journals' in selections:
        journals = get_journal_list.run(connection, **{})
        add_journals(c, journals)
    if 'publishers' in selections:
        publishers = get_publisher_list.run(connection, **{})
        add_publishers(c, publishers)
    if 'publications' in selections:
        publications = get_article_list.run(connection, **{})
        add_publications(c, publications)
    if 'grants' in selections:
        grants = get_grant_list.run(connection, **{})
        add_grants(c, grants)
    if 'organizations' in selections:
        organizations = get_organization_list.run(connection, **{})
        add_organizations(c, organizations)

    conn.commit()
    conn.close()

def prep_tables(c):
    c.execute('''create table if not exists authors
                (n_num text, last text collate nocase, first text collate nocase, middle text collate nocase, display text collate nocase, date_added text)''')
    c.execute('''create table if not exists journals
                (n_num text, name text collate nocase, issn text, date_added text)''')
    c.execute('''create table if not exists publishers
                (n_num text, name text collate nocase, date_added text)''')
    c.execute('''create table if not exists publications
                (n_num text, title text collate nocase, doi text, pmid text, type text, date_added text)''')
    c.execute('''create table if not exists grants
                (n_num text, name text collate nocase, ps_num text, pi_num text, pi_name text, start_date text, end_date text, date_added text)''')
    c.execute('''create table if not exists organizations
                (n_num text, name text collate nocase, type text, date_added text)''')

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
            c.execute('INSERT INTO journals (n_num, name, issn, date_added) VALUES(?, ?, ?, ?)', (nnum, journal[0], journal[1], timestamp))
        except sqlite3.IntegrityError as e:
            continue

def add_publishers(c, publishers):
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d")
    for nnum, publisher in publishers.items():
        try:
            c.execute('INSERT INTO publishers (n_num, name, date_added) VALUES(?, ?, ?)', (nnum, publisher, timestamp))
        except sqlite3.IntegrityError as e:
            continue

def add_publications(c, publications):
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d")
    for nnum, publication in publications.items():
        try:
            c.execute('INSERT INTO publications (n_num, title, doi, pmid, type, date_added) VALUES(?, ?, ?, ?, ?, ?)', (((nnum,) + publication + (timestamp,))))
        except sqlite3.IntegrityError as e:
            continue

def add_grants(c, grants):
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d")
    for nnum, grant in grants.items():
        try:
            c.execute('INSERT INTO grants (n_num, name, ps_num, pi_num, pi_name, start_date, end_date, date_added) VALUES(?, ?, ?, ?, ?, ?, ?, ?)', ((nnum,) + grant + (timestamp,)))
        except sqlite3.IntegrityError as e:
            continue

def add_organizations(c, organizations):
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d")
    for nnum, org in organizations.items():
        try:
            c.execute('INSERT INTO organizations (n_num, name, type, date_added) VALUES(?, ?, ?, ?)', (nnum, org[0], org[1], timestamp))
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
