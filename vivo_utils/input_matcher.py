from vivo_utils.queries import find_n_for_label
from vivo_utils.queries import find_n_for_doi
from vivo_utils.queries import find_n_for_issn

def match_input(connection, label, category, disamb_file, interact=False):
    details = queries.find_n_for_label.get_params(connection)
    details['Thing'].name = label
    details['Thing'].extra = label
    details['Thing'].type = category

    matches = queries.find_n_for_label.run(connection, **details)

    #no matches
    if (len(matches) == 0):
        #label is passed with doi. this counts on there being no articles with the doi as their name.
        if category == "academic_article":
            matches = queries.find_n_for_doi.run(connection, **details)
            if len(matches) == 1:
                for key in matches:
                    match = key

        #label is passed with issn. this counts on there being no journals with the issn as their name.
        elif category == "journal":
            matches = queries.find_n_for_issn.run(connection, **details)
            if len(matches) == 1:
                for key in matches:
                    match = key

        else:
            match = None

    #single match using title
    elif len(matches) == 1:
        for key in matches:
            match = key

    #multiple matches
    else:
        if interact:
            choices = {}

            options = list(matches.items())
            for c, option in enumerate(options, 1):
                choices[c] = option

            index = -1
            for key, val in choices.items():
                number,label = val
                print((str(key) + ': ' + label + ' (' + number + ')\n'))

            index = input("Do any of these match your input? (if none, write -1): ")
            if not index == -1:
                nnum, label = choices.get(index)
                match = nnum
            else:
                match = None
        else:
            match = None
    
    if len(matches) > 1:
        with open(disamb_file, "a+") as dis_file:
            dis_file.write("{} has possible uris: \n{}\n".format(label, list(choices.keys())))

    return match