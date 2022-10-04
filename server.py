from flask import Flask, request
from tradingview import tradingview
import json
#from threading import Thread
app = Flask(__name__)

@app.route('/validate/<username>', methods=['GET'])
def validate(username):
  try:
    print(username)
    tv = tradingview()
    response = tv.validate_username(username)
    return json.dumps(response), 200, {'Content-Type': 'application/json; charset=utf-8'}
  except Exception as e:
    print("[X] Exception Occured : ", e)
    failureResponse = {
      'errorMessage':'Unknown Exception Occurred1'
    }
    return json.dumps(failureResponse), 500, {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/check-access/<username>', methods=['POST'])
def check_access(username):
  print(username)
  try:
    jsonPayload = request.json
    print(jsonPayload)
    pine_id = jsonPayload.get('pine_id')
    
    print(jsonPayload)
    print(pine_id)
    tv = tradingview()
    accessList = []
    access = tv.get_access_details(username, pine_id)
    accessList = accessList + [access]
      
    return json.dumps(accessList), 200, {'Content-Type': 'application/json; charset=utf-8'}
        
  except Exception as e:
    print("[X] Exception Occured : ", e)
    failureResponse = {
      'errorMessage':'Unknown Exception Occurred'
    }
    return json.dumps(failureResponse), 500, {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/access/<username>', methods=['POST', 'DELETE'])
def access(username):
  print(username)
  try:
    jsonPayload = request.json
    pine_id = jsonPayload.get('pine_id')
    
    print(jsonPayload)
    print(pine_id)
    tv = tradingview()
    accessList = []
    #for pine_id in pine_ids:
    access = tv.get_access_details(username, pine_id)

    
    accessList = accessList + [access]
      
    print("+++++++++",accessList)
    

    if request.method == 'POST':
      duration = jsonPayload.get('duration')
      dNumber = int(duration[:-1])
      dType = duration[-1:]
      for access in accessList:
        tv.add_access(access, dType, dNumber)

    if request.method == 'DELETE':
      for access in accessList:
        tv.remove_access(access)
    return json.dumps(accessList), 200, {'Content-Type': 'application/json; charset=utf-8'}
        
  except Exception as e:
    print("[X] Exception Occured : ", e)
    failureResponse = {
      'errorMessage':'Unknown Exception Occurred'
    }
    return json.dumps(failureResponse), 500, {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/')
def main():
  return 'Your bot is alive!'

# def run():
#   app.run(host='0.0.0.0', port=5000)


# def start_server_async():
#   server = Thread(target=run)
#   server.start()

def start_server():
  app.run(host='0.0.0.0', port=5000)