from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from gui.inferencepanel import InferencePanel
from kivy.uix.accordion import Accordion, AccordionItem
from gui.elements import AllLayout
from gui.calendarpanel import CalendarPanel
from reader.parser import Parser


class IspApp(App):

    def __init__(self, url, stages):
        super(IspApp, self).__init__()
        self.url = url
        self.accordion = Accordion()
        self.pnlCalendar = CalendarPanel(stages)

    def build(self):
        Window.size = (1400, 800)
        bltAll = AllLayout()
        bltCenter = BoxLayout()
        aciInf = AccordionItem(title='ISP Selection')
        aciInf.add_widget(InferencePanel(self.url, self))
        aciCal = AccordionItem(title='Calendar')
        aciCal.add_widget(self.pnlCalendar)
        self.accordion.add_widget(aciInf)
        self.accordion.add_widget(aciCal)
        bltCenter.add_widget(self.accordion)
        bltAll.add_widget(bltCenter)
        return bltAll

    def update(self, courses):
        self.pnlCalendar.update_selected_courses(courses)


def main():
    parser = Parser()
    edj = parser.read('/home/herbert/PycharmProjects/Thesis/reader/DomainTI.json')
    isp = IspApp('/home/herbert/PycharmProjects/Thesis/reader/DomainTI.json', edj.stages)
    isp.run()

if __name__ == "__main__":
    main()
