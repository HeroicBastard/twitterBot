from requests import request
from PyQt5 import QtCore, QtGui, QtWidgets
import tweepy
import twitterbot
import sys
import random
import time
import os

consumer_key = 'dQOAl3jdLZWqvvbustAdVL3pB'
consumer_secret = 'hNiLxOz7qHAQArWOUNEkpxOedDyiVydzeRqFO60qKZ5uS9U1i1'

#app end authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

# Redirect user to Twitter to authorize
try:
    redirect_url = auth.get_authorization_url()
    print("\n" + redirect_url + "\n")
except:
    print("broken token")

#Check to break loop
global stop
stop = False

#UI class
class twitterbot(QtWidgets.QMainWindow, twitterbot.Ui_TwitterBot):
    def __init__(self, parent=None):
        super(twitterbot, self).__init__(parent)
        self.setupUi(self)
        self.home()

    def home(self):
        self.url.setPlainText(redirect_url)
        self.followBtn.clicked.connect(self.follow)
        self.unfollowBtn.clicked.connect(self.unfollow)
        self.exitBtn.clicked.connect(self.close)
        self.stopBtn.clicked.connect(self.stop)
        self.stopBtn.clicked.connect(self.stop)

    def login(self):
        verifier = self.pinLine.text()
        auth.get_access_token(verifier)
        access_token = auth.access_token
        access_secret = auth.access_token_secret

        TokenFileName = 'tokens.txt'
        TokenDataFile = open(TokenFileName, 'w')
        TokenDataFile.write(access_token+'\n')
        TokenDataFile.write(access_secret+'\n')

    def unfollow(self):
        global stop
        stop = False

        #Check for existing token data
        access_token = ''
        access_secret = ''
        if not os.path.isfile('tokens.txt'):
        	self.login()

        #Login using token data
        TokenDataFile = open('tokens.txt', 'r')
        for i, line in enumerate(TokenDataFile):
            if i == 0:
                access_token = line.rstrip()
                print(access_token)
            if i == 1:
                access_secret = line.rstrip()
                print(access_secret)
        auth.set_access_token(access_token, access_secret)
        api = tweepy.API(auth)

        #self information
        my_user = api.me()
        my_id = my_user.id
        my_followers = api.followers_ids(my_id)
        my_following = api.friends_ids(my_id)
        unfollowAmount = self.amountLine.text()
        skipMutuals = self.skipMutuals.isChecked()
        stableMode = self.stableMode.isChecked()

        #follow function
        unfollowed = 0
        count = 0
        for following in my_following:
            QtCore.QCoreApplication.processEvents()
            if unfollowed >= int(unfollowAmount): 
                break
            if stop:
                break
            current_screen_name = api.get_user(following).screen_name
            try:
                if skipMutuals:
                    if following not in my_followers:
                        api.destroy_friendship(my_id, following)
                        unfollowed+=1 
                        count+=1
                        print("Unfollowed %s" % current_screen_name)
                    else:
                        count+=1
                else:
                    api.destroy_friendship(my_id, following)
                    unfollowed+=1
                    count+=1
            except:
                print('Error unfollowing %s' % current_screen_name)
                count+=1

            #update progress bar
            fill = unfollowed / int(unfollowAmount) * 100
            self.progressBar.setValue(fill)
            self.show()

            #random sleep to avoid detection
            if stableMode:
                sleep = random.uniform(1.0, 1.7)
                time.sleep(sleep)
        print("Successfully unfollowed %s users" % unfollowed)
        self.home()


    def follow(self):
        global stop
        stop = False

        #Check for existing token data
        access_token = ''
        access_secret = ''
        if not os.path.isfile('tokens.txt'):
            self.login()

        #Login using token data
        TokenDataFile = open('tokens.txt', 'r')
        for i, line in enumerate(TokenDataFile):
            if i == 0:
                access_token = line.rstrip()
                print(access_token)
            if i == 1:
                access_secret = line.rstrip()
                print(access_secret)
        auth.set_access_token(access_token, access_secret)
        api = tweepy.API(auth)

        #gather self information
        my_user = api.me()
        my_id = my_user.id
        followAmount = self.amountLine.text()

        #gather target information
        target = self.targetLine.text()
        target_user = api.get_user(target)
        target_followers = api.followers_ids(target_user.id)
        print(target_user.id)

        #follow function
        requested = 0
        followed = 0
        count = 0
        for follow in target_followers:
            QtCore.QCoreApplication.processEvents()
            if followed >= int(followAmount): 
                break
            if requested >= int(followAmount) / 10 + 5:
                break
            if stop:
                break
            current_screen_name = api.get_user(follow).screen_name
            try:
                api.create_friendship(my_id, follow)
                followed+=1 
                count+=1
                print("Followed %s" % current_screen_name)
            except:
                print('Already requested %s' % current_screen_name)
                target_followers.remove(follow)
                requested+=1
                count+=1

            #update progress bar
            fill = followed / int(followAmount) * 100
            self.progressBar.setValue(followed/int(followAmount) * 100)
            self.show()

            #self.amountLine.setPlainText(followAmount-followed)

            #random sleep to avoid detection
            sleep = random.uniform(1.0, 1.7)
            time.sleep(sleep)
        print("Successfully followed %s users" % followed)
        self.home()

    def stop(self):
        global stop
        stop = True

    def close(self):
        sys.exit()

def main():
    app = QtWidgets.QApplication(sys.argv)
    form = twitterbot()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()
