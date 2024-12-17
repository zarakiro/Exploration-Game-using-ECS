import pygame
import random

# Initialisation
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Charger l'image de fond
background = pygame.image.load("assets/mapleonardo.jpg").convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))  # Adapter à la taille de l'écran

# Charger l'image du personnage
character_image = pygame.image.load("assets/character.png").convert_alpha()
character_image = pygame.transform.scale(character_image, (120, 120))
character_crouching= pygame.image.load("assets/character_crouching.png").convert_alpha()
character_crouching = pygame.transform.scale(character_crouching, (120, 120))
character_jumping= pygame.image.load("assets/character_jumping.png").convert_alpha()
character_jumping = pygame.transform.scale(character_jumping, (120, 120))

# Charger les images des obstacles
hole_image = pygame.image.load("assets/hole.png").convert_alpha()
log_image = pygame.image.load("assets/log1.png").convert_alpha()
hole_image = pygame.transform.scale(hole_image, (120, 120))
log_image = pygame.transform.scale(log_image, (160, 160))

# Variables pour le défilement du fond
bg_y1 = 0  # Position du premier segment
bg_y2 = -HEIGHT  # Position du second segment

line_positions = [
                    WIDTH // 4 - 110,
                    WIDTH // 2 - 60,
                    3 * WIDTH // 4 + 10
                ]
 
# ECS - Classes de base
class Entity:
    def __init__(self):
        self.components = {}

    def add_component(self, component):
        self.components[component.__class__] = component

    def get_component(self, component_type):
        return self.components.get(component_type, None)

class Component:
    pass

class System:
    def update(self, entities, *args):
        pass

# Composants
class PositionComponent(Component):
    def __init__(self, x, y):
        self.x = x
        self.y = y

class VelocityComponent(Component):
    def __init__(self, speed):
        self.speed = speed

class LineComponent(Component):
    def __init__(self, current_line, total_lines):
        self.current_line = current_line  # Ligne actuelle (0, 1, 2)
        self.total_lines = total_lines    # Nombre total de lignes

class TargetPositionComponent(Component):
    def __init__(self, x):
        self.x = x  # Position X cible

class ObstacleComponent(Component):
    def __init__(self, type_, line, x_position):
        self.type = type_
        self.line = line
        self.x_position = x_position

class AnimationComponent(Component):
    def __init__(self):
        self.is_crouching = False
        self.crouch_timer = 0
        self.is_jumping = False
        self.jump_timer = 0

# Systèmes
class MovementSystem(System):
    def update(self, entities, dt):
        for entity in entities:
            pos = entity.get_component(PositionComponent)
            vel = entity.get_component(VelocityComponent)
            if pos and vel:
                pos.y += vel.speed * dt

class InputSystem(System):
    def __init__(self):
        self.key_pressed = {"left": False, "right": False, "down": False, "up": False} 

    def update(self, entities):
        keys = pygame.key.get_pressed()
        for entity in entities:
            line = entity.get_component(LineComponent)
            target_pos = entity.get_component(TargetPositionComponent)
            animation = entity.get_component(AnimationComponent)
            if line and target_pos and animation:
                # Détection d'appui unique pour la gauche (flèches ou Q)
                if (keys[pygame.K_LEFT] or keys[pygame.K_q]) and not self.key_pressed["left"]:
                    line.current_line = max(0, line.current_line - 1)
                    self.key_pressed["left"] = True
                elif not (keys[pygame.K_LEFT] or keys[pygame.K_q]):
                    self.key_pressed["left"] = False

                # Détection d'appui unique pour la droite (flèches ou D)
                if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and not self.key_pressed["right"]:
                    line.current_line = min(line.total_lines - 1, line.current_line + 1)
                    self.key_pressed["right"] = True
                elif not (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
                    self.key_pressed["right"] = False

                if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and not self.key_pressed["down"]:
                    animation.is_crouching = True
                    animation.crouch_timer = 0.7
                    self.key_pressed["down"] = True
                elif not (keys[pygame.K_DOWN] or keys[pygame.K_s]):
                    self.key_pressed["down"] = False
                
                if (keys[pygame.K_UP] or keys[pygame.K_z]) and not self.key_pressed["up"]:
                    animation.is_jumping = True
                    animation.jump_timer = 0.7
                    self.key_pressed["up"] = True
                elif not (keys[pygame.K_UP] or keys[pygame.K_z]):
                    self.key_pressed["up"] = False

                # Mise à jour de la position cible en fonction de la ligne
                target_pos.x = line_positions[line.current_line]

class TransitionSystem(System):
    def __init__(self, speed, epsilon=5):
        self.speed = speed  # Vitesse de transition (pixels par seconde)
        self.epsilon = epsilon  # Tolérance pour arrêter le mouvement

    def update(self, entities, dt):
        for entity in entities:
            pos = entity.get_component(PositionComponent)
            target_pos = entity.get_component(TargetPositionComponent)
            if pos and target_pos:
                # Calculer la distance à parcourir
                delta = target_pos.x - pos.x
                if abs(delta) > self.epsilon:  # Se déplacer seulement si l'écart dépasse epsilon
                    pos.x += self.speed * dt * (1 if delta > 0 else -1)  # Mouvement fluide
                else:
                    pos.x = target_pos.x  # Alignement final précis

class AnimationSystem(System):
    def update(self, entities, dt):
        for entity in entities:
            animation = entity.get_component(AnimationComponent)
            if animation:
                if animation.is_crouching:
                    animation.crouch_timer -= dt
                    if animation.crouch_timer <= 0:
                        animation.is_crouching = False
                if animation.is_jumping:
                    animation.jump_timer -= dt
                    if animation.jump_timer <= 0:
                        animation.is_jumping = False

class CollisionSystem(System):
    def __init__(self):
        self.collision_tolerance = 50

    def update(self, player, obstacles, score_ref):
        player_pos = player.get_component(PositionComponent)
        player_anim = player.get_component(AnimationComponent)
        if not player_pos or not player_anim:
            return

        for obstacle in obstacles:
            obstacle_pos = obstacle.get_component(PositionComponent)
            obstacle_comp = obstacle.get_component(ObstacleComponent)
            if not obstacle_pos or not obstacle_comp:
                continue

            if obstacle_comp.type == "hole":
                if abs(player_pos.y - obstacle_pos.y) < self.collision_tolerance and abs(player_pos.x - obstacle_pos.x) < self.collision_tolerance:
                    if player_anim.is_jumping:
                        score_ref[0]+=3
                        obstacles.remove(obstacle)
                    else:
                        print("Collision avec un trou ! Game Over")
                        return True

            elif obstacle_comp.type == "log":
                if abs(player_pos.y - obstacle_pos.y) < self.collision_tolerance and abs(player_pos.x - obstacle_pos.x) < 2*self.collision_tolerance:
                    if player_anim.is_crouching:
                        score_ref[0]+=3
                        obstacles.remove(obstacle)
                    else:
                        print("Collision avec une bûche ! Game Over")
                        return True
        return False

class RenderingSystem(System):
    def update(self, entities, screen, bg_y1, bg_y2, obstacles, score):
        # Dessin du fond défilant
        screen.blit(background, (0, bg_y1))
        screen.blit(background, (0, bg_y2))

        # Dessin des holes derriere le character
        for obstacle in obstacles:
            pos = obstacle.get_component(PositionComponent)
            obst = obstacle.get_component(ObstacleComponent)
            if pos and obst and obst.type == "hole":
                image = hole_image
                screen.blit(image, (pos.x, pos.y))

        # Dessin des entités (joueur)
        for entity in entities:
            pos = entity.get_component(PositionComponent)
            animation=entity.get_component(AnimationComponent)
            if pos:
                if animation and animation.is_crouching:
                    screen.blit(character_crouching, (pos.x, pos.y))
                elif animation and animation.is_jumping:
                    screen.blit(character_jumping, (pos.x, pos.y))
                else:
                    screen.blit(character_image, (pos.x, pos.y))

        # Dessin des "log" devant le character
        for obstacle in obstacles:
            pos = obstacle.get_component(PositionComponent)
            obst = obstacle.get_component(ObstacleComponent)
            if pos and obst and obst.type == "log":
                image = log_image
                screen.blit(image, (pos.x, pos.y))

        score_surface = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_surface, (10, 10))
        pygame.display.flip()

# Fonction pour créer des obstacles
def spawn_obstacle(obstacle_list, lines):
    line = random.choice(range(len(lines)))
    x_position = lines[line]
    obstacle_type = random.choice(["hole", "log"])
    if obstacle_type == "log":
        x_position -= 50

    obstacle = Entity()
    obstacle.add_component(PositionComponent(x_position, -50))
    obstacle.add_component(VelocityComponent(scroll_speed))
    obstacle.add_component(ObstacleComponent(obstacle_type, line, x_position))
    obstacle_list.append(obstacle)

def show_menu():
    font = pygame.font.SysFont(None, 72)
    text = font.render("Start Game", True, (255, 255, 255))
    quit_text = font.render("Quit", True, (255, 255, 255))

    button_start = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 50, 300, 50)
    button_quit = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 50, 300, 50)

    screen.blit(background, (0, 0))
    pygame.draw.rect(screen, (0, 128, 0), button_start)
    pygame.draw.rect(screen, (128, 0, 0), button_quit)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 2 + 50))

    pygame.display.flip()

    return button_start, button_quit

def show_game_over(score):
    font = pygame.font.SysFont(None, 72)
    game_over_text = font.render("Game Over", True, (255, 0, 0))
    score_text = font.render(f"Score: {score[0]}", True, (255, 255, 255))
    
    retry_text = font.render("Play Again", True, (255, 255, 255))
    quit_text = font.render("Quit", True, (255, 255, 255))

    button_retry = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 50, 300, 50)
    button_quit = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 50, 300, 50)

    screen.blit(background, (0, 0))
    pygame.draw.rect(screen, (0, 128, 0), button_retry)
    pygame.draw.rect(screen, (128, 0, 0), button_quit)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 150))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - 100))
    screen.blit(retry_text, (WIDTH // 2 - retry_text.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 2 + 50))

    pygame.display.flip()

    return button_retry, button_quit

# Création du joueur
player = Entity()
player.add_component(PositionComponent(WIDTH // 2 - 25, HEIGHT - 130))
player.add_component(VelocityComponent(0))
player.add_component(LineComponent(current_line=1, total_lines=3))
player.add_component(TargetPositionComponent(WIDTH // 2 - 25))
player.add_component(AnimationComponent())

# Systèmes
movement_system = MovementSystem()
input_system = InputSystem()
animation_system = AnimationSystem()
collision_system = CollisionSystem()
rendering_system = RenderingSystem()
transition_system = TransitionSystem(speed=700) # Vitesse de transition entre deux lignes

# Boucle principale
running = True
game_started = False
game_over=False
spawn_timer = 0
obstacles = []
score = [0]
score_timer = 0
font=pygame.font.SysFont(None, 48)

while running:
    dt = clock.tick(60) / 1000
    spawn_timer += dt

    if not game_over:
        score_timer += dt
        if score_timer >= 1:
            score[0] += 1
            score_timer = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_started and not game_over:
        button_start, button_quit = show_menu()

        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        # Vérifier si le bouton Start est cliqué
        if button_start.collidepoint(mouse_pos) and mouse_pressed[0]:
            game_started = True

        # Vérifier si le bouton Quit est cliqué
        if button_quit.collidepoint(mouse_pos) and mouse_pressed[0]:
            running = False

    elif game_started and not game_over:
        scroll_speed = 200 + (score[0] // 10) * 20
        spawn_interval = max(0.5, 2.0 - (score[0] // 20) * 0.2)

        # Spawn des obstacles toutes les 2 secondes
        if spawn_timer > spawn_interval:
            spawn_obstacle(obstacles, line_positions)
            spawn_timer = 0

        # Mettre à jour les positions des obstacles
        for obstacle in obstacles:
            pos = obstacle.get_component(PositionComponent)
            vel = obstacle.get_component(VelocityComponent)
            if pos and vel:
                pos.y += vel.speed * dt
                vel.speed = scroll_speed
            if pos.y > HEIGHT:
                obstacles.remove(obstacle)

        # Mise à jour des systèmes
        input_system.update([player])
        transition_system.update([player], dt)
        animation_system.update([player], dt)
        game_over=collision_system.update(player, obstacles, score)
        movement_system.update([player], dt)
        rendering_system.update([player], screen, bg_y1, bg_y2, obstacles, score[0])

        # Fond défilant
        bg_y1 += scroll_speed * dt
        bg_y2 += scroll_speed * dt
        if bg_y1 >= HEIGHT:
            bg_y1 = bg_y2 - HEIGHT
        if bg_y2 >= HEIGHT:
            bg_y2 = bg_y1 - HEIGHT
    elif game_over:
        button_retry, button_quit = show_game_over(score)

        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        # Vérifier si le bouton Rejouer est cliqué
        if button_retry.collidepoint(mouse_pos) and mouse_pressed[0]:
            game_started = True
            game_over = False
            obstacles.clear()
            score[0] = 0

        # Vérifier si le bouton Quitter est cliqué
        if button_quit.collidepoint(mouse_pos) and mouse_pressed[0]:
            running = False

pygame.quit()
