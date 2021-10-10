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
#from twilio.rest import TwilioRestClient
import json #Json load the data from the phonecountry code 
import serial 
from gpiozero import LED 
translator = Translator(service_urls=['translate.google.com','translate.google.com',])
lang = 'th'
lang2 = 'en'
sox_effects = ('speed',"1.14")
Activate_word = ["translation","Translation","mode","translate","Translate"] #Activate translate mode concern word need more vocabulary 
Direction_translate = ["to","in to"]
Call_active_com = ["Call","to","number"]
Code_active_country = ["to","destination","destinations","Destination"]
Cancel_Call = ["Cancel","call"]
Receive_call_mode = ['Receive', 'phone', 'calls']
mem_country_destination = []
Current_mode = []
Remover_country = []
vibrator = LED(21) #vibrator function 
reset = LED(6) #reset function
led = LED(26) #LED light 
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
file = open("Extracted_code_country.json",'r') #Read the file 
codedata = json.load(file) #code data for load json country code and name 
# Twilio phone number goes here. Grab one at https://twilio.com/try-twilio
# and use the E.164 format, for example: "+12025551234"
#TWILIO_PHONE_NUMBER = "+12055743990" #Trial number for phone call 

# list of one or more phone numbers to dial, in "+19732644210" format
DIAL_NUMBERS = []

# URL location of TwiML instructions for how to handle the phone call
#TWIML_INSTRUCTIONS_URL = \
#  "http://static.fullstackpython.com/phone-calls-python.xml"
#Joining number 
Joiningnumber = []
# replace the placeholder values with your Account SID and Auth Token
# found on the Twilio Console: https://www.twilio.com/console
#client = TwilioRestClient("AC2700afd0f2277138948384d03c83df73", "243684daa3aa1f20c234f472309d0d9f")
Current_country_code = [] #Store the current country code 
try:
  sim800l = serial.Serial('/dev/ttyS0',115200)
  print("GPRS module found................[OK]")
  sim800l.write('AT\r'.encode('UTF-8')) #
  Getresponse = sim800l.readline().decode('UTF-8')
  print("GPRS command.........",Getresponse)
  Getresponse_status = sim800l.readline().decode('UTF-8')
  print("GPRS status.........",Getresponse_status)
  speech = Speech("GPRS status........."+str(Getresponse_status)+"Smart glasses is now working 100%",'en')
  speech.play(sox_effects)
except:
   print("Please check the UART connection between the GPRS module")
'''   
class SIM800L:
          def __init__(self,status,phonenumber,Country_code,reset):
                #Phone initial function 
                self.status = status
                self.phonenumber = phonenumber
                self.reset = reset
                self.Country_code = Country_code 
          def __str__(self):
                return f"Status:{self.status} Phonenumber:{self.phonenumber} Country_code:{self.Country_code} reset:{self.reset}"
          def Callmode(self,status,phonenumber): #Getting the phonenumber
                if status == "Call_mode":
                     dials = "ATD"+phonenumber+";\n"
                     sim800l.write(dials.encode('UTF-8')) #Getting the sim800l call 
                     get_response = sim800l.readline().decode('UTF-8')       
                     return get_response 
                if status == "Receive_call_mode":
                     sim800l.write("ATA\n".encode('UTF-8'))
                     get_response = sim800l.readline().decode('UTF-8')                      
                     return get_response
                if status == "Hangup_mode": 
                     sim800l.write("ATH\n".encode('UTF-8'))
                     get_response = sim800l.readline().decode('UTF-8') 
                     return get_response
                
          def Check_battery(self): #getting the batteryvalue
                sim800l.write("AT+CBC\n".encode('UTF-8')) 
                get_response = sim800l.read().decode('UTF-8')
                return get_response         
          def Vibrator(self,state):
             if state == "RING":
                 for vib in range(0,1):
                      if vib == 0:
                            vibrator.off()
                      time.sleep(0.5)
                      if vib == 1:
                            vibrator.on()
                      time.sleep(0.5)
             if state !="RING":
                     vibrator.off()   
'''                     
 
#Data of preposition word in the list of the dictionary file 

