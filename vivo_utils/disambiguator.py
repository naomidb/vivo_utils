from vivo_utils.vdos.auth_match import Auth_Match
from vivo_utils import queries

class Disamiguator(object):
    def __init__(name):
        self.name = name
        self.wos_cats = []
        self.pmids = []




matches = []
index = 0
for choice_n, choice_name in choices.items():
    scoop = queries.get_articles_for_author.get_params(connection)
    scoop['Author'].n_number = choice_n
    pub_list = queries.get_articles_for_author.run(connection, **scoop)

    matches.append(Auth_Match())
    matches[index].n_number = choice_n
    matches[index].name = choice_name
    matches[index].pubs = pub_list

    index += 1

wos_config = get_config('wos/wos_config.yaml')
wosnnection = WOSnnection(wos_config)
wos_pubs = wos.get_pubs.run(wosnnection, label, categories)

best_match = None
for match in matches:
    for title in wos_pubs:
        match.compare_pubs(title)
    if match.points > 0:
        if best_match:
            if match.points > best_match.points:
                best_match = match
        else:
            best_match = match
if best_match:
    print("Match found.")
    return best_match.n_number
else:
    return None