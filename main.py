import pygame, random
from pygame.math import Vector2

# button class
class Button():
  # constructor
  def __init__(self, x, y, image, scale):
    width = image.get_width()
    height = image.get_height()
    self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
    self.rect = self.image.get_rect()
    self.rect.topleft = (x, y)
    self.clicked = False

  # method to create the button on screen
  def draw(self, surface):
    action = False
    # getting mouse position
    pos = pygame.mouse.get_pos()

    # check if clicked or not
    if self.rect.collidepoint(pos):
      if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
        self.clicked = True
        action = True

    # drawing button on screen
    surface.blit(self.image, (self.rect.x, self.rect.y))

    return action

# snake class
class Snake():
  # constructor
  def __init__(self, x, y, head, middle, end):
    self.x = x
    self.y = y
    self.body = [Vector2(x, y), Vector2(x - 1, y), (x - 2, y)]
    self.left_pressed = False
    self.right_pressed = False
    self.up_pressed = False
    self.down_pressed = False
    self.vector = Vector2(0,0)
    self.crashed = False
    self.angle = 0
    self.score = 0
    self.head = pygame.transform.scale(head, (cell_size, cell_size))
    self.middle = pygame.transform.scale(middle, (cell_size, cell_size))
    self.end = pygame.transform.scale(end, (cell_size, cell_size))

  # draws snake on screen
  def draw(self, window):
    for index, block in enumerate(self.body):
      block_rect = pygame.Rect(block[0] * cell_size, block[1] * cell_size, cell_size, cell_size)
      # makes a 'block' in the place where the item will appear on screen

      if index == 0: # checks if the current block is for the head
        if self.vector == (0,0) or self.vector == (1,0): # checks if the snake is stationary or moving right
          newHead = self.head # makes a copy of the head
        elif self.vector == (-1, 0): # checks if the snake is moving left
          newHead = pygame.transform.rotate(self.head, 180) # makes a copy of the head that is rotated 180 degrees
        elif self.vector == (0, 1): # checks if the snake is moving down
          newHead = pygame.transform.rotate(self.head, 270) # makes a copy of the snake that is rotated 270 degrees anti-clockwise
        elif self.vector == (0, -1): # checks if the snake is moving up
          newHead = pygame.transform.rotate(self.head, 90) # makes a copy of the snake that is rotated 90 degrees anti-clockwise

        screen.blit(newHead, block_rect) # shows the head on screen with the right location and orientation

      elif index == len(snake.body) - 1: # checks if the current block is for the end of the snake
        if snake.body[index - 1][0] > snake.body[index][0]: # checks if the previous block is right of the current block
          newEnd = self.end # makes a copy of the end
        elif snake.body[index - 1][0] < snake.body[index][0]: # checks if the previous block is left of the current block
          newEnd = pygame.transform.rotate(self.end, 180) # makes a copy of the end that is rotated 180 degrees
        elif snake.body[index - 1][1] < snake.body[index][1]: # checks if the previous block is above the current block
          newEnd = pygame.transform.rotate(self.end, 90) # makes a copy of the snake that is rotated 90 degrees anti-clockwise
        elif snake.body[index - 1][1] > snake.body[index][1]: # checks if the previous block is below the current block
          newEnd = pygame.transform.rotate(self.end, 270) # makes a copy of the snake that is rotated 270 degrees anti-clockwise

        screen.blit(newEnd, block_rect) # shows the end of the snake on screen with the right location and orientation

      else:
        screen.blit(self.middle, block_rect) # shows the middle part of the snake on screen at the right location

  # moving the snake
  def move(self):
    # if the snake crashes it no longer moves
    if self.crashed:
      self.vector = (0,0)

    else:
      # creating the vector which is used to move the snake
      if self.left_pressed:
        self.vector = Vector2(-1, 0)
      if self.right_pressed:
        self.vector = Vector2(1, 0)
      if self.up_pressed:
        self.vector = Vector2(0, -1)
      if self.down_pressed:
        self.vector = Vector2(0, 1)

    if self.vector != (0,0): # prevents adjustments to the snake when it isn't moving
      self.body.insert(0, self.body[0] + self.vector) # creates a new block in the new position
      if len(self.body) > self.score + 3:
        self.body.pop(-1) # whenever the difference between body length and score is more than 3 the tail is removed

  def detectCrash(self):
    if not (self.body[0][0] >= 0 and self.body[0][0] < cell_number and self.body[0][1] >= 0 and self.body[0][1] < cell_number):
      self.crashed = True

    for i in range(1, len(self.body)):
      if self.body[0] == self.body[i]:
        self.crashed = True
        break

# fruit class
class Fruit():
  # constructor
  def __init__(self, image):
    self.image = pygame.transform.scale(image, (cell_size, cell_size))
    self.position = Vector2(-1, -1)

  # drawing the fruit on the screen
  def draw(self, width, height, window, list):
    while self.position in list or self.position == (-1,-1):
      self.position = Vector2(random.randint(0, cell_number - 1), random.randint(0, cell_number - 1))
    window.blit(self.image, self.position * cell_size)
    self.drawn = True

pygame.init()

