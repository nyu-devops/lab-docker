# Copyright 2015, 2021 John J. Rofrano All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Redis Counter Demo in Docker
"""
import os
from flask import jsonify, json, abort, request, url_for
from . import app, status  # HTTP Status Codes
from service import DATABASE_URI
from .models import Counter, DatabaseConnectionError

DEBUG = os.getenv("DEBUG", "False") == "True"
PORT = os.getenv("PORT", "8080")

############################################################
# Health Endpoint
############################################################
@app.route("/health")
def health():
    """ Health Status """
    return jsonify(dict(status="OK")), status.HTTP_200_OK


############################################################
# Home Page
############################################################
@app.route("/")
def index():
    """ Home Page """
    return app.send_static_file("index.html")

############################################################
# List counters
############################################################
@app.route("/counters", methods=["GET"])
def list_counters():
    app.logger.info("Request to list all counters...")
    try:
        counters = Counter.all()
    except DatabaseConnectionError as err:
        abort(status.HTTP_503_SERVICE_UNAVAILABLE, err)

    return jsonify(counters)


############################################################
# Read counters
############################################################
@app.route("/counters/<name>", methods=["GET"])
def read_counters(name):
    app.logger.info("Request to Read counter: {}...".format(name))

    try:
        counter = Counter.find(name)
    except DatabaseConnectionError as err:
        abort(status.HTTP_503_SERVICE_UNAVAILABLE, err)

    if not counter:
        abort(status.HTTP_404_NOT_FOUND, "Counter {} does not exist".format(name))

    app.logger.info("Returning: {}...".format(counter.value))
    return jsonify(counter.serialize())


############################################################
# Create counter
############################################################
@app.route("/counters/<name>", methods=["POST"])
def create_counters(name):
    app.logger.info("Request to Create counter...")
    try:
        counter = Counter.find(name)
        if counter is not None:
            return jsonify(code=409, error="Counter already exists"), 409

        counter = Counter(name)
    except DatabaseConnectionError as err:
        abort(status.HTTP_503_SERVICE_UNAVAILABLE, err)

    location_url = url_for('read_counters', name=name, _external=True)
    return jsonify(counter.serialize()), status.HTTP_201_CREATED, {'Location': location_url}


############################################################
# Update counters
############################################################
@app.route("/counters/<name>", methods=["PUT"])
def update_counters(name):
    app.logger.info("Request to Update counter...")
    try:
        counter = Counter.find(name)
        if counter is None:
            return jsonify(code=404, error="Counter {} does not exist".format(name)), 404

        count = counter.increment()
    except DatabaseConnectionError as err:
        abort(status.HTTP_503_SERVICE_UNAVAILABLE, err)

    return jsonify(name=name, counter=count)


############################################################
# Delete counters
############################################################
@app.route("/counters/<name>", methods=["DELETE"])
def delete_counters(name):
    app.logger.info("Request to Delete counter...")
    try:
        counter = Counter.find(name)
        if counter:
            del counter.value
    except DatabaseConnectionError as err:
        abort(status.HTTP_503_SERVICE_UNAVAILABLE, err)

    return "", status.HTTP_204_NO_CONTENT


############################################################
#  U T I L I T Y   F U N C I O N S
############################################################

@app.before_first_request
def init_db():
    try:
        app.logger.info("Initializing the Redis database")
        Counter.connect(DATABASE_URI)
        app.logger.info("Connected!")
    except DatabaseConnectionError as err:
        app.logger.error(str(err))
