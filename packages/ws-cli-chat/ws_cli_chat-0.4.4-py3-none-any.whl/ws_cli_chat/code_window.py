import PySimpleGUI as sg
from pysimpleevent import EventSimpleGUI


def run_code_window() -> None | str:
    loop = EventSimpleGUI()
    code_win = sg.Window(
        "Escreva o codigo",
        [
            [sg.Text("puts your code here!")],
            [sg.Multiline( k='code', expand_x=True, expand_y=True )],
            [sg.Button("send", expand_x=True, key='send'), sg.Button('close', key='send')]
        ], resizable=True
    )
    try:
        obj = loop.run_window(code_win, return_values=True, close_event='send')
        if obj:
            return obj.get('code', 'invalid input')
    except KeyboardInterrupt:
        return None


