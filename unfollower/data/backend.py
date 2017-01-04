from requests import request
from PyQt5 import QtCore, QtGui, QtWidgets
import tweepy
import unfollower
import sys
import random
import time
import os

#app end authentication
auth = tweepy.OAuthHandler("ounrAEDBVakonuga48NO9qt4s", "Gfa9upTLigvrCVHwCE7m1btwxUiCp7gDDTZRdJDtHs8EZNnxb1")

# Redirect user to Twitter to authorize
def getURL():
    redirect_url = ''
    try:
        redirect_url = auth.get_authorization_url()
        print("\n" + redirect_url + "\n")
        return redirect_url
    except:
        print("broken token")
        return redirect_url

#UI class
class unfollower(QtWidgets.QMainWindow, unfollower.Ui_MainWindow):
    def __init__(self, parent=None):
        super(unfollower, self).__init__(parent)
        self.setupUi(self)
        self.home()

    def home(self):
        self.url.setPlainText(getURL())
        self.followBtn.clicked.connect(self.unfollow)
        self.stopBtn.clicked.connect(self.stop)
        self.exitBtn.clicked.connect(self.exit)

    def unfollow(self):
        #Authenicate using pin
        verifier = self.pinLine.text()
        auth.get_access_token(verifier)
        access_token = auth.access_token
        access_secret = auth.access_token_secret
        print(access_token, access_secret)
        auth.set_access_token(access_token, access_secret)
        api = tweepy.API(auth)

        #self information
        my_user = api.me()
        my_id = my_user.id
        my_followers = api.followers_ids(my_id)
        my_following = api.friends_ids(my_id)
        unfollowAmount = self.unfollowLine.text()
        skipMutuals = self.skipMutuals.isChecked()
        stableMode = self.stableMode.isChecked()

        #follow function
        unfollowed = 0
        count = 0
        for following in my_following:
            QtCore.QCoreApplication.processEvents()
            if unfollowed >= int(unfollowAmount): 
                break
            current_screen_name = api.get_user(following).screen_name
            try:
                if skipMutuals:
                    if following not in my_followers:
                        api.destroy_friendship(my_id, following)
                        unfollowed+=1 
                        count+=1
                        print('\x1b[2K\r',)
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
            print(fill)
            self.progressBar.setValue(fill)
            self.show()

            #random sleep to avoid detection
            if stableMode:
                sleep = random.uniform(1.0, 1.7)
                time.sleep(sleep)
        print("Successfully unfollowed %s users" % unfollowed)
        self.home()

    def stop(self):
        print("STOP!")

    def exit(self):
        sys.exit()

def main():
    app = QtWidgets.QApplication(sys.argv)
    form = unfollower()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()
