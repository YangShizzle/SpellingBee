"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function
from random import random


# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def getWord():
    words = ['CAT','DOG','EVIL','SNIDE','CREED','OCTOPUS','CRAWL','SMILING','FEVER','EARTH','EVENING','COPYING','USEFUL','QUARTER','MAMMAL','TRAIN','DISCOVER','VACATION','SURPRISE','PROBABLY','EXPRESS','ACTOR','STOMACH','TERRIBLE','JOURNEY','REQUIREMENT','AEROPLANE','MECHANIC','VEGETABLE','PERFORMANCE','APPEARANCE','RECTANGULAR','OMINOUS','VERTIGO','OCCURRED','PROCRASTINATE','INFLUENCE','PHRASE','CELERY','STATISTICS','HAVOC','VACUU','AUTHORITY','PATIENT','SNOBBERY','CAPABLY','VENOM','EMBARGO','HONORARY','ABSTAIN','PERMEATE','UNDULY','PRECOCIOUS']
    range = len(words)-1
    randNum = int(range*random())
    word = words[randNum]
    return word
    
def get_welcome_response():

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to Spelling Bee. Do you want to begin?" 
    reprompt_text = "Do you want to begin the spelling bee? "
    should_end_session = False
    
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for playing to the spelling bee"
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

start = False

def begun():
    global start
    start = True
    
def reset():
    global start
    start = False

def beginSession(intent, session):

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False
    global testWord
    testWord = getWord()
    
    if start == False:
        beginInput = intent['slots']['beginInput']['value']
        if beginInput == "maybe later" or beginInput == "no":
            speech_output = "alright maybe next time"
            reprompt_text = None
            should_end_session = True
        elif beginInput == "yes" or beginInput == "let's go":
            speech_output = "alright, how do you spell " + testWord + "? Begin your answer with: The answer is."
            reprompt_text = "how do you spell" + testWord + "?"
            begun()
        else:
            speech_output = "I'm sorry, did you want to start?"
            reprompt_text = "I'm sorry, did you want to start?"
    else:
        speech_output = "The word you need to spell is " + testWord
        reprompt_text = None
        
    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))


def spellingBee(intent, session):
    session_attributes = {}
    reprompt_text = None
    card_title = intent['name']
    global testWord
    
    if start == True:
        if intent['slots']['spellingInput']['value'] == testWord:
            speech_output = "Congratulations! you spelled " + testWord + " correctly!"
            should_end_session = True
        else:
            speech_output = "Try again"
            should_end_session = False
    else:
        speech_output = "You haven't started the game yet, say let's go if you want to begin"
        should_end_session = False
        
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


# --------------- Events ------------------

def on_launch(launch_request, session):
    reset()
    return get_welcome_response()


def on_intent(intent_request, session):

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    if intent_name == "getBeginIntent":
        return beginSession(intent, session)
    elif intent_name == "getSpellingInput":
        return spellingBee(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


# --------------- Main handler ------------------
def lambda_handler(event, context):

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])


