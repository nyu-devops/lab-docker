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

import os
import redis
from flask import Flask, jsonify, json

app = Flask(__name__)

# GET /
@app.route('/')
def Welcome():
    return app.send_static_file('index.html')

# GET /counter
@app.route('/counter', methods=['GET'])
def get_counter():
    redis_server.incr('counter')
    count = redis_server.get('counter')
    return jsonify(counter=count), 200

# POST /counter
@app.route('/counter', methods=['POST'])
def set_counter():
    redis_server.set('counter', 0)
    count = redis_server.get('counter')
    return jsonify(counter=count), 201

# Initialize Redis
def init_redis(hostname, port, password):
    # Connect to Redis Server
    global redis_server
    redis_server = redis.Redis(host=hostname, port=port, password=password)
    try:
        response = redis_server.client_list()
    except redis.ConnectionError:
        # if you end up here, redis instance is down.
        print '*** FATAL ERROR: Could not conect to the Redis Service'

def connect_to_redis():
    # Get the crdentials from the Bluemix environment
    if 'VCAP_SERVICES' in os.environ:
        VCAP_SERVICES = os.environ['VCAP_SERVICES']
        services = json.loads(VCAP_SERVICES)
        redis_creds = services['rediscloud'][0]['credentials']
        # pull out the fields we need
        redis_hostname = redis_creds['hostname']
        redis_port = int(redis_creds['port'])
        redis_password = redis_creds['password']
    else:
        print "VCAP_SERVICES not found looking for host: redis"
        response = os.system("ping -c 1 redis")
        if response == 0:
            redis_hostname = 'redis'
        else:
            redis_hostname = '127.0.0.1'
        redis_port = 6379
        redis_password = None

    init_redis(redis_hostname, redis_port, redis_password)


if __name__ == "__main__":
    print "Hit Counter Service Starting..."
    connect_to_redis()
    debug = (os.getenv('DEBUG', 'False') == 'True')
    port = os.getenv('PORT', '5000')
    app.run(host='0.0.0.0', port=int(port), debug=debug)
