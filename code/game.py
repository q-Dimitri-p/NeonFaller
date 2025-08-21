import pygame
import sys
import random
from player import Player
from obstacle import Obstacle

class Game:
    def __init__(self):
        # Initialize pygame
        pygame.init()
        pygame.mixer.init()  # Initialize the mixer


        self.obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacle_timer, 2500)  # cria prédio a cada 2.5s


        # Score
        self.score = 0
        self.high_score = 0
        self.score_font = pygame.font.Font(None, 36)

        # Screen settings
        self.WIDTH = 400
        self.HEIGHT = 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Neon Faller")
        # Load background image
        self.bg_img = pygame.image.load("./assets/menubg.gif").convert()
        self.bg_img = pygame.transform.scale(self.bg_img, (self.WIDTH, self.HEIGHT))

        # Load static menu background image
        self.menu_bg_img = pygame.image.load("assets/newmenu.gif").convert()
        self.menu_bg_img = pygame.transform.scale(self.menu_bg_img, (self.WIDTH, self.HEIGHT))

        # Game state
        self.state = "menu"

        # Font
        self.font = pygame.font.Font(None, 48)  # default font
        self.small_font = pygame.font.Font(None, 32)



        # Clock
        self.clock = pygame.time.Clock()
        self.FPS = 60

        # Background color (later replace with cyberpunk image)
        self.bg_color = (10, 10, 30)

        # Create player
        self.player = Player(50, self.HEIGHT // 2, "assets/Airship.png")

        # Obstacles
        self.obstacles = []
        self.spawn_timer = 0
        self.spawn_interval = 6000  # milliseconds between buildings
        pygame.time.set_timer(self.obstacle_timer, 2500)  # milliseconds between buildings
        self.obstacle_width = 70
        self.obstacle_img = "./assets/building.gif"

        # Load menu music
        self.menu_music_path = "assets/menubgm.mp3"
        self.menu_music_playing = False

        # Load scene music
        self.scene_music_path = "assets/scene.mp3"

    def reset_game(self):
        self.player = Player(50, self.HEIGHT // 2, "assets/Airship.png")
        self.obstacles = []
        self.score = 0

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()

            pygame.display.flip()
            self.clock.tick(self.FPS)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if self.state == "menu":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        # Stop menu music and play scene music
                        if self.menu_music_playing:
                            pygame.mixer.music.stop()
                            self.menu_music_playing = False
                        pygame.mixer.music.load(self.scene_music_path)
                        pygame.mixer.music.play(-1)
                        self.state = "playing"
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

            elif self.state == "playing":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.player.jump()
                if event.type == self.obstacle_timer:
                    self.obstacles.append(
                        Obstacle("assets/building.gif", self.WIDTH + 100, self.HEIGHT)
                    )


            elif self.state == "game_over":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        if self.score > self.high_score:
                            self.high_score = self.score
                        self.reset_game()
                        self.state = "menu"
                        # Start menu music if not already playing
                        if not self.menu_music_playing:
                            pygame.mixer.music.load(self.menu_music_path)
                            pygame.mixer.music.play(-1)
                            self.menu_music_playing = True


    def update(self):
        if self.state == "playing":
            self.player.update()
            for obstacle in self.obstacles:
                obstacle.update()

            # Remove obstacles that have left the screen
            self.obstacles = [ob for ob in self.obstacles if ob.rect_top.right > 0]

            # Increase score when obstacles pass the ship
            for obstacle in self.obstacles:
                if not obstacle.scored and obstacle.rect_top.right < self.player.rect.left:
                    self.score += 1
                    obstacle.scored = True

            # Collision with top/bottom of screen
            if self.player.rect.top <= 0 or self.player.rect.bottom >= self.HEIGHT:
                self.state = "game_over"

            # Collision with obstacles
            for obstacle in self.obstacles:
                if self.player.rect.colliderect(obstacle.rect_top) or self.player.rect.colliderect(obstacle.rect_bottom):
                    self.state = "game_over"

            # Spawn obstacles with minimum distance check
            self.spawn_timer += self.clock.get_time()
            min_distance = 3000  # Minimum horizontal distance between obstacles
            can_spawn = (
                not self.obstacles or
                self.obstacles[-1].rect_top.x < self.WIDTH - min_distance
            )
            if self.spawn_timer >= self.spawn_interval and can_spawn:
                self.spawn_timer = 0
                new_obstacle = Obstacle(
                    "assets/building.gif", self.WIDTH + 100, self.HEIGHT
                )
                self.obstacles.append(new_obstacle)

    def draw(self):
        if self.state == "menu":
            # Play menu music if not already playing
            if not self.menu_music_playing:
                pygame.mixer.music.load(self.menu_music_path)
                pygame.mixer.music.play(-1)  # Loop indefinitely
                self.menu_music_playing = True

            # Draw static menu background
            self.screen.blit(self.menu_bg_img, (0, 0))

            title_text = self.font.render("Neon Faller", True, (0, 255, 200))
            play_text = self.small_font.render("Press SPACE to Play", True, (255, 255, 255))
            quit_text = self.small_font.render("Press Q to Quit", True, (255, 100, 100))

            # Center texts
            self.screen.blit(title_text, (self.WIDTH//2 - title_text.get_width()//2, 200))
            self.screen.blit(play_text, (self.WIDTH//2 - play_text.get_width()//2, 300))
            self.screen.blit(quit_text, (self.WIDTH//2 - quit_text.get_width()//2, 350))

        elif self.state == "playing":
            # Background
            self.screen.blit(self.bg_img, (0, 0))

            # Player
            self.player.draw(self.screen)

            # Obstacles
            for obstacle in self.obstacles:
                obstacle.draw(self.screen)

            score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
            self.screen.blit(score_text, (10, 10))


        elif self.state == "game_over":
            # Stop scene music and play menu music if not already playing
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
            if not self.menu_music_playing:
                pygame.mixer.music.load(self.menu_music_path)
                pygame.mixer.music.play(-1)
                self.menu_music_playing = True

            self.screen.fill((0, 0, 0))

            game_over_text = self.font.render("GAME OVER", True, (255, 50, 50))
            score_text = self.small_font.render(f"Score: {self.score}", True, (255, 255, 255))
            high_score_text = self.small_font.render(f"High Score: {self.high_score}", True, (200, 200, 0))
            restart_text = self.small_font.render("Press SPACE to return to Menu", True, (255, 255, 255))

            self.screen.blit(game_over_text, (self.WIDTH//2 - game_over_text.get_width()//2, 150))
            self.screen.blit(score_text, (self.WIDTH//2 - score_text.get_width()//2, 250))
            self.screen.blit(high_score_text, (self.WIDTH//2 - high_score_text.get_width()//2, 300))
            self.screen.blit(restart_text, (self.WIDTH//2 - restart_text.get_width()//2, 400))
