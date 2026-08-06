from lib import db_conn

db = db_conn.DATABASE()
request = {'cmd':'test'}
response = db.request_response(request)

if 'result' not in response:
    print("Incorrect server server response")
    exit()

if response['result'] != 'OK':
    print("Server returned %s"%response['result'])
    exit()

print("Success! Server response msg: %s"%response.get("msg", ''))