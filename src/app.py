from flask import Flask
app = Flask(__name__)

@app.route('/api/v1/http/')
def url_endpoint():
    url = request.args.get('url')
    if pass_connection('url'):
        # Generate request to the URL, serve back to user
        pass
    else:
        generate_503()

@app.route('/api/v1/sms/')
def sms_endpoint():
    number = request.args.get('number')
    message = request.args.get('message')
    if pass_connection("sms"):
        pass
    else:
        reject_sms()

@app.route('/api/v1/call/')
def call_endpoint():
    number = request.args.get('number')
    message = request.args.get('message')
    if pass_connection("call"):
        pass
    else:
        reject_call()

@app.route('/api/v1/emergency_call/')
def e_call_endpoint():
    number = request.args.get('number')
    if pass_connection("ecall"):
        pass
    else:
        reject_ecall()

@app.route('/api/v1/stats/')
def return_stats():
    pass

def pass_connection(connection_type):
    pass

def generate_503():
    pass

def reject_sms():
    pass

def reject_call():
    pass

def reject_ecall():
    pass

if __name == '__main__':
    app.run()
