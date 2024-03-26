#!/usr/bin/env python3
"""This module uses pymongo to change names"""


dei update_topics(mongo_collection, name, topics):
    """
    changes all topics of a school docment based on the name.
    """
    mongo_collection.update_many({ "name": name }, { "$set": { "topics": topics } })
