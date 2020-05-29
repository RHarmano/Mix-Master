import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
from PyQt5 import QtWidgets

# spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id = 'b4da95b62d814121a68d18ed5e711833',client_secret = '4f3456ccada649fa9a28174650f15fe7'))

scope = 'user-library-read playlist-modify-public playlist-read-private'
client_id = 'b4da95b62d814121a68d18ed5e711833'
client_secret = '4f3456ccada649fa9a28174650f15fe7'
redirect_uri = 'http://localhost:8888/callback'

class App(QtWidgets.QWidget):
    def __init__(self):
        
        super().__init__()
        self.title = 'Spotify Playlist Creator'
        self.left = 0
        self.top = 0
        # sizeModal = QtWidgets.QDesktopWidget.screenGeometry()
        self.width = 0 #sizeModal.width()
        self.height = 0 #sizeModal.height()
        self.initUI()

    def loginUser(self):
        user, okPressed = QtWidgets.QInputDialog.getText(self,'User Login','Username:',QtWidgets.QLineEdit.Normal,'')
        token = spotipy.util.prompt_for_user_token(user, scope, client_id, client_secret, redirect_uri)
        return token

    def trackInput(self):
        text, okPressed = QtWidgets.QInputDialog.getText(self,'Seed Track Input','Track Name:',QtWidgets.QLineEdit.Normal,'')
        if okPressed and text != '':
            return text

    def selectTrack(self,track_val):
        track_name_list = pd.DataFrame({'tracks':[],'ids':[]},dtype=str)
        search_results = self.spotify.search(q=self.track, limit=10, offset=0, type='track')
        for i in range(len(search_results['tracks']['items'])):
            track_name = search_results['tracks']['items'][i]['name']
            track_id = search_results['tracks']['items'][i]['id']
            track_name_list = track_name_list.append(pd.DataFrame({'tracks':[track_name],'ids':[track_id]}), ignore_index=True)

        item, okPressed = QtWidgets.QInputDialog.getItem(self,'Select Correct Track','Did you mean: ',track_name_list['tracks'],0,False)
        if okPressed and item:
            return item

    def initUI(self):
        """
        Initialize UI
        """
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        token = self.loginUser()
        self.spotify = spotipy.Spotify(auth=token)

        self.track = self.trackInput()
        self.correct_track = self.selectTrack(self.track)
        self.query = self.spotify.search(q=self.correct_track, limit=1, offset=0, type='track')
        self.correct_id = self.query['tracks']['items'][0]['id']
        print(self.correct_id)
        self.recs = self.spotify.recommendations(seed_tracks=self.correct_id)
        print(self.recs)
        self.show()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())