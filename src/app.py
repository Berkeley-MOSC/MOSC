from flask import Flask, render_template, abort, request, redirect
import requests
import filter as mf
# import twilio.twiml

app = Flask(__name__)

mf_instance = mf.mosc_buffer()

################### Routes #####################
@app.route('/api/v1/http/')
def url_endpoint():
    url = request.args.get('url')
    if pass_connection('data'):
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
    xml = ""
    # Emergency calls
    xml += "<ecall>\n"
    xml += "    <received>"
    xml += mf_instance.num_received_ecalls()
    xml += "    </received>\n"
    xml += "    <served>"
    xml += mf_instance.num_served_ecalls()
    xml += "    </served>\n"
    xml += "</ecall>\n"

    # Standard calls
    xml += "<call>\n"
    xml += "    <received>"
    xml += mf_instance.num_received_calls()
    xml += "    </received>\n"
    xml += "    <served>"
    xml += mf_instance.num_served_calls()
    xml += "    </served>\n"
    xml += "</call>\n"

    # SMS
    xml += "<sms>\n"
    xml += "    <received>"
    xml += mf_instance.num_received_sms()
    xml += "    </received>\n"
    xml += "    <served>"
    xml += mf_instance.num_served_sms()
    xml += "    </served>\n"
    xml += "</sms>\n"

    # Data
    xml += "<data>\n"
    xml += "    <received>"
    xml += mf_instance.num_received_data()
    xml += "    </received>\n"
    xml += "    <served>"
    xml += mf_instance.num_served_data()
    xml += "    </served>\n"
    xml += "</data>"
    return Response(xml, mimetype='text/xml')

################### Responses #####################
def pass_connection(connection_type):
    return mf_instance(connection_type)

def generate_503():
	return render_template('503view.html'), 503

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


################### Twilio #####################
callers = {
    "+16507769918": "Gavin Chan",
    "+14158675310": "Boots",
    "+14158675311": "Virgil",
    "+12566671171": "MOSC",
}
 
@app.route("/", methods=['GET', 'POST'])
def hello_monkey():
    # Get the caller's phone number from the incoming Twilio request
    from_number = request.values.get('From', None)
    resp = twilio.twiml.Response()
 
    # if the caller is someone we know:
    if from_number in callers:
        # Greet the caller by name
        resp.say("Hello " + callers[from_number])
    else:
        resp.say("Hello Monkey")
 
    return str(resp)




if __name__ == '__main__':
    app.run()
