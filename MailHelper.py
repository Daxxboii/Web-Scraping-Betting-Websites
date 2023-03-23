import imaplib, email
import Credentials

user = Credentials.Email_Address
password = Credentials.Password
imap_url = 'imap.gmail.com'

# Function to get email content part i.e its body part
def get_body(msg):
	if msg.is_multipart():
		return get_body(msg.get_payload(0))
	else:
		return msg.get_payload(None, True)

# Function to search for a key value pair
def search(key, value, con):
	result, data = con.search(None, key, '"{}"'.format(value))
	return data

# Function to get the list of emails under this label
def get_emails(result_bytes):
	msgs = [] 
	for num in result_bytes[0].split():
		typ, data = con.fetch(num, '(RFC822)')
		msgs.append(data)

	return msgs


con = imaplib.IMAP4_SSL(imap_url)


con.login(user, password)

# calling function to check for email under this label
con.select('Inbox')


msgs = get_emails(search('FROM', Credentials.OddsJam_EmailAddress, con))



# Finding the required content from our msgs
# User can make custom changes in this part to
# fetch the required content 

def FetchLatestOddsJamMessage():
	indexend=""
	# printing them by the order they are displayed in your gmail
    #for msg in msgs[::-1]:
	#printing the latest msg
	for sent in msgs[len(msgs)-1]:
		if type(sent) is tuple:

			# encoding set as utf-8
			content = str(sent[1], 'utf-8')
			data = str(content)

			# Handling errors related to unicodenecode
			try:
				indexstart = data.find("ltr")
				data2 = data[indexstart + 5: len(data)]
				indexend = data2.find("</div>")

				# printing the required content which we need
				# to extract from our email i.e our body
				print(data2[0: indexend])
				#print(data2)

			except UnicodeEncodeError as e:
				pass
	return indexend
	

	