# creating text fonts and colours
font = pygame.font.SysFont('Calibri', 24)
titleFont = pygame.font.SysFont('Calirbri', 36, False, False)
black = (0, 0, 0)
white = (255, 255, 255)

# creating a grid
cell_size = 25 # size of each cell in the grid
cell_number = 26 # number of grids and an axis
screen = pygame.display.set_mode((cell_size * cell_number, cell_size * cell_number))

# giving the window a name
pygame.display.set_caption("Snek")

# making a colour for the background
background = (0, 175, 0)

# creating images from text
startImg = font.render(("Start"), True, black, background)
retryImg = font.render(("Retry"), True, black, background)
mainMenuImg = font.render(("Main Menu"), True, black, background)
welcomeImg = titleFont.render(("WELCOME TO SNEK"), True, white, background)
gameOverImg = titleFont.render(("GAME OVER"), True, white, background)

# loading images from computer into the program
snakeHead = pygame.image.load("snakeHead.png").convert_alpha()
snakeBody = pygame.image.load("snakeBody.png").convert_alpha()
snakeEnd = pygame.image.load("snakeEnd.png").convert_alpha()
fruitImg = pygame.image.load("fruit.png").convert_alpha()

# making buttons using the images
startButton = Button(cell_size, 3 * cell_size, startImg, 1)
retryButton = Button(cell_size, (cell_size * cell_number - retryImg.get_height())/ 2, retryImg, 1)
mainMenuButton = Button(cell_size * (cell_number - 1) - mainMenuImg.get_width(), (cell_size * cell_number - mainMenuImg.get_height())/ 2, mainMenuImg, 1)

# game states
gameStarted = False
gameOver = False
mainMenu = True

snake = Snake(cell_number / 2, cell_number / 2, snakeHead, snakeBody, snakeEnd)

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 83) # screen is updated every 83 milliseconds

# main gameplay loop
run = True
while run:
  score = font.render(("Score: " + str(snake.score)), True, black, background)
  for event in pygame.event.get():
    # ending the game when the window is closed
    if event.type == pygame.QUIT:
        run = False

    if event.type == SCREEN_UPDATE:
      snake.move()
      snake.detectCrash()

    # changing the direction of movement depending on the key that was pressed
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_LEFT and not snake.right_pressed:
        pygame.time.delay(83)
        snake.left_pressed = True
        snake.up_pressed = False
        snake.down_pressed = False
      if event.key == pygame.K_RIGHT and not snake.left_pressed:
        pygame.time.delay(83)
        snake.right_pressed = True
        snake.up_pressed = False
        snake.down_pressed = False
      if event.key == pygame.K_UP and not snake.down_pressed:
        pygame.time.delay(83)
        snake.up_pressed = True
        snake.right_pressed = False
        snake.left_pressed = False
      if event.key == pygame.K_DOWN and not snake.up_pressed:
        pygame.time.delay(83)
        snake.down_pressed = True
        snake.right_pressed = False
        snake.left_pressed = False

    # checking if the game should end
    gameOver = snake.crashed

  # giving the screen its colour
  screen.fill(background)

  # pressing a button change the game states
  if mainMenu:
    gameOver = False
    screen.blit(welcomeImg, ((cell_number * cell_size - welcomeImg.get_width()) / 2, cell_size)) # displays welcome
    if startButton.draw(screen): # draws button on screen and checks if it's clicked
      # changing game state
      gameStarted = True
      mainMenu = False

      startButton.clicked = False # allows the button to be clicked again later
      snake = Snake(cell_number / 2, cell_number / 2, snakeHead, snakeBody, snakeEnd) # instantiates snake object
      apple = Fruit(fruitImg) # instantiates apple object
      apple.position = (-1, -1) # causes the apple to be assigned a random location on screen

  if gameStarted:
    screen.blit(score, (0, 0))
    if apple.position == snake.body[0]:  # checking if the head of the snake is in the same position as the fruit
      snake.score += 1 # increasing score
      pygame.display.update() # updating the screen to show new score

    snake.draw(screen) # draws the snake on the screen
    apple.draw(cell_size * cell_number, cell_size * cell_number, screen, snake.body) # draws the apple in a random position on the screen

  if gameOver:
    gameStarted = False # ends the game
    scoreImg = font.render(("Your score was "+str(snake.score)), True, black, background) # making an image to display the score
    screen.blit(gameOverImg, ((cell_number * cell_size - gameOverImg.get_width()) / 2, cell_size)) # displaying game over
    screen.blit(scoreImg, ((cell_size * cell_number - scoreImg.get_width()) / 2, (cell_size * cell_number) / 4)) # displays score obtained
    if retryButton.draw(screen): # draws retry button on screen and checks if it's been clicked
      # changing game states
      gameStarted = True
      gameOver = False

      retryButton.clicked = False # allows the button to be clicked later
      snake = Snake(cell_number / 2, cell_number / 2, snakeHead, snakeBody, snakeEnd) # instantiates new snake
      apple.position = (-1, -1) # causes the apple to be drawn at a random location on screen

    if mainMenuButton.draw(screen): # draws main menu button on screen and checks if it's been clicked
      # changing game states
      mainMenu = True
      gameOver = False

      mainMenuButton.clicked = False # allows the button to be clicked later

  pygame.display.update()
  # updating the screen

pygame.quit()