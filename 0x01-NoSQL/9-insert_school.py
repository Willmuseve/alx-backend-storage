#!/usr/bin/env python3
"""
inserts a new document in a collection based in kwargs.
"""


def insert_school(mongo_collection, **kwargs):
    """
    this function ret the new '_id'
    """
    id_object = mongo_collection.insert_one(kwargs)
    return (id_object.inserted_id)
