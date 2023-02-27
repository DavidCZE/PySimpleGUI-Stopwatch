import PySimpleGUI as sg
import time

# Před spuštěním je potřeba nainstalovat 'PySimpleGUI': napište do terminálu "pip install pysimplegui"

def time_as_int():
    """Vrátí čas v podobě int, vytvořené pro možnost formátování"""
    return int(round(time.time() * 100))


def create_window():
    """Vytvoření nového okna (Vytvořené primárně pro akci 'Obnovit')"""
    sg.theme("DarkAmber")
    layout = [
        [sg.VPush()],
        [sg.Text('', font='Young 50', key='-CAS-')],
        [sg.Button('Start', button_color=('#FFFFFF', '#00FF00'),
                   mouseover_colors='#FFFF00', border_width=0, key='-STARTSTOP-'),
         sg.Button('Kolo', button_color=('#FFFFFF', '#0000FF'),
                   mouseover_colors='#FFFF00', border_width=0, key='-KOLO-',
                   visible=False)],
        [sg.Column([[]], key='-KOLA-')],
        [sg.VPush()]
    ]
    return sg.Window('Stopky',
                     layout, size=(300, 300),
                     keep_on_top=True,
                     element_justification='center',
                     grab_anywhere=True,
                     resizable=True)


window = create_window()
start_time = 0
active = False
pocet_kol = 1

while True:
    event, values = window.read(timeout=10)
    if event == sg.WIN_CLOSED:
        break
    if event == '-STARTSTOP-':
        if active:
            active = False
            window['-STARTSTOP-'].update('Obnovit')
            window['-KOLO-'].update('Pokračovat')
            paused_time = time_as_int()
        else:
            if start_time > 0:
                window.close()
                window = create_window()
                start_time = 0
                pocet_kol = 1
            else:
                start_time = time_as_int()
                active = True
                window['-STARTSTOP-'].update('Stop')
                window['-KOLO-'].update(visible=True)
    if active:
        elapsed_time = round(time_as_int() - start_time, 1)
        window['-CAS-'].update('{:02d}:{:02d}.{:02d}'.format((elapsed_time // 100) // 60,
                                                             (elapsed_time //
                                                              100) % 60,
                                                             elapsed_time % 100))
        if elapsed_time == max:
            window['-CAS-'].update('STOP')
            active = False
    if event == '-KOLO-':
        if active:
            window.extend_layout(
                window['-KOLA-'], [[sg.Text(pocet_kol), sg.VSeparator(),
                                    sg.Text('{:02d}:{:02d}.{:02d}'.format((elapsed_time // 100) // 60,
                                                                          (elapsed_time //
                                                                           100) % 60,
                                                                          elapsed_time % 100))]])
            pocet_kol += 1
        else:
            start_time = start_time + time_as_int() - paused_time
            window['-KOLO-'].update('Kolo')
            window['-STARTSTOP-'].update('Stop')
            active = True
window.close()
