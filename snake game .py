
from pygame.locals import *
from random import randint
import pygame
import time


SIZE = 20
BACKGROUND_COLOUR = (0,51,0)

class Apple:
    def __init__(self,surface):
        self.surface = surface
        self.apple = pygame.image.load('/home/sonia/Music/sonia/scripts/apple.png').convert()
        
        # size small
        self.apple = pygame.transform.scale(self.apple,(SIZE,SIZE))

        #corodinates of aapple
        self.x = 100
        self.y = 100

    def draw(self):

        # draw image
        self.surface.blit(self.apple,(self.x,self.y))
        # pygame.display.flip()
        
     
    def move(self):
        self.x = randint(1,24) * SIZE
        self.y = randint(1,19) * SIZE
        


class Snake():
    def __init__(self,surface):
        self.surface = surface

        # BLOCK LOAD
        self.block = pygame.image.load("/home/sonia/Music/sonia/scripts/block.png").convert()

        # SMALL BLOCK SIZE
        self.block = pygame.transform.scale(self.block,(SIZE,SIZE))
        self.direction = 'right'
        

        # length of block
        self.length = 1
        self.score = 0

        #block size 
        self.x = [SIZE] 
        self.y = [SIZE] 
   
    
    def move_left(self):
        self.direction = 'left'
    
    def move_right(self):
        self.direction = 'right'
    
    def move_up(self):
        self.direction = 'up'
    
    def move_down(self):
        self.direction = 'down'
    
   
    def walk(self):
        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]
        
        if self.direction == 'left':
            self.x[0] -= SIZE 
        
        if self.direction == 'right':
            self.x[0] += SIZE
        
        if self.direction == 'up':
            self.y[0] -= SIZE

        if self.direction == 'down':
            self.y[0] += SIZE
        
        self.draw()
        

    def draw(self):
            # fill surface with  colour 
            
            self.surface.fill(BACKGROUND_COLOUR)
            # blit block
            for i in range(self.length):
                self.surface.blit (self.block,(self.x[i],self.y[i]))

            # pygame.display.flip()
    
    def increase_length(self):
        self.length += 1
        self.score += 1
        
        self.x.append(-1)
        self.y.append(-1)
        


class Game :
    def __init__(self):
        pygame.init()
        
        pygame.display.set_caption('snake and apple game')
       
        self.surface = pygame.display.set_mode((500,500))
      
        pygame.mixer.init()
        self.play_background_music()
        

        # initlize snake
        self.snake = Snake(self.surface)
        self.snake.draw()

        # initilize apple
        self.apple = Apple(self.surface)
        self.apple.draw()
    
    def play_background_music(self):
        pygame.mixer.music.load('/home/sonia/Music/sonia/scripts/Snake Game - Theme Song.mp3')
        pygame.mixer.music.play(-1, 0)

    
    def play_music(self):
        sound = pygame.mixer.Sound('/home/sonia/Music/sonia/scripts/game over music.wav')
        pygame.mixer.Sound.play(sound)


    def reset(self):
        self.snake = Snake(self.surface)
        self.apple = Apple(self.surface)
        
    
    def is_collosion(self,x1,y1,x2,y2):
        if x1 >= x2  and x1 < x2 + SIZE :
            if y1 >= y2 and y1 < y2 + SIZE :
                return True
        return False
    
   



    def play(self):
        
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        
        pygame.display.flip()
    
        # snake coliding with apple
        if self.is_collosion(self.snake.x[0],self.snake.y[0],self.apple.x,self.apple.y):
            self.snake.increase_length()
            self.apple.move()
            
    # snake coliiding with itself
        for i in range(3,self.snake.length):
            if self.is_collosion(self.snake.x[0],self.snake.y[0],self.snake.x[i],self.snake.y[i]):
                 
                raise 'collision occurred'

        # snake colliding with the boundries of the window
        if not (0 <= self.snake.x[0] <= 1000 and 0 <= self.snake.y[0] <= 800):
            raise "Hit the boundry error"
                
                    
    def display_score(self):
        font = pygame.font.SysFont(None,40)
        score = font.render(f"Score: {self.snake.score}",True,(155,0,200))
        self.surface.blit(score,(380,20))
        
    

    def show_game_over(self):
        
        font = pygame.font.SysFont('arial',20)
        line1 = font.render(f'Game over! Your score is {self.snake.score}.',True ,(250,250,250))
        self.surface.blit(line1,(100,200))
        line2 = font.render('To play again press Enter.To exit press Escape.',True ,(250,250,250))
        self.surface.blit(line2,(25,220))
        pygame.mixer.music.pause()
        self.play_music()
        
        pygame.display.flip()

    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_ESCAPE:
                        running = False
                    
                    if event.key == pygame.K_RETURN:
                        pygame.mixer.music.unpause()
                        
                        pause = False
                    
                    if not pause:
                        if event.key == pygame.K_LEFT:
                            self.snake.move_left()
                            
                    
                        if event.key == pygame.K_RIGHT:
                            self.snake.move_right()

                        if event.key == pygame.K_UP:
                            self.snake.move_up()

                        if event.key == pygame.K_DOWN:
                            self.snake.move_down()

                elif event.type == pygame.QUIT:
                    running = False   
            try :
                if not pause:
                    self.play()
            
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()
               
                

            time.sleep(0.5)
        
if __name__ == '__main__':
    game = Game()
    game.run()
    