Example Single Sign On application built by me at my previous employer

Utlizing Google App Engine to deploy the the Cloud and make use of a user already being signed in to their Google Apps account.

App checks to see if the user exists (user is signed in to ther Google Apps account)
Then it makes a RESTful api request to the vendor to obtain a token
Then it uses the token to generate a login URI and redirects the user to it

If an error occurs, the system logs relevant information and then notifies the user to contact IT (me)