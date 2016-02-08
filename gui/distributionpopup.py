from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView


class DistributionPopup(Popup):

    def __init__(self, distributions, minimum, maximum):
        super(DistributionPopup, self).__init__()
        self.title = 'Distribution'
        self.size_hint = (None, None)
        self.size = (500, 500)
        self.distributions = distributions
        self.minimum = minimum
        self.maximum = maximum
        self.build()

    def build(self):
        svMain = ScrollView()
        bltTable = BoxLayout(orientation='vertical', size_hint_y=None, height=40*(len(self.distributions.keys())+1))
        bltTitle = BoxLayout(size_hint_y=None, height=40, orientation='horizontal', spacing=5)
        bltTitle.add_widget(Label(text='VakGroep', size_hint=(None,None), size=(170,40)))
        bltTitle.add_widget(Label(text='Minimum', size_hint=(None,None), size=(100,40)))
        bltTitle.add_widget(Label(text='Geslecteerd', size_hint=(None,None), size=(100,40)))
        bltTitle.add_widget(Label(text='Maximum', size_hint=(None,None), size=(100,40)))
        bltTable.add_widget(bltTitle)
        for group in self.distributions.keys():
            bltItem = BoxLayout(size_hint_y=None, height=40, orientation='horizontal',spacing=5)
            lblName = Label(text=group, size_hint=(None,None), size=(170,40), text_size=(170,40), shorten=True, valign='middle')
            lblMin = Label(text=str(self.minimum.get(group)), size_hint=(None,None), size=(100,40))
            lblDistr = Label(text=str(self.distributions.get(group)), size_hint=(None,None), size=(100,40))
            lblMax = Label(text=str(self.maximum.get(group)), size_hint=(None,None), size=(100,40))
            bltItem.add_widget(lblName)
            bltItem.add_widget(lblMin)
            bltItem.add_widget(lblDistr)
            bltItem.add_widget(lblMax)
            bltTable.add_widget(bltItem)
        svMain.add_widget(bltTable)
        self.add_widget(svMain)