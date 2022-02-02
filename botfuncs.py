import time
from pyautogui import *
import pyautogui
from python_imagesearch.imagesearch import *
import win32api, win32con
import codecs

# constants
padding = 12
cellDim = 99
boardDim = 4

pathLetters = {
    "å": "ao",
    "ä": "ae",
    "ö": "oe"
  }

def readAllWords():
  with codecs.open("data/words.txt", encoding="utf-8") as file:
    return [line.rstrip("\n").rstrip("\r") for line in file]

def findLocations():
  startBox = None
  while startBox == None:
      startBox = pyautogui.locateOnScreen("data/start.png", grayscale=True, confidence=0.9)

      if startBox != None:
          return startBox

      time.sleep(0.05)

def getPathLetter(letter):
  return letter if not letter in pathLetters else pathLetters[letter]

def setupBoard(startX, startY):
  board = []
  
  for y in range(boardDim):
    for x in range(boardDim):
      screenX = startX + (cellDim + padding) * x
      screenY = startY + (cellDim + padding) * y
      
      #missing Q, W
      alphabet = u'åäöabcdefghijklmnoprstuvxyz'
      im = region_grabber(
        (int(screenX), 
        int(screenY), 
        int(screenX) * 2 + cellDim, 
        int(screenY) * 2 + cellDim))

      for letter in alphabet:
        imgPath = u'data/{}.png'.format(getPathLetter(letter))
        pos = imagesearcharea(imgPath, 
          screenX, screenY, screenX + cellDim, screenY + cellDim, 0.99, im)

        if pos[0] != -1:
          board.append(letter)
          break

  return board

def findCompatibleWords(board, allWords):
  compatibleWords = []
  for word in allWords:
      available = board[:]
      compatible = True
      for letter in word:
          if available.count(letter) > 0:
              available.remove(letter)
          else:
              compatible = False
              break

      if compatible:
          compatibleWords.append(word)

  return compatibleWords

def outOfBounds(x, y):
  index = y * boardDim + x

  return (x < 0 or 
          x >= boardDim or 
          y < 0 or 
          y >= boardDim or 
          index < 0 or 
          index >= (boardDim * boardDim))

def tryGetPath(word, board, x, y, path):
  if word == "" or path == None:
    return path

  boardIndex = y * boardDim + x
  
  if (outOfBounds(x, y) or 
      board[boardIndex] != word[0] or
      path.count(boardIndex) > 0):
    return None

  path.append(boardIndex)
  
  for yOff in range(-1, 2):
    for xOff in range(-1, 2):
      if yOff == 0 and xOff == 0:
        continue

      newPath = tryGetPath(word[1:], board, x + xOff, y + yOff, path[:])
      if newPath != None:
        return newPath

  return None
  
def findPath(word, board):
  for y in range(boardDim):
    for x in range(boardDim):
      index = y * boardDim + x
      if board[index] == word[0]:
        path = tryGetPath(word, board, x, y, []) 
        if path != None:
          return path

  return None

def executePath(path, startX, startY):
  start = path[0]
  centerOffset = cellDim / 2

  x = int((start % boardDim) * (cellDim + padding) + startX + centerOffset)
  y = int(int(start / boardDim) * (cellDim + padding) + startY + centerOffset)

  win32api.SetCursorPos((x,y))
  time.sleep(0.05)
  win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
  time.sleep(0.05)

  for i in range(len(path) - 1):
    next = path[i + 1]
    x = int((next % boardDim) * (cellDim + padding) + startX + centerOffset)
    y = int(int(next / boardDim) * (cellDim + padding) + startY + centerOffset)
    win32api.SetCursorPos((x, y))
    time.sleep(0.05)

  win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
  time.sleep(0.05)
