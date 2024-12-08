from os import environ

# Stop It!
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

import pygame, sys
from pygame.locals import *

FPS = 25  # frames per second, general speed of program
WINDOWWIDTH = 800  # size of window's width in pixels
WINDOWHEIGHT = 600  # size of window's height in pixels
CELLSIZE = 150  # size of cell width & height in pixels
CELLWIDTH = 6
SCALE = 3
GAPSIZE = 9  # size of gap between cells in pixels
BOARDWIDTH = 3  # number of columns
BOARDHEIGHT = 3  # number of rows
assert BOARDWIDTH == BOARDHEIGHT == 3, "only modified for (3×3)×(3×3) \
mega tic tac toe"
XMARGIN = (WINDOWWIDTH - (BOARDWIDTH * (CELLSIZE + GAPSIZE))
- GAPSIZE) // 2
YMARGIN = (WINDOWHEIGHT - (BOARDHEIGHT * (CELLSIZE + GAPSIZE))
- GAPSIZE) // 2
XYMARGIN = (CELLSIZE - (BOARDWIDTH * (((CELLSIZE - BOARDWIDTH *
(GAPSIZE + 1) * 2) // SCALE) + GAPSIZE))) // 2
# ((CELLSIZE - BOARDWIDTH * (GAPSIZE + 1) * 2) // SCALE) // 2

#                  R     G     B
BLACK = (  0,     0,     0)
CYAN   = (   0, 255, 255)
LIME    = (   0, 255,     0)
PINK    = (255, 192, 192)
WHITE = (255, 255, 255)

BGCOLOR = BLACK
HIGHLIGHTCOLOR = CYAN
HOVERCOLOR = LIME
CELLCOLOR = PINK
TEXTCOLOR = WHITE
X = "X"
O = "O"
ALLPLAYERS = [X, O]

pygame.init()
fontSizes = (36, 216)
smallFont = pygame.font.SysFont("29lt arapix", size = fontSizes[0])
smallFont.set_script("Arab")
smallFont.set_direction(DIRECTION_RTL)
bigFont = pygame.font.SysFont("29lt arapix", size = fontSizes[1])
bigFont.set_script("Arab")
bigFont.set_direction(DIRECTION_RTL)

smallx = smallFont.render(X, True, TEXTCOLOR)
smallo = smallFont.render(O,True, TEXTCOLOR)
bigx = bigFont.render(X, True, TEXTCOLOR)
bigo = bigFont.render(O, True, TEXTCOLOR)
smallxw, smallxh = smallx.get_rect()[2:]
smallow, smalloh = smallo.get_rect()[2:]
bigxw, bigxh = bigx.get_rect()[2:]
bigow, bigoh = bigo.get_rect()[2:]

# winning conditions
WINCONDS = [
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6)]


# Game Loop:
#    Handle Events
#    Update the Game State
#    Draw the Game State on Screen
def main():
    global FPSCLOCK, DISPLAYSURF, turn, moves
    turn = X
    moves = 1
    TURNPROMPT = smallFont.render(f"نوبت {turn}", True, TEXTCOLOR)
    MOVESPROMPT = smallFont.render(f"حرکت شماره {moves}", True, TEXTCOLOR)
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    mousex = 0  # used to store x coordinate of mouse event
    mousey = 0  # used to store y coordinate of mouse event
    pygame.display.set_caption("MEGA TIC TAC TOE")

    DISPLAYSURF.fill(BGCOLOR)
    XPROMPT = smallFont.render(X, True, PINK)
    OPROMPT = smallFont.render(O,True, PINK)
    TURNPROMPTW, TURNPROMPTH = TURNPROMPT.get_rect()[2:]
    MOVESPROMPTW, MOVESPROMPTH = MOVESPROMPT.get_rect()[2:]
    XPROMPTW, XPROMPTH = XPROMPT.get_rect()[2:]
    OPROMPTW, OPROMPTH = OPROMPT.get_rect()[2:]
    DISPLAYSURF.blit(TURNPROMPT, ((WINDOWWIDTH - TURNPROMPTW) // 2, 20 -
TURNPROMPTH // 2))
    DISPLAYSURF.blit(MOVESPROMPT, ((WINDOWWIDTH - MOVESPROMPTW) // 2, -50 +
WINDOWHEIGHT - MOVESPROMPTH // 2))
    board = [*[(None, True)] * 9]
    subBoard = [*[(None, True)] * 81]
    board, subBoard = drawBoard(board, subBoard, None)

    while True:
        cellx, celly, index = getCellAtPixel(mousex, mousey)
        XPROMPT = smallFont.render(X, True, PINK)
        OPROMPT = smallFont.render(O,True, PINK)
        DISPLAYSURF.fill(BGCOLOR)
        TURNPROMPT = smallFont.render(f"نوبت {turn}", True, TEXTCOLOR)
        MOVESPROMPT = smallFont.render(f"حرکت شماره {''.join(reversed(str(moves)))}", True, TEXTCOLOR)
        board, subBoard = drawBoard(board, subBoard, index)
        DISPLAYSURF.blit(TURNPROMPT, ((WINDOWWIDTH - TURNPROMPTW) // 2,
20 - TURNPROMPTH // 2))
        DISPLAYSURF.blit(MOVESPROMPT, ((WINDOWWIDTH - MOVESPROMPTW) //
2, - 50 + WINDOWHEIGHT - MOVESPROMPTH // 2))
        if cellx != None and celly != None:
            conqurer, available = board[index // 9]
            subconqurer, subavailable = subBoard[index]
            if available and subavailable:
                XPROMPT = smallFont.render(X, True, HOVERCOLOR)
                OPROMPT = smallFont.render(O,True, HOVERCOLOR)
                if turn == X:
                    DISPLAYSURF.blit(XPROMPT, (cellx - XPROMPTW // 2 +
fontSizes[0] // 16 + ((CELLSIZE - BOARDWIDTH * (GAPSIZE + 1) * 2) //
SCALE) // 2, celly - XPROMPTH // 2 - fontSizes[0] // 4 + ((CELLSIZE -
BOARDHEIGHT * (GAPSIZE + 1) * 2) // SCALE) // 2))
                    if mouseClicked:
                        board, subBoard = makeMove(board, subBoard, index)
                        board, subBoard = hasWon(board, subBoard, index)
                else:
                    DISPLAYSURF.blit(OPROMPT, (cellx - OPROMPTW // 2 +
fontSizes[0] // 16 + ((CELLSIZE - BOARDWIDTH * (GAPSIZE + 1) * 2) //
SCALE) // 2, celly - OPROMPTH // 2 - fontSizes[0] // 4 + ((CELLSIZE -
BOARDHEIGHT * (GAPSIZE + 1) * 2) // SCALE) // 2))
                    if mouseClicked:
                        board, subBoard = makeMove(board, subBoard, index)
                        board, subBoard = hasWon(board, subBoard, index)
            else:
                if turn == X:
                    DISPLAYSURF.blit(XPROMPT, (mousex - XPROMPTW // 2 +
fontSizes[0] // 16, mousey - XPROMPTH // 2 - fontSizes[0] // 4))
                else:
                    DISPLAYSURF.blit(OPROMPT, (mousex - XPROMPTW // 2 +
fontSizes[0] // 16, mousey - XPROMPTH // 2 - fontSizes[0] // 4))
        else:
            if turn == X:
                DISPLAYSURF.blit(XPROMPT, (mousex - XPROMPTW // 2 +
fontSizes[0] // 16, mousey - XPROMPTH // 2 - fontSizes[0] // 4))
            else:
                DISPLAYSURF.blit(OPROMPT, (mousex - XPROMPTW // 2 +
fontSizes[0] // 16, mousey - XPROMPTH // 2 - fontSizes[0] // 4))

        mouseClicked = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def winAnimation(winner):
    time = 10
    color1 = PINK
    color2 = CYAN
    while time >= 0:
        if winner:
            text = f"{winner} برنده شد شروع دوباره {''.join(reversed(str(time)))}"
        else:
            text = f"هيچکس برنده نشد شروع دوباره {''.join(reversed(str(time)))}"
        prompt = smallFont.render(text, True, TEXTCOLOR)
        w, h = prompt.get_rect()[2:]
        DISPLAYSURF.fill(color1)
        color1, color2 = color2, color1
        DISPLAYSURF.blit(prompt, (WINDOWWIDTH // 2 - w // 2, WINDOWHEIGHT // 2 - h // 2))
        time -= 1
        pygame.display.update()
        pygame.time.wait(1000)
    


def hasWon(board, subBoard, target):
    global moves
    start = target // 9 * 9
    end = start + 9
    subwins = {}
    wins = {}
    WIN = False
    sublist = subBoard[start: end]
    for index, cell in enumerate(sublist):
        conqurer, available = cell
        if conqurer:
            subwins[index] = conqurer
    for cond in WINCONDS:
        for player in ALLPLAYERS:
            win = 0
            for cell in cond:
                if cell in subwins:
                    if subwins[cell] == player:
                        win += 1
                        if win == 3:
                            board[target // 9] = (player, False)
                            for index, ceell in enumerate(board):
                                conqurer, available = ceell
                                if conqurer:
                                    wins[index] = conqurer
                    else:
                        win = 0
    else:
        if len(subwins) == 9:
            if not board[target // 9][0]:
                board[target // 9] = (False, False)
    if len(wins):
        for cond in WINCONDS:
            for player in ALLPLAYERS:
                win = 0
                for cell in cond:
                    if cell in wins:
                        if wins[cell] == player:
                            win += 1
                            if win == 3:
                                WIN = player
                                win = 0
                                break
                        else:
                            win = 0
    if WIN:
        winAnimation(WIN)
        board = [*[(None, True)] * 9]
        subBoard = [*[(None, True)] * 81]
        moves -= moves
    else:
        for i, cell in enumerate(board):
            if cell[1]:
                break
        else:
            for i, cell in enumerate(board):
                if not cell[1] and cell[0] == None:
                    board[i] = (None, True)
    return (board, subBoard)


def getCellAtPixel(x, y):
    index = 0
    target = None
    for celly in range(BOARDHEIGHT):
        for cellx in range(BOARDWIDTH):
            for subcelly in range(BOARDHEIGHT):
                for subcellx in range(BOARDWIDTH):
                    left, top = leftTopCoordsOfCell(cellx, celly, subcellx, subcelly)
                    boxRect = pygame.Rect(left, top, ((CELLSIZE -
BOARDWIDTH * (GAPSIZE + 1) * 2) // SCALE), ((CELLSIZE - BOARDWIDTH *
(GAPSIZE + 1) * 2) // SCALE))
                    if boxRect.collidepoint(x, y):
                        return (left, top, index)
                    index += 1
    return (None, None, None)


def leftTopCoordsOfCell(cellx, celly, *args):
    # Convets board coordinates to pixel coordinates
    left = WINDOWWIDTH - XMARGIN - ((cellx + 1) * (CELLSIZE + GAPSIZE))
    top = celly * (CELLSIZE + GAPSIZE) + YMARGIN
    if args:
        subcellx, subcelly = args
        left = left + CELLSIZE - ((subcellx + 1) * (CELLSIZE + GAPSIZE) // SCALE) + XYMARGIN
        top = top = top + subcelly * ((CELLSIZE) //SCALE) + XYMARGIN - 5
    return (left, top)


def makeMove(boardState, subBoardState, index):
    global turn, moves
    board = boardState
    subBoard = subBoardState
    subBoard[index] = (turn, False)
    target = index % 9
    if turn == X:
        turn = O
    else:
        turn = X
    moves += 1
    for i, cell in enumerate(board):
        conqurer, available = cell
        if i == target:
            if conqurer == None:
                board[i] = (conqurer, True)
        else:
            board[i] = (conqurer, False)
    return (board, subBoard)


def drawBoard(boardState, subBoardState, target):
    board = boardState
    subBoard = subBoardState
    index = 0
    index2 = 0
    for celly in range(BOARDHEIGHT):
        for cellx in range(BOARDWIDTH):
            conqurer, available = board[index]
            left, top = leftTopCoordsOfCell(cellx, celly)
            color = CELLCOLOR
            color2 = HIGHLIGHTCOLOR
            color3 = HOVERCOLOR
            if available:
                if not target:
                    color, color2 = color2, color
                else:
                    if index == target % 9:
                        if board[target // 9][1]:
                            color, color3 = color3, color
                        else:
                            color, color2 = color2, color
                    else:
                        color, color2 = color2, color
            else:
                if target:
                    if index == target % 9:
                        if board[target // 9][1]:
                            color, color3 = color3, color
            pygame.draw.rect(DISPLAYSURF, color, (left, top, CELLSIZE,
CELLSIZE), CELLWIDTH)
            if conqurer:
                if conqurer == X:
                    DISPLAYSURF.blit(bigx, (left - bigxw // 2 +
fontSizes[1] // 16 + CELLSIZE // 2, top - bigxh // 2 - fontSizes[1] //
4 + CELLSIZE // 2))
                else:
                    DISPLAYSURF.blit(bigo, (left - bigow // 2 +
fontSizes[1] // 16 + CELLSIZE // 2, top - bigoh // 2 - fontSizes[1] //
4 + CELLSIZE // 2))
            board[index] = (conqurer, available)
            for subcelly in range(BOARDHEIGHT):
                for subcellx in range(BOARDWIDTH):
                    subconqurer, subavailable = subBoard[index2]
                    color = CELLCOLOR
                    color2 = HIGHLIGHTCOLOR
                    color3 = HOVERCOLOR
                    subleft, subtop = leftTopCoordsOfCell(cellx, celly,
subcellx, subcelly)
                    if available and subavailable and not subconqurer:
                        color, color2 = color2, color
                        subBoard[index2] = (subconqurer, subavailable)
                    else:
                        subBoard[index2] = (subconqurer, subavailable)
                    if not conqurer:
                        pygame.draw.rect(DISPLAYSURF, color, (subleft,
subtop, ((CELLSIZE - BOARDWIDTH * (GAPSIZE + 1) * 2) // SCALE), ((CELLSIZE
- BOARDHEIGHT * (GAPSIZE + 1) * 2) // SCALE)), CELLWIDTH // SCALE)
                        if subconqurer:
                            if subconqurer == X:
                                DISPLAYSURF.blit(smallx, (subleft -
smallxw // 2 + fontSizes[0] // 16 + ((CELLSIZE - BOARDWIDTH * (GAPSIZE +
1) * 2) // SCALE) // 2, subtop - smallxh // 2 - fontSizes[0] // 4 + ((
CELLSIZE - BOARDWIDTH * (GAPSIZE + 1) * 2) // SCALE) // 2))
                            else:
                                DISPLAYSURF.blit(smallo, (subleft -
smallow // 2 + fontSizes[0] // 16 + ((CELLSIZE - BOARDWIDTH * (GAPSIZE +
1) * 2) // SCALE) // 2, subtop - smalloh // 2 - fontSizes[0] // 4 + ((
CELLSIZE - BOARDWIDTH * (GAPSIZE + 1) * 2) // SCALE) // 2))
                    index2 += 1
            index += 1
    return (board, subBoard)


if __name__ == "__main__":
    main()
