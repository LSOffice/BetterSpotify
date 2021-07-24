import wx, wx.adv, spotipy, os, requests, json

# Add Logs

class BetterSpotify(wx.App):
    def __init__(self):
        super().__init__(clearSigInt=True)
        try:
            os.mkdir("./cache")
            open("./cache/config.txt", "x")
        except FileExistsError:
            pass

        self.InitFrame()

    def InitFrame(self):
        frame = Frame()
        frame.Show()


class Frame(wx.Frame):
    def __init__(self, title="BetterSpotify", pos=(400, 400)):
        super().__init__(None, title=title, pos=pos)
        self.OnInit()

    def OnInit(self):
        self.SetBackgroundColour((255, 255, 255))
        self.MainScene = MainScene(self)
        self.CredentialsScene = CredentialsScene(self)
        self.MainScene.Hide()
        self.CredentialsScene.Hide()

        if os.stat("./cache/config.txt").st_size == 0:
            self.CredentialsScene.Show()
        else:
            self.MainScene.Show()

        self.Fit()

class CredentialsScene(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent=parent)

        title = wx.StaticText(self, wx.ID_ANY, 'BetterSpotify by LSOffice')

        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(title)

        text1 = wx.StaticText(self, wx.ID_ANY, "It seems you haven't used BetterSpotify before!")
        text1.SetFont(wx.Font(18, wx.DEFAULT, wx.BOLD, wx.NORMAL))
        titleIco = wx.StaticBitmap(self, wx.ID_ANY, wx.ArtProvider.GetBitmap(id=wx.ART_ERROR,
                                                                             client=wx.ART_OTHER, size=(16, 16)))

        sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer3.Add(titleIco, 0, wx.ALL | wx.EXPAND, 5)
        sizer3.Add(text1, 0, wx.ALL, 5)
        text2 = wx.StaticText(self, wx.ID_ANY, "We require authentication to your spotify account!")
        text2.SetFont(wx.Font(18, wx.DEFAULT, wx.BOLD, wx.NORMAL))
        holderText1 = wx.StaticText(self, wx.ID_ANY, "")
        holderText1.SetFont(wx.Font(18, wx.DEFAULT, wx.BOLD, wx.NORMAL))
        holderText1.SetForegroundColour((255, 255, 255))
        self.textbox1 = wx.TextCtrl(parent=self, value='Enter your spotify username...', style=wx.TE_CENTRE)
        self.textbox1.Bind(wx.EVT_SET_FOCUS, self.highlightTextCtrl)
        self.button1 = wx.Button(parent=self, label='Proceed')
        self.button1.Bind(wx.EVT_BUTTON, self.onSwitchFromCredentials)

        sizer2 = wx.BoxSizer(wx.VERTICAL)
        sizer2.Add(sizer3, 0, wx.CENTER)
        sizer2.Add(text2, 0, wx.CENTER)
        sizer2.Add(holderText1)
        sizer2.Add(self.textbox1, 0, wx.ALL | wx.EXPAND, 5)
        sizer2.Add(self.button1, 0, wx.CENTER)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(sizer1, 0, wx.CENTER)
        mainSizer.Add(wx.StaticLine(self), 0, wx.ALL | wx.EXPAND, 5)
        mainSizer.Add(sizer2, 0, wx.ALL | wx.EXPAND, 5)
        self.SetSizer(mainSizer)
        mainSizer.Fit(self)
        self.Layout()

    def highlightTextCtrl(self, event):
        if 'Enter your spotify username...' in self.textbox1.GetValue():
            self.textbox1.SetValue('')

    def onSwitchFromCredentials(self, event):
        if self.textbox1.GetValue() == "" or self.textbox1.GetValue() == "Enter your spotify username...":
            dlg = wx.RichMessageDialog(parent=None,
                                       message="You need to enter a value!",
                                       caption="Error!",
                                       style=wx.OK)
            dlg.ShowModal()
            event.Skip()

        token = spotipy.util.prompt_for_user_token(self.textbox1.GetValue(), 'user-read-currently-playing', redirect_uri='http://127.0.0.1:4321/callback')
        if token:
            sp = spotipy.Spotify(auth=token)

        print(token)

        open("./cache/config.txt", "a").write(self.textbox1.GetValue())
        dlg = wx.RichMessageDialog(parent=None,
                                   message="Restart the app!",
                                   caption="Thanks!",
                                   style=wx.OK)
        dlg.ShowModal()
        exit()


