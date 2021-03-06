from kivy.app import App
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.widget import Widget

from electrum_vestx.gui.kivy.i18n import _

Builder.load_string('''
<Question@Popup>
    id: popup
    title: ''
    message: ''
    size_hint: 0.8, 0.5
    pos_hint: {'top':0.9}
    BoxLayout:
        orientation: 'vertical'
        canvas.before:
            Color:
                rgba: 0.180, 0.145, 0.196, 0.7
            BorderImage:
                source: 'atlas://electrum_vestx/gui/kivy/theming/light/card_bottom'
                size: self.size
                pos: self.pos
        Label:
            id: label
            text: root.message
            text_size: self.width, None
        Widget:
            size_hint: 1, 0.1
        BoxLayout:
            orientation: 'horizontal'
            size_hint: 1, 0.2
            Button:
                text: _('No')
                size_hint: 0.5, None
                height: '48dp'
                on_release:
                    root.callback(False)
                    popup.dismiss()
            Button:
                text: _('Yes')
                size_hint: 0.5, None
                height: '48dp'
                on_release:
                    root.callback(True)
                    popup.dismiss()
''')



class Question(Factory.Popup):

    def __init__(self, msg, callback):
        Factory.Popup.__init__(self)
        self.title = _('Question')
        self.message = msg
        self.callback = callback
