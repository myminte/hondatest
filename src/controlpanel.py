import configparser

import os
import sys

import EnhancedStatusBar

import wx
import wx.lib.agw.labelbook as lb
import wx.lib.buttons as buttons

from appdirs import AppDirs

# from version import __VERSION__

class HondaECUControlPanel(wx.Frame):

    lbstyle = lb.INB_FIT_LABELTEXT | lb.INB_LEFT | lb.INB_DRAW_SHADOW | lb.INB_GRADIENT_BACKGROUND

    def __init__(self, version_full, nobins=False, restrictions=None, force_restrictions=False):
    #     self.stats = {
    #         "retries": 0,
    #         "checksum_errors": 0,
    #     }
    #     adirs = AppDirs("HondaECU", "MCUInnovationsInc", version=__VERSION__)
    #     self.prefsdir = adirs.user_config_dir
    #     if not os.path.exists(self.prefsdir):
    #         os.makedirs(self.prefsdir)
    #     self.configfile = os.path.join(self.prefsdir, 'hondaecu.ini')
    #     self.config = configparser.ConfigParser()
    #     if os.path.isfile(self.configfile):
    #         self.config.read(self.configfile)
    #     if "retries" not in self.config['DEFAULT']:
    #         self.config['DEFAULT']['retries'] = "3"
    #     if "timeout" not in self.config['DEFAULT']:
    #         self.config['DEFAULT']['timeout'] = "0.2"
    #     if "klinemethod" not in self.config['DEFAULT']:
    #         self.config['DEFAULT']['klinemethod'] = "loopback_ping"
    #     else:
    #         if self.config['DEFAULT']['klinemethod'] == "poll_modem_status":
    #             self.config['DEFAULT']['klinemethod'] = "loopback_ping"
    #     if "kline_timeout" not in self.config['DEFAULT']:
    #         self.config['DEFAULT']['kline_timeout'] = "0.1"
    #     if "kline_wait" not in self.config['DEFAULT']:
    #         self.config['DEFAULT']['kline_wait'] = "0.002"
    #     if "kline_testbytes" not in self.config['DEFAULT']:
    #         self.config['DEFAULT']['kline_testbytes'] = "1"
    #     with open(self.configfile, 'w') as configfile:
    #         self.config.write(configfile)
        # self.nobins = nobins
        # self.restrictions = restrictions
        # self.force_restrictions = force_restrictions
    #     self.run = True
    #     self.active_ftdi_device = None
    #     self.ftdi_devices = {}
    #     self.warned = []
    #     self.__clear_data()

    #     if getattr(sys, 'frozen', False):
    #         self.basepath = sys._MEIPASS
    #     else:
    #         self.basepath = os.path.dirname(os.path.realpath(__file__))

        self.version_full = version_full
        self.version_short = self.version_full.split("-")[0]

    #     # self.apps = {
    #     #     "flash": {
    #     #         "label": "Flash",
    #     #         "panel": HondaECUFlashPanel,
    #     #     },
    #     #     "eeprom": {
    #     #         "label": "EEPROM",
    #     #         "panel": HondaECUEEPROMPanel,
    #     #     },
    #     #     # "hrc": {
    #     #     # 	"label":"HRC Data Settings",
    #     #     # 	"panel":HondaECUHRCDataSettingsPanel,
    #     #     # },
    #     #     "data": {
    #     #         "label": "Data Logging",
    #     #         "panel": HondaECUDatalogPanel,
    #     #     },
    #     #     "dtc": {
    #     #         "label": "Trouble Codes",
    #     #         "panel": HondaECUErrorPanel,
    #     #     },
    #     # }
    #     self.appanels = {}

        wx.Frame.__init__(self, None, title="HondaECU %s" % self.version_full,style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER, size=(500, 300))

        ib = wx.IconBundle()
        ib.AddIcon(os.path.join(self.basepath, "images", "honda.ico"))
        self.SetIcons(ib)

        self.menubar = wx.MenuBar()
        self.SetMenuBar(self.menubar)
        filemenu = wx.Menu()
        self.menubar.Append(filemenu, '&File')
        settingsitem = wx.MenuItem(filemenu, wx.ID_ANY, 'Settings')
        self.Bind(wx.EVT_MENU, self.OnSettings, settingsitem)
        filemenu.Append(settingsitem)
        filemenu.AppendSeparator()
        quititem = wx.MenuItem(filemenu, wx.ID_EXIT, '&Quit\tCtrl+Q')
        self.Bind(wx.EVT_MENU, self.OnClose, quititem)
        filemenu.Append(quititem)
        helpmenu = wx.Menu()
        self.menubar.Append(helpmenu, '&Help')
        debugitem = wx.MenuItem(helpmenu, wx.ID_ANY, 'Show debug log')
        self.Bind(wx.EVT_MENU, self.OnDebug, debugitem)
        helpmenu.Append(debugitem)
        helpmenu.AppendSeparator()
        detectmapitem = wx.MenuItem(helpmenu, wx.ID_ANY, 'Detect map id')
        self.Bind(wx.EVT_MENU, self.OnDetectMap, detectmapitem)
        helpmenu.Append(detectmapitem)
        checksumitem = wx.MenuItem(helpmenu, wx.ID_ANY, 'Validate bin checksum')
        self.Bind(wx.EVT_MENU, self.OnBinChecksum, checksumitem)
        helpmenu.Append(checksumitem)
        statsitem = wx.MenuItem(helpmenu, wx.ID_ANY, 'Adapter stats')
        self.Bind(wx.EVT_MENU, self.OnStats, statsitem)
        helpmenu.Append(statsitem)

        self.statusicons = [
            wx.Image(os.path.join(self.basepath, "images/bullet_black.png"), wx.BITMAP_TYPE_ANY).ConvertToBitmap(),
            wx.Image(os.path.join(self.basepath, "images/bullet_yellow.png"), wx.BITMAP_TYPE_ANY).ConvertToBitmap(),
            wx.Image(os.path.join(self.basepath, "images/bullet_green.png"), wx.BITMAP_TYPE_ANY).ConvertToBitmap(),
            wx.Image(os.path.join(self.basepath, "images/bullet_blue.png"), wx.BITMAP_TYPE_ANY).ConvertToBitmap(),
            wx.Image(os.path.join(self.basepath, "images/bullet_purple.png"), wx.BITMAP_TYPE_ANY).ConvertToBitmap(),
            wx.Image(os.path.join(self.basepath, "images/bullet_red.png"), wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        ]

        self.statusbar = EnhancedStatusBar.EnhancedStatusBar(self, -1)
        self.SetStatusBar(self.statusbar)
        self.statusbar.SetSize((-1, 28))
        self.statusicon = wx.StaticBitmap(self.statusbar)
        self.statusicon.SetBitmap(self.statusicons[0])
        self.ecmidl = wx.StaticText(self.statusbar)
        self.flashcountl = wx.StaticText(self.statusbar)
        self.dtccountl = wx.StaticText(self.statusbar)
        self.statusbar.SetFieldsCount(4)
        self.statusbar.SetStatusWidths([32, 170, 130, 110])
        self.statusbar.AddWidget(self.statusicon, pos=0)
        self.statusbar.AddWidget(self.ecmidl, pos=1, horizontalalignment=EnhancedStatusBar.ESB_ALIGN_LEFT)
        self.statusbar.AddWidget(self.flashcountl, pos=2, horizontalalignment=EnhancedStatusBar.ESB_ALIGN_LEFT)
        self.statusbar.AddWidget(self.dtccountl, pos=3, horizontalalignment=EnhancedStatusBar.ESB_ALIGN_LEFT)
        self.statusbar.SetStatusStyles([wx.SB_SUNKEN, wx.SB_SUNKEN, wx.SB_SUNKEN, wx.SB_SUNKEN])

        self.outerp = wx.Panel(self)

        self.adapterboxp = wx.Panel(self.outerp)
        self.securebutton = wx.Button(self.adapterboxp, label="Security Access")
        self.securebutton.Enable(False)
        self.adapterboxsizer = wx.StaticBoxSizer(wx.HORIZONTAL, self.adapterboxp, "FTDI Devices:")
        self.adapterboxp.SetSizer(self.adapterboxsizer)
        self.adapterlist = wx.Choice(self.adapterboxp, wx.ID_ANY, size=(-1, 32))
        self.adapterboxsizer.Add(self.adapterlist, 1, wx.ALL | wx.EXPAND, border=5)
        self.adapterboxsizer.Add(self.securebutton, 0, wx.ALL, border=5)

        self.labelbook = lb.LabelBook(self.outerp, agwStyle=self.lbstyle)

        self.bookpages = {}
        maxdims = [0, 0]
        for a, d in self.apps.items():
            enablestates = None
            if "enable" in self.apps[a]:
                enablestates = self.apps[a]["enable"]
            self.bookpages[a] = d["panel"](self, a, self.apps[a], enablestates)
            x, y = self.bookpages[a].GetSize()
            if x > maxdims[0]:
                maxdims[0] = x
            if y > maxdims[1]:
                maxdims[1] = y
            self.labelbook.AddPage(self.bookpages[a], d["label"], False)
        for k in self.bookpages.keys():
            self.bookpages[k].SetMinSize(maxdims)

        self.modelp = wx.Panel(self.outerp, style=wx.BORDER_SUNKEN)
        self.modelbox = wx.BoxSizer(wx.VERTICAL)
        self.modell = wx.StaticText(self.modelp, label="", style=wx.ALIGN_CENTRE_HORIZONTAL | wx.ALIGN_CENTRE_VERTICAL)
        self.ecupnl = wx.StaticText(self.modelp, label="", style=wx.ALIGN_CENTRE_HORIZONTAL | wx.ALIGN_CENTRE_VERTICAL)
        font1 = self.GetFont().Bold()
        font2 = self.GetFont().Bold()
        font1.SetPointSize(font1.GetPointSize() * 1.25)
        font2.SetPointSize(font2.GetPointSize() * 2)
        self.modell.SetFont(font2)
        self.ecupnl.SetFont(font1)
        self.modelbox.AddSpacer(5)
        self.modelbox.Add(self.modell, 0, wx.CENTER)
        self.modelbox.Add(self.ecupnl, 0, wx.CENTER)
        self.modelbox.AddSpacer(5)
        self.modelp.SetSizer(self.modelbox)

        self.outersizer = wx.BoxSizer(wx.VERTICAL)
        self.outersizer.Add(self.adapterboxp, 0, wx.EXPAND | wx.ALL, 5)
        self.outersizer.Add(self.modelp, 0, wx.EXPAND | wx.ALL, 5)
        self.outersizer.Add(self.labelbook, 2, wx.EXPAND | wx.ALL, 5)
        self.outerp.SetSizer(self.outersizer)

        self.mainsizer = wx.BoxSizer(wx.VERTICAL)
        self.mainsizer.Add(self.outerp, 1, wx.EXPAND)
        self.mainsizer.SetSizeHints(self)
        self.SetSizer(self.mainsizer)

        self.securebutton.Bind(wx.EVT_BUTTON, self.OnSecure)
        self.adapterlist.Bind(wx.EVT_CHOICE, self.OnAdapterSelected)
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        # self.debuglog = HondaECULogPanel(self)

        # dispatcher.connect(self.USBMonitorHandler, signal="USBMonitor", sender=dispatcher.Any)
        # dispatcher.connect(self.kline_worker_handler, signal="KlineWorker", sender=dispatcher.Any)
        # dispatcher.connect(self.ecu_stats_handler, signal="ecu.stats", sender=dispatcher.Any)

        # self.usbmonitor = USBMonitor(self)
        # self.klineworker = KlineWorker(self)

        self.Layout()
        self.Center()
        self.Show()

    #     self.usbmonitor.start()
    #     self.klineworker.start()

    #     self.settings = SettingsDialog(self)
    #     self.passwordd = PasswordDialog(self)

    # def __clear_data(self):
    #     self.ecuinfo = {}

    # def __clear_widgets(self):
    #     self.ecmidl.SetLabel("")
    #     self.flashcountl.SetLabel("")
    #     self.dtccountl.SetLabel("")
    #     self.modell.SetLabel("")
    #     self.ecupnl.SetLabel("")
    #     self.statusicon.SetBitmap(self.statusicons[0])
    #     self.statusbar.OnSize(None)

    # def ecu_stats_handler(self, data):
    #     self.stats = data
    #     print(data)

    # def kline_worker_handler(self, info, value):
    #     if info in ["ecmid", "flashcount", "dtc", "dtccount", "state"]:
    #         self.ecuinfo[info] = value
    #         print(info,value)
    #         if info == "state":
    #             self.securebutton.Enable(False)
    #             self.statusicon.SetToolTip(wx.ToolTip("state: %s" % (str(value).split(".")[-1])))
    #             if value in [ECUSTATE.OFF, ECUSTATE.UNKNOWN]:  # BLACK
    #                 self.__clear_widgets()
    #                 self.statusicon.SetBitmap(self.statusicons[0])
    #             elif value in [ECUSTATE.RECOVER_NEW, ECUSTATE.RECOVER_OLD]:  # YELLOW
    #                 self.statusicon.SetBitmap(self.statusicons[1])
    #             elif value in [ECUSTATE.OK]:  # GREEN
    #                 self.securebutton.Enable(True)
    #                 self.statusicon.SetBitmap(self.statusicons[2])
    #             elif value in [ECUSTATE.FLASH]:  # BLUE
    #                 self.statusicon.SetBitmap(self.statusicons[3])
    #             elif value in [ECUSTATE.SECURE]:  # PURPLE
    #                 self.statusicon.SetBitmap(self.statusicons[4])
    #                 self.modell.SetLabel("Unknown Model")
    #                 self.ecupnl.SetLabel("~ Security Access Mode ~")
    #                 self.Layout()
    #         elif info == "ecmid":
    #             if len(value) > 0:
    #                 ecmid = " ".join(["%02x" % i for i in value])
    #                 self.ecmidl.SetLabel("   ECM ID: %s" % ecmid)
    #                 if value in ECM_IDs:
    #                     model = "%s (%s)" % (ECM_IDs[value]["model"], ECM_IDs[value]["year"])
    #                     pn = ECM_IDs[value]["pn"]
    #                 else:
    #                     model = "Unknown Model"
    #                     pn = "-"
    #                     for m in ECM_IDs.keys():
    #                         if m[:3] == value[:3]:
    #                             model = "%s (%s)" % (ECM_IDs[m]["model"], ECM_IDs[m]["year"])
    #                             break
    #                 self.modell.SetLabel(model)
    #                 self.ecupnl.SetLabel(pn)
    #                 self.Layout()
    #         elif info == "flashcount":
    #             if value >= 0:
    #                 self.flashcountl.SetLabel("   Flash Count: %d" % value)
    #         elif info == "dtccount":
    #             if value >= 0:
    #                 self.dtccountl.SetLabel("   DTC Count: %d" % value)
    #         self.statusbar.OnSize(None)
    #     elif info == "data":
    #         if info not in self.ecuinfo:
    #             self.ecuinfo[info] = {}
    #         self.ecuinfo[info][value[0]] = value[1:]

    # def OnStats(self, _event):
    #     wx.MessageDialog(None, str(self.stats), "", wx.CENTRE | wx.STAY_ON_TOP).ShowModal()

    # def OnSecure(self, _event):
    #     self.passwordd._Show()

    # def OnSettings(self, _event):
    #     self.settings.Show()

    # def OnClose(self, _event):
    #     with open(self.configfile, 'w') as configfile:
    #         self.config.write(configfile)
    #     self.run = False
    #     self.usbmonitor.join()
    #     self.klineworker.join()
    #     for w in wx.GetTopLevelWindows():
    #         w.Destroy()

    # def OnDetectMap(self, _event):
    #     with wx.FileDialog(self, "Open ECU dump file", wildcard="ECU dump (*.bin)|*.bin",
    #                        style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
    #         if fileDialog.ShowModal() == wx.ID_CANCEL:
    #             return
    #         pathname = fileDialog.GetPath()
    #         ecupn = os.path.splitext(os.path.split(pathname)[-1])[0]
    #         for i in ECM_IDs.values():
    #             if ecupn == i["pn"] and "keihinaddr" in i:
    #                 fbin = open(pathname, "rb")
    #                 nbyts = os.path.getsize(pathname)
    #                 byts = bytearray(fbin.read(nbyts))
    #                 fbin.close()
    #                 idadr = int(i["keihinaddr"], 16)
    #                 wx.MessageDialog(None, "Map ID: " + byts[idadr:(idadr + 7)].decode("ascii"), "",wx.CENTRE | wx.STAY_ON_TOP).ShowModal()
    #                 return
    #         wx.MessageDialog(None, "Map ID: unknown", "", wx.CENTRE | wx.STAY_ON_TOP).ShowModal()

    # def OnBinChecksum(self, _event):
    #     with wx.FileDialog(self, "Open ECU dump file", wildcard="ECU dump (*.bin)|*.bin",style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
    #         if fileDialog.ShowModal() == wx.ID_CANCEL:
    #             return
    #         pathname = fileDialog.GetPath()
    #         fbin = open(pathname, "rb")
    #         nbyts = os.path.getsize(pathname)
    #         byts = bytearray(fbin.read(nbyts))
    #         fbin.close()
    #         wx.MessageDialog(None, "Checksum: %s" % ("good" if checksum8bitHonda(byts) == 0 else "bad"), "",wx.CENTRE | wx.STAY_ON_TOP).ShowModal()
    #         return

    # def OnDebug(self, _event):
    #     self.debuglog.Show()

    # def USBMonitorHandler(self, action, device, config):
    #     dirty = False
    #     if action == "error":
    #         if device not in self.warned:
    #             self.warned.append(device)
    #             if platform.system() == "Windows":
    #                 wx.MessageDialog(None, "libusb error: make sure libusbk is installed", "",wx.CENTRE | wx.STAY_ON_TOP).ShowModal()
    #     elif action == "add":
    #         if device not in self.ftdi_devices:
    #             self.ftdi_devices[device] = config
    #             dirty = True
    #     elif action == "remove":
    #         if device in self.ftdi_devices:
    #             if device == self.active_ftdi_device:
    #                 dispatcher.send(signal="FTDIDevice", sender=self, action="deactivate",device=self.active_ftdi_device, config=self.ftdi_devices[self.active_ftdi_device])
    #                 self.active_ftdi_device = None
    #                 self.__clear_data()
    #             del self.ftdi_devices[device]
    #             dirty = True
    #     if len(self.ftdi_devices) > 0:
    #         if not self.active_ftdi_device:
    #             self.active_ftdi_device = list(self.ftdi_devices.keys())[0]
    #             dispatcher.send(signal="FTDIDevice", sender=self, action="activate", device=self.active_ftdi_device,config=self.ftdi_devices[self.active_ftdi_device])
    #             dirty = True
    #     else:
    #         pass
    #     if dirty:
    #         self.adapterlist.Clear()
    #         for device in self.ftdi_devices:
    #             cfg = self.ftdi_devices[device]
    #             self.adapterlist.Append("Bus %03d Device %03d: %s %s %s" % (
    #                 cfg.bus, cfg.address, usb.util.get_string(cfg, cfg.iManufacturer),
    #                 usb.util.get_string(cfg, cfg.iProduct), usb.util.get_string(cfg, cfg.iSerialNumber)))
    #         if self.active_ftdi_device:
    #             self.adapterlist.SetSelection(list(self.ftdi_devices.keys()).index(self.active_ftdi_device))

    # def OnAdapterSelected(self, _event):
    #     device = list(self.ftdi_devices.keys())[self.adapterlist.GetSelection()]
    #     print(device)
    #     if device is not self.active_ftdi_device:
    #         print("xxxx")
    #         if self.active_ftdi_device != None:
    #             dispatcher.send(signal="FTDIDevice", sender=self, action="deactivate", device=self.active_ftdi_device,config=self.ftdi_devices[self.active_ftdi_device])
    #         self.__clear_data()
    #         self.active_ftdi_device = device
    #         print(device)
    #         dispatcher.send(signal="FTDIDevice", sender=self, action="activate", device=self.active_ftdi_device,config=self.ftdi_devices[self.active_ftdi_device])