import pygame, sys
import pygame.draw as draw
import pygame.gfxdraw
import time
import math
pygame.init()
screen = pygame.display.set_mode((1000, 800), vsync=1)
pygame.display.set_caption("Reversi", "Reversi")



global show_legal_movesQSize
opposite = {1:2, 2:1}
winner = None
cheats = False
show_legal_movesQ = True
show_legal_movesQSize = 1
GAME = "Othello"
Usernameplayer1 = "Black"
Usernameplayer2 = "White"
animationsflip = True
animationsplace = True
animationslegals = True
animationflipincre = 2
animationflipspeed = 0
animationplaceincre = 1
animationplacespeed = 0.005
animationlegalsincre = 1
animationlegalsspeed = 0.005

arrows = [
    [(0,0),(100,0)]
]

def draw_aacircle(surface, x, y, r, color):
    pygame.gfxdraw.filled_circle(surface, x, y, r, color)
    pygame.gfxdraw.aacircle(surface, x, y, r, color)

def draw_aacircle_outline(surface, x, y, r, color, width):
    pygame.draw.circle(surface, color, (x,y), r, width)
    pygame.gfxdraw.aacircle(surface, x,y, r, color)
    pygame.gfxdraw.aacircle(surface, x-1,y-1, r, color)
    pygame.gfxdraw.aacircle(surface, x-1,y, r, color)
    pygame.gfxdraw.aacircle(surface, x,y-1, r, color)

    pygame.gfxdraw.aacircle(surface, x,y, r-width, color)
    pygame.gfxdraw.aacircle(surface, x-1,y-1, r-width, color)
    pygame.gfxdraw.aacircle(surface, x-1,y, r-width, color)
    pygame.gfxdraw.aacircle(surface, x,y-1, r-width, color)

def draw_board_grid():
    colorswitch = False
    for x in range(8):
        colorswitch = not colorswitch
        for y in range(8):
            colorswitch = not colorswitch
            if (x == 3 or x == 4) and (y == 3 or y == 4):
                draw.rect(screen, (0,170,0), (x*100, y*100, 100, 100))
            elif colorswitch:
                draw.rect(screen, (0,150,0), (x*100, y*100, 100, 100))
            elif not colorswitch:
                draw.rect(screen, (0,140,0), (x*100, y*100, 100, 100))

def draw_aaline(surface, color, start, end, width):
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    distance = int(max(abs(dx), abs(dy)))
    for i in range(distance):
        x = int(start[0] + float(i) / distance * dx)
        y = int(start[1] + float(i) / distance * dy)
        draw_aacircle(surface, x, y, width, color)

def draw_aatriangle(surface, color, x, y, size, angle):
    #draw a triangle with an angle(rotation)
    draw.polygon(surface, color, ((x,y),(x+size*math.cos(angle),y+size*math.sin(angle)),(x+size*math.cos(angle+math.pi/2),y+size*math.sin(angle+math.pi/2))))

def draw_board_grid_lines():
    for i in range(0,800,100):
        pygame.draw.line(screen, (0,0,0), (i,0), (i,800), 2)
        pygame.draw.line(screen, (0,0,0), (0,i), (800,i), 2)

def draw_board_orientationpoints():
    draw_aacircle(screen, 201,201, 8, (0,0,0))
    draw_aacircle(screen, 601,201, 8, (0,0,0))
    draw_aacircle(screen, 201,601, 8, (0,0,0))
    draw_aacircle(screen, 601,601, 8, (0,0,0))

def draw_board_discs():
    for x in range(8):
            for y in range(8):
                if grid[y][x] == 1:
                    draw_aacircle(screen, 50+100*x,50+100*y, 39, (0,0,0))
                elif grid[y][x] == 2:
                    draw_aacircle(screen, 50+100*x,50+100*y, 39, (255,255,255))

