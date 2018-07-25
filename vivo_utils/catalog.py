'''
Return a list of the available queries.
'''
import importlib

from vivo_utils import queries

def list_queries():
    method_list = importlib.import_module('vivo_utils.queries')
    query_list = []
    for method in dir(method_list):
        if method != "vivo_utils":
            if not method.startswith('__'):
                query_list.append(method)
    
    return query_list
