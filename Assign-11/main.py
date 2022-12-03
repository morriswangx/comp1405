import pygame.font
import sys

pygame.init()
pygame.font.init()

# Window colors
SCREEN_R = 212
SCREEN_G = 224
SCREEN_B = 236


win = pygame.display.set_mode((1200, 900))
# refresh frequency
FREQUENCY = 120
clock = pygame.time.Clock()
# Step 1 - Load the font
font = pygame.font.SysFont("Verdana", 30)

# Step 2 - Render the font
myText = font.render("Pygame font and text", True, [0,9,120])


def updateText(size, text, color, x, y):
    # blit the names
    myfont = pygame.font.SysFont("arial", size, True)
    textSurface = myfont.render(text, True, color)
    TextRect = textSurface.get_rect()
    TextRect.center = [x, y]
    win.blit(textSurface, TextRect)

Running = True
while Running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    win.fill((SCREEN_R, SCREEN_G, SCREEN_B))
    updateText(29, "text", [255,0,0], 500, 450)
    # Step 3 - Draw the text
    win.blit(myText, [100, 200])
    pygame.display.update()
    clock.tick(FREQUENCY)