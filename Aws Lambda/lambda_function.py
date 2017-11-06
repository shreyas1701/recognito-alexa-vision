import numpy as np
import urllib
import cv2
import boto3
import logging
import json
##############################
# Builders
##############################


def build_PlainSpeech(body):
    speech = {}
    speech['type'] = 'PlainText'
    speech['text'] = body
    return speech


def build_response(message, session_attributes={}):
    response = {}
    response['version'] = '1.0'
    response['sessionAttributes'] = session_attributes
    response['response'] = message
    return response


def build_SimpleCard(title, body):
    card = {}
    card['type'] = 'Simple'
    card['title'] = title
    card['content'] = body
    return card


##############################
# Responses
##############################


def conversation(title, body, session_attributes):
    speechlet = {}
    speechlet['outputSpeech'] = build_PlainSpeech(body)
    speechlet['card'] = build_SimpleCard(title, body)
    speechlet['shouldEndSession'] = False
    return build_response(speechlet, session_attributes=session_attributes)


def statement(title, body):
    speechlet = {}
    speechlet['outputSpeech'] = build_PlainSpeech(body)
    speechlet['card'] = build_SimpleCard(title, body)
    speechlet['shouldEndSession'] = True
    return build_response(speechlet)


def continue_dialog():
    message = {}
    message['shouldEndSession'] = False
    message['directives'] = [{'type': 'Dialog.Delegate'}]
    return build_response(message)


##############################
# Custom Intents
##############################

def recognize_intent(event, context): 
    #Call Rasberry Pi for image Capture
    resp = urllib.urlopen('https://cf51fc88.ngrok.io/capture')
    #image = Image.open(BytesIO(response.read()))
    #image = np.asarray(bytearray(response.read()), dtype="uint8")
    #image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    key_id = 'ACCESS_KEY'
    secret_key = 'SECRETE_KEY'
    client = boto3.client('rekognition', region_name='us-east-1', aws_access_key_id=key_id, aws_secret_access_key=secret_key)
    res = client.detect_labels(Image={'Bytes': resp.read()})
    obj = []
    for i in res['Labels']:
        obj.append(i)
    for i in range(len(obj)):
        obj[i]['Confidence'] = int(obj[i]['Confidence'])
    max_val = obj[0]
    recongnized_objects = []
    for i in range(len(obj)):
        if(max_val['Confidence'] == obj[i]['Confidence']):
            recongnized_objects.append(obj[i])
    name = ""
    for i in range(len(recongnized_objects)):
        name = name + " "+recongnized_objects[i]['Name'] + ", "
    result = "The object could be "
    result = result + name
    return statement("", result)


##############################
# Required Intents
##############################


def cancel_intent():
    return statement("CancelIntent", "You want to cancel")


def help_intent():
    return statement("CancelIntent", "You want help")


def stop_intent():
    return statement("StopIntent", "You want to stop")


##############################
# On Launch
##############################


def on_launch(event, context):
    return statement("title", "body")


##############################
# Routing
##############################


def intent_router(event, context):
    intent = event['request']['intent']['name']

    # Custom Intents

    if intent == "RecognizeIntent":
        return recognize_intent(event, context)

    # Required Intents

    if intent == "AMAZON.CancelIntent":
        return cancel_intent()

    if intent == "AMAZON.HelpIntent":
        return help_intent()

    if intent == "AMAZON.StopIntent":
        return stop_intent()


##############################
# Program Entry
##############################


def lambda_handler(event, context):
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event, context)

    elif event['request']['type'] == "IntentRequest":
        return intent_router(event, context)