def reset_board():
    #resets the board
    global grid, player_turn, winner
    grid = [[0 for _ in range(8)] for _ in range(8)]
    grid[4][4] = 2
    grid[3][3] = 2
    grid[4][3] = 1
    grid[3][4] = 1
    player_turn = 1
    winner = None

def check_line(grid, x,y,val,piece,amount,continue_check = False, nextx = 0, nexty = 0):
    if (x > -1 and x < 8 and y > -1 and y < 8):
        if continue_check:
            if is_posev(grid, x, y, val):
                return check_line(grid, x+nextx, y+nexty, val, piece, amount+1, continue_check=True, nextx=nextx, nexty=nexty)
            elif is_posev(grid, x, y, piece):
                return amount+1
            else:
                return 0
        else:
            if is_posev(grid, x, y, 0) and is_posev(grid, x+nextx, y+nexty, val):
                return check_line(grid, x+nextx, y+nexty, val, piece, amount+1, continue_check=True, nextx=nextx, nexty=nexty)
            else: return 0
    else: 
        return 0

def is_posev(grid, x,y,val):
    #IS POSition Equal to Val
    if x > -1 and x < 8 and y > -1 and y < 8:
        if grid[y][x] == val:
            return True
    return False

def flip_line(grid, x,y,val,piece,amount, nextx = 0, nexty = 0, rep = 0):
    if (x > -1 and x < 8 and y > -1 and y < 8):
        if rep <= 2:
            return grid
        else:
            grid[y][x] = piece
            if animationsflip:
                draw_board_grid()
                draw_board_grid_lines()
                draw_board_orientationpoints()
                draw_board_discs()
                for color in range(0,255, animationflipincre):
                    time.sleep(animationflipspeed)
                    if grid[y][x] == 1:
                        draw_aacircle(screen, 50+100*x,50+100*y, 39, (255-color,255-color,255-color))
                    elif grid[y][x] == 2:
                        draw_aacircle(screen, 50+100*x,50+100*y, 39, (color,color,color))
                    pygame.display.update()
            return flip_line(grid, x+nextx, y+nexty, val, piece, amount+1, nextx=nextx, nexty=nexty, rep=rep-1)
    return grid

def check_all(grid, gridposx,gridposy,val,piece,amount):
    mousedown = pygame.mouse.get_pressed()[0]
    nexts = [[-1,0],[-1,-1],[0,-1],[1,-1],[1,0],[1,1],[0,1],[-1,1]]
    placable = False
    for i in range(len(nexts)):
        if check_line(grid, gridposx, gridposy, val, piece, amount, continue_check=False, nextx=nexts[i][0], nexty=nexts[i][1]) > 0:
            placable = True
    return placable

