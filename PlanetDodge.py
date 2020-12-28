import pygame
from random import randint
from math import sqrt
from time import clock


class Planet:
    def __init__(self, image, x_position, y_position, velocity = [1, "down"]):
        self.image = image
        self.x_position = x_position
        self.y_position = y_position
        self.velocity = velocity
    def planet_velocity(self, time):
        if (self.velocity[0] <= 5 and self.velocity[1] == "down"):
            self.velocity[0] = 1 + (time / 60)
        elif (self.velocity[0] >= -5):
            self.velocity[0] = -1 - (time / 60)
    def planet_position(self, screen):
        self.y_position += self.velocity[0]
        if (self.velocity[1] == "down" and self.y_position >= 816):
            self.x_position = randint(-20, 390)
            self.y_position = -100
        elif (self.y_position <= -150):
            self.x_position = randint(-20, 390)
            self.y_position = 850
        screen.blit(self.image, (self.x_position, self.y_position))


class Shuttle:
    def __init__(self, image):
        self.image = image
        self.x_position = 200
        self.y_position = 300
        self.x_speed = 0
        self.y_speed = 0
    def shuttle_position(self, screen):
        self.x_position += self.x_speed
        self.y_position += self.y_speed
        if (self.x_position <= -20):
            self.x_position = -15
        if (self.x_position >= 410):
            self.x_position = 405
        if (self.y_position <= -5):
            self.y_position = 0
        if (self.y_position >= 640):
            self.y_position = 635
        screen.blit(self.image, (self.x_position, self.y_position))


def collision_check(shuttle, planet):
    x_difference = (planet.x_position - shuttle.x_position - 9) ** 2
    x_absolute = abs(planet.x_position - shuttle.x_position - 9) < 12
    y_difference = (planet.y_position - shuttle.y_position - 10) ** 2
    top_distance = (sqrt(x_difference + y_difference) <= 74) and x_absolute
    x_difference = (planet.x_position - shuttle.x_position - 9) ** 2
    x_absolute = abs(planet.x_position - shuttle.x_position - 9) < 10
    y_difference = (planet.y_position - shuttle.y_position) ** 2
    bottom_distance = (sqrt(x_difference + y_difference) <= 74) and x_absolute
    x_difference = (planet.x_position - shuttle.x_position - 9) ** 2
    y_difference = (planet.y_position - shuttle.y_position) ** 2
    overall_distance = (sqrt(x_difference + y_difference) <= 74)
    return (overall_distance or top_distance or bottom_distance)


def generate_planets():
    generated_planets = []
    planet_choices = ["images/planet_one.png", "images/planet_two.png", "images/planet_three.png", "images/planet_four.png"]
    for iteration in range(6):
        planet_selection = randint(0, 3)
        planet_image = pygame.image.load(planet_choices[planet_selection])
        planet_image = pygame.transform.scale(planet_image, (128, 128))
        if (iteration % 2 == 0):
            new_planet = Planet(image=planet_image, x_position=-200, y_position=randint(0, 750))
            generated_planets.append(new_planet)
        else:
            new_planet = Planet(image=planet_image, x_position=-200, y_position=randint(0, 750), velocity=[-1, "up"])
            generated_planets.append(new_planet)
    return generated_planets


def generate_shuttle():
    shuttle_image = pygame.image.load("images/shuttle.png")
    shuttle_image = pygame.transform.scale(shuttle_image, (112, 112))
    generated_shuttle = Shuttle(shuttle_image)
    return generated_shuttle


pygame.init()
screen = pygame.display.set_mode((500, 750))
background = pygame.image.load("images/space.png")
shuttle_icon = pygame.image.load("images/shuttle.png")
pygame.display.set_caption("PLANET DODGE")
pygame.display.set_icon(shuttle_icon)
font_type = pygame.font.SysFont("Comic Sans", 45)


def new_game():
    planets = generate_planets()
    shuttle = generate_shuttle()
    time_start = clock()
    while (True):
        screen.blit(background, (0, 0))
        time_display = font_type.render("SCORE: " + str(int(clock() - time_start)), True, (255, 255, 255))
        screen.blit(time_display, (10, 10))
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                exit()
            if (event.type == pygame.KEYDOWN):
                if (event.key == pygame.K_a):
                    shuttle.x_speed = -5
                if (event.key == pygame.K_d):
                    shuttle.x_speed = 5
                if (event.key == pygame.K_w):
                    shuttle.y_speed = -5
                if (event.key == pygame.K_s):
                    shuttle.y_speed = 5
            if (event.type == pygame.KEYUP):
                if (event.key == pygame.K_a or event.key == pygame.K_d):
                    shuttle.x_speed = 0
                if (event.key == pygame.K_w or event.key == pygame.K_s):
                    shuttle.y_speed = 0
        shuttle.shuttle_position(screen)
        for planet in planets:
            current_time = clock() - time_start
            planet.planet_velocity(current_time)
            planet.planet_position(screen)
            if (collision_check(planet, shuttle) == True):
                return 0
        pygame.display.update()


new_game()
while (True):
    pygame.draw.rect(screen, (255, 255, 255), (20, 362, 462, 50))
    continue_game = font_type.render("PRESS SPACE TO PLAY AGAIN", True, (0, 0, 0))
    screen.blit(continue_game, (25, 375))
    pygame.display.update()
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            exit()
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
            new_game()
