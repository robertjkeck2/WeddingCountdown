#Built-ins
import time
import os
from datetime import datetime
import smtplib
from random import randrange
from urllib import request

#Externals
import lxml.html
import pandas as pd


#Hard-coded wedding date
WEDDING_DAY = datetime(2017, 10, 28)

def get_time_to_wedding():
	"""
	Uses datetime module to return countdown values

	Args: None
	"""

	now = datetime.now()
	time_to_wedding = WEDDING_DAY - now
	days_to_wedding = time_to_wedding.days
	hours_to_wedding = divmod(time_to_wedding.seconds, 3600)[0]
	minutes_to_wedding = int(round(((divmod(time_to_wedding.seconds, 60)[0] / 60) - hours_to_wedding) * 60, 0))
	seconds_to_wedding = divmod(time_to_wedding.seconds, 60)[1]
	return str(days_to_wedding), str(hours_to_wedding), str(minutes_to_wedding), str(seconds_to_wedding), now

def pull_pinterest():
	"""
	Uses requests to parse all links with keywords pin and activity and returns first found

	Args: None
	"""

	connection = request.urlopen('https://www.pinterest.com/categories/weddings/')

	dom =  lxml.html.fromstring(connection.read())

	for link in dom.xpath('//a/@href'):
		if (link[0:5] == '/pin/') and (link[-10:] != '/activity/'):
			return ('https://www.pinterest.com' + link) 
			break

def get_message(days, hours, minutes, seconds, link):
	"""
	Pulls stock message parts from messages.xlsx and combines with countdown to create message

	Args: days, hours, minutes, seconds - countdown time
		  link - pinterest random wedding pin link from pull_pinterest function
	"""

	df = pd.read_excel('messages.xlsx')

	message_components = []
	for i in range(0,len(df.columns)):
		randnum = randrange(0,len(df.index))
		message_components.append(df[df.columns[i]][randnum])

	formatted_countdown = '{} days, {} hours, {} minutes, and {} seconds until our wedding day!!!'.format(days, hours, minutes, seconds)
	wedding_link = "Here's a random wedding pin for your pinning pleasure: " + '\n' + str(link)
	double_line = '\n\n'
	new_line = '\n'

	message = (message_components[0] 
		    + double_line 
			+ message_components[2]
			+ formatted_countdown
			+ double_line
			+ wedding_link
			+ double_line
			+ message_components[1]
			+ new_line
			+ 'John')

	return message

def send_email(message, now):
	"""
	Uses smtplib to send countdown message to recipient

	Args: message - countdown message from get_message function
		  now - current date from datetime module
	"""

	from_address = 'from_email'
	to_address = 'to_email'
	subject = 'Wedding Countdown: ' + str(now.month) + '/' + str(now.day) + '/' + str(now.year)
	msg = message 
	
	conn = smtplib.SMTP('smtp.gmail.com', 587)
	conn.ehlo()
	conn.starttls()
	conn.login('email', 'password')
	error_log = conn.sendmail(from_address, to_address, 'Subject: ' + subject + '\n\n' + msg)
	return error_log

def log(link, error_log):
	"""
	Log each run along with the Pin link for each day

	Args: link - pinterest random pin link from pull_pinterest function
		  error_log - status of email send from send_email function
	"""

	today = datetime.now().strftime('%Y-%m-%d')
	logrow = today + ' ' + str(error_log) + ' ' + link
	fp = open('wedding_logfile.txt','a')
	fp.write(logrow + '\n')
	fp.close()