def play_check_all(grid, gridposx,gridposy,val,piece,amount,next_turn):
    player_turn = piece
    old_grid = grid
    mousedown = pygame.mouse.get_pressed()[0]
    nexts = [[-1,0],[-1,-1],[0,-1],[1,-1],[1,0],[1,1],[0,1],[-1,1]]
    flips = []
    placable = False
    reps = 0
    for i in range(len(nexts)):
        reps = check_line(old_grid, gridposx, gridposy, val, piece, amount, continue_check=False, nextx=nexts[i][0], nexty=nexts[i][1])
        if check_line(old_grid, gridposx, gridposy, val, piece, amount, continue_check=False, nextx=nexts[i][0], nexty=nexts[i][1]) > 0:
            if not mousedown:
                if piece == 1:
                    draw_aacircle_outline(screen, newpos[0], newpos[1], 39, (0,30,0), 5)
                else:
                    draw_aacircle_outline(screen, newpos[0], newpos[1], 39, (235,235,235), 5)
            if mousedown:
                flips.append([nexts[i], reps])
                placable = True
    if placable:
        if animationsplace:
            if player_turn == 1:
                colorchangespeed = 30/20
            else:
                colorchangespeed = 55/20
            colorchange = 0
            if show_legal_movesQ:
                #animation place
                for size in range(20,40, animationplaceincre):
                    colorchange += colorchangespeed
                    time.sleep(animationplacespeed)
                    if player_turn == 1: draw_aacircle(screen, 50+100*gridposx,50+100*gridposy, size, (30-colorchange,30-colorchange,30-colorchange))
                    elif player_turn == 2: draw_aacircle(screen, 50+100*gridposx,50+100*gridposy, size, (200+colorchange,200+colorchange,200+colorchange))
                    global show_legal_movesQSize
                    show_legal_movesQSize = 1
                    pygame.display.update()
            else:
                for size in range(0,40, animationplaceincre*2):
                    colorchange += colorchangespeed
                    time.sleep(animationplacespeed)
                    if player_turn == 1:
                        draw_aacircle(screen, 50+100*gridposx,50+100*gridposy, size, (30-colorchange,30-colorchange,30-colorchange))
                    elif player_turn == 2:
                        draw_aacircle(screen, 50+100*gridposx,50+100*gridposy, size, (200+colorchange,200+colorchange,200+colorchange))
                    pygame.display.update()
        grid[gridposy][gridposx] = player_turn
        player_turn = next_turn
        for i in range(len(flips)):
            grid = flip_line(grid, gridposx+flips[i][0][0], gridposy+flips[i][0][1], val, piece, amount, nextx=flips[i][0][0], nexty=flips[i][0][1], rep=flips[i][1])
    return player_turn, grid

def is_player_able_to_play(grid,player_turn):
    all_empty_spots = []
    able_to_move = False
    for x in range(8):
        for y in range(8):
            if grid[y][x] == 0:
                all_empty_spots.append((x,y))
    for i in range(len(all_empty_spots)):
        if check_all(grid, all_empty_spots[i][0], all_empty_spots[i][1], opposite[player_turn], player_turn, 0):
            able_to_move = True
    return able_to_move

def count_pieces(grid):
    white_pieces = 0
    black_pieces = 0
    white_pieces, black_pieces = sum(grid[y][x] == 2 for x in range(8) for y in range(8)), sum(grid[y][x] == 1 for x in range(8) for y in range(8))
    return white_pieces, black_pieces

def show_legal_moves(grid, player_turn, size=20):
    for x in range(8):
        for y in range(8):
            if check_all(grid, x, y, opposite[player_turn], player_turn, 0):
                if player_turn == 1:
                    draw_aacircle(screen, 50+x*100,50+y*100, size, (30,30,30))
                else:
                    draw_aacircle(screen, 50+x*100,50+y*100, size, (200,200,200))

def draw_arrow(screen, x1, y1, x2, y2, x3, y3, color,arrowheadsize = 30):
    draw_aaline(screen, color, (x1, y1), (x2, y2), 5)
    draw_aatriangle(screen, color, x3, y3, arrowheadsize, math.atan2(y2 - y1, x2 - x1)-255.25)


