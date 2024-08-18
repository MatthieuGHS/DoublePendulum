import math
import time
import pygame
import pygame.gfxdraw
from scipy.integrate import odeint

pygame.init()
screen = pygame.display.set_mode((650, 600))
clock = pygame.time.Clock()
running = True

xc, yc = (screen.get_width() / 2, screen.get_height() / 2)

g = 9.81
m1 = 5
m2 = 5
l1 = 100
l2 = 100

theta0_1 = math.pi/2
theta0_2 = math.pi/2
theta_v0_1 = 0
theta_v0_2 = 0

# Conditions initiales pour odeint
initial_state = [theta0_1, theta_v0_1, theta0_2, theta_v0_2]

path = []

def equations(state, t):
    theta_1, theta_v_1, theta_2, theta_v_2 = state

    num1_1 = -g * (2 * m1 + m2) * math.sin(theta_1)
    num2_1 = -m2 * g * math.sin(theta_1 - 2 * theta_2)
    num3_1 = -2 * math.sin(theta_1 - theta_2) * m2 * (theta_v_2**2 * l2 + theta_v_1**2 * l1 * math.cos(theta_1 - theta_2))
    den1 = l1 * (2 * m1 + m2 - m2 * math.cos(2 * theta_1 - 2 * theta_2))

    theta_a_1 = (num1_1 + num2_1 + num3_1) / den1

    fact = 2 * math.sin(theta_1 - theta_2)
    num1_2 = theta_v_1**2 * l1 * (m1 + m2)
    num2_2 = g * (m1 + m2) * math.cos(theta_1)
    num3_2 = theta_v_2**2 * l2 * m2 * math.cos(theta_1 - theta_2)
    den2 = l2 * (2 * m1 + m2 - m2 * math.cos(2 * theta_1 - 2 * theta_2))

    theta_a_2 = (fact * (num1_2 + num2_2 + num3_2)) / den2

    return [theta_v_1, theta_a_1, theta_v_2, theta_a_2]

t = 0
dt = 1/60 * 3

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  

    screen.fill("white")

    t_values = [t, t + dt]
    state = odeint(equations, initial_state, t_values)[1]
    theta_1, theta_v_1, theta_2, theta_v_2 = state

    x1, y1 = xc + math.sin(theta_1) * l1, yc + math.cos(theta_1) * l1
    x2, y2 = x1 + math.sin(theta_2) * l2, y1 + math.cos(theta_2) * l2

    path.append((x2, y2))

    pygame.draw.circle(screen, "black", (xc, yc), 5)

    pygame.draw.aaline(screen, "black", (xc, yc), (x1, y1))
    pygame.draw.circle(screen, "blue", (x1, y1), 10)
    pygame.draw.aaline(screen, "black", (x1, y1), (x2, y2))
    pygame.draw.circle(screen, "blue", (x2, y2), 10)

    if len(path) >= 2:
        for i in range(1, len(path)):
            pygame.draw.aaline(screen, "black", path[i-1], path[i])

    pygame.display.flip()
    clock.tick(60)

    initial_state = [theta_1, theta_v_1, theta_2, theta_v_2]
    t += dt*10

pygame.quit()
