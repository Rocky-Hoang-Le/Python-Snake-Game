# Snake game project
# Goal is to recreate snake using python with pygame module without looking up any tutorials

# Import required modules
import pygame
import random

pygame.init()  # Initialize pygame

# Game window attributes
screen_width = 640
screen_height = 480
window = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Snake Game')  # Sets the title of the game window


# SnakeBlock class which gives information about each part of the snakes position
class SnakeBlock:
    snake_count = 0
    size = (20, 20)

    def __init__(self, _pos):
        self.x, self.y = _pos

    def __str__(self):
        return f'I am SnakeBlock# {SnakeBlock.snake_count} and i am at position{(self.x, self.y)}'


# Food class which will hold position and size information about the food
class Food:
    food_count = 0
    size = (15, 15)

    def __init__(self, _pos):
        self.x, self.y = _pos
        Food.food_count += 1

    def __str__(self):
        return f'I am Food# {Food.food_count}, and i am at position{(self.x, self.y)}'


# Main game loop and initial values
run = True
dead = False
vel = 5  # Snake speed
snake = [SnakeBlock((x, 50)) for x in range(90, 10, -20)]  # Store snakeblocks in a list which creates the snake
random_pos = (random.randint(0, screen_width - Food.size[0]), random.randint(0, screen_height - Food.size[1]))
food = Food(random_pos)  # produce food at a random position on the screen
facing = {'Left': False, 'Right': True, 'Up': False,
          'Down': False}  # Dictionary to dictate which direction the snake is facing
score = 0

# Render Score text
font = pygame.font.SysFont('TIMES.ttf', 32)
text = font.render(f'Score: {score}', True, (255, 255, 255), (0, 0, 0))
text_rect = text.get_rect()
text_rect.center = (50, 12)

while run:
    # Setup Game functions and systems
    pygame.time.delay(25)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    if Food.food_count < 1:
        random_pos = (random.randint(0, screen_width - Food.size[0]), random.randint(0, screen_height - Food.size[1]))
        food = Food(random_pos)

    # Function to add to the snake based on the direction the snake is facing
    def add_snake():
        if facing['Right']:
            snake.insert(0, SnakeBlock((snake[0].x + 15, snake[0].y)))
        if facing['Left']:
            snake.insert(0, SnakeBlock((snake[0].x - 15, snake[0].y)))
        if facing['Up']:
            snake.insert(0, SnakeBlock((snake[0].x, snake[0].y - 15)))
        if facing['Down']:
            snake.insert(0, SnakeBlock((snake[0].x, snake[0].y + 15)))

    # Function to check if the snake head is touching any part of the snakes body or the walls
    def snake_death(block):
        if facing['Right']:
            if snake[0].x + 5 == block.x and snake[0].y == block.y:
                return True
        if facing['Left']:
            if snake[0].x - 5 == block.x and snake[0].y == block.y:
                return True
        if facing['Up']:
            if snake[0].x == block.x and snake[0].y - 5 == block.y:
                return True
        if facing['Down']:
            if snake[0].x == block.x and snake[0].y + 5 == block.y:
                return True
        if snake[0].x >= screen_width - snake[0].size[0] or snake[0].x <= 0 or \
                snake[0].y >= screen_height - snake[0].size[0] or snake[0].y <= 0:
            return True

        return False


    # Check if snake is dead and if so perform a play again check
    keys = pygame.key.get_pressed()  # returns all key presses and stores it
    # This block checks if the snake is dead and if so produce game over screen
    for block in range(1, len(snake)):
        if snake_death(snake[block]):
            facing.update((k, False) for k in facing)
            vel = 0
            font = pygame.font.SysFont('TIMES.ttf', 32)
            text = font.render('You Lose! Play again? x = yes, z = no', True, (255, 255, 255), (0, 0, 0))
            text_rect = text.get_rect()
            text_rect.center = (screen_width / 2, screen_height / 2)
            window.blit(text, text_rect)
            dead = True
            break
    # This block is for receiving input as to whether or not the player wishes to continue or quit
    if dead:
        if keys[pygame.K_x]:
            snake.clear()
            vel = 5
            snake = [SnakeBlock((x, 50)) for x in range(90, 10, -20)]
            random_pos = (
                random.randint(0, screen_width - Food.size[0]), random.randint(0, screen_height - Food.size[1]))
            food = Food(random_pos)
            score = 0
            text = font.render(f'Score: {score}', True, (255, 255, 255), (0, 0, 0))
            text_rect = text.get_rect()
            text_rect.center = (50, 12)
            window.blit(text, text_rect)
            facing['Right'] = True
        elif keys[pygame.K_z]:
            run = False

    # This block of code is for moving the snake by removing the tail, moving the snake, then inserting what was
    # removed back to the front of list
    snake.pop()
    if keys[pygame.K_RIGHT] or facing['Right']:
        facing.update((k, False) for k in facing)
        facing['Right'] = True
        snake[0].x += vel

    if keys[pygame.K_LEFT] or facing['Left']:
        facing.update((k, False) for k in facing)
        facing['Left'] = True
        snake[0].x -= vel

    if keys[pygame.K_UP] or facing['Up']:
        facing.update((k, False) for k in facing)
        facing['Up'] = True
        snake[0].y -= vel

    if keys[pygame.K_DOWN] or facing['Down']:
        facing.update((k, False) for k in facing)
        facing['Down'] = True
        snake[0].y += vel
    snake.insert(0, SnakeBlock((snake[0].x, snake[0].y)))

    # Draws the Game and check if when to add to snake and if game over
    window.fill((0, 0, 0))
    food_mask = pygame.Rect(food.x, food.y, Food.size[0], Food.size[1])
    snake_head_mask = pygame.Rect(snake[0].x, snake[0].y, SnakeBlock.size[0], SnakeBlock.size[1])

    # Check if snake touches food
    if snake_head_mask.colliderect(food_mask):
        score += 1
        text = font.render(f'Score: {score}', True, (255, 255, 255), (0, 0, 0))
        random_pos = (random.randint(0, screen_width - Food.size[0]), random.randint(0, screen_height - Food.size[1]))
        food = Food(random_pos)
        add_snake()

    # Draw snake, food, score text and update display
    for block in snake:
        pygame.draw.rect(window, (0, 255, 0), (block.x, block.y, SnakeBlock.size[0], SnakeBlock.size[1]))

    pygame.draw.rect(window, (0, 0, 255), food_mask)
    window.blit(text, text_rect)
    pygame.display.update()

pygame.display.quit()
pygame.quit()
