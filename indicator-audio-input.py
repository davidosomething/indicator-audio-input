#!/usr/bin/python2
# -*- coding: utf-8 -*-

# Copyright (c) 2015, David O'Trakoun (https://github.com/davidosomething)

import gtk
import appindicator
import os

APP_NAME = "Audio Input indicator"
APP_VERSION = "0.2"


class IndicatorAudioInput:
    def __init__(self):
        self.icon_unmuted = "microphone11.png"
        self.icon_muted = "microphone109.png"

        self.indicator = appindicator.Indicator(
                "audio-input",
                "audio-input",
                appindicator.CATEGORY_APPLICATION_STATUS)

        self.indicator.set_icon_theme_path(os.path.dirname(os.path.realpath(__file__)))
        self.indicator.set_status(appindicator.STATUS_ACTIVE)

        self.setup_menu()

        # This is immediately set False in toggle
        self.is_muted = False

    def main(self):
        self.toggle()
        gtk.main()
        return 0

    def quit(self, widget):
        gtk.main_quit()

    def setup_menu(self):
        self.menu = gtk.Menu()

        self.item_toggle = gtk.MenuItem("Toggle")
        self.item_toggle.connect("activate", self.menu_toggle)
        self.item_toggle.show()
        self.menu.append(self.item_toggle)

        self.item_about = gtk.MenuItem("About")
        self.item_about.connect("activate", self.about)
        self.item_about.show()
        self.menu.append(self.item_about)

        self.item_exit = gtk.MenuItem("Exit")
        self.item_exit.connect("activate", self.quit)
        self.item_exit.show()
        self.menu.append(self.item_exit)

        self.indicator.set_menu(self.menu)

    def menu_toggle(self, menu_item):
        self.toggle()

    def toggle(self):
        self.is_muted = not self.is_muted
        if self.is_muted:
            os.system("amixer -q set Capture cap")
            self.indicator.set_icon(self.icon_unmuted)
            self.item_toggle.set_label("Mute")
        else:
            os.system("amixer -q set Capture nocap")
            self.indicator.set_icon(self.icon_muted)
            self.item_toggle.set_label("Unmute")

    def about(self, widget):
        about = gtk.AboutDialog()
        about.set_name(APP_NAME)
        about.set_comments("Audio Input indicator")
        about.set_copyright("Copyright (c) 2015 David O'Trakoun")
        about.set_version(APP_VERSION)
        about.set_website("http://davidosomething.com")
        about.set_authors(["David O'Trakoun <me@davidosomething.com>"])
        res = about.run()
        if res == -4 or -6:  # close events
            about.destroy()

if __name__ == '__main__':
    indicator = IndicatorAudioInput()
    indicator.main()
