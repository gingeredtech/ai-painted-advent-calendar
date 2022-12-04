import pygame
import sys
import time
import random
import datetime
import webbrowser
import config

HEIGHT = config.HEIGHT
WIDTH = config.WIDTH
LINEHEIGHT = 30
CLICKABLEHEIGHT = 150
FONT = 'verdana'

# Colors
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
WHITE = (255, 255, 255)
RED = (200, 0, 0)

# use a seeded random shuffle on numbers 1 to 25 
# specify seed to always generate the same random sequence of door labels for our 5x5 grid
doormap=list(range(1,HEIGHT*WIDTH+1))
random.seed(1) 
random.shuffle(doormap)

#get current time
d = datetime.datetime.now()
#get the day of month
datemax=int(d.strftime("%d"))

#lambda function to convert eg 1 to 1st, 2 to 2nd
ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4])


# Create game
pygame.init()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Finxter Advent Calendar')

#font_name = 'calibr'#pygame.font.get_default_font()
bigfont = pygame.font.SysFont(FONT, 20)
hugefont = pygame.font.SysFont(FONT, 40)

# Compute board size
BOARD_PADDING = 10
board_width = width - (BOARD_PADDING * 2)
board_height = height - (BOARD_PADDING * 2)
cell_size = int(min(board_width / WIDTH, board_height / HEIGHT))
halfcell_size=cell_size/2+10
board_origin = (BOARD_PADDING, BOARD_PADDING)

# utility function to add text to screen
def addText(text, position, color):
    giftText = bigfont.render(text, True, color)
    giftRect = giftText.get_rect()
    giftRect.center = position
    screen.blit(giftText, giftRect)

# start from the main grid when dooropen>0 it indicate the door/image to display
dooropen=0

while True:

    # Check if game quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(BLACK)

    if dooropen:

        # paint the correct image onto the screen
        filename='images/image'+ (f"{dooropen:02d}") +".jpg"
        image = pygame.image.load(filename)
        rect = image.get_rect()
        screen.blit(image, rect)

        # going to create a semi transparent clickable area which can link to a URL 
        # the URL 'gifts' are stored in the imported config
        giftlabel,gifturl = config.gifts[dooropen%len(config.gifts)]
        s = pygame.Surface((width,CLICKABLEHEIGHT))  
        s.set_alpha(200)            
        s.fill(GRAY)
        screen.blit(s, (0,height-CLICKABLEHEIGHT))
        clickable = pygame.Rect(0,height-CLICKABLEHEIGHT,width,CLICKABLEHEIGHT)

        # add text to the clickable area
        if(dooropen==25):
            addText("It's Christmas!", ((width / 2), 4*cell_size+LINEHEIGHT), RED)
        else: 
            addText("On the "+ ordinal(25-dooropen) +" night before xmas", ((width / 2), 4*cell_size), WHITE)
            addText("Finxter brought unto me:", ((width / 2), 4*cell_size+LINEHEIGHT), WHITE)
            addText(giftlabel, ((width / 2), 4*cell_size+(2*LINEHEIGHT)), RED)

        # open URL in browser if clickable area clicked
        # otherwise close the door by setting dooropen to 0
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if clickable.collidepoint(mouse) :
                time.sleep(0.2)
                webbrowser.open(gifturl, new=dooropen, autoraise=True)
            else:
               dooropen = 0
            time.sleep(0.2)

        pygame.display.flip()
        continue

    # Draw board
    cells = []
    for i in range(HEIGHT):
        row = []
        for j in range(WIDTH):

            # Draw rectangle for cell
            rect = pygame.Rect(
                board_origin[0] + j * cell_size,
                board_origin[1] + i * cell_size,
                cell_size, cell_size
            )
            pygame.draw.rect(screen, GRAY, rect)
            pygame.draw.rect(screen, WHITE, rect, 3)

            doornumber=doormap[(j*HEIGHT)+i]

            label = hugefont.render(str(doornumber), True, RED if doornumber<=datemax else WHITE)
            labelRect = label.get_rect()
            labelRect.center = (j * cell_size+halfcell_size, i * cell_size+halfcell_size)
            screen.blit(label, labelRect)

            row.append(rect)
        cells.append(row)

    move = None

    left, _, right = pygame.mouse.get_pressed()

    if left:
        mouse = pygame.mouse.get_pos()
        for i in range(HEIGHT):
            for j in range(WIDTH):
                if cells[i][j].collidepoint(mouse) and dooropen==0:
                    dooropen=doormap[(j*HEIGHT)+i]
                    # did they attempt to open a door ahead of current date
                    # dont allow that!
                    if dooropen>datemax:
                        dooropen=0
                    time.sleep(0.2)

    pygame.display.flip()