Detected_language = ['th','en'] #Detected language   
Inner_trans = 'en'      
def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3 
def Hangup_call(listwordinput,executelist):
        word_intersection = intersection(listwordinput,executelist)
        print("Getting the intersection word",word_intersection) 
        superposition = intersection(word_intersection,executelist)
        print("Word superpositioning",superposition)
        percent=difflib.SequenceMatcher(None,superposition,executelist)
        print(percent.ratio()*100) 
        if percent.ratio()*100 > 33:
                   for Dat in range(0,len(executelist)-1):
                          if Cancel_Call[Dat] in listwordinput:
                                 print("Hangup mode activated..........")                                                                                
                                 sim800l.write("ATH\n".encode('UTF-8')) 
                                 get_responsezero = sim800l.readline().decode('UTF-8')
                                 print(get_responsezero)
                                 speech = Speech("Hangup mode activated",'en')
                                 speech.play(sox_effects)
                                 reset.on()
                                 time.sleep(0.5)
                                 reset.off()        
def Receive_call(listwordinput,executelist):
        #get_responsezero = sim800l.readline().decode('UTF-8')
        #print(get_responsezero)
        get_response = sim800l.readline().decode('UTF-8')
        print(get_response)    
        word_intersection = intersection(listwordinput,executelist)
        print("Getting the intersection word",word_intersection) 
        superposition = intersection(word_intersection,executelist)
        print("Word superpositioning",superposition)
        percent=difflib.SequenceMatcher(None,superposition,executelist)
        print(percent.ratio()*100) 
        if percent.ratio()*100 >= 33:
                   get_responsezero = sim800l.readline().decode('UTF-8')
                   print(get_responsezero)
                   get_response = sim800l.readline().decode('UTF-8')
                   print(get_response)
                   if get_response == "RING":
                           vibrator.on()
                   for rc in range(0,len(executelist)-1):
                          if Receive_call_mode[rc] in listwordinput:
                                 print("Receive call activated..........")
                                 sim800l.write("ATA\n".encode('UTF-8'))
                                 vibrator.off() 
                                 speech = Speech("Receive call activated",'en')
                                 speech.play(sox_effects)
                                 
                                
                                 


 #Function call back of the speech recognition command
