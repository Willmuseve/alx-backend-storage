#!/usr/bin/env python3
"""
A func that  lists all documents in a collection.
"""


def list_all(mongo_collection):
    """
    Returns list of all documents in the collection,
    or an empty list if otherwise.
    """
    coll = mongo_collection.find()

    return [document for document in coll]
