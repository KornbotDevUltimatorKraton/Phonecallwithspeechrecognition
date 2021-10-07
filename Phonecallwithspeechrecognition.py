#!/usr/bin/env python3

# NOTE: this example requires PyAudio because it uses the Microphone class 
import time
import math 
import speech_recognition as sr
import itertools 
import numpy as np 
import serial  #Serial communication talking to the GPRS module 
from google_speech import* 
from googletrans import Translator # Google translate  
import os 
import sys
import  wordninja
import difflib #Finding the similarlity of the matching sequence 
from twilio.rest import TwilioRestClient

translator = Translator(service_urls=['translate.google.com','translate.google.com',])
lang = 'th'
lang2 = 'en'
sox_effects = ('speed',"1.14")
Activate_word = ["translation","Translation","mode","translate","Translate"] #Activate translate mode concern word need more vocabulary 
Direction_translate = ["to","in to"]
Call_active_com = ["Call","to","number"]
#List language of translation function 
Languages = {
    'af': 'Afrikaans',
    'sq': 'Albanian',
    'am': 'Amharic',
    'ar': 'Arabic',
    'hy': 'Armenian',
    'az': 'Azerbaijani',
    'eu': 'Aasque',
    'be': 'Belarusian',
    'bn': 'Bengali',
    'bs': 'Bosnian',
    'bg': 'Bulgarian',
    'ca': 'Batalan',
    'ceb': 'Bebuano',
    'ny': 'Chichewa',
    'zh-cn': 'Chinese',
    'zh-tw': 'Chinese (traditional)',
    'co': 'Corsican',
    'hr': 'Croatian',
    'cs': 'Czech',
    'da': 'Danish',
    'nl': 'Dutch',
    'en': 'English',
    'eo': 'Esperanto',
    'et': 'Estonian',
    'tl': 'Filipino',
    'fi': 'Finnish',
    'fr': 'French',
    'fy': 'Frisian',
    'gl': 'Galician',
    'ka': 'Georgian',
    'de': 'German',
    'el': 'Greek',
    'gu': 'Gujarati',
    'ht': 'Haitian creole',
    'ha': 'Hausa',
    'haw': 'Hawaiian',
    'iw': 'Hebrew',
    'he': 'Hebrew',
    'hi': 'Hindi',
    'hmn': 'Hmong',
    'hu': 'Hungarian',
    'is': 'Icelandic',
    'ig': 'Igbo',
    'id': 'Indonesian',
    'ga': 'Irish',
    'it': 'Italian',
    'ja': 'Japanese',
    'jw': 'Javanese',
    'kn': 'Kannada',

    'kk': 'Kazakh',
    'km': 'Khmer',
    'ko': 'Korean',
    'ku': 'Kurdish (kurmanji)',
    'ky': 'Kyrgyz',
    'lo': 'Lao',
    'la': 'Latin',
    'lv': 'Latvian',
    'lt': 'Lithuanian',
    'lb': 'Luxembourgish',
    'mk': 'Macedonian',
    'mg': 'Malagasy',
    'ms': 'Malay',
    'ml': 'Malayalam',
    'mt': 'Maltese',
    'mi': 'Maori',
    'mr': 'Marathi',
    'mn': 'Mongolian',
    'my': 'Myanmar (burmese)',
    'ne': 'Nepali',
    'no': 'Norwegian',
    'or': 'Odia',
    'ps': 'Pashto',
    'fa': 'Persian',
    'pl': 'Polish',
    'pt': 'Portuguese',
    'pa': 'Punjabi',
    'ro': 'Romanian',
    'ru': 'Russian',
    'sm': 'Samoan',
    'gd': 'Scots gaelic',
    'sr': 'Serbian',
    'st': 'Sesotho',
    'sn': 'Shona',
    'sd': 'Sindhi',
    'si': 'Sinhala',
    'sk': 'Slovak',
    'sl': 'Slovenian',
    'so': 'Somali',
    'es': 'Spanish',
    'su': 'Sundanese',
    'sw': 'Swahili',
    'sv': 'Swedish',
    'tg': 'Tajik',
    'ta': 'Tamil',
    'te': 'Telugu',
    'th': 'Thai',
    'tr': 'Turkish',
    'uk': 'Ukrainian',
    'ur': 'Urdu',
    'ug': 'Uyghur',
    'uz': 'Uzbek',
    'vi': 'Vietnamese',
    'cy': 'Welsh',
    'xh': 'Xhosa',
    'yi': 'Yiddish',
    'yo': 'Yoruba',
    'zu': 'Zulu'}
# Twilio phone number goes here. Grab one at https://twilio.com/try-twilio
# and use the E.164 format, for example: "+12025551234"
TWILIO_PHONE_NUMBER = "+12055743990" #Trial number for phone call 

# list of one or more phone numbers to dial, in "+19732644210" format
DIAL_NUMBERS = []

# URL location of TwiML instructions for how to handle the phone call
TWIML_INSTRUCTIONS_URL = \
  "http://static.fullstackpython.com/phone-calls-python.xml"
#Joining number 
Joiningnumber = []
# replace the placeholder values with your Account SID and Auth Token
# found on the Twilio Console: https://www.twilio.com/console
client = TwilioRestClient("AC2700afd0f2277138948384d03c83df73", "243684daa3aa1f20c234f472309d0d9f")


def dial_numbers(numbers_list):
    """Dials one or more phone numbers from a Twilio phone number."""
    for number in numbers_list:
        print("Dialing " + number)
        # set the method to "GET" from default POST because Amazon S3 only
        # serves GET requests on files. Typically POST would be used for apps
        client.calls.create(to=number, from_=TWILIO_PHONE_NUMBER,
                            url=TWIML_INSTRUCTIONS_URL, method="GET")

def gprs_phone_module(status,sleepmode,phonenumber):
          print("Calling mode activated.....")

#Data of preposition word in the list of the dictionary file 

Detected_language = ['th','en'] #Detected language   
Inner_trans = 'en'  
def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3 
 #Function call back of the speech recognition command
def Call_command(splitword,Call_active_com):
        word_intersection = intersection(splitword,Call_active_com)
        print("Getting the intersection word",word_intersection) 
        superposition = intersection(word_intersection,Call_active_com)
        print("Word superpositioning",superposition)
        percent=difflib.SequenceMatcher(None,superposition,Call_active_com)
        print(percent.ratio()*100) 
        if percent.ratio()*100 >= 33:
           for call in range(0,len(Call_active_com)-1):
              if Call_active_com[call] in splitword:
                  print("Detect Phone call mode")
                  print(splitword)
                  if Joiningnumber !=[]:
                           Joiningnumber.clear()
                  if Joiningnumber ==[]:
                          try:
                              for i in range(0,len(Call_active_com)):
                             
                                    splitword.remove(Call_active_com[i])
                          except:
                               print("System command flaw detected")
                          print("Phone number extracted:",splitword)
                          #Joiningnumber.append(splitword)
                  frontnumber = splitword[0]
                  numlist = list(frontnumber)
                  numlist.remove('0')
                  print(numlist,numlist[0]+numlist[1])
                  front_pt = numlist[0]+numlist[1]
                  splitword.remove(splitword[0])
                  print(numlist,front_pt,splitword)
                  Insertnumlist =  splitword.insert(0,front_pt)
                  print(' '.join(splitword))
                  Phone_rearanged = "+66"+' '.join(splitword)
                  DIAL_NUMBERS.clear()
                  if  DIAL_NUMBERS == []:
                           DIAL_NUMBERS.append(Phone_rearanged+",")
                  
                  dial_numbers(DIAL_NUMBERS)       
def callback(recognizer, audio):
    # received audio data, now we'll recognize it using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        print("Catbot Speech Recognition thinks you said " + recognizer.recognize_google(audio,language = 'th'))
        
        '''
        translation = translator.translate(recognizer.recognize_google(audio,language = 'th'))
        print(translation)
        speech = Speech(translation,lang)
        speech.play(sox_effects)
        '''
        if len(Detected_language) >=2:
           translations = translator.translate(str(recognizer.recognize_google(audio,language =str(Detected_language[0]))),dest =str(Detected_language[len(Detected_language)-1]))
           translations2 = translator.translate(str(recognizer.recognize_google(audio,language =str(Detected_language[0]))),dest = Inner_trans)
        #Setting default of the language detected from the function of the language detection activate from the unknown non destination language 
        if len(Detected_language) <2:
            translations = translator.translate(str(recognizer.recognize_google(audio,language =str(Detected_language[0]))),dest =str(Detected_language[0]))
            translations2 = translator.translate(str(recognizer.recognize_google(audio,language =str(Detected_language[0]))),dest = Inner_trans)
        #for translation in translations:
        print(translations.text) # Print out translation
        if len(Detected_language) >=2: 
            speech = Speech(translations.text,Detected_language[1])
        if len(Detected_language) <2: 
            speech = Speech(translations.text,Detected_language[0]) 
            Detected_language.clear()
            Detected_language.append('en')
            speech = Speech("Not detected destination language now using"+"\t"+str(Languages.get(Detected_language[0])+"\t"+"as default"),'en')


        splitword = wordninja.split(str(translations2.text))
        print(splitword)
        word_intersection = intersection(splitword,Activate_word)
        print("Getting the intersection word",word_intersection) 
        superposition = intersection(word_intersection,Activate_word)
        print("Word superpositioning",superposition)
        percent=difflib.SequenceMatcher(None,superposition,Activate_word)
        print(percent.ratio()*100)
        values_languages = list(Languages.values())
        key_languages = list(Languages.keys()) 
        #print(values_languages)
        if percent.ratio()*100 >= 33:
                  print("Detect translation mode")
                  print(values_languages)
                  Detected_language.clear() 
                  for lang in range(0,len(splitword)):
                           if splitword[lang] in values_languages:
                                     Detected_language.append(key_languages[values_languages.index(splitword[lang])]) # Detected language translation on each language detected in the array 
                  print(Detected_language)
        #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>..
         #Phone call function 
        Call_command(splitword,Call_active_com) #Call mode function  
        speech.play(sox_effects)

    except sr.UnknownValueError:
        print("Smart glasses Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Smart glasses Speech Recognition service; {0}".format(e))


r = sr.Recognizer()
m = sr.Microphone()
with m as source:
    r.adjust_for_ambient_noise(source)  # we only need to calibrate once, before we start listening


# start listening in the background (note that we don't have to do this inside a `with` statement)
stop_listening = r.listen_in_background(m, callback)
# `stop_listening` is now a function that, when called, stops background listening

# do some unrelated computations for 5 seconds
for i in itertools.count():time.sleep(0.2)  # we're still listening even though the main thread is doing other things

# calling this function requests that the background listener stop listening
#stop_listening(wait_for_stop=False)

# do some more unrelated things
#whil True:time.sleep(0.1) # we're not listening anymore, even though the background thread might still be running for a second or two while cleaning up and stopping
#raise SystemExit
