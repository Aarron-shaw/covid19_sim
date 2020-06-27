import pygame
import math
import random
import winsound
import time
import matplotlib.pyplot as plt

#pygame.display.init()
pygame.init()
info = pygame.display.Info()
SIZE_X = info.current_w
SIZE_Y = info.current_h

screen = pygame.display.set_mode((0, 0),pygame.FULLSCREEN)



SIZE_TEXT_X = 100
SIZE_TEXT_Y = 50


speed = 1
max_peeps = 500
max_inf = 10
target_list = []
inf_chance = 30
person_size = 1
home_chance = 30
recover_chance = 50
death_chance = 10

WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(255, 0, 0) 
BLACK = pygame.Color(0,0,0)
BLUE = pygame.Color(86,145,204)
DRED = pygame.Color(91,57,57)

FPS = 60


clock = pygame.time.Clock()

font = pygame.font.SysFont('roboto',22)
text_surface = font.render('Some Text', False, WHITE)



def DrawWindow():
    global infected
    global recovered
    global dead
    infected = 0
    recovered = 0
    dead = 0
    screen.fill(BLACK)
    counter = time.time()
    target_list_active = []
    for v,t in enumerate(ball):
        target_list_active.append(ball[v].target)
        ball[v].move(ball[v].id)
        ball[v].change_state()
        
        if ball[v].inf == 0:    
            for b in ball[v-1:]:
                if b.inf == 1:
                    ball[v].check(b)
        ball[v].draw(screen)
        if ball[v].inf == 0:
            infected += 1
        if ball[v].inf == 3:
            recovered += 1
        if ball[v].inf == 2:
            dead += 1
        ball[v].recover()
    
    day_str = "Day: " + str(days)
    inf_str = "Infected: "+ str(infected)
    rec_str = "Recovered: "+ str(recovered)
    dead_str = "Dead: "+ str(dead)
    text_surface = font.render(day_str, False, WHITE)
    text_surface2 = font.render(inf_str, False, WHITE)
    text_surface3 = font.render(rec_str, False, WHITE)
    text_surface4 = font.render(dead_str, False, WHITE)
    
    
    screen.blit(text_surface,(0,0))
    screen.blit(text_surface2,(0,25))
    screen.blit(text_surface3,(0,50))
    screen.blit(text_surface4,(0,75))
    pygame.display.update()
    #print("it took", time.time() - counter, "seconds.")
    #print(set([x for x in target_list_active if target_list_active.count(x) > 1]))
    
        
def randx():
    return random.randint(SIZE_TEXT_X + person_size ,SIZE_X - person_size)
def randy():
    return random.randint(SIZE_TEXT_Y + person_size,SIZE_Y - person_size)
    
def debug_gm():
    pygame.time.wait(60)

def debug_people(list):
    for i,lister in enumerate(list):
        print(list[i].id,list[i].target)
                
            
                
            


