import pygame
import random
import pygame.font

# screen
pygame.init()
screen = pygame.display.set_mode((640, 360))
clock = pygame.time.Clock()
pygame.display.set_caption("Flappy Bird Clone")
running = True
dt = 0
left_boundary = 0
right_boundary = 0
top_boundary = 0
bottom_boundary = 340
game_over_font = pygame.font.Font("BaiJamjuree-Bold.ttf", 40)


# music loop
pygame.mixer.music.load("Fluffing-a-Duck.mp3")
pygame.mixer.music.play(-1)

#player variables
player_pos = pygame.Vector2(36, 32)

player_image = pygame.draw.circle(screen, "white", player_pos, 40)
score = 0
gravity = 0

pipe_width = 70
pipe_gap = 150
pipe_speed = 5

class Pipe:
    def __init__(self, x):
        self.top = random.randint(0, 60)
        self.bottom = self.top + pipe_gap
        self.x = x
        
    def move(self):
        self.x -= pipe_speed
        
    def draw(self):
        pygame.draw.rect(screen, "GREEN", (self.x, 0, pipe_width, self.top))
        pygame.draw.rect(screen, "GREEN", (self.x, self.bottom, pipe_width, 360 - self.bottom))

def create_pipes():
    x = 640
    pipe = Pipe(x)
    if pipe.x + pipe_width < left_boundary:
        return create_pipes()
    else:
        return pipe

pipes = []
pipes.append(create_pipes())

#game loop
while running:
    gravity = 2.25
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    for pipe in pipes:
        pipe.move()
        if pipe.x + pipe_width < left_boundary:
            pipes.remove(pipe)
            pipes.append(create_pipes())

    screen.fill("Light Blue")

    pygame.draw.circle(screen, "white", player_pos, 15)
    player_pos.y += gravity

    #jumping:
    def jumping():
        gravity = 0
        player_pos.y -= 500 * dt

    for pipe in pipes:
        pipe.draw()

    # hit detection
    if player_pos.x + 20 > pipe.x and player_pos.x - 20 < pipe.x + pipe_width:
        if player_pos.y - 20 < pipe.top or player_pos.y + 20 > pipe.bottom:
            game_over_surface = game_over_font.render("Game Over", True, (0, 100, 255))
            game_over_rect = game_over_surface.get_rect()
            game_over_rect.center = (640 // 2, 360 // 2)
            screen.blit(game_over_surface, game_over_rect)
            pygame.display.flip()
            pygame.time.wait(1000)
            
    # score system
    
    #fps counter
    font = pygame.font.Font("BaiJamjuree-Bold.ttf", 25)
    fps = int(clock.get_fps())
    fps_text = font.render(f"FPS: {fps}", True, (255, 255, 255))
    screen.blit(fps_text, (screen.get_width() - fps_text.get_width() - 10, 10))
    pygame.display.update()

    #keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        jumping()
    
    #game over
    if player_pos.y > bottom_boundary:
        player_pos.y = bottom_boundary
        game_over_surface = game_over_font.render("Game Over", True, (0, 100, 255))
        game_over_rect = game_over_surface.get_rect()
        game_over_rect.center = (640 // 2, 360 // 2)
        screen.blit(game_over_surface, game_over_rect)
    
    # print("playercoords: ", player_pos)
    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
