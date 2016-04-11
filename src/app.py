from flask import Flask
app = Flask(__name__)

@app.route('/api/v1/http/<path:url>')
def url_endpoint(url):
    pass

@app.route('/api/v1/sms/<path:number>/<path:message>')
def sms_endpoint(number, message):
    pass

@app.route('/api/v1/call/<path:number>/<path:message>')
def call_endpoint(number, message):
    pass

@app.route('/api/v1/emergency_call/<path:message>')
def e_call_endpoint(number, message):
    pass

@app.route('/api/v1/stats')
def return_stats():
    pass

if __name == '__main__':
    app.run()
