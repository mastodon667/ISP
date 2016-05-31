from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from gui.inferencepanel import InferencePanel
from kivy.uix.accordion import Accordion, AccordionItem
from gui.elements import AllLayout
from gui.calendarpanel import CalendarPanel
from reader.parser import Parser
from automaton.reader import Reader

class IspApp(App):

    def __init__(self, location, file, stages):
        super(IspApp, self).__init__()
        self.url = location + file
        self.accordion = Accordion()
        self.location = location
        self.stages = stages
        self.pnlCalendar = None

    def build(self):
        Window.size = (1400, 800)
        self.pnlCalendar = CalendarPanel(self.stages, self.location)
        bltAll = AllLayout()
        bltCenter = BoxLayout()
        aciInf = AccordionItem(title='ISP Selectie')
        aciInf.add_widget(InferencePanel(self.url, self))
        aciCal = AccordionItem(title='Lessenrooster')
        aciCal.add_widget(self.pnlCalendar)
        self.accordion.add_widget(aciInf)
        self.accordion.add_widget(aciCal)
        bltCenter.add_widget(self.accordion)
        bltAll.add_widget(bltCenter)
        return bltAll

    def update(self, courses):
        self.pnlCalendar.update_selected_courses(courses)


def main():
    location = 'C:/Users/Herbert/PycharmProjects/ISP/'
    #location = '/home/herbert/PycharmProjects/Thesis/'
    parser = Parser()
    edj = parser.read(location + 'reader/DomainTI.json')
    isp = IspApp(location, 'reader/DomainTI.json', edj.stages)
    isp.run()

if __name__ == "__main__":
    main()
