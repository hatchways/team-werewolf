import os
from datetime import datetime
from pymongo import MongoClient
from bson import json_util
import json
from flask import Blueprint, request
mentions_handler = Blueprint('mentions_handler', __name__)


@mentions_handler.route('/mentions', methods=['GET', 'POST', 'DELETE'])
def mentions():
    connection_string = 'mongodb+srv://{username}:{password}@{server}/?retryWrites=true&w=majority'
    client = MongoClient(connection_string.format(
        username=os.getenv('USERNAME'),
        password=os.getenv('PASSWORD'),
        server=os.getenv('DB_SERVER')
    ))
    db = client[os.getenv('DB_NAME')]
    mentions_collection = db.mentions
    # this POST functionality is just to load some data for testing
    if request.method == 'POST':
        result = mentions_collection.insert_one({
            'title': 'Foo',
            'content': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
            'platform': 'Twitter',
            'image': 'https://via.placeholder.com/150',
            'date': datetime.now(),
            'popularity': 1
        })
        return {'insertedId': str(result.inserted_id)}
    elif request.method == 'DELETE':
        result = mentions_collection.delete_many({})
        return {'documentsDeleted': result.deleted_count}
    elif request.method == 'GET':
        mentions = []
        for mention in mentions_collection.find():
            mentions.append(mention)
        # using json.dumps here instead of jsonify
        # needed a way to pass a default type for types that could not be converted to JSON
        return json.dumps({'mentions': mentions}, default=json_util.default)
