#imports
from PyQt5 import QtCore, QtGui, QtWidgets
import tweepy as tp 
import sys, random, time, os, webbrowser

#app data (work on fetching)
consumer_key = 'dQOAl3jdLZWqvvbustAdVL3pB'
consumer_secret = 'hNiLxOz7qHAQArWOUNEkpxOedDyiVydzeRqFO60qKZ5uS9U1i1'

#working
def redirect():
	auth = tp.OAuthHandler(consumer_key, consumer_secret)
	auth_url = auth.get_authorization_url()
	webbrowser.open(auth_url)

redirect()