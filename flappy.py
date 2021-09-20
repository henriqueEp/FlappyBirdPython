import pygame, random, sys
from pygame.locals import *

# Variáveis tamanho da tela
screen_wdh = 400
screen_hgt = 800
initial_spd = 10
gravt = 1
game_spd = 10


ground_width = 2 * screen_wdh
ground_height = 100

pipe_wdt = 80
pipe_hgt = 500
pipe_gap = 200
# Criando Classe Passaro
class Bird(pygame.sprite.Sprite):
    
    # Construtor da classe
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        #precisamos que o passaro mecha as asas
        self.images = [pygame.image.load('assets/sprites/bluebird-upflap.png').convert_alpha(),
                       pygame.image.load('assets/sprites/bluebird-midflap.png').convert_alpha(),
                       pygame.image.load('assets/sprites/bluebird-downflap.png').convert_alpha()]
        
        self.speed = initial_spd
        
        self.current_image = 0
        # Chamando a imagem do passaro
        self.image = pygame.image.load('assets/sprites/bluebird-midflap.png').convert_alpha()
        # fazendo o rect -> o rect tem 4 informações, as 2 primeiras infos diz onde está a imagem na tela ( 
        # no caso a imagem do passaro ) e as outras 2 dizem o tamanho
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        
        # vamos colocar o passaro no meio da tela
        # esse é nosso rect rect(0, 0, 34, 24)
        self.rect[0] = screen_wdh / 2
        self.rect[1] = screen_hgt / 2
        
        #precisamos que o passaro mecha as asas
        self.images = [pygame.image.load('assets/sprites/bluebird-upflap.png').convert_alpha(),
                       pygame.image.load('assets/sprites/bluebird-midflap.png').convert_alpha(),
                       pygame.image.load('assets/sprites/bluebird-downflap.png').convert_alpha()]
        print(self.rect)
        
    def update(self):
        # vamos fazer a imagem atualizar a cada batida de asa
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[ self.current_image ]
        
        self.speed += gravt
        
        # atualizar altura
        self.rect[1] += self.speed
        
    def bump(self):
        self.speed = -initial_spd
        
class Pipe(pygame.sprite.Sprite):
    
    def __init__(self, inverted, xpos, ysize):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load('assets/sprites/pipe-red.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (pipe_wdt, pipe_hgt))

        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        
        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect[1] = -(self.rect[3] - ysize)
        else:
            self.rect[1] = screen_hgt - ysize
        
        self.mask = pygame.mask.from_surface(self.image)
        
      
    
    def update(self):
        self.rect[0] -= game_spd
        
        
class Ground(pygame.sprite.Sprite):
    
    def __init__(self, xpos):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load('assets/sprites/base.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (ground_width, ground_height))
        
        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.rect[1] = screen_hgt - ground_height
        
    def update(self):
        self.rect[0] -= game_spd
        
def is_off_screen(sprite):
    return sprite.rect[0] < -(sprite.rect[2]) 
    
def get_random_pipes(xpos):
    size = random.randint(100, 300)
    pipe = Pipe(False, xpos, size)
    pipe_inverted = Pipe(True, xpos, screen_hgt - size - pipe_gap)
    return(pipe, pipe_inverted)

def plus_score(bird_sprite, pipe_sprite):
    return pipe_sprite.rect[0] == ( bird_sprite.rect[0] - game_spd)

# Iniciando Pygame
pygame.init()
screen = pygame.display.set_mode((screen_wdh, screen_hgt))

FONT = pygame.font.Font('8-bit-pusab.ttf', 15)
score_text = FONT.render('Score: 0', True, (255, 255, 0))

# Background Pygame
backg = pygame.image.load('assets/sprites/background-day.png')
backg = pygame.transform.scale(backg, (screen_wdh, screen_hgt))

# para mostrar o passaro na tela vamos criar um grupo
bird_group = pygame.sprite.Group()

# criamos um objeto do tipo bird
bird = Bird()

# adicionando o objeto do tipo bird no grupo
bird_group.add(bird)

ground_group = pygame.sprite.Group()
for i in range(2):
    ground = Ground(ground_width * i)
    ground_group.add(ground)


pipe_group = pygame.sprite.Group()
for i in range(2):
    pipes = get_random_pipes(screen_wdh * i + 800)
    pipe_group.add(pipes[0])
    pipe_group.add(pipes[1])

clock = pygame.time.Clock()
current_pipe = 0
current_score = 0

while True:
    
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.ext()
            
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                bird.bump()  
                 
        screen.blit(backg, (10, 10))       
        
        if is_off_screen(ground_group.sprites()[0]):
            ground_group.remove(ground_group.sprites()[0])
                    
            new_ground = Ground(ground_width - 20)
            ground_group.add(new_ground)
            
        if plus_score(bird_group.sprites()[0], pipe_group.sprites()[0]):
            current_score += 1
            score_text = FONT.render('Score: '+str(current_score), False, (255, 255, 0))
            
        if is_off_screen(pipe_group.sprites()[0]):   
            pipe_group.remove(pipe_group.sprites()[0])
            pipe_group.remove(pipe_group.sprites()[0])
            
            pipes = get_random_pipes(screen_wdh * 2)
            pipe_group.add(pipes[0])
            pipe_group.add(pipes[1])

        # atualiza o passaro na tela
        bird_group.update()
        ground_group.update()
        pipe_group.update()
        
        # desenha todos os elementos no grupo
        bird_group.draw(screen)
        pipe_group.draw(screen)
        ground_group.draw(screen)
              
        pygame.display.update()
        
        if pygame.sprite.groupcollide(bird_group, ground_group, False, False, pygame.sprite.collide_mask) or (
           pygame.sprite.groupcollide(bird_group, pipe_group, False, False, pygame.sprite.collide_mask)):
            # Game Over
            input()
            break