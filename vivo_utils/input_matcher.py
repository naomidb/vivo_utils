import sys

from vivo_utils import vivo_log
from vivo_utils.auth_match import Auth_Match

def pub_matching(publication, db_name):
    if isinstance(publication, str):
        matches = vivo_log.lookup(db_name, 'publications', publication, 'title')
    else:
        matches = vivo_log.lookup(db_name, 'publications', publication.title, 'title')
        if len(matches) == 0:
            # doi match
            if publication.doi:
                # make sure doi is not 999999?
                matches = vivo_log.lookup(db_name, 'publications', publication.doi, 'doi')
        if len(matches) == 0:
            # pmid match
            if publication.pmid:
                matches = vivo_log.lookup(db_name, 'publications', publication.pmid, 'pmid')
        # if len(matches) == 0:
        #     # wosid match
        #     matches = vivo_log.lookup(db_name, 'publications', publication.wosid, 'wosid')
    
    return matches

def journal_matching(publication, db_name, added_journals=None):
    if isinstance(publication, str):
        matches = vivo_log.lookup(db_name, 'journals', publication, 'name')
        if len(matches) == 0:
            # lenient string match
            matches = vivo_log.lookup(db_name, 'journals', publication, 'name', True)
    else:
        matches = vivo_log.lookup(db_name, 'journals', publication.journal, 'name')
        if publication.journal in added_journals.keys():
            matches.append(added_journals[publication.journal])
        if len(matches) == 0:
            # lenient string match
            matches = vivo_log.lookup(db_name, 'journals', publication.journal, 'name', True)
        if len(matches) == 0:
            # issn match
            matches = vivo_log.lookup(db_name, 'journals', publication.issn, 'issn')
        if len(matches) == 0:
            # eissn match
            matches = vivo_log.lookup(db_name, 'journals', publication.eissn, 'eissn')
        if len(matches) == 0:
            # eissn in issn match
            matches = vivo_log.lookup(db_name, 'journals', publication.eissn, 'issn')
    
    return matches

def publisher_matching(publisher, db_name):
    matches = vivo_log.lookup(db_name, 'publishers', publisher, 'name')
    if len(matches) == 0:
        # lenient string match
        matches = vivo_log.lookup(db_name, 'publishers', publisher, 'name', True)

    return matches

def organization_matching(organization, db_name, added_orgs=None):
    matches = vivo_log.lookup(db_name, 'organizations', organization, 'name')
    if organization in added_orgs.keys():
        matches.append(added_orgs[org_name])
    if len(matches) == 0:
        # lenient string match
        matches = vivo_log.lookup(db_name, 'organizations', organization, 'name', True)

    return matches

def author_match(author, db_name, added_authors=None):
    matches = vivo_log.lookup(db_name, 'authors', author, 'display')
    if author in added_authors.keys():
        matches.append(added_authors[author], author)
    if len(matches) == 0:
        # lenient string match
        matches = vivo_log.lookup(db_name, 'authors', author, 'display', True)
    return matches

def advanced_author_match(connection, matches, journal, coauthors, output_file, match_ratio=2):
    stdout = sys.stdout
    sys.stdout = open(output_file, 'a+')
    options = []
    print(str(len(matches)) + " possible matches for author.")
    for match in matches:
        option = Auth_Match(connection)
        option.n_number, option.name = match[0:2]

        option.get_journals()
        option.get_coauthors()

        if journal in option.journals.values():
            option.journal_match = True
        for auth in coauthors:
            if auth in option.coauthors.values():
                option.coauthor_matches.append(auth)
        option.get_points(len(coauthors))
        print(option.n_number + " (" + option.name + ") has " + str(option.points) + " points")
        options.append(option)

    sorted_options = sorted(options, key=lambda option: option.points, reverse=True)
    print("Highest points: " + sorted_options[0].n_number + 
            " with " + str(sorted_options[0].points) + " points")

    sys.stdout = stdout
    if sorted_options[0].points > (sorted_options[1].points * match_ratio):
        return sorted_options[0].n_number
    else:
        return list(options.values())