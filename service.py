# Copyright 2015 IBM Corp. All Rights Reserved.
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
'''
Redis Counter Demo in Docker
'''
import os
import sys
import logging
from redis import Redis
from redis.exceptions import ConnectionError
from flask import Flask, jsonify, json, abort

DEBUG = (os.getenv('DEBUG', 'False') == 'True')
PORT = os.getenv('PORT', '5000')

app = Flask(__name__)

redis_server = None

# GET /
@app.route('/')
def index():
    ''' Home Page '''
    return app.send_static_file('index.html')

# GET /counter
@app.route('/counter', methods=['GET'])
def get_counter():
    ''' get the counter '''
    try:
        redis_server.incr('counter')
        count = redis_server.get('counter')
    except:
        abort(404, "Redis service not found")
    return jsonify(counter=count), 200

# POST /counter
@app.route('/counter', methods=['POST'])
def set_counter():
    ''' Set the counter '''
    try:
        redis_server.set('counter', 0)
        count = redis_server.get('counter')
    except:
        abort(404, "Redis service not found")
    return jsonify(counter=count), 201

# Initialize Redis
def connect_to_redis(hostname, port, password):
    ''' Connects to Redis and tests the connection '''
    global redis_server
    app.logger.info("Testing Connection to: %s:%s", hostname, port)
    redis_server = Redis(host=hostname, port=port, password=password)
    try:
        redis_server.ping()
        app.logger.info("Connection established")
    except ConnectionError:
        app.logger.info("Connection Error from: %s:%s", hostname, port)
        redis_server = None
    return redis_server


def init_db():
    '''
    Initialized Redis database connection

    This method will work in the following conditions:
      1) In Bluemix with Redis bound through VCAP_SERVICES
      2) With Redis running on the local server as with Travis CI
      3) With Redis --link in a Docker container called 'redis'
    '''
    global redis_server
    # Get the credentials from the Bluemix environment
    if 'VCAP_SERVICES' in os.environ:
        app.logger.info("Using VCAP_SERVICES...")
        vcap_services = os.environ['VCAP_SERVICES']
        services = json.loads(vcap_services)
        creds = services['rediscloud'][0]['credentials']
        app.logger.info("Conecting to Redis on host %s port %s",
                        creds['hostname'], creds['port'])
        redis_server = connect_to_redis(creds['hostname'], creds['port'], creds['password'])
    else:
        app.logger.info("VCAP_SERVICES not found, checking localhost for Redis")
        redis_server = connect_to_redis('127.0.0.1', 6379, None)
        if not redis_server:
            app.logger.info("No Redis on localhost, looking for redis host")
            redis_server = connect_to_redis('redis', 6379, None)
    if not redis_server:
        # if you end up here, redis instance is down.
        app.logger.fatal('*** FATAL ERROR: Could not connect to the Redis Service')

def initialize_logging(log_level=logging.INFO):
    """ Initialized the default logging to STDOUT """
    if not app.debug:
        print 'Setting up logging...'
        # Set up default logging for submodules to use STDOUT
        # datefmt='%m/%d/%Y %I:%M:%S %p'
        fmt = '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
        logging.basicConfig(stream=sys.stdout, level=log_level, format=fmt)

        # Make a new log handler that uses STDOUT
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter(fmt))
        handler.setLevel(log_level)

        # Remove the Flask default handlers and use our own
        handler_list = list(app.logger.handlers)
        for log_handler in handler_list:
            app.logger.removeHandler(log_handler)
        app.logger.addHandler(handler)
        app.logger.setLevel(log_level)
        app.logger.info('Logging handler established')

if __name__ == "__main__":
    print "Hit Counter Service Starting..."
    init_db()
    app.run(host='0.0.0.0', port=int(PORT), debug=DEBUG)