class MainScene(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent=parent)
        try:
            self.token = json.load(open(f"./.cache-{open('./cache/config.txt', 'r').read()}", "r+"))['access_token']
            if self.token:
                sp = spotipy.Spotify(auth=self.token)

            title = wx.StaticText(self, wx.ID_ANY, 'BetterSpotify by LSOffice')

            sizer1 = wx.BoxSizer(wx.HORIZONTAL)
            sizer1.Add(title)

            img_data = requests.get(sp.currently_playing()['item']['album']['images'][0]['url']).content
            with open(f"./cache/{sp.currently_playing()['item']['album']['artists'][0]['name']}_{sp.currently_playing()['item']['name']}.jpg", 'wb') as handler:
                handler.write(img_data)

            text1 = wx.StaticText(self, wx.ID_ANY, 'Currently listening to:')
            text1.SetFont(wx.Font(18, wx.DEFAULT, wx.BOLD, wx.NORMAL))
            holderText1 = wx.StaticText(self, wx.ID_ANY, "htext")
            holderText1.SetForegroundColour((255, 255, 255))
            png = wx.StaticBitmap(self, -1, wx.Bitmap(f"./cache/{sp.currently_playing()['item']['album']['artists'][0]['name']}_{sp.currently_playing()['item']['name']}.jpg", wx.BITMAP_TYPE_ANY))
            holderText2 = wx.StaticText(self, wx.ID_ANY, "htext")
            holderText2.SetFont(wx.Font(6, wx.DEFAULT, wx.BOLD, wx.NORMAL))
            holderText2.SetForegroundColour((255, 255, 255))
            hyperlink = wx.adv.HyperlinkCtrl(self, wx.ID_ANY, sp.currently_playing()['item']['name'],
                                         sp.currently_playing()['item']['external_urls']['spotify'])
            hyperlink.SetFont(wx.Font(30, wx.DEFAULT, wx.NORMAL, wx.NORMAL))
            hyperlink.SetNormalColour((0, 0, 0))
            hyperlink.SetHoverColour((0, 0, 255))
            hyperlink.SetVisitedColour((0, 0, 0))
            hyperlink2 = wx.adv.HyperlinkCtrl(self, wx.ID_ANY, sp.currently_playing()['item']['album']['artists'][0]['name'],
                                          sp.currently_playing()['item']['album']['artists'][0]['external_urls']['spotify'])
            hyperlink2.SetFont(wx.Font(23, wx.DEFAULT, wx.NORMAL, wx.NORMAL))
            hyperlink2.SetNormalColour((0, 0, 0))
            hyperlink2.SetHoverColour((0, 0, 255))
            hyperlink2.SetVisitedColour((0, 0, 0))

            sizer2 = wx.BoxSizer(wx.VERTICAL)
            sizer2.Add(text1, 0, wx.CENTER)
            sizer2.Add(holderText1, 0, wx.CENTER)
            sizer2.Add(png, 0, wx.CENTER)
            sizer2.Add(holderText2, 0, wx.CENTER)
            sizer2.Add(hyperlink, 0, wx.CENTER)
            sizer2.Add(hyperlink2, 0, wx.CENTER)

            mainSizer = wx.BoxSizer(wx.VERTICAL)
            mainSizer.Add(sizer1, 0, wx.CENTER)
            mainSizer.Add(wx.StaticLine(self), 0, wx.ALL | wx.EXPAND, 5)
            mainSizer.Add(sizer2, 0, wx.ALL | wx.EXPAND, 5)

            self.SetSizer(mainSizer)
            mainSizer.Fit(self)
            self.Layout()
        except Exception:
            pass


if __name__ == '__main__':
    app = BetterSpotify()
    app.MainLoop()
