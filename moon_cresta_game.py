import pygame
import random
import math
import sys

# Inicialização do Pygame
pygame.init()

# Configurações da tela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Moon Cresta - Jogo Retro")

# Cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

# Fonte
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

# Carregar sprites dos inimigos
try:
    enemy_sprite1 = pygame.image.load("sprint1.png")
    enemy_sprite2 = pygame.image.load("sprint2.png")
    enemy_sprite3 = pygame.image.load("sprint3.png")

    # Redimensionar sprites para tamanho adequado
    enemy_sprite1 = pygame.transform.scale(enemy_sprite1, (40, 40))
    enemy_sprite2 = pygame.transform.scale(enemy_sprite2, (45, 45))
    enemy_sprite3 = pygame.transform.scale(enemy_sprite3, (50, 50))

    enemy_sprites = [enemy_sprite1, enemy_sprite2, enemy_sprite3]
    sprites_loaded = True
except:
    print("Erro ao carregar sprites. Usando formas geométricas.")
    enemy_sprites = []
    sprites_loaded = False


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 40
        self.speed = 5
        self.stage = 1
        self.max_stage = 3
        self.bullets = []
        self.bullet_speed = 7
        self.shoot_delay = 0
        self.max_shoot_delay = 10
        self.health = 100
        self.invulnerable = False
        self.invulnerable_timer = 0

    def draw(self, screen):
        if self.invulnerable and pygame.time.get_ticks() % 200 < 100:
            return  # Piscar quando invulnerável

        # Corpo principal da nave
        pygame.draw.polygon(
            screen,
            WHITE,
            [
                (self.x, self.y - self.height // 2),
                (self.x - self.width // 2, self.y + self.height // 2),
                (self.x + self.width // 2, self.y + self.height // 2),
            ],
        )

        # Estágios adicionais
        if self.stage >= 2:
            # Segundo estágio (esquerda)
            pygame.draw.polygon(
                screen,
                CYAN,
                [
                    (self.x - self.width // 2 - 10, self.y - self.height // 3),
                    (self.x - self.width // 2 - 20, self.y + self.height // 3),
                    (self.x - self.width // 2, self.y + self.height // 2),
                ],
            )

            # Segundo estágio (direita)
            pygame.draw.polygon(
                screen,
                CYAN,
                [
                    (self.x + self.width // 2 + 10, self.y - self.height // 3),
                    (self.x + self.width // 2 + 20, self.y + self.height // 3),
                    (self.x + self.width // 2, self.y + self.height // 2),
                ],
            )

        if self.stage >= 3:
            # Terceiro estágio (esquerda)
            pygame.draw.polygon(
                screen,
                MAGENTA,
                [
                    (self.x - self.width // 2 - 20, self.y - self.height // 2),
                    (self.x - self.width // 2 - 30, self.y),
                    (self.x - self.width // 2 - 20, self.y + self.height // 3),
                ],
            )

            # Terceiro estágio (direita)
            pygame.draw.polygon(
                screen,
                MAGENTA,
                [
                    (self.x + self.width // 2 + 20, self.y - self.height // 2),
                    (self.x + self.width // 2 + 30, self.y),
                    (self.x + self.width // 2 + 20, self.y + self.height // 3),
                ],
            )

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x > self.width // 2:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < SCREEN_WIDTH - self.width // 2:
            self.x += self.speed
        if keys[pygame.K_UP] and self.y > self.height // 2:
            self.y -= self.speed
        if keys[pygame.K_DOWN] and self.y < SCREEN_HEIGHT - self.height // 2:
            self.y += self.speed

    def shoot(self, keys):
        if keys[pygame.K_SPACE] and self.shoot_delay <= 0:
            # Tiro principal
            self.bullets.append(
                Bullet(self.x, self.y - self.height // 2, 0, -self.bullet_speed, WHITE)
            )

            # Tiros laterais baseados no estágio
            if self.stage >= 2:
                self.bullets.append(
                    Bullet(
                        self.x - 15,
                        self.y - self.height // 3,
                        -2,
                        -self.bullet_speed,
                        CYAN,
                    )
                )
                self.bullets.append(
                    Bullet(
                        self.x + 15,
                        self.y - self.height // 3,
                        2,
                        -self.bullet_speed,
                        CYAN,
                    )
                )

            if self.stage >= 3:
                self.bullets.append(
                    Bullet(
                        self.x - 25,
                        self.y - self.height // 2,
                        -3,
                        -self.bullet_speed,
                        MAGENTA,
                    )
                )
                self.bullets.append(
                    Bullet(
                        self.x + 25,
                        self.y - self.height // 2,
                        3,
                        -self.bullet_speed,
                        MAGENTA,
                    )
                )

            self.shoot_delay = self.max_shoot_delay

    def update(self):
        if self.shoot_delay > 0:
            self.shoot_delay -= 1

        if self.invulnerable:
            self.invulnerable_timer -= 1
            if self.invulnerable_timer <= 0:
                self.invulnerable = False

        # Atualizar balas
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.y < 0:
                self.bullets.remove(bullet)

    def upgrade_stage(self):
        if self.stage < self.max_stage:
            self.stage += 1
            return True
        return False


class Enemy:
    def __init__(self, x, y, enemy_type=1):
        self.x = x
        self.y = y
        self.enemy_type = enemy_type
        self.speed = random.uniform(1, 3)
        self.health = enemy_type * 10
        self.max_health = self.health
        self.width = 20 + enemy_type * 5
        self.height = 20 + enemy_type * 5
        self.shoot_delay = 0
        self.max_shoot_delay = random.randint(60, 120)
        self.bullets = []
        self.bullet_speed = 3

    def draw(self, screen):
        # Desenhar inimigo baseado no tipo
        if sprites_loaded and self.enemy_type <= len(enemy_sprites):
            # Usar sprite
            sprite = enemy_sprites[self.enemy_type - 1]
            sprite_rect = sprite.get_rect()
            sprite_rect.center = (int(self.x), int(self.y))
            screen.blit(sprite, sprite_rect)
        else:
            # Fallback para formas geométricas
            if self.enemy_type == 1:
                color = RED
                shape = "circle"
            elif self.enemy_type == 2:
                color = YELLOW
                shape = "square"
            else:
                color = MAGENTA
                shape = "triangle"

            if shape == "circle":
                pygame.draw.circle(
                    screen, color, (int(self.x), int(self.y)), self.width // 2
                )
            elif shape == "square":
                pygame.draw.rect(
                    screen,
                    color,
                    (
                        self.x - self.width // 2,
                        self.y - self.height // 2,
                        self.width,
                        self.height,
                    ),
                )
            elif shape == "triangle":
                pygame.draw.polygon(
                    screen,
                    color,
                    [
                        (self.x, self.y - self.height // 2),
                        (self.x - self.width // 2, self.y + self.height // 2),
                        (self.x + self.width // 2, self.y + self.height // 2),
                    ],
                )

        # Barra de vida
        if self.health < self.max_health:
            health_width = (self.health / self.max_health) * self.width
            pygame.draw.rect(
                screen,
                RED,
                (
                    self.x - self.width // 2,
                    self.y - self.height // 2 - 10,
                    self.width,
                    5,
                ),
            )
            pygame.draw.rect(
                screen,
                GREEN,
                (
                    self.x - self.width // 2,
                    self.y - self.height // 2 - 10,
                    health_width,
                    5,
                ),
            )

    def update(self):
        self.y += self.speed

        # Atirar ocasionalmente
        if self.shoot_delay > 0:
            self.shoot_delay -= 1
        else:
            if random.random() < 0.01:  # 1% de chance por frame
                self.bullets.append(
                    Bullet(self.x, self.y + self.height // 2, 0, self.bullet_speed, RED)
                )
                self.shoot_delay = self.max_shoot_delay

        # Atualizar balas
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.y > SCREEN_HEIGHT:
                self.bullets.remove(bullet)

    def take_damage(self, damage):
        self.health -= damage
        return self.health <= 0


class Bullet:
    def __init__(self, x, y, dx, dy, color):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.color = color
        self.radius = 3

    def update(self):
        self.x += self.dx
        self.y += self.dy

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)


class Explosion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.timer = 30
        self.particles = []
        for _ in range(10):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 6)
            self.particles.append(
                {
                    "x": x,
                    "y": y,
                    "dx": math.cos(angle) * speed,
                    "dy": math.sin(angle) * speed,
                    "life": 30,
                }
            )

    def update(self):
        self.timer -= 1
        for particle in self.particles:
            particle["x"] += particle["dx"]
            particle["y"] += particle["dy"]
            particle["life"] -= 1

    def draw(self, screen):
        for particle in self.particles:
            if particle["life"] > 0:
                alpha = int((particle["life"] / 30) * 255)
                color = (255, 255, 0, alpha)
                pygame.draw.circle(
                    screen, (255, 255, 0), (int(particle["x"]), int(particle["y"])), 2
                )


class Game:
    def __init__(self):
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
        self.enemies = []
        self.explosions = []
        self.score = 0
        self.level = 1
        self.enemies_per_level = 10
        self.enemies_spawned = 0
        self.spawn_timer = 0
        self.max_spawn_timer = 60
        self.game_state = "playing"  # "playing", "level_complete", "victory"
        self.level_complete_timer = 0
        self.background_stars = []

        # Criar estrelas de fundo
        for _ in range(50):
            self.background_stars.append(
                {
                    "x": random.randint(0, SCREEN_WIDTH),
                    "y": random.randint(0, SCREEN_HEIGHT),
                    "speed": random.uniform(0.5, 2),
                }
            )

    def spawn_enemy(self):
        if self.spawn_timer <= 0 and self.enemies_spawned < self.enemies_per_level:
            x = random.randint(50, SCREEN_WIDTH - 50)
            enemy_type = min(self.level, 3)  # Máximo 3 tipos de inimigos
            self.enemies.append(Enemy(x, -50, enemy_type))
            self.enemies_spawned += 1
            self.spawn_timer = self.max_spawn_timer

    def update_background(self):
        for star in self.background_stars:
            star["y"] += star["speed"]
            if star["y"] > SCREEN_HEIGHT:
                star["y"] = -10
                star["x"] = random.randint(0, SCREEN_WIDTH)

    def draw_background(self, screen):
        screen.fill(BLACK)
        for star in self.background_stars:
            pygame.draw.circle(screen, WHITE, (int(star["x"]), int(star["y"])), 1)

    def check_collisions(self):
        # Colisão entre balas do jogador e inimigos
        for bullet in self.player.bullets[:]:
            for enemy in self.enemies[:]:
                distance = math.sqrt(
                    (bullet.x - enemy.x) ** 2 + (bullet.y - enemy.y) ** 2
                )
                if distance < enemy.width // 2 + bullet.radius:
                    if bullet in self.player.bullets:
                        self.player.bullets.remove(bullet)
                    if enemy.take_damage(10):
                        self.enemies.remove(enemy)
                        self.explosions.append(Explosion(enemy.x, enemy.y))
                        self.score += enemy.enemy_type * 100
                    break

        # Colisão entre balas dos inimigos e jogador
        if not self.player.invulnerable:
            for enemy in self.enemies:
                for bullet in enemy.bullets[:]:
                    distance = math.sqrt(
                        (bullet.x - self.player.x) ** 2
                        + (bullet.y - self.player.y) ** 2
                    )
                    if distance < self.player.width // 2 + bullet.radius:
                        enemy.bullets.remove(bullet)
                        self.player.health -= 20
                        self.player.invulnerable = True
                        self.player.invulnerable_timer = 120  # 2 segundos
                        if self.player.health <= 0:
                            self.game_state = "game_over"
                        break

        # Colisão entre jogador e inimigos
        if not self.player.invulnerable:
            for enemy in self.enemies[:]:
                distance = math.sqrt(
                    (enemy.x - self.player.x) ** 2 + (enemy.y - self.player.y) ** 2
                )
                if distance < (enemy.width + self.player.width) // 2:
                    self.enemies.remove(enemy)
                    self.explosions.append(Explosion(enemy.x, enemy.y))
                    self.player.health -= 30
                    self.player.invulnerable = True
                    self.player.invulnerable_timer = 120
                    if self.player.health <= 0:
                        self.game_state = "game_over"

    def update(self):
        if self.game_state == "playing":
            keys = pygame.key.get_pressed()
            self.player.move(keys)
            self.player.shoot(keys)
            self.player.update()

            self.spawn_timer -= 1
            self.spawn_enemy()

            for enemy in self.enemies[:]:
                enemy.update()
                if enemy.y > SCREEN_HEIGHT + 50:
                    self.enemies.remove(enemy)

            for explosion in self.explosions[:]:
                explosion.update()
                if explosion.timer <= 0:
                    self.explosions.remove(explosion)

            self.check_collisions()
            self.update_background()

            # Verificar se o nível foi completado
            if (
                self.enemies_spawned >= self.enemies_per_level
                and len(self.enemies) == 0
            ):
                if self.level < 3:
                    self.game_state = "level_complete"
                    self.level_complete_timer = 180  # 3 segundos
                else:
                    self.game_state = "victory"

        elif self.game_state == "level_complete":
            self.level_complete_timer -= 1
            if self.level_complete_timer <= 0:
                self.next_level()

    def next_level(self):
        self.level += 1
        self.player.upgrade_stage()
        self.enemies_spawned = 0
        self.spawn_timer = 0
        self.game_state = "playing"
        self.enemies_per_level += 5  # Mais inimigos por nível

    def draw(self, screen):
        self.draw_background(screen)

        if self.game_state == "playing":
            self.player.draw(screen)

            for bullet in self.player.bullets:
                bullet.draw(screen)

            for enemy in self.enemies:
                enemy.draw(screen)
                for bullet in enemy.bullets:
                    bullet.draw(screen)

            for explosion in self.explosions:
                explosion.draw(screen)

            # Interface do usuário
            score_text = font.render(f"Score: {self.score}", True, WHITE)
            level_text = font.render(f"Level: {self.level}", True, WHITE)
            stage_text = font.render(f"Stage: {self.player.stage}/3", True, WHITE)
            health_text = font.render(f"Health: {self.player.health}", True, WHITE)

            screen.blit(score_text, (10, 10))
            screen.blit(level_text, (10, 50))
            screen.blit(stage_text, (10, 90))
            screen.blit(health_text, (10, 130))

            # Barra de vida
            health_width = (self.player.health / 100) * 200
            pygame.draw.rect(screen, RED, (10, 170, 200, 20))
            pygame.draw.rect(screen, GREEN, (10, 170, health_width, 20))

        elif self.game_state == "level_complete":
            complete_text = font.render(f"Level {self.level} Complete!", True, WHITE)
            upgrade_text = font.render("Ship upgraded!", True, GREEN)
            continue_text = small_font.render(
                "Preparing for next level...", True, WHITE
            )

            screen.blit(
                complete_text,
                (
                    SCREEN_WIDTH // 2 - complete_text.get_width() // 2,
                    SCREEN_HEIGHT // 2 - 60,
                ),
            )
            screen.blit(
                upgrade_text,
                (
                    SCREEN_WIDTH // 2 - upgrade_text.get_width() // 2,
                    SCREEN_HEIGHT // 2 - 20,
                ),
            )
            screen.blit(
                continue_text,
                (
                    SCREEN_WIDTH // 2 - continue_text.get_width() // 2,
                    SCREEN_HEIGHT // 2 + 20,
                ),
            )

        elif self.game_state == "victory":
            victory_text = font.render("VICTORY!", True, GREEN)
            final_score_text = font.render(f"Final Score: {self.score}", True, WHITE)
            thanks_text = small_font.render("Thanks for playing!", True, WHITE)
            restart_text = small_font.render(
                "Press R to restart or ESC to quit", True, WHITE
            )

            screen.blit(
                victory_text,
                (
                    SCREEN_WIDTH // 2 - victory_text.get_width() // 2,
                    SCREEN_HEIGHT // 2 - 80,
                ),
            )
            screen.blit(
                final_score_text,
                (
                    SCREEN_WIDTH // 2 - final_score_text.get_width() // 2,
                    SCREEN_HEIGHT // 2 - 40,
                ),
            )
            screen.blit(
                thanks_text,
                (SCREEN_WIDTH // 2 - thanks_text.get_width() // 2, SCREEN_HEIGHT // 2),
            )
            screen.blit(
                restart_text,
                (
                    SCREEN_WIDTH // 2 - restart_text.get_width() // 2,
                    SCREEN_HEIGHT // 2 + 40,
                ),
            )

        elif self.game_state == "game_over":
            game_over_text = font.render("GAME OVER", True, RED)
            final_score_text = font.render(f"Final Score: {self.score}", True, WHITE)
            restart_text = small_font.render(
                "Press R to restart or ESC to quit", True, WHITE
            )

            screen.blit(
                game_over_text,
                (
                    SCREEN_WIDTH // 2 - game_over_text.get_width() // 2,
                    SCREEN_HEIGHT // 2 - 40,
                ),
            )
            screen.blit(
                final_score_text,
                (
                    SCREEN_WIDTH // 2 - final_score_text.get_width() // 2,
                    SCREEN_HEIGHT // 2,
                ),
            )
            screen.blit(
                restart_text,
                (
                    SCREEN_WIDTH // 2 - restart_text.get_width() // 2,
                    SCREEN_HEIGHT // 2 + 40,
                ),
            )


def main():
    clock = pygame.time.Clock()
    game = Game()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r and (
                    game.game_state == "game_over" or game.game_state == "victory"
                ):
                    game = Game()  # Reiniciar jogo

        game.update()
        game.draw(screen)

        pygame.display.flip()
        clock.tick(60)  # 60 FPS

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