class person(object):
    def __init__(self,x,y,inf,state,id):
    #give the person an x,y,infected state, and a movement state.
    #infect is 0 for infected, 1 for not infect, 2 for dead, 3 for recovered.
    #state is 0 for stationary and 1 for moving. 
        self.x = x
        self.y = y
        self.x_start = x
        self.y_start = y
        self.inf = inf
        self.infected = -1
        self.state = state
        self.r = person_size
        self.target = -1    
        self.color = WHITE
        self.id = id
        self.speed = random.uniform(0.2,2)
        
    def draw(self,screen):
        if self.inf == 0:
            self.color = RED
            if self.target == -1:
                my_target_x = self.x_start
                my_target_y = self.y_start
            else:
                my_target_x = ball[self.target].x
                my_target_y = ball[self.target].y
            #pygame.draw.line(screen,RED,(self.x,self.y),(my_target_x,my_target_y))
            #print(self.target)
        if self.inf == 1:
            self.color = WHITE
        if self.inf == 2:
            self.color = DRED
            my_target_x = self.x_start
            my_target_y = self.y_start
            pygame.draw.line(screen,RED,(self.x,self.y),(my_target_x,my_target_y))
        if self.inf == 3:
            self.color = BLUE
        
        #print(screen,self.color,(int(self.x),int(self.y)),self.r)
        pygame.draw.circle(screen,self.color,(int(self.x),int(self.y)),self.r)
        
    def move(self,id):
        #print(self)
        #move at a random angle 
        if self.state == 0:
            return
        if self.target == -1:
            target_y = self.y_start - self.r
            target_x = self.x_start - self.r
            
        else:
            try:
                target_y = ball[self.target].y - self.r
                target_x = ball[self.target].x - self.r
            except:
                print("Error here!")
        radians = math.atan2(target_y - self.y, target_x - self.x)
        distance = math.hypot(target_x - self.x ,  target_y - self.y) / speed
        distance = int(distance)
        
        dx = math.cos(radians) * self.speed
        dy = math.sin(radians) * self.speed
                
        #pygame.draw.line(screen,RED,(self.x,self.y),(target_x,target_y))
        
        if distance:
            
            self.x += dx
            self.y += dy
            if self.x > SIZE_X:
                self.picknew()
            if self.y > SIZE_Y:
                self.picknew()
            if self.x < SIZE_TEXT_X + self.r:
                self.picknew()
            if self.y < SIZE_TEXT_Y + self.r:
                self.picknew()
        #collision occured. 
        if distance < self.r * 4:
            
            #print(self.target,target_list)
            if self.target in target_list:
                target_list.remove(self.target)
            #print(target_list)
            
            #debug_people(ball)
            self.infect()
            self.picknew()
            
    def picknew(self):
        
        if self.state == 0:
            return
        if self.inf == 2:
            return
        found = False
        fail = 0
        while not found:
            fail += 1
            dice = random.randint(1,100)
            if dice < home_chance:
                try: 
                    target_list.remove(self.target)
                except:
                    pass
                self.target = -1
                found = True
            seed = random.randint(0,max_peeps-1)
            #print(seed,target_list)
            
            if seed not in target_list:
                target_list.append(seed)
                self.target = seed
                found = True
            if fail > max_peeps:
                target_list.remove(seed)
        #print(set([x for x in target_list if target_list.count(x) > 1]))
                
    def infect(self):
        if self.target == -1:
            return
        if self.inf > 1 or ball[self.target].inf > 1:
            return
        dice = random.randint(1,100)
        if dice < inf_chance and self.inf == 0:
            ball[self.target].inf = 0
            ball[self.target].infected = days
        elif dice < inf_chance and ball[self.target].inf == 0:
            self.inf = 0
            self.infected = days
            
    def infect_collide(self,person):
        dice = random.randint(1,100)
        if self.inf > 1 or person.inf > 1:
            return
        if dice < inf_chance and self.inf == 0:
            person.inf = 0
            person.infected = days
        elif dice < inf_chance and person.inf == 0:
            self.inf = 0 
            self.infected = days
            
    def recover(self):
        if days-self.infected > 21 and self.inf == 0:
            dice = random.randint(0,100)
            if dice < recover_chance:
            
                self.inf = 3
            else: 
                dice = random.randint(0,100)
                if dice < death_chance:
                    self.inf = 2
                    self.kill()
                else:
                    self.infected += 1
    def check(self,person):
        try:
            target_y = person.y - self.r
            target_x = person.x - self.r
        except:
            print("error")
            print(type(person))
        #radians = math.atan2(target_y - self.y, target_x - self.x)
        sum = (target_x - self.x)**2  +(target_y - self.y)**2
        distance = math.sqrt(sum) #/ speed
        distance = int(distance)
        
        # dx = math.cos(radians) * self.speed
        # dy = math.sin(radians) * self.speed
        
        if distance < self.r:
            self.infect_collide(person)
            
    
            
            
    def change_state(self):
        dice = random.randint(1,100)
        change = 10
        if self.inf == 2:
            return
        if dice < change:
            if self.state == 0:
                self.state = 1
            else:
                self.state = 0
                self.picknew()
                    
    def kill(self):
        #we want to send our dead particle to the top starting from 
        # SIZE_TEXT_X,SIZE_TEXT_Y
        
        
        self.target = -1 
        self.x_start = SIZE_TEXT_X + (self.id + (max_peeps / 10 / 2))
        self.y_start = 10
        self.state = 1
        self.speed = 2
        
        pass
        
        
        
ball = []
count = 0
#spawn 100 random people 
for i in range(0,max_peeps):
    
    #print(max_inf)
    if i < max_inf:
        move = random.randint(0,1) 
        infected = 0
    else:
        infected = 1
        move = random.randint(0,1)

    ball.append(person(randx(),randy(),infected,move,i))
print(len(ball))

for i in range(0,max_peeps):
    ball[i].picknew()

last_day = 0
timer = 0
infection_list = []
dead_list = []
recovered_list = []
days = 0
day_list = []
counter = time.time()
frames = 0
count = 0
while True:
    timer += 1
    
    if days < int(timer / FPS):
        print("it took", time.time() - counter, "seconds.")
        counter = time.time()
        infection_list.append(infected)
        dead_list.append(dead)
        recovered_list.append(recovered)
        day_list.append(int(timer / FPS))
        print("Day: ", days,"Infected: ",infected,"Dead: ",dead,"Recovered: ",recovered)
    days = int(timer / FPS)
    
    
    #pressed = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        pygame.event.pump()
        # if pressed[pygame.K_ESCAPE]:
            # quit()
    DrawWindow()
    frames += 1
    # file = "img/" + str(frames) +".bmp"
    # if frames%5 == 0:
        # count += 1
        # file = "img/" + str(count) +".bmp"
        # pygame.image.save(screen,file)
    clock.tick(FPS)
    if infected == 0:
        print(infection_list)
        print(dead_list)
        print(recovered_list)
        fig, ax = plt.subplots()
        ax.plot(day_list,infection_list, label="Infections")
        ax.plot(day_list,recovered_list, label="Recovered")
        ax.plot(day_list,dead_list, label="Dead")
        plt.ticklabel_format(style = 'plain')
        ax.legend()
        plt.show()
        quit()