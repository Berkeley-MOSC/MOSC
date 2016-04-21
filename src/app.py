import requests
import filter as mf
from flask import Flask, render_template, abort, request, redirect
import twilio.twiml
from twilio.rest import TwilioRestClient

app = Flask(__name__)
#TWILIO CREDENTIALS###

# Find these values at https://twilio.com/user/account
# TODO: Change these credentials since they're now in the repo history
account_sid = "AC5d82215d4d388331b5076dde9bb50ef9"
auth_token = "4388759bc6c4455bcd983069cbb88c49"
client = TwilioRestClient(account_sid, auth_token)

###############GLOBAL VARS###########################
# set up buffer for filtering algorithm
mosc_buff = mf.mosc_buffer()

twil_num = "+12566671171"
twil_msg = "This is the data being sent."
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
        return reject_ecall("+12566671171")


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
# returns true or false whether we can connect
def pass_connection(connection_type):
    if type(connection_type) is not str:
        raise ValueError("conneciton_type must be of type str")
    packet = Packet(connection_type)
    success = mosc_buff.add(packet)
    if success:
        return True
    else:
        return False
    #     # call apporporaite send_ funciton
    #     if connection_type == "data":
    #         # send_call(twil_num, twil_msg)
    #         # ASK NICK
    #     if connection_type == "call":
    #         send_call(twil_num, twil_msg)
    #     if connection_type == "emergency":
    #         send_ecall(twil_num)
    #     if connection_type == "sms":
    #         send_sms(twil_num, twil_msg)
    # else:
    #     # call appropriate reject_ function
    #     if connection_type == "data":
    #         #ASK NICK
    #     if connection_type == "call":
    #         reject_call()
    #     if connection_type == "emergency":
    #         reject_ecall()
    #     if connection_type == "sms":
    #         reject_sms()
    pass

def generate_503():
    resp = twilio.twiml.Response()
    return render_template('503view.html'), 503

def send_sms(number, message):
    # resp = twilio.twiml.Response()
    message = client.messages.create(to=number, from_=twil_num,
                                     body="Hello there, your message been successfully sent!")

def send_call(number, message):
    resp = twilio.twiml.Response()
    call = client.calls.create(to=number,  # Any phone number
                           from_=twil_num, # Must be a valid Twilio number
                           url="") # SET UP URL FOR VOICE RESPONSE

def send_ecall(number):
    resp = twilio.twiml.Response()
    resp.say("This call represents an emergency call.  If you are experiencing\
        a real emergency, please hang up now and dial 9-1-1.")

def reject_sms():
    resp = twilio.twiml.Response()
    resp.say("Sorry your SMS cannot be sent at this time. ")

def reject_call():
    resp = twilio.twiml.Response()
    resp.say("Sorry your call cannot be completedat this time. ")

def reject_ecall():
    resp = twilio.twiml.Response()
    resp.say("Sorry your emergency call cannot be completed at this time. ")

################### Twilio #####################
callers = {
    "+16507769918": "Gavin Chan",
    "+14158675310": "Boots",
    "+14158675311": "Virgil",
    "+12566671171": "MOSC",
}

@app.route("/", methods=['GET', 'POST'])
def root_page():
    html = "Hello world!"
    return Response(html, mimetype='text/plaintext')
    # Get the caller's phone number from the incoming Twilio request
    from_number = request.values.get('From', None)
    resp = twilio.twiml.Response()
    resp.say("Hi Kelvin")
    # return str(resp)

    # if the caller is someone we know:
    # if from_number in callers:
    #     # Greet the caller by name
    #     resp.say("Hello " + callers[from_number])
    # else:
    #     resp.say("Hello Monkey")

    # return str(resp)

if __name__ == '__main__':
    app.debug = True
    app.run()
