import PySimpleGUI as sg
import os

import subprocess

noFont = ("Helvetica", 1)


games = ['ssbb','punch','metroid','sports']

buttons = [sg.Button(game, image_filename=f'./assets/{game}.png', font=noFont) for game in games]
stopButton = sg.Button("Stop", visible=False)

debugBox = sg.Checkbox('Debug:', default=False, key="-DEBUG-")


layout = [
    [sg.Text("Choose your controller", size=(40, 1))], 
    [stopButton],
    buttons,
    [debugBox]
]

# Create the window
window = sg.Window("unKinect", layout, font=("Helvetica", 18))


process = None

# Create an event loop
while True:
    event, values = window.read()

    if event in games:
        buttons[0].hide_row()
        debugBox.hide_row()
        stopButton.unhide_row()
        stopButton.update(visible=True)

        gameIndex = games.index(event)
        process = subprocess.Popen(['/usr/local/anaconda3/envs/fastpose/bin/python3', 'pyMove.py', str(values["-DEBUG-"]), str(gameIndex)])

    if event == 'Stop':
        if process:
            process.terminate()
            process = None
        stopButton.update(visible=False)
        stopButton.hide_row()
        buttons[0].unhide_row()
        debugBox.unhide_row()


    
    if event == sg.WIN_CLOSED:
        if process:
            process.terminate()
        break

window.close()