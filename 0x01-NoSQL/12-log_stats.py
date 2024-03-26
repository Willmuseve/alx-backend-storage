#!/usr/bin/env python3
"""
Below script provides some stats about Nginx
logs stored in MongoDB.
"""

from pymongo import MongoClient


if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_logs = client.logs.nginx

    doc_number = nginx_logs.count_documents({})
    get = nginx_logs.count_documents({'method': 'GET'})
    post = nginx_logs.count_documents({'method': 'POST'})
    put = nginx_logs.count_documents({'method': 'PUT'})
    patch = nginx_logs.count_documents({'method': 'PATCH'})
    delete = nginx_logs.count_documents({'method': 'DELETE'})
    get_st = nginx_logs.count_documents({'method': 'GET',
                                            'path': '/status'})

    print("{} logs".format(doc_number))
    print("Methods:")
    print("\tmethod GET: {}".format(get))
    print("\tmethod POST: {}".format(post))
    print("\tmethod PUT: {}".format(put))
    print("\tmethod PATCH: {}".format(patch))
    print("\tmethod DELETE: {}".format(delete))
    print("{} status check".format(get_st))
