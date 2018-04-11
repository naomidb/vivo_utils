'''
Return a list of the available queries.
'''
import importlib

from vivo_queries import queries

def list_queries():
    method_list = importlib.import_module('vivo_queries.queries')
    query_list = []
    for method in dir(method_list):
        if method != "vivo_queries":
            if not method.startswith('__'):
                query_list.append(method)
    
    return query_list
