#File: 		tt-sso.py
#Author:	James LeGeros
#Company:	---------------------
#Email:		jlegeros@------------.com
#Summary:	------------ Single Sign On implementation for Google Apps
#			Utilizes Google Apps for authentication
#			Classified sections redacted (--------)
#			Example SSO utilizing Google Apps authentication
#			App requests a token through a GET request to the AuthenticateAndGetUserInfo API
#			It then supplies that token along with the username to be logged in
#			Then redirects the user to the login URI
#			User is determined based on their logged in Google Apps account
#			If an error occurs, system logs the error internally and notifies the user to contact IT

import webapp2
import urllib2
from google.appengine.api import users
from pprint import pprint
from google.appengine.api import urlfetch

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        urlfetch.set_default_fetch_deadline(15)
        
        user = users.get_current_user()
        if user:
            #delcare some values
            device = "restcalls"
            parentUser = "your-username"
            password = "your-password"
            
            uri = "https://rest.----------------.com/user/AuthenticateAndGetUserInfo?username=" + parentUser + "&password=" + password + "&device=" + device
            
            #prints to log
            print('Trying to run a get on ' + uri)
            print('for ' + user.nickname())
            
            responseJSON = urllib2.urlopen(uri).read()
            responseDICT = eval(responseJSON)

            if responseDICT['wasSuccessful']:
                parentToken = responseDICT['data']['authenticationToken']
                childUser = "UNQID_" + user.nickname()
                
                # Remove periods from email addresses... since vendor doesn't accept periods in usernames
                childUser = childUser.translate(None, '.')
                
                uri = "https://rest.-------------------.com/user/AuthenticateChild?authToken=" + parentToken + "&username=" + childUser
                
                print('Trying to run a get on ' + uri)
                print('for ' + user.nickname())
                
                responseJSON = urllib2.urlopen(uri).read()            
                responseDICT = eval(responseJSON)
                
                if responseDICT['wasSuccessful']:
                    loginURI = "http://www.----------------.com/tokenlogin/?token=" + responseDICT['data']['authenticationToken']
                    self.redirect(loginURI)
                else:
                    print('Error occurred, Child authentication was not successful...')
                    print(childUser)
                    print(uri)
                    print(responseDICT)
                    self.response.write('An Error occurred\n\nPlease contact your IT administrator\n\nJames LeGeros\njlegeros@---------------------.com')
            else:
                print('Error occurred, Parent authentication was not successful...')
                print(responseDICT)
                self.response.write('An Error occurred\n\nPlease contact your IT administrator\n\nJames LeGeros\njlegeros@-----------------.com')

application = webapp2.WSGIApplication([
    ('/.*', MainPage),
], debug=True)