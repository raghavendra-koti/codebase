import json
import sys

from httplib2 import Http


print("Running Endpoint Tester....\n")
address = 'http://localhost:5000'

# TEST 1: TRY TO REGISTER A NEW USER
try:
    h = Http()
    url = address + '/users'
    data = dict(username="Peter", password="Pan")
    data = json.dumps(data)
    resp, content = h.request(url, 'POST', body=data, headers={"Content-Type": "application/json"})
    if resp['status'] != '201' and resp['status'] != '200':
        raise Exception('Received an unsuccessful status code of %s' % resp['status'])

except Exception as err:
    print("Test 1 FAILED: Could not make a new user")
    print(err.args)
    sys.exit()
else:
    print("Test 1 PASS: Successfully made a new user")

# TEST 2: OBTAIN A TOKEN
try:
    h = Http()
    h.add_credentials('Peter', 'Pan')
    url = address + '/token'
    resp, content = h.request(url, 'GET', headers={"Content-Type": "application/json"})
    if resp['status'] != '200':
        raise Exception('Received an unsuccessful status code of %s' % resp['status'])
    new_content = json.loads(content.decode('ascii'))
    if not new_content['token']:
        raise Exception('No Token Received!')
    token = new_content['token']
    print("received token: %s" % token)
except Exception as err:
    print("Test 2 FAILED: Could not exchange user credentials for a token")
    print(err.args)
    sys.exit()
else:
    print("Test 2 PASS: Successfully obtained token! ")

# TEST 3: TRY TO ADD PRODUCS TO DATABASE
try:
    h = Http()
    h.add_credentials(token, 'blank')
    url = address + '/products'
    data = dict(name="apple", category="fruit", price="$.99")
    resp, content = h.request(url, 'POST', body=json.dumps(data), headers={"Content-Type": "application/json"})
    if resp['status'] != '200':
        raise Exception('Received an unsuccessful status code of %s' % resp['status'])
except Exception as err:
    print("Test 3 FAILED: Could not add new products")
    print(err.args)
    sys.exit()
else:
    print("Test 3 PASS: Successfully added new products")
