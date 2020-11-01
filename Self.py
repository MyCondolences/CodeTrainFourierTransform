import math
import pygame
import time
from CodingTrainLogo import drawing

PI_Two = 2 * math.pi
PI = math.pi
Mytime = 0
disp_width = 1280
disp_height = 1080

fourierX = []
fourierY = []

time_start = time.process_time()

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

Display = pygame.display.set_mode((disp_width, disp_height))
Display.fill(black)

pixAr = pygame.PixelArray(Display)
pixAr[10][20] = green

# pygame.draw.line(Display, blue, (100, 200), (300, 450), 5)

# pygame.draw.polygon(Display, green, ((25, 75), (76, 125), (250, 375), (400, 25), (60, 540)))

x = []
y = []
path = []


def dft(xElement):
    X = []
    N = len(xElement)
    for k in range(N):
        re = 0
        im = 0
        for n in range(N):
            phi = (PI_Two * k * n) / N
            re += xElement[n] * math.cos(phi)
            im -= xElement[n] * math.sin(phi)

        re = re / N
        im = im / N

        freq = k
        amp = math.sqrt(re * re + im * im)
        phase = math.atan2(im, re)

        X.append((re, im, freq, amp, phase))
    return X


# dtf returns 0:re 1:im 2:freq 3:amp 4:phase


def setup():
    global fourierX
    global fourierY
    steps = 5
    for i in range(0, len(drawing), steps):
        x.insert(0, round(drawing[i][0]))
        y.insert(0, round(drawing[i][1]))

    fourierX = dft(x)
    fourierY = dft(y)

    fourierX.sort(key=lambda me: me[3], reverse=True)  # sorts 2d array by amplitude
    fourierY.sort(key=lambda me: me[3], reverse=True)  # largest to smallest


def epi_cycle(xElement, yElement, rotation, fourier):
    for i in range(len(fourier)):
        prevx = xElement
        prevy = yElement

        # fourier 0:re 1:im 2:freq 3:amp 4:phase

        freq = fourier[i][2]
        radius = fourier[i][3]
        phase = fourier[i][4]
        xElement += radius * math.cos(freq * Mytime + phase + rotation)
        yElement += radius * math.sin(freq * Mytime + phase + rotation)

        pygame.draw.circle(Display, white, (round(prevx), round(prevy)), math.ceil(radius), 1)
        pygame.draw.line(Display, blue, (round(prevx), round(prevy)), (round(xElement), round(yElement)), 1)
    Vector = (xElement, yElement)
    return Vector


def draw():
    global Display
    global Mytime
    global time_start
    global path

    Display.fill(black)

    vx = epi_cycle(disp_width / 2 + 100, 100, 0, fourierX)
    vy = epi_cycle(100, disp_height / 2 + 100, PI / 2, fourierY)
    # vectors return 0:x 1:y
    v = (vx[0], vy[1])
    path.insert(0, v)
    pygame.draw.line(Display, blue, (round(vx[0]), round(vx[1])), (round(v[0]), round(v[1])), 1)
    pygame.draw.line(Display, blue, (round(vy[0]), round(vy[1])), (round(v[0]), round(v[1])), 1)

    for i in range(len(path) - 1):
        pygame.draw.line(Display, blue, (round(path[i][0]), round(path[i][1])),
                         (round(path[i + 1][0]), round(path[i + 1][1])), 1)

    dt = PI_Two / len(fourierX)
    Mytime += dt

    if Mytime > PI_Two:
        time.sleep(2.5)
        Mytime = 0
        path = []

        # radius = 50
    # pygame.draw.circle(Display, white, (200, 200), radius, 1)
    #
    # x = round(radius * math.cos(Mytime) + 200)
    # y = round(radius * math.sin(Mytime) + 200)
    # pygame.draw.circle(Display, green, (x, y), 4)

    # Mytime += time.process_time() - time_start
    # time_start = time.process_time()


setup()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    draw()
    pygame.display.update()
