#!/usr/bin/env python3
#
# ---------------------------------------
# Version 2212.19.1
# Copyright Gattancha Computer Services
# https://github.com/gcsprojects
# ---------------------------------------

## ---------------------------------------------------------------------------------------
## Pre-Requisites
## 
## 1. Python clicksend client API - https://pypi.org/project/clicksend-client/#files
## 2. ClickSend Account - https://www.clicksend.com/
## 3. Change 'api_username' and 'api_key' as appropriate
##
## ---------------------------------------------------------------------------------------
##
## This app is designed for use in the UK
## To use elsewhere, try changing the 'intl_prefix'
## Some countries may have other restrictions so refer to Clicksend
## for more details. 
## ---------------------------------------------------------------------------------------

# Import relevant classes and modules
from __future__ import print_function
import time
import clicksend_client
from clicksend_client import SmsMessage
from clicksend_client.rest import ApiException
from pprint import pprint

# Set the API Username and Passsword/Key
# These can be obtained from your ClickSend Dashboard
api_username = 'ENTER-USERNAME-HERE'
api_key = 'ENTER-API-KEY-OR-PASSWORD-HERE'

# It is not normally necessary to alter thse value
max_sms_length = 160	# Set the max length of an SMS message (Usually 160 Characters)
intl_prefix = "+44"		# Sets the International Prefix (eg +44 for the UK) 

# --------------------------- #
# DO NOT EDIT BELOW THIS LINE #
# --------------------------- #

# Function to test if the phone number if formatted correctly
def check_number(phone_number):
	print("Checking Number Format...")
	if phone_number.isdigit() == False:
		print("[!]\tInvalid Phone Number. It can only contain numbers")
		exit(1)
	if phone_number[0] == '0':
		phone_number = phone_number[1:]
	if intl_prefix not in phone_number:
		phone_number = intl_prefix + phone_number
	return phone_number

# Function to check the length of the message.
def check_message_length(message):
	if (len(message) > max_sms_length):
		print("\n")
		print ("[!]\tYour message is longer than " + str(max_sms_length) + " characters and cannot be sent.")
		exit(1)
	else:
		return message

# Function to check the foramt of the Senders Name
# It must be a maximum of 11 AlphaNumeric characters and have no spaces
def check_sender_id(sender_id):
	if ' ' in sender_id:
		sender_id = sender_id.replace(' ','')
	if (len(sender_id) > 11):
		print("\n")
		print("[!]\tSender ID too long")
		exit(1)
	if sender_id.isalpha() == False:
		print("\n")
		print("[!]\tSender ID contains Illegal Characters. Only AlphaNumeric allowed")
		exit(1)
	else:
		return sender_id

#Get the message details from the user
sms_message_id = input("Enter Sender ID: ")
sms_phone_number = input("Enter Recipient's Number: ")
sms_message_body = input("Enter your SMS Message: ")

# Setup the ClickSend API
configuration = clicksend_client.Configuration()
configuration.username = api_username
configuration.password = api_key

# create an instance of the API class
api_instance = clicksend_client.SMSApi(clicksend_client.ApiClient(configuration))

#Create our SMS Message
sms_message = SmsMessage(source="php",
                        body=check_message_length(sms_message_body),
                        to=check_number(sms_phone_number),
                        _from=check_sender_id(sms_message_id)
                        )

sms_messages = clicksend_client.SmsMessageCollection(messages=[sms_message])

#Send the SMS message
try:
	api_response = api_instance.sms_send_post(sms_messages)
	pprint(api_response)
except ApiException as e:
	print("Exception when calling AccountApi->account_get: %s\n" % e)
