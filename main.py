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
  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.body = [Vector2(x, y), Vector2(x - 1, y), (x - 2, y)]
    self.rect = pygame.Rect(self.x, self.y, 32, 32)
    self.velX = 0
    self.velY = 0
    self.left_pressed = False
    self.right_pressed = False
    self.up_pressed = False
    self.down_pressed = False
    self.vector = Vector2(0,0)
    self.crashed = False
    self.angle = 0
    self.score = 0

  # draws snake on screen
  def draw(self, window):
    for block in self.body:
      block_rect = pygame.Rect(block[0] * cell_size, block[1] * cell_size, cell_size, cell_size)
      pygame.draw.rect(screen,(128,0,128), block_rect)

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

# creating text font and colour
font = pygame.font.SysFont('Arial', 24)
black = (0, 0, 0)

# creating a grid
cell_size = 25 # size of each cell in the grid
cell_number = 26 # number of grids and an axis
screen = pygame.display.set_mode((cell_size * cell_number, cell_size * cell_number))

# giving the window a name
pygame.display.set_caption("Snek")

# making a colour for the background
background = (0, 175, 0)

# loading images from computer into the program
startImg = pygame.image.load("start").convert_alpha()
snakeHead = pygame.image.load("snakeHead.png").convert_alpha()
snakeBody = pygame.image.load("snakeBody.png").convert_alpha()
snakeEnd = pygame.image.load("snakeEnd.png").convert_alpha()
fruitImg = pygame.image.load("fruit.png").convert_alpha()

# making a button using the image
startButton = Button(20, 10, startImg, 0.2)

gameStarted = False
gameOver = False
snake = Snake(cell_number / 2, cell_number / 2)
apple = Fruit(fruitImg)

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
        snake.left_pressed = True
        snake.up_pressed = False
        snake.down_pressed = False
      if event.key == pygame.K_RIGHT and not snake.left_pressed:
        snake.right_pressed = True
        snake.up_pressed = False
        snake.down_pressed = False
      if event.key == pygame.K_UP and not snake.down_pressed:
        snake.up_pressed = True
        snake.right_pressed = False
        snake.left_pressed = False
      if event.key == pygame.K_DOWN and not snake.up_pressed:
        snake.down_pressed = True
        snake.right_pressed = False
        snake.left_pressed = False

    # ending the game when the snake hits the edge
    if snake.crashed and not gameOver:
      print("Game over")
      gameStarted = False
      snake.x = cell_size * cell_number / 2
      snake.y = cell_size * cell_number / 2
      gameOver = True

  # giving the screen its colour
  screen.fill(background)

  # pressing a button will turn one of the boolean values to true
  if not gameStarted:
    screen.fill(background)
    if startButton.draw(screen):
      gameStarted = True

  if gameStarted:
    # making the background and drawing the score, snake and fruit on top
    screen.fill(background)
    snake.draw(screen)
    apple.draw(cell_size * cell_number, cell_size * cell_number, screen, snake.body)
    print(apple.position)
    screen.blit(score, (0, 0))
    if apple.position == snake.body[0]:  # checking if the head of the snake is in the same position as the fruit
      snake.score += 1 # increasing score
      pygame.display.update() # updating the screen to show new score

  pygame.display.update()
  # updating the screen

pygame.quit()
