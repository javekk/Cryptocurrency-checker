from flask import Flask
from flask import request
from flask import jsonify

# Make the Flask Service
app = Flask(__name__)

# Implementaion for the root URL, on http://localhost:5000/ 
@app.route('/')
def index():
    return "This is the Service's root"

# Implement the actual service on http://localhost:5000/cryptos/
@app.route('/cryptos', methods = ['POST'])
def user():
    auth_token = "not_provided"
    if 'auth_token' in request.headers:
        auth_token = request.headers['auth_token']
    if auth_token == '12aw3serxdcrftg987h': # Check the authentication token
        data = request.json 
        print(data)
        return 'ok'
    return 'something went wrong...'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')