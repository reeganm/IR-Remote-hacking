#!/usr/bin/python3

from firebase import firebase
import json
import os
import sys
import time
import json
import serial

myDataBase = 'https://mydatabase-f7de1.firebaseio.com/'

#import messages
from IR_messages import messages

#check number of input arguments
if len(sys.argv) == 2:
   #check valid input argument
   if sys.argv[1] in messages:
       print('Transmitting Command: ' + sys.argv[1])
   else:
       print('Invalid Command')
       print('Valid Commands Are:')
       print(list(messages.keys()))
       #exit program with non zero
       
else:
   print('Wrong Number of Input Arguments')
   print('Script Usage:')
   print('./AC_control.py <command>')
   #exit program
   
firebase = firebase.FirebaseApplication(myDataBase,None)

data = json.dumps( {'COMMAND':sys.argv[1]} )

result = firebase.put('IR','IR_ctr',data)
print('Success')
