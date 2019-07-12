import os

from kivy.app import App
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.lang import Builder

from electrum_vestx.util import base_units

from ...i18n import _
from .label_dialog import LabelDialog

Builder.load_string('''
#:import os os
<WalletDialog@Popup>:
    title: _('Wallets')
    id: popup
    path: os.path.dirname(app.get_wallet_path())
    background:  'atlas://electrum_vestx/gui/kivy/theming/light/background'
    BoxLayout:
        orientation: 'vertical'
        padding: '10dp'
        canvas.before:
            Color:
                rgba: 0.122, 0.133, 0.200, 0.7
            BorderImage:
                source: 'atlas://electrum_vestx/gui/kivy/theming/light/card_bottom'
                size: self.size
                pos: self.pos
        FileChooserListView:
            id: wallet_selector
            dirselect: False
            filter_dirs: True
            filter: '*.*'
            path: root.path
            rootpath: root.path
            size_hint_y: 0.6
        Widget
            size_hint_y: 0.1
        GridLayout:
            cols: 3
            size_hint_y: 0.1
            Button:
                id: open_button
                size_hint: 0.1, None
                height: '48dp'
                text: _('New')
                on_release:
                    popup.dismiss()
                    root.new_wallet(app, wallet_selector.path)
            Button:
                id: open_button
                size_hint: 0.1, None
                height: '48dp'
                text: _('Open')
                disabled: not wallet_selector.selection
                on_release:
                    popup.dismiss()
                    root.open_wallet(app)
''')

class WalletDialog(Factory.Popup):

    def new_wallet(self, app, dirname):
        def cb(text):
            if text:
                app.load_wallet_by_name(os.path.join(dirname, text))
        d = LabelDialog(_('Enter wallet name'), '', cb)
        d.open()

    def open_wallet(self, app):
        app.load_wallet_by_name(self.ids.wallet_selector.selection[0])