def Call_command(splitword,Call_active_com):
        word_intersection = intersection(splitword,Call_active_com)
        print("Getting the intersection word",word_intersection) 
        superposition = intersection(word_intersection,Call_active_com)
        print("Word superpositioning",superposition)
        percent=difflib.SequenceMatcher(None,superposition,Call_active_com)
        print(percent.ratio()*100) 
        if percent.ratio()*100 >= 66:
           if Current_mode !=[]:
                       Current_mode.clear()
           if Current_mode  == []: 
                       Current_mode.append("Call mode") #add the current function to activate 
           for call in range(0,len(Call_active_com)-1):
              if Call_active_com[call] in splitword:
                  print("Detect Phone call mode")
                  print(splitword)
                  if Joiningnumber !=[]:
                           Joiningnumber.clear()
                  if Joiningnumber ==[]:
                          try:
                              for i in range(0,len(Call_active_com)):
                             
                                    splitword.remove(word_intersection[i])
                          except:
                               print("System command flaw detected")
                          print("Phone number extracted:",splitword)
                          #Joiningnumber.append(splitword)
                  frontnumber = splitword[0]
                  numlist = list(frontnumber)
                  try:
                     numlist.remove('0')
                     print(numlist,numlist[0]+numlist[1])
                     front_pt = numlist[0]+numlist[1]
                     splitword.remove(splitword[0])
                     print(numlist,front_pt,splitword)
                     Insertnumlist =  splitword.insert(0,front_pt)
                     print(' '.join(splitword))
                     Phone_rearanged = ' '.join(splitword)
                     DIAL_NUMBERS.clear()
                     if  DIAL_NUMBERS == []:
                           DIAL_NUMBERS.append(Phone_rearanged)
                           print(DIAL_NUMBERS)
                           #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                           #Extract destination code 
                           #Extract_and_Execute(DIAL_NUMBERS,code_active_country)      
                           for country in range(0,len(DIAL_NUMBERS[0].split(" "))-1):
                                   if DIAL_NUMBERS[0].split(" ")[country] in list(codedata):
                                                         print(DIAL_NUMBERS[0].split(" ")[country])
                                                         extracted_country = DIAL_NUMBERS[0].split(" ")[country]
                                                         get_code = codedata.get(extracted_country)
                                                         print("Country:"+"\t"+extracted_country+"code:",get_code)
                                                         print(DIAL_NUMBERS[0].split(" "))
                                                         if mem_country_destination != []:
                                                                    mem_country_destination.clear()
                                                         if mem_country_destination == []:
                                                                 for re in range(0,len(DIAL_NUMBERS[0].split(" "))):
                                                                              mem_country_destination.append(str(DIAL_NUMBERS[0].split(" ")[re]))
                                                         print("From memory:",mem_country_destination)
                                                         #Remover_country.append(str(extracted_country))
                                                         #Remover_country.append(str(Code_active_country[0]))
                                                         #for rem in range(0,len(Remover_country)-1):
                                                         #The problem is code active country list need to find new solution
                                                         try:
                                                             mem_country_destination.remove(str(extracted_country))
                                                             for rrev in range(0,len(Code_active_country)-1):
                                                                    if Code_active_country[rrev] in mem_country_destination:
                                                                              mem_country_destination.remove(str(Code_active_country[rrev])) 
                                                           
                                                         except:
                                                              print("Removing the wrong sorting order")
                                                              #mem_country_destination.remove(str(Code_active_country[0]))
                                                              #mem_country_destination.remove(str(extracted_country)) 
                                                              #mem_country_destination.remove(str(Code_active_country[0]))     
                                                         print(mem_country_destination)
                                                         Phonenumber = ' '.join(mem_country_destination)
                                                         Phonedails = get_code+' '.join(mem_country_destination)      
                                                         print("Complete phonenumber",Phonedails)
                                                         if Current_mode[0] == "Call mode":
                                                                speech = Speech(str(Phonedails)+"destination"+str(extracted_country),'en')    
                                                                speech.play(sox_effects)
                                                         if Current_mode[0] != "Call mode":
                                                                     print("You are now in"+"\t"+str(Current_mode[0])) 
                                                         dials_num = "ATD"+str(Phonedails)+";\n" 
                                                         sim800l.write(dials_num.encode('UTF-8'))
                                                          
                           #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>                        
                  except:
                      print("Processing number error") 
                      speech = Speech('Processing number error','en')
                      speech.play(sox_effects)                     
def callback(recognizer, audio):
    # received audio data, now we'll recognize it using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        print("Smart glasses Speech Recognition thinks you said " + recognizer.recognize_google(audio,language = 'th'))
           
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
        if percent.ratio()*100 >= 33:
                  print("Detect translation mode")
                  if Current_mode !=[]:
                       Current_mode.clear()
                  if Current_mode  == []:
                       Current_mode.append("Translate mode") #add the current function to activate  
                  print(values_languages)
                  Detected_language.clear() 
                  for lang in range(0,len(splitword)):
                           if splitword[lang] in values_languages:
                                     Detected_language.append(key_languages[values_languages.index(splitword[lang])]) # Detected language translation on each language detected in the array 
                  print(Detected_language)
        if Current_mode !=[]: 
             if Current_mode[0] == "Translate mode":
                           speech.play(sox_effects)
             if Current_mode[0] != "Translate mode":
                           print("You now in"+"\t"+str(Current_mode[0]))          
        #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>..
         #Phone call function 
        Call_command(splitword,Call_active_com) #Call mode function 
        Hangup_call(splitword,Cancel_Call)
        Receive_call(splitword,Receive_call_mode) 
       
        
    except sr.UnknownValueError:
        print("Smart glasses Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Smart glasses Speech Recognition service; {0}".format(e))


r = sr.Recognizer()
m = sr.Microphone()
with m as source:
    r.adjust_for_ambient_noise(source) 
stop_listening = r.listen_in_background(m, callback)
for i in itertools.count():time.sleep(0.2)  