player_turn = 1
running = True
reset_board()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                reset_board()
            if cheats:
                if event.key == pygame.K_LALT:
                    player_turn = 1
                if event.key == pygame.K_RALT:
                    player_turn = 2
            if event.key == pygame.K_l:
                show_legal_movesQ = not show_legal_movesQ
            if event.key == pygame.K_c:
                cheats = not cheats
            if event.key == pygame.K_a:
                animationsflip = not animationsflip
                animationsplace = not animationsplace
                animationslegals = not animationslegals
    #Draw SideBarRight
    screen.fill((0,0,0))
    pygame.draw.rect(screen, (139,90,43), pygame.Rect(802,2,198,798))

    #InitFont
    font = pygame.font.SysFont("Arial", 30)
    white_pieces, black_pieces = count_pieces(grid)

    #Render Username1
    text = font.render(Usernameplayer1, 1, (255,255,255))
    screen.blit(text, (820, 50))
    pygame.draw.aaline(screen, (255,255,255), (820,80), (830+text.get_width(),80), 5)

    #Render Black Piece Counter
    draw_aacircle(screen, 830,115, 15, (0,0,0))
    text = font.render(str(black_pieces), True, (255,255,255))
    screen.blit(text, (850,100))

    #Render Username2
    text = font.render(Usernameplayer2, 1, (255,255,255))
    screen.blit(text, (820, 145))
    pygame.draw.aaline(screen, (255,255,255), (820,175), (830+text.get_width(),175), 5)

    #Render White Piece Counter
    draw_aacircle(screen, 830,205, 15, (255,255,255))
    text = font.render(str(white_pieces), True, (255,255,255))
    screen.blit(text, (850,190))
    
    #Draw Grid
    draw_board_grid()

    #Drawing Orientation Points
    draw_board_orientationpoints()

    #draw board grid lines
    draw_board_grid_lines()
    
    #Draw Legal Moves Animation
    if show_legal_movesQ:
        if animationslegals:
            time.sleep(animationlegalsspeed)
            if show_legal_movesQSize < 20: show_legal_movesQSize += animationlegalsincre
            if show_legal_movesQSize > 20: show_legal_movesQSize = 20
        else:
            show_legal_movesQSize = 20
        show_legal_moves(grid, player_turn, show_legal_movesQSize)

    #Draw Discs
    draw_board_discs()

    if not((is_player_able_to_play(grid, 1)) or (is_player_able_to_play(grid, 2))):
        white_pieces, black_pieces = count_pieces(grid)
        if white_pieces > black_pieces:
            text = font.render("White Wins", 1, (255,255,255))
            screen.blit(text, (825, 10))
        elif white_pieces < black_pieces:
            text = font.render("Black Wins", 1, (255,255,255))
            screen.blit(text, (825, 10))
        else:
            text = font.render("Draw", 1, (255,255,255))
            screen.blit(text, (865, 10))
    else:
        #Draw Game Title
        text = font.render(GAME, 1, (255,255,255))
        screen.blit(text, (850, 10))
    #Draw Game Title Underline
    pygame.draw.aaline(screen, (255,255,255), (820,40), (980,40), 5)

    pos = pygame.mouse.get_pos()
    gridposx = pos[0]//100
    gridposy = pos[1]//100

    if player_turn != 0 and winner == None:
        if is_player_able_to_play(grid, player_turn):
            newpos = (pos[0]//100*100 + 50, pos[1]//100*100 + 50)
            player_turn, grid = play_check_all(grid, gridposx, gridposy, opposite[player_turn], player_turn, 0, opposite[player_turn])
        else:
            if GAME == "Othello":
                player_turn = opposite[player_turn]
            elif GAME == "Reversi":
                winner = 3
    
    #if both cant play, Decide The Winner
    if not((is_player_able_to_play(grid, 1)) or (is_player_able_to_play(grid, 2))):
        white_pieces, black_pieces = count_pieces(grid)
        if white_pieces > black_pieces:
            text = font.render("White Wins", 1, (255,255,255))
            screen.blit(text, (825, 10))
            winner = 2
        elif white_pieces < black_pieces:
            text = font.render("Black Wins", 1, (255,255,255))
            screen.blit(text, (825, 10))
            winner = 1
        else:
            text = font.render("Draw", 1, (255,255,255))
            screen.blit(text, (865, 10))
            winner = 3
        #Reset Text
        font = pygame.font.SysFont("Arial", 25)
        text = font.render("Space to Reset", 1, (255,255,255))
        screen.blit(text, (815, 760))
    #check for cheats
    if cheats and winner == None:
        text = font.render("Cheats On", 1, (255,125,125))
        screen.blit(text, (815, 760))
    if player_turn == 3:
        winner = 3
    #draw_arrow(screen, 50+gridposx*100, 50+gridposy*100, 100+gridposy*100, 50+gridposy*100, 100+gridposy*100, 50+gridposy*100, (255,255,255))
    pygame.display.update()
