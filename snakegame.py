import pygame
import sys
import random

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLOCK_SIZE = 20

GRID_WIDTH = SCREEN_WIDTH // BLOCK_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // BLOCK_SIZE

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

WHITE = (255, 255, 255)
RED = (255, 0, 0)

food_image = pygame.image.load('apple.png').convert_alpha()
food_image = pygame.transform.scale(food_image, (BLOCK_SIZE, BLOCK_SIZE))
snake_head_image = pygame.image.load('snake.png')
snake_head_image = pygame.transform.scale(snake_head_image, (BLOCK_SIZE, BLOCK_SIZE))
snake_body_image = pygame.image.load('snake.png')
snake_body_image = pygame.transform.scale(snake_body_image, (BLOCK_SIZE, BLOCK_SIZE))
snake_tail_image = pygame.image.load('snake.png')  # Load tail image
snake_tail_image = pygame.transform.scale(snake_tail_image, (BLOCK_SIZE, BLOCK_SIZE))  # Scale tail image


border_color = (WHITE)
border_thickness = 4

def drawSnake(snake, direction):
    for i, segment in enumerate(snake):
        x, y = segment
        x *= BLOCK_SIZE
        y *= BLOCK_SIZE
        if i == 0:
            if direction == pygame.math.Vector2(1, 0):
                screen.blit(pygame.transform.rotate(snake_head_image, 0), (x, y))
            elif direction == pygame.math.Vector2(0, -1):
                screen.blit(pygame.transform.rotate(snake_head_image, 90), (x, y))
            elif direction == pygame.math.Vector2(0, 1):
                screen.blit(pygame.transform.rotate(snake_head_image, -90), (x, y))
            elif direction == pygame.math.Vector2(-1, 0):
                screen.blit(pygame.transform.rotate(snake_head_image, 180), (x, y))
        elif i == len(snake) - 1:
            if direction == pygame.math.Vector2(1, 0):
                screen.blit(pygame.transform.rotate(snake_tail_image, 0), (x, y))
            elif direction == pygame.math.Vector2(0, -1):
                screen.blit(pygame.transform.rotate(snake_tail_image, 90), (x, y))
            elif direction == pygame.math.Vector2(0, 1):
                screen.blit(pygame.transform.rotate(snake_tail_image, -90), (x, y))
            elif direction == pygame.math.Vector2(-1, 0):
                screen.blit(pygame.transform.rotate(snake_tail_image, 180), (x, y))
        else:
            if direction == pygame.math.Vector2(1, 0):
                screen.blit(pygame.transform.rotate(snake_body_image, 0), (x, y))
            elif direction == pygame.math.Vector2(0, -1):
                screen.blit(pygame.transform.rotate(snake_body_image, 90), (x, y))
            elif direction == pygame.math.Vector2(0, 1):
                screen.blit(pygame.transform.rotate(snake_body_image, -90), (x, y))
            elif direction == pygame.math.Vector2(-1, 0):
                screen.blit(pygame.transform.rotate(snake_body_image, 180), (x, y))

def checkBorderCollision(snake):
    #head = snake[0]
    #if not screen.get_rect().contains(head):
        #return True
    #return False
    head_x, head_y = snake[0]
    if head_x < 0 or head_x >= GRID_WIDTH or head_y < 0 or head_y >= GRID_HEIGHT:
        return True
    return False

def displayGameOver():
    game_over_text = font.render("GAME OVER", True, WHITE)
    game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    play_again_text = font.render("'P' to play agin 'Q' to quit", True, WHITE)
    play_again_rect = play_again_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
    screen.blit(game_over_text, game_over_rect)
    screen.blit(play_again_text, play_again_rect)
    pygame.display.flip()

def main():
    snake = [(5, 12), (4, 12), (3, 12)]
    #snake = [pygame.Rect(100, 250, BLOCK_SIZE, BLOCK_SIZE), pygame.Rect(80, 250, BLOCK_SIZE, BLOCK_SIZE), pygame.Rect(60, 250, BLOCK_SIZE, BLOCK_SIZE)]
    direction = pygame.math.Vector2(1, 0)
    #food = pygame.Rect(400, 300, BLOCK_SIZE, BLOCK_SIZE)
    food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction.y != 1:
                    direction = pygame.math.Vector2(0, -1)
                elif event.key == pygame.K_DOWN and direction.y != -1:
                    direction = pygame.math.Vector2(0, 1)
                elif event.key == pygame.K_LEFT and direction.x != 1:
                    direction = pygame.math.Vector2(-1, 0)
                elif event.key == pygame.K_RIGHT and direction.x != -1:
                    direction = pygame.math.Vector2(1, 0)

        new_head = (snake[0][0] + direction.x, snake[0][1] + direction.y)
        #new_head = pygame.Rect(snake[0].x + direction.x * BLOCK_SIZE, snake[0].y + direction.y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
        snake.insert(0, new_head)

        #if new_head.colliderect(food):
            #food.x = random.randint(0, (SCREEN_WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
            #food.y = random.randint(0, (SCREEN_HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        if new_head == food:
            food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1)) 
        else:
            snake.pop()

        #if checkBorderCollision(snake) or any(segment.colliderect(snake[0]) for segment in snake[1:]):
            #game_over = True
            
        if checkBorderCollision(snake) or any(segment == snake[0] for segment in snake[1:]):
            game_over = True

        screen.fill((0, 0, 0))
        drawSnake(snake, direction)
        #screen.blit(food_image, food)
        screen.blit(food_image, (food[0] * BLOCK_SIZE, food[1] * BLOCK_SIZE))


        pygame.display.flip()
        clock.tick(10)

   
    displayGameOver()
    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    main()  # Restart the game
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()


if __name__ == "__main__":
    main()
