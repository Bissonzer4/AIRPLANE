import pygame
import random
import sys

# Inicialização do Pygame
pygame.init()

# Configurações da tela
screen_width = 1980
screen_height = 1080
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

# Título e ícone
pygame.display.set_caption("Flappy Plane")

# Carregar imagens
bird_img = pygame.image.load("aviao.png")
pipe_img = pygame.image.load("predio.png")
pipe2_img = pygame.image.load("nuvem.png")
logo_img = pygame.image.load("logo.png")
explosion_img = pygame.image.load("explosao.jpg")
espaco_img = pygame.image.load("espaco.png")
background_img = pygame.image.load("sky.png")
sair_img = pygame.image.load("sair.png")

# Função para centralizar um item na tela
def center_image(image):
    return (screen_width - image.get_width()) // 2, (screen_height - image.get_height()) // 2

# Classe do Jogador (Avião)
class Bird:
    def __init__(self):
        self.x = 20
        self.y = screen_height // 2
        self.gravity = 0.8
        self.lift = -10
        self.velocity = 0

    def update(self):
        self.velocity += self.gravity
        self.velocity *= 0.9
        self.y += self.velocity

        if self.y > screen_height:
            self.y = screen_height
            self.velocity = 0

        if self.y < 0:
            self.y = 0
            self.velocity = 0

    def up(self):
        self.velocity += self.lift

    def show(self):
        screen.blit(bird_img, (self.x, self.y))

    def get_rect(self):
        return bird_img.get_rect(topleft=(self.x, self.y))

# Classe dos Canos
class Pipe:
    def __init__(self):
        self.spacing = 200
        self.top = random.randint(max(50, screen_height // 2 - 200), screen_height // 2)
        self.bottom = screen_height - self.top - self.spacing
        self.x = screen_width
        self.w = 80
        self.speed = 15

    def update(self):
        self.x -= self.speed

    def show(self):
        screen.blit(pipe2_img, (self.x, self.top - pipe2_img.get_height()))
        screen.blit(pipe_img, (self.x, screen_height - self.bottom))

    def offscreen(self):
        return self.x < -self.w

    def get_rects(self):
        # Caixa de colisão para o pipe_img (prédio)
        top_rect = pygame.Rect(self.x, self.top, 10, 976)  # Tamanho e posição ajustados
        return top_rect

# Função do Menu
def menu():
    
    font = pygame.font.Font(None, 36)
    logo_x = (screen_width - logo_img.get_width()) // 2
    logo_y = (screen_height - logo_img.get_height()) // 2 - 200
    espaco_x = (screen_width - espaco_img.get_width()) // 2
    espaco_y = (screen_height - espaco_img.get_height()) // 2

    screen.blit(logo_img, (logo_x, logo_y))
    screen.blit(espaco_img, (espaco_x, espaco_y))
    menu_text = font.render("", True, (255, 255, 255))
    menu_rect = menu_text.get_rect(center=(screen_width // 2, screen_height // 2))

    screen.blit(menu_text, menu_rect)
    
    # Posicionamento do botão "Sair" no centro inferior do menu
    sair_x = (screen_width - sair_img.get_width()) // 2
    sair_y = screen_height - sair_img.get_height() - 50
    screen.blit(sair_img, (sair_x, sair_y))

    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False

# Função para desenhar o placar na tela
def draw_score():
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (100, 100))  # Posição no canto superior esquerdo

# Função principal do jogo
def game():
    global score  # Variável global para pontuação
    score = 0  # Inicialização da pontuação

    clock = pygame.time.Clock()
    bird = Bird()
    pipes = [Pipe()]
    running = True
    game_over = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Sair do jogo ao pressionar ESC
                    pygame.quit()
                    sys.exit()

                if event.key == pygame.K_SPACE and not game_over:
                    bird.up()
                if event.key == pygame.K_r and game_over:
                    game()  # Reiniciar o jogo

        if not game_over:
            bird.update()

            for pipe in pipes:
                pipe.update()
                if pipe.offscreen():
                    pipes.remove(pipe)
                    pipes.append(Pipe())

                # Verificar colisão
                bird_rect = bird.get_rect()
                top_rect = pipe.get_rects()  # Obter a caixa de colisão do pipe1
                if bird_rect.colliderect(top_rect):
                    game_over = True  # Jogo termina ao colidir

                # Verificar se o jogador passou pelo cano
                if pipe.x < bird.x < pipe.x + pipe.speed:
                    score += 1  # Aumentar a pontuação quando o jogador passar pelo cano

            # Desenhar plano de fundo
            screen.blit(background_img, (0, 0))

            bird.show()
            for pipe in pipes:
                pipe.show()

            # Desenhar pontuação na tela
            draw_score()

            # Desenhar texto de saída na tela
            font = pygame.font.Font(None, 24)
            exit_text = font.render("Pressione ESC para sair do jogo", True, (255, 255, 255))
            screen.blit(exit_text, (10, 10))

        else:
            # Mostrar cena de explosão
            explosion_x = (screen_width - explosion_img.get_width()) // 2
            explosion_y = (screen_height - explosion_img.get_height()) // 2

            screen.blit(explosion_img, (explosion_x, explosion_y))

            # Desenhar pontuação na tela de morte
            draw_score()

            # Desenhar texto de saída na tela de morte
            font = pygame.font.Font(None, 24)
            exit_text = font.render("Pressione ESC para sair do jogo", True, (255, 255, 255))
            screen.blit(exit_text, (10, 10))

        pygame.display.update()
        clock.tick(30)

# Iniciar o jogo
menu()
game()
pygame.quit()
