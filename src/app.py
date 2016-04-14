from flask import Flask
import requests
app = Flask(__name__)

################### Routes #####################
@app.route('/api/v1/http/')
def url_endpoint():
    url = request.args.get('url')
    if pass_connection('url'):
        # Generate request to the URL, serve back to user
        req = request.get(url, stream = True)
        return Response(stream_with_context(req.iter_content()), 
                content_type = req.headers['content-type'])
    else:
        return generate_503()

@app.route('/api/v1/sms/')
def sms_endpoint():
    number = request.args.get('number')
    message = request.args.get('message')
    if pass_connection("sms"):
        return send_sms(number, message)
    else:
        return reject_sms()

@app.route('/api/v1/call/')
def call_endpoint():
    number = request.args.get('number')
    message = request.args.get('message')
    if pass_connection("call"):
        return send_call(number, message)
    else:
        return reject_call()

@app.route('/api/v1/emergency_call/')
def e_call_endpoint():
    number = request.args.get('number')
    if pass_connection("ecall"):
        return send_ecall(number)
    else:
        return reject_ecall()

@app.route('/api/v1/stats/')
def return_stats():
    pass

################### Responses #####################
def pass_connection(connection_type):
    pass

def generate_503():
    pass

def send_sms(number, message):
    pass

def send_call(number, message):
    pass

def send_ecall(number):
    pass

def reject_sms():
    pass

def reject_call():
    pass

def reject_ecall():
    pass

if __name == '__main__':
    app.run()
