from jinja2 import Environment
import json
import requests
import xml.etree.cElementTree as ET

from vivo_utils.vdos.auth_match import Auth_Match
from vivo_utils.queries import find_n_for_label

def match_from_label(connection, label):
    params = queries.find_n_for_label.get_params(connection)
    params['Thing'].extra = label
    params['Thing'].type = 'person'

    current_list = queries.find_n_for_label.run(connection, **params)
    choices = {}

    for key, val in current_list.items():
        #Get rid of leading and trailing spaces
        val = val.rstrip()
        val = val.lstrip()
        #perfect match
        if label.lower() == val.lower():
            choices[key] = val
        #match contains label
        if len(choices) == 0:
            for key, val in current_list.items():
                if label.lower in val.lower():
                    choices[key] = val
    return choices

def make_options(authors):
    #create auth_match for each potential author
    options = []
    for author_n, author_name in authors:
        option = Auth_Match
        option.n_number = author_n
        option.name = author_name

        first = middle = last = ''
        try:
            last, rest = author_name.split(', ')
            try:
                first, middle = rest.split(' ', 1)
            except ValueError as e:
                first = rest
        except ValueError as e:
            last = author_name
        option.first = first
        option.middle = middle
        option.last = last
        
        options.append(option)

def coauthor_match(connection, choices, author_list):
    for choice in choices:
        params = get_all_coauthors.get_params(connection)
        params['Author'] = choice.n_number
        coauthors = get_all_coauthors.run(connection, **params)
        choice.coauthors = coauthors

        for author in author_list:
            if author in choice.coauthors:
                choice.coauthor_matches.append(author)

    overlap = {}
    for choice in choices:
        if len(choice.coauthor_matches) >= 1:
            overlap[choice] = len(choice.coauthor_matches)
    # get all co-authors from articles
    # check if any have matches from Publication
    # if only one: choose that
    # if multiple: ?

def match_from_wos(connection, credentials, label, topics, choices):
    whandler = WHandler(credentials)
    #author_uris = [connection.upload_url + n for n in choices.keys()]
    biblio = {}
    journio = {}
    for author in choices.keys():
        params = get_articles_for_author.get_params(connection)
        params['Author'].n_number = author
        pubs = get_articles_for_author.run(connection, **params)
        journals = get_journals_for_author.run(connection, **params)
        biblio[author] = list(pubs.values())
        journio[author] = list(journals.values())

    first = True
    q = "(AU=" + author + ")"
    top_query = ""
    if topics:
        for topic in topics:
            if first:
                top_query = "TS=" + topic
                first = False
            else:
                top_query = top_query + " OR TS=" + topic
        q = q + " AND (" + top_query + ")"
    results = whandler.get_data(q, None, None)
    
    titles= []
    venues = []
    for result in results:
        root = ET.fromstring(result)
        for record in root.iter('records'):
            titag = record.find('title')
            title = titag.find('value').text
            titles.append(title)

    top_match = ('', 0)
    for person, pubs in biblio.items():
        pubs = [pub.lower() for pub in pubs]
        pub_match = 0
        for name in titles:
            if name.lower() in pubs:
                pub_match += 1
        if pub_match > top_match[1]:
            top_match = (person, pub_match)



def match_from_pm(connection, choices, pmid):
    pmid_filter_file = 'pmid_filter.json'
    with open(pmid_filter_file, 'r') as pmid_log:
        pmid_filter = json.load(pmid_log)
    
    match_found = False
    for choice in choices:
        while not match_found:
            if choice.n_number in pmid_filter.keys():
                if pmid in pmid_filter[choice.n_number][0]:
                    match = choice.n_number
                    match_found = True
                elif pmid in pmid_filter[choice.n_number][1]:
                    continue
                else:
                    query, params = write_query(connection, choice, pmid_filter)
                    pmid_list = run_query(query, **params)
                    if pmid in pmid_list:
                        match = choice.n_number
                        pmid_filter[match][0].append(pmid)

    if match_found:
        for identity, collections in pmid_filter.items():
            if identity not match:
                if pmid not in collections[1]:
                    collections[1].append(pmid)

    with open(pmid_filter_file, 'w') as pmid_log:
        json.dump(pmid_filter, pmid_log)

    return match
