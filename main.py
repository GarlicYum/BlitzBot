from tkinter import *
from tkinter.ttk import *
from botfuncs import *

# constants
yOffset = 493

# variables
allWords = readAllWords()

def runHack():
    startTime = time.time()
    timeLimit = 82
    startBox = findLocations()
    startX = startBox.left
    startY = startBox.top - yOffset
    board = setupBoard(startX, startY)
    compatibleWords = findCompatibleWords(board, allWords)

    for word in compatibleWords:

        path = findPath(word, board)
        if path != None:
            executePath(path, startX, startY)

        if(time.time() - startTime) > timeLimit:
            break

window = Tk(className="Blitz Bot")
window.geometry("400x200")
button = Button(window, text='Heck', width=20, command=runHack)
button.place(relx = 0.5, rely = 0.5, anchor = CENTER)
window.mainloop()
