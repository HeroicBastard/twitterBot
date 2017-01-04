from requests import request
from PyQt5 import QtCore, QtGui, QtWidgets
import tweepy
import follower
import sys
import random
import time
import os

#app end authentication
auth = tweepy.OAuthHandler("ounrAEDBVakonuga48NO9qt4s", "Gfa9upTLigvrCVHwCE7m1btwxUiCp7gDDTZRdJDtHs8EZNnxb1")

# Redirect user to Twitter to authorize
try:
    redirect_url = auth.get_authorization_url()
    print("\n" + redirect_url + "\n")
except:
    print("broken token")

#UI class
class follower(QtWidgets.QMainWindow, follower.Ui_MainWindow):
    def __init__(self, parent=None):
        super(follower, self).__init__(parent)
        self.setupUi(self)

        self.home()

    def home(self):
        self.url.setPlainText(redirect_url)
        self.followBtn.clicked.connect(self.follow)
        self.stopBtn.clicked.connect(self.close)

    def follow(self):
        #Authenicate using pin
        verifier = self.pinLine.text()
        auth.get_access_token(verifier)
        access_token = auth.access_token
        access_secret = auth.access_token_secret
        print(access_token, access_secret)
        auth.set_access_token(access_token, access_secret)
        api = tweepy.API(auth)

        #target information
        target = self.targetLine.text()
        target_user = api.get_user(target)
        target_followers = api.followers_ids(target_user.id)
        print(target_user.id)

        #self information
        my_user = api.me()
        my_id = my_user.id
        followAmount = self.followLine.text()

        #follow function
        requested = 0
        followed = 0
        count = 0
        for follow in target_followers:
            if followed >= int(followAmount): 
                break
            current_screen_name = api.get_user(follow).screen_name
            try:
                api.create_friendship(my_id, follow)
                followed+=1 
                count+=1
                print('\x1b[2K\r',)
                print("Followed %s" % current_screen_name)
            except:
                print('Already requested %s' % current_screen_name)
                target_followers.remove(follow)
                count+=1

            #update progress bar
            fill = followed / int(followAmount) * 100
            print(fill)
            self.progressBar.setValue(followed/int(followAmount) * 100)
            self.show()

            #random sleep to avoid detection
            sleep = random.uniform(1.0, 1.7)
            time.sleep(sleep)
        print("Successfully followed %s users" % followed)
        self.home()

    def stop(self):
        print("Stopping!")

    def close(self):
        sys.exit()

def main():
    app = QtWidgets.QApplication(sys.argv)
    form = follower()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()
