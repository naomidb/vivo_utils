import os
import os.path
import shutil
import sys

def fix_name(desired_name, direc):
    files = os.listdir(direc)
    filenames = [str(f) for f in files]

    new_name = desired_name
    change = False
    count = 1
    while (new_name + '.py') in filenames:
        new_name = desired_name + '_' + str(count)
        count += 1
        change = True

    if change:
        desired_name = new_name
        print("Query name was in use. Name changed to " + desired_name)

    return desired_name

def get_template():
    jinja_check = raw_input("Will your query be using Jinja2? (y/n) ")
    update_check = raw_input("Will you be using the query api (getting information from VIVO) or the update api (sending information to VIVO)? Write q for query api or u for update api: ")
    if jinja_check=='y' or jinja_check=='Y':
        if update_check=='u' or update_check=='U':
            template = 'template_jinja_update.py'
        else:
            template = 'template_jinja_query.py'
    else:
        if update_check=='u' or update_check=='U':
            template = 'template_update.py'
        else:
            template = 'template_query.py'

    return template

def main(new_query):
    parent_dir = os.path.dirname(os.getcwd())
    direc = os.path.join(parent_dir, 'queries')
    query = fix_name(new_query, direc)

    filename = query + '.py'
    filepath = os.path.join(direc, filename)

    template = get_template()

    shutil.copy(template, filepath)
    with open(os.path.join(direc, '__init__.py'), 'a+') as output:
        output.write('\nimport ' + query)
    print("Added " + filepath)

if __name__ == '__main__':
    main(sys.argv[1])
