import time
import sys
from PIL import ImageGrab
from PIL import Image
import pyautogui
from pathlib import Path
path = Path(__file__).parent.absolute()

#========= hard coding RGBA values ========
emptyA = (162, 209, 73)
emptyB = (170, 215, 81)
discoveredA = (229, 194, 159)
discoveredB = (215, 184, 153)
one = (25, 118, 210)
two = (56, 142, 60)
three = (214, 148, 125)
threeB = (224, 155, 130)
four = (227, 191, 159)
fourB = (214, 182, 153)
five = (255, 143, 0)
# six =
# seven =
# eight = 
#==========================================

#========= hard coding board size =========
#where it is on the screen
x0 = 745
y0 = 214
x1 = 1287
y1 = 636

#how big the board is
BoxesX = 18
BoxesY = 14
#==========================================

sizeY = int(y1-y0)
sizeX = int(x1-x0)

middle = [x0 + int(sizeX/2) , y0 + int(sizeY/2)]

#=======================================

unexplored = "-"
mine = "*"
safe = "s"
unclear = ";"
def setIdentity(RGBA):
    if RGBA == emptyA or RGBA == emptyB:
        return unexplored
    if RGBA == discoveredA or RGBA == discoveredB:
        return 0
    if RGBA == one:
        return 1
    if RGBA == two:
        return 2
    if RGBA == three or RGBA == threeB:
        return 3
    if RGBA == four or RGBA == fourB:
        return 4
    if RGBA == five:
        return 5

#=======================================
#Show mental board
def print_board():
    #print board
    output = ""
    for i in range(BoxesY):
        for j in range(BoxesX):
            output += str(board[i][j]["identity"]) + " "
        output = output[:-1]
        output += "\n"
    output = output[:-1]
    print(output)
    #print board perimeter
    p = ""
    for box in perimeter:
        p += str(box["identity"]) + " "
    if p == "":
        p = "empty"
    else :
        p = p[:-1]
    print("Perimeter : \n" + p)
    if p == "empty":
        sys.exit()
#=======================================

def Take_Picture():
    global pix
    image = ImageGrab.grab(bbox=(x0,y0,x1,y1))
    image.save(path / "board.png")
    im = Image.open(path / "board.png")
    pix = im.load()
    Scan()

# Scan board

board = []
perimeter = []

def Scan():
    global board
    board = []
    for i in range(BoxesY):
        board.append([])
        for j in range(BoxesX):
            x = int(sizeX/BoxesX)*(j+1) - int((sizeX/BoxesX)/2)
            y = int(sizeY/BoxesY)*(i+1) - int((sizeY/BoxesY)/2) - 5
            RGBA = pix[x,y]
            #print("color on (" + str(i) + "," + str(j) + ") is : " + str(RGBA))
            board[i].append({
                "identity" : setIdentity(RGBA) ,
                "location" : ( x0+x , y0+y ) ,
                "mental_location": ( i , j ),
                "color" : RGBA
            })

    getPerimeter()

#=======================================

def isValid(y,x):
    return (x >= 0 and y >= 0 and x < BoxesX and y < BoxesY)

def getAround(i,j):
    return [(i-1,j-1),(i,j-1),(i+1,j-1),(i-1,j),(i+1,j),(i-1,j+1),(i,j+1),(i+1,j+1)]

def IS(item,i,j):
    return board[i][j]["identity"] == item

def getPerimeter():
    global perimeter
    perimeter = []
    for i in range(BoxesY):
        for j in range(BoxesX):
            n = board[i][j]["identity"]
            if type(n) == int and n != 0 :
                perimeter.append(board[i][j])

def refresh():
    for i in range(BoxesY):
        for j in range(BoxesX):
            if IS(safe,i,j):
                x,y = board[i][j]["location"]
                pyautogui.click(x,y)
    pyautogui.moveTo(middle[0],y0-20)
    time.sleep(1)
    Take_Picture()

def Solve():
    global board
    solved = False
    for box in perimeter:
        i,j = box["mental_location"]
        identity = board[i][j]["identity"]
        unconstrained = getAround(i,j)
        around_blocks = [ c for c in unconstrained if isValid(c[0],c[1]) ]
        constraints = [ c for c in around_blocks if IS(unexplored,c[0],c[1]) ]
        mines = [ c for c in around_blocks if IS(mine,c[0],c[1]) ]
        m = len(mines)
        if m == identity:
            for c in constraints:
                board[c[0]][c[1]]["identity"] = safe
            continue
        if len(constraints) == identity - m:
            for c in constraints:
                board[c[0]][c[1]]["identity"] = mine
                print("Found mine on (%d,%d)!!" % (c[0],c[1]))
                solved = True
    if solved :
        print("Recursing.....")
        Solve()
        return

    refresh()
    print_board()
    Solve()
    
    
#=======================================

if __name__ == "__main__":

    pyautogui.click(middle[0],middle[1])
    pyautogui.moveTo(middle[0],y0-20)
    time.sleep(1)

    Take_Picture()

    print_board()

    Solve()

