var twilio = require('twilio');
var express = require('express');
var router = express.Router();
var http = require('http');
var bodyParser = require('body-parser');
var mongoose = require('mongoose');
var parseString = require('xml2js').parseString;
var fs = require('fs');
var request = require('request');


//twilio client
var accountSid = 'AC29bc1c6ef10880d4ce43183250848606';
var twilioAuthToken = "d92f0aa0dbfd150994b0285f928f430b";
var twilioClient = twilio(accountSid, twilioAuthToken);


/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Express' });
});

router.post('/', function (req, res) {
	for (var i = 0; i < contacts.length; i++) {
        twilioClient.sms.messages.create({
          body: url.data.url,
          // body: "hELLO!!@#!!!@# ^___^v",
          to: contacts[i],
          from: "4803767068"
        }, function(error, message) {
            if (!error) {
                console.log('Success! The SID for this SMS message is:');
                console.log(message.sid);
                console.log('Message sent on:');
                console.log(message.dateCreated);
            } else {
                console.log('Oops! There was an error.');
                console.log("error", error);
            }
        });
      }
	}

module.exports = router;
