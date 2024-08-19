import math
import time
import pygame
import pygame.gfxdraw
from scipy.integrate import odeint

pygame.init()
screen = pygame.display.set_mode((1000, 850))
clock = pygame.time.Clock()

xc, yc = (screen.get_width() / 2, screen.get_height() / 2)
g = 9.81


class Pendule():
    def __init__(self) :
        self.color = "blue"
        self.m1 = 5
        self.m2 = 5
        self.l1 = 200
        self.l2 = 200
        self.f = 1/10000*0 
        self.var = (self.m1,self.m2,self.l1,self.l2)
        self.theta0_1 = 2*math.pi/3
        self.theta0_2 = math.pi - math.pi/100
        self.theta_v0_1 = 0
        self.theta_v0_2 = 0

        self.initial_state = [self.theta0_1, self.theta_v0_1, self.theta0_2, self.theta_v0_2]

        self.path = []

    def update(self):
        self.initial_state = [self.theta0_1, self.theta_v0_1, self.theta0_2, self.theta_v0_2]


def equations(state, t, m1, m2, l1, l2):
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

def main():
    running = True
    t = 0
    dt = 1/60 * 3
    p1 = Pendule()
    p2 = Pendule()
    p2.color = "red"
    p2.theta0_2 = math.pi - math.pi/102
    p2.update()

    p = [p1,p2]

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  

        screen.fill("white")
        t_values = [t, t + dt]

        for pend in p :
            m1, m2, l1, l2 = pend.var
            pend.state = odeint(equations, pend.initial_state, t_values, args=(m1, m2, l1, l2))[1]
            pend.theta_1, pend.theta_v_1, pend.theta_2, pend.theta_v_2 = pend.state

            pend.theta_v_1 -= pend.f*pend.theta_v_1
            pend.theta_v_2 -= pend.f*pend.theta_v_2

            x1, y1 = xc + math.sin(pend.theta_1) * pend.l1, yc + math.cos(pend.theta_1) * pend.l1
            x2, y2 = x1 + math.sin(pend.theta_2) * pend.l2, y1 + math.cos(pend.theta_2) * pend.l2

            pend.path.append((x2, y2))

            pygame.draw.circle(screen, "black", (xc, yc), 5)

            pygame.draw.aaline(screen, "black", (xc, yc), (x1, y1))
            pygame.draw.circle(screen, pend.color, (x1, y1), 10)
            pygame.draw.aaline(screen, "black", (x1, y1), (x2, y2))
            pygame.draw.circle(screen, pend.color, (x2, y2), 10)

            if len(pend.path) >= 2:
                for i in range(1, len(pend.path)):
                    pygame.draw.aaline(screen, pend.color, pend.path[i-1], pend.path[i])

            pend.initial_state = [pend.theta_1, pend.theta_v_1, pend.theta_2, pend.theta_v_2]

        pygame.display.flip()
        clock.tick(60)
        t += dt*10
main()
pygame.quit()
