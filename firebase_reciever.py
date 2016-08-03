#!/usr/bin/python3

path = '/home/pi/IR-Remote-hacking/'

import time
from firebase import firebase
import json
import os

#import IR messages
from IR_messages import messages

myDataBase = 'https://mydatabase-f7de1.firebaseio.com/'

#start fire base
firebase = firebase.FirebaseApplication(myDataBase,None)


try:
    #get specific snapshot: IR
    result = firebase.get('IR','IR_ctr')
except:
    print('Firebase error')

#check if data was retrieved
if result:
    data = json.loads(result)
    print(data)

    #check if there is a command in the data
    if 'COMMAND' in data:
    
        #check if it's a valid command
        if isinstance(data['COMMAND'], str): #check if its a string
            print('Command found: ' + data['COMMAND'])
            
            if data['COMMAND'] in messages:
                print('Translates to IR message:')
                print(messages[data['COMMAND']])

                #send command to transmitter
                os.system(path + 'AC_control.py ' + data['COMMAND'])

                #update most recent command sent
                #this gives feedback that message was recieved
                firebase.put('IR','past_IR_ctr',result)
        
            else:
                print('Not a valid command')
                
        else:
            print('Error: non string input')
            
        #delete command
        firebase.delete('IR','IR_ctr')

    else:
        print('No command found')

else:
    print('No data found')


