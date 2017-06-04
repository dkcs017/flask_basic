from flask import Flask, request, make_response, jsonify

import json

app = Flask(__name__)

user_map = {'EUREXEXCSPV':{'F001INQ':0,'F001MAI':3},
            'EUREXMBRSPV':{'F001INQ':3,'F001MAI':2},
            'EUREXEEXSPV':{'F002INQ': 3,'F001MAI': 2,'F001INQ': 3,'F003MAI': 2},
            }

@app.route('/')
def list_routes():
	response = {}
	for route in app.url_map.iter_rules():
		response.update({route.endpoint : route.rule})
	print response
	return make_response(jsonify(routes=response), 200)


@app.route('/layer/settings',methods = ['POST'])
def view_settings():
    '''
    	url:
	request: 
		 { 
			'username' : 'EUREXEEXSPV' , 
			'privList' : [ 
					'F002INQ',
					'F001MAI' 
				     ]
		 }
    '''
    if request.is_json:
        try:
            json_request = json.loads(request.get_data())
            if json_request['username'] in user_map:
                privilege_map = user_map[json_request['username']]
                entitlement = {}
                for priv in json_request['privList']:
                    try:
                        entitlement.update({priv:privilege_map[priv]})
                    except KeyError as ke:
                        entitlement.update({priv:'unknown'})

                response  = make_response(jsonify(entitlementLevel=entitlement),200)
            else:
                response = make_response(jsonify(entitlementLevel='Unknown User %s' % json_request['username']),
                                         {'content-type': 'application/json'}, 200)
        except Exception as ex:
            response = make_response(jsonify(errorMessage='Not a valid json request'),500)
            print ex
    else:
        response = make_response(jsonify(errorMessage='Not a json'), 400)

    return response


@app.route('/layer/update_settings',methods = ['POST'])
def update_settings():
    '''
    	url:
	request: 
		 { 
			'username' : 'EUREXEEXSPV' , 
			'privList' : { 
					'F002INQ': 3,
					'F001MAI': 2 
				     }
		 }
    '''
    if request.is_json:
        try:
            json_request = json.loads(request.get_data())
            if json_request['username'] in user_map:
                privilege_map = user_map[json_request['username']]
                entitlement = {}
                for priv in json_request['privList']:
                    try:
			user_map[json_request['username']][priv] = json_request['privList'][priv]
                        entitlement.update({priv:privilege_map[priv]})
                    except KeyError as ke:
                        entitlement.update({priv:'unknown'})

                response  = make_response(jsonify(entitlementLevel=entitlement),200)
            else:
                response = make_response(jsonify(entitlementLevel='Unknown User %s' % json_request['username']),
                                         {'content-type': 'application/json'}, 200)
        except Exception as ex:
            response = make_response(jsonify(errorMessage='Not a valid json request'),500)
            print ex
    else:
        response = make_response(jsonify(errorMessage='Not a json'), 400)

    return response


if __name__ == '__main__':
    app.run(debug=True)
