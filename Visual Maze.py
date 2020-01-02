import pygame, queue, time
from tkinter import *
from tkinter import ttk, messagebox
import time

def CreateMaze():
    maze = []
    maze.append([" " for i in range(8)])
    maze.append([" " for i in range(8)])
    maze.append([" " for i in range(8)])
    maze.append([" " for i in range(8)])
    maze.append([" " for i in range(8)])
    maze.append([" " for i in range(8)])
    maze.append([" " for i in range(8)])
    maze.append([" " for i in range(8)])
    
    return maze

black = (0,0,0)

def draw_grid(maze,screen):
    for no,row in enumerate(maze):
        y = 50*no+20
        for pos,el in enumerate(row):
            x = pos*50+20
            if el==" ":
                pygame.draw.rect(screen,black,[x,y,50,50],3)
            elif el=="#":
                pygame.draw.rect(screen,black,[x,y,50,50])
    
    
wnd = Tk()
wnd.config(bg="black")
wnd.geometry("400x320+150+150")
wnd.title("Maze Settings")
wnd.iconbitmap("icon.ico")

maze = CreateMaze()

font = ("Helvetica,12,bold")
Label(wnd,text=" ",bg="black").pack()

Label(wnd,text="Enter Starting Point Coords",font=font,fg="white",bg="black").pack()
start_coords = ttk.Entry(wnd,font=font)
start_coords.pack(fill=X)
Label(wnd,text=" ",bg="black").pack()

Label(wnd,text="Enter Ending Point Coords",font=font,fg="white",bg="black").pack()
end_coords = ttk.Entry(wnd,font=font)
end_coords.pack(fill=X)
Label(wnd,text=" ",bg="black").pack()

Label(wnd,text="Enter Obstacle Coords",font=font,fg="white",bg="black").pack()
obs_coords = ttk.Entry(wnd,font=font)
obs_coords.insert(0,"(0, 0);(0, 1);(0, 2);(0, 3);(0, 4);(0, 5);(0, 6);(7, 7)")
obs_coords.pack(fill=X)
Label(wnd,text=" ",bg="black").pack()

def gamePlay():
    s_coords = [int(start_coords.get()[1:-1].split(",")[0]),int(start_coords.get()[1:-1].split(",")[1])]
    e_coords = [int(end_coords.get()[1:-1].split(",")[0]),int(end_coords.get()[1:-1].split(",")[1])]
    o_coords = []

    for coords in obs_coords.get().split(";"):
        o_coords.append([int(coords[1:-1].split(",")[0]),int(coords[1:-1].split(",")[1])])
        
    start_x=s_coords[0]
    start_y=s_coords[1]
    maze[start_y][start_x] = "O"

    end_x = e_coords[0]
    end_y = e_coords[1]
    maze[end_y][end_x] = "X"

    for coords in o_coords:
        maze[coords[1]][coords[0]] = "#"
    
    start = pygame.image.load('starter.png')
    target = pygame.image.load('target.png')

    def valid(maze, moves):
        for no, row in enumerate(maze):
            for x, pos in enumerate(row):
                if pos == "O":
                    start = x
                    cur = no

        i = start
        j = cur
        for move in moves:
            if move == "L":
                i -= 1

            elif move == "R":
                i += 1

            elif move == "U":
                j -= 1

            elif move == "D":
                j += 1

            if not(0 <= i < len(maze[0]) and 0 <= j < len(maze)):
                return False
            elif (maze[j][i] == "#"):
                return False

        return True


    def findEnd(maze, moves):
        for no, row in enumerate(maze):
            for x, pos in enumerate(row):
                if pos == "O":
                    start = x
                    cur = no
        
        i = start
        j = cur
        positions = [[i,j]]
        for move in moves:
            if move == "L":
                i -= 1

            elif move == "R":
                i += 1

            elif move == "U":
                j -= 1

            elif move == "D":
                j += 1
            positions.append([i,j])
            
        if maze[j][i] == "X":
            #print("Found: " + moves)
            return True,positions,moves
        
        return False,positions,moves


    # MAIN ALGORITHM
    nums = queue.Queue()
    nums.put("")
    add = ""

    while not findEnd(maze, add)[0]: 
        add = nums.get()
        #print(add)
        for j in ["L", "R", "U", "D"]:
            put = add + j
            if valid(maze, put):
                nums.put(put)
                positions = findEnd(maze,put)[1]
                moves = findEnd(maze,put)[2]
                
    positions = positions[1:-1]
    
    running = 1
    count = 0
    
    while running:
        width,height = (450,450)
        screen = pygame.display.set_mode((width,height))
        pygame.display.set_caption('PathFinder')
        white = (255,255,255)
        screen.fill(white)
        icon = pygame.image.load('icon.ico')
        pygame.display.set_icon(icon)

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running = 0
            if event.type==pygame.KEYDOWN and event.key==pygame.K_RETURN:
                running = 0
                

        screen.blit(start,(start_x*50+30,start_y*50+30))
        screen.blit(target,(end_x*50+30,end_y*50+30))
        draw_grid(maze,screen)
        yellow = (255,255,0)
        blue = (0,0,155)
        
        for pos in positions:
            x = pos[0]*50+20
            y = 50*pos[1]+20
            if positions.index(pos)==len(positions)-1:
                pygame.draw.rect(screen,blue,[x,y,50,50])
            else:
                pygame.draw.rect(screen,yellow,[x,y,48,48])
            pygame.display.flip()
            time.sleep(0.5)

        if count==0:
            messagebox.showinfo("Path Found!",moves)
            count+=1
            
        pygame.display.flip()
       
    pygame.quit()

submit = Button(wnd,text="View Path!",font=font,command=gamePlay)
submit.pack()



    
    
