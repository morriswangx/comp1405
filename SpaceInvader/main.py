# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import pygame


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
#if __name__ == '__main__':
#    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

# Initialize the pygame
pygame.init()

screenMaxWidth = 1200
screenMaxHeight = 1000
amove = 1
leftEdgeWidth = 50
rightEdgeWidth = 100

screen = pygame.display.set_mode((screenMaxWidth, 1000))

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load("spaceship-small.png")
playerX = 550
playerY = 880
direc = "EB"

def player(x,y):
    screen.blit(playerImg, (x,y))



running = True
while running:

    # RGB: red, green and blue
    screen.fill((155, 228, 118))
    if playerX <(screenMaxWidth-rightEdgeWidth) and direc == "EB":
        playerX += amove
        print(playerX)

    else:
        print(playerX)
        if playerX == screenMaxWidth-rightEdgeWidth or playerX >screenMaxWidth-rightEdgeWidth:
            direc = "WB"
            playerX -= amove
        if playerX > leftEdgeWidth and direc == "WB":
            playerX -= amove
            if playerX == leftEdgeWidth or playerX < leftEdgeWidth:
                direc = "EB"

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player(playerX, playerY)
    pygame.display.update()
