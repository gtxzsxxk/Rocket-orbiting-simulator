import pygame
import os
import random
import time
import math
import threading
from decimal import Decimal
import numpy

"""
CONFIGURATIONS
"""
PARTICLE_NUMBER = 100
PARTICLE_RANGE = 10
PARTICLE_VELOCITY = 130
PARTICLE_DRAW_FPS = 30

PHYSICS_CRASH_VELOCITY = 50

GRAPHICS_CLOUDS_DELAY = 30
GRAPHICS_CLOUD_DRAW_ALT = 300
INFINITE_FUEL = 0
TRACK_RECORD = 100

"""
粒子系统
"""
# PARTICLE SYSTEM
PARTICLESYS_EFFECT_SPOUT = 0
PARTICLESYS_EFFECT_CLOUD = 1
# PARTICLESYS_FPS=10


class Particle:
    x = 0
    y = 0
    v = 0
    direction = 0

    def __init__(self, x, y, v, dir):
        self.x = x
        self.y = y
        self.v = v
        self.direction = dir


class Cloud:
    x = 0
    y = 0

    def __init__(self, direction=0):  # if direction head to 0 ,
        # it means the velocity is upper.Clouds should be loaded from screen's top
        self.x = random.randint(10, 610)
        if direction == 0:
            self.y = -188
        else:
            self.y = 800


class ParticleSys(threading.Thread):
    particles = []  # store particles' location as class defining
    clouds = []  # store the cloud's data, being called and drawn in the GameManager
    mode = 0
    number = 0
    # range=0
    lx = 0
    ly = 0
    v = 0
    d = 0
    cloudcnt = 0

    def __init__(self):
        super(self.__class__, self).__init__()
        self.__flag = threading.Event()  # 用于暂停线程的标识
        self.__flag.set()  # 设置为True
        self.__running = threading.Event()  # 用于停止线程的标识
        self.__running.set()  # 将running设置为True

    def addParticlesEffect(self, mode, number, x, y, v, d):
        self.mode = mode
        self.number = number
        # self.range=range
        self.lx = x
        self.ly = y
        self.v = v
        self.d = d

    def UpdateVD(self, v, d):
        self.v = v
        self.d = d

    def throttleOffset(self, t):
        return -0.06 * t * t + 6.9 * t

    def run(self):
        while True:
            time.sleep(1 / PARTICLE_DRAW_FPS)
            stdx = self.lx - 60 * math.sin(rocket.direction)
            stdy = self.ly + 60 * math.cos(rocket.direction)
            # spout new particles
            if rocket.engine_throttle > 0 and rocket.engine_on == 1:
                for i in range(
                    int(
                        self.number
                        / PARTICLE_DRAW_FPS
                        * self.throttleOffset(rocket.engine_throttle)
                        / 100
                    )
                ):
                    nx = random.randint(-PARTICLE_RANGE, PARTICLE_RANGE) + stdx
                    ny = random.randint(-PARTICLE_RANGE, PARTICLE_RANGE) + stdy
                    nd = 3.14 + random.randint(-52, 52) / 100.0
                    self.particles.append(Particle(nx, ny, self.v, nd))

            del_list = []
            for i in self.particles:
                # particles motion
                if i.x >= 800 or i.y >= 600 or i.x < 0 or i.y < 0:
                    del_list.append(i)
                    continue
                i.x = (
                    i.x
                    + i.v
                    * math.sin(rocket.direction + i.direction)
                    * 1
                    / PARTICLE_DRAW_FPS
                )
                i.y = (
                    i.y
                    - i.v
                    * math.cos(rocket.direction + i.direction)
                    * 1
                    / PARTICLE_DRAW_FPS
                )  # + or -????

            # kill particles
            for i in del_list:
                self.particles.remove(i)

            # As for Clouds
            self.cloudcnt = self.cloudcnt + 1
            if rocket.py > GRAPHICS_CLOUD_DRAW_ALT and rocket.py < 16000:
                if self.cloudcnt > GRAPHICS_CLOUDS_DELAY:
                    self.cloudcnt = 0
                    cl = None
                    if rocket.vy > 0:
                        cl = Cloud()
                    else:
                        cl = Cloud(direction=1)
                    self.clouds.append(cl)
                    # print("clouds added y="+str(cl.x))
            cl_dellist = []
            for ccl in self.clouds:
                ccl.y = ccl.y + rocket.vy * 1 / PARTICLE_DRAW_FPS
                ccl.x = ccl.x - rocket.vx * 1 / PARTICLE_DRAW_FPS
                if ccl.y > 800 or ccl.y < -200 or ccl.x < -200 or ccl.x > 1000:
                    cl_dellist.append(ccl)

            # kill clouds
            for i in cl_dellist:
                self.clouds.remove(i)

            """if self.mode==PARTICLESYS_EFFECT_CLOUD:
                time.sleep(1/GRAPHICS_CLOUDS_NUMBER)
                #put new clouds
                nx = random.randint(100, 600)
                ny = random.randint(50, 500)
                self.particles.append(Particle(nx, ny, self.v, self.d))

                del_list = []
                for i in self.particles:
                    # particles motion
                    if i.x >= 800 or i.y >= 600 or i.x < 0 or i.y < 0:
                        del_list.append(i)
                        continue
                    i.x = i.x + i.v  * 1 / PARTICLESYS_FPS
                    i.y = i.y - i.v  * 1 / PARTICLESYS_FPS

                # kill particles
                for i in del_list:
                    self.particles.remove(i)
            #graphics
            if rocket.engine_on==1:
                for p in self.particles:
                    pimage = pygame.transform.scale(pygame.image.load(r"resources/particle.png"), (7, 7))
                    prect = pimage.get_rect().move(p.x - 3.5, p.y)
                    screen.blit(pimage, prect)"""

    def pause(self):
        self.__flag.clear()  # 设置为False, 让线程阻塞

    def resume(self):
        self.__flag.set()  # 设置为True, 让线程停止阻塞


class ParticleDrawer(threading.Thread):
    def run(self):
        if particlesys != None:
            particlesys.number = rocket.engine_throttle / 2
            for p in particlesys.particles:
                pimage = pygame.transform.scale(
                    pygame.image.load(r"resources/particle.png"), (7, 7)
                )
                prect = pimage.get_rect().move(p.x - 3.5, p.y - 15)
                screen.blit(pimage, prect)


# All the physical variables should involve their directions information by aing signs.


class PhyPoint:
    name = ""
    lx = 0
    ly = 600000
    height = 0
    ev = 0  # expected velocity
    tim = 0  # time to reach the point
    enable = 1


earthmass_const = 5.29 * 10**22
gravity_const = 6.67 * 10**-11
sim_timebase = 0.01  # seconds

# Real World Atmosphere Calc:
pressure = 0
temperature = 0  # K
rou = 0  # kg/m^3


def calcPressure(height):
    global pressure
    # P=P0×（1-H/44300)^5.256
    pressure = 101325 * 2.718 ** (-height / 5800)


# referred to USSA data
def calcTemprature(height):
    global temperature
    h = height / 1000
    if height <= 11000:
        temperature = 288.15 - 6.5 * h
    elif height > 8800 and height <= 16000:
        temperature = 216.65
    elif height > 16000 and height <= 25600:
        temperature = 196.65 + h
    elif height > 25600 and height <= 37600:
        temperature = 139.05 + 2.8 * h
    elif height > 37600 and height <= 40800:
        temperature = 270.65
    elif height > 40800 and height <= 56800:
        temperature = 413.45 - 2.8 * h
    elif height > 56800 and height <= 68800:
        temperature = 356.65 - 2 * h


def calcRou(height):
    global pressure, temperature, rou
    calcPressure(height)
    calcTemprature(height)
    rou = pressure * 29 / 8.314 / temperature / 1000  # not the best way
    return rou


class PhyObject:
    name = ""
    mass = 0
    px = 0  # GLOBAL!
    py = 600000  # GLOBAL!
    vx = 0
    vy = 0
    ax = 0
    ay = 0
    crashed = False
    air_dragforce = 0
    last_radium = 0
    dist = 0
    dist2 = 0
    height = 0
    horizondisplacement = 0
    orbit_track = []  # (x,y)
    apPoint = None
    pePoint = None
    orbitangle = 0
    tanangle = 0
    onOrbit = 0
    lastx = 0
    lasty = 0
    tanangle_sin = 0  # to describe the orbit tangent angle
    tanangle_cos = 0

    def __int__(self, name, mass, px, py, vx, vy):
        self.name = name
        self.mass = mass
        self.px = px
        self.py = py
        self.vx = vx
        self.vy = vy

    def __init__(self, name, mass):
        self.name = name
        self.mass = mass

    def GetAlt(self):
        return self.py

    def UserForcesCompute(self):
        return

    def Calculate(self):
        self.ax = 0
        self.ay = 0
        # accumulate velocity onto displacement
        # radium = (self.px % 3768000) / 600000
        self.px = self.px + self.vx * sim_timebase
        # self.py = (self.py + self.vy * sim_timebase)+(600000-600000*math.cos(radium))- \
        #          +(600000 - 600000 * math.cos(self.last_radium))
        self.py = self.py + self.vy * sim_timebase

        # process outside forces' effects first
        self.UserForcesCompute()
        # process default forces as gravity and air drag
        # gravity
        self.dist2 = self.px * self.px + self.py * self.py
        self.dist = math.sqrt(self.dist2)
        self.height = self.dist - 600000
        angelwithy = math.acos(self.py / self.dist)  # radius
        self.horizondisplacement = angelwithy * 600000
        if self.dist != 600000:
            self.ax = (
                self.ax
                - gravity_const * earthmass_const / self.dist2 * self.px / self.dist
            )
            self.ay = (
                self.ay
                - gravity_const * earthmass_const / self.dist2 * self.py / self.dist
            )
        # air drag
        calcRou(self.height)
        v = math.sqrt(self.vx * self.vx + self.vy * self.vy)
        if v > PHYSICS_CRASH_VELOCITY and self.height < 0:
            self.crashed = True
        elif v <= PHYSICS_CRASH_VELOCITY and self.height < 0:

            self.py = math.sqrt(self.dist2 - self.px * self.px)
            self.px = math.sqrt(600000 * 600000 - self.py * self.py)
            self.vx = 0
            self.vy = 0
            return

        if v > 0 and self.height < 68000:

            acc_airdrag = (
                0.5 * rou * (self.vx * self.vx + self.vy * self.vy) * 0.2 * 0.008
            )
            self.air_dragforce = acc_airdrag * self.mass
            acc_airdrag_x = abs(acc_airdrag * self.vx / v)
            acc_airdrag_y = abs(acc_airdrag * self.vy / v)

            if self.vx > 0:
                self.ax = self.ax - acc_airdrag_x
            elif self.vx <= 0:
                self.ax = self.ax + acc_airdrag_x

            if self.vy > 0:
                self.ay = self.ay - acc_airdrag_y
            elif self.vy <= 0:
                self.ay = self.ay + acc_airdrag_y

        # accumulate accelerations onto velocity seperated by timebase
        self.vx = self.vx + self.ax * sim_timebase
        self.vy = self.vy + self.ay * sim_timebase
        # self.last_radium=radium

        if self.lastx == 0 and self.lasty == 0:
            self.lastx = self.px
            self.lasty = self.py

        # if self.onOrbit == 1:
        # if self.tanangle <= 2*3.14+0.01 and self.tanangle >= 2*3.14-0.01:
        #    self.tanangle = 0
        if self.px != self.lastx and self.py != self.lasty:
            tox = self.px - self.lastx
            toy = self.py - self.lasty
            tod = math.sqrt(tox * tox + toy * toy)
            # print(tox,toy,tod)
            self.tanangle_sin = toy / tod
            self.tanangle_cos = tox / tod
            # cosangle = self.cosCalc(nvx, nvy, 0, 1)
            # self.tanangle = math.acos(cosangle)
        self.lastx = self.px
        self.lasty = self.py

    def cosCalc(self, x1, y1, x2, y2):
        vector1 = numpy.array([x1, y1])
        vector2 = numpy.array([x2, y2])
        # print(hx1,hy1,d1)
        ans = float(vector1.dot(vector2))
        return ans / numpy.linalg.norm(vector1) / numpy.linalg.norm(vector2)

    def orbitCalc(self):
        bgx = self.px
        bgy = self.py
        qdd = math.sqrt(bgx * bgx + bgy * bgy)
        bgvector = (bgx, bgy)
        bglen = qdd
        cangle = 0  # accumulated angle
        tx = self.px
        ty = self.py
        _vx = self.vx
        _vy = self.vy
        self.orbit_track.clear()
        self.apPoint = PhyPoint()
        self.pePoint = PhyPoint()
        self.apPoint.name = "Ap"
        self.apPoint.name = "Fe"
        lastDist = 0
        # for i in range(429496):
        cnt = 0
        maxheight = 0
        minheight = 99999999999
        maxcircle = 15000
        timb = 5
        for i in range(maxcircle):
            cnt = cnt + 1
            dd2 = tx * tx + ty * ty
            dd = math.sqrt(dd2)

            aax = -gravity_const * earthmass_const / dd2 * tx / dd
            aay = -gravity_const * earthmass_const / dd2 * ty / dd
            _vx = _vx + aax * timb
            _vy = _vy + aay * timb
            tx = tx + _vx * timb
            ty = ty + _vy * timb
            if dd > 600000:
                self.orbit_track.append((tx, ty))
            else:
                self.pePoint.enable = 0
                break

            current_vector = (tx, ty)
            cosangle = self.cosCalc(tx, ty, bgx, bgy)
            current_angle = math.acos(cosangle)
            cangle = cangle + current_angle
            if cnt > 1000:
                if cangle >= 2 * 3.14:
                    break

            if dd > maxheight:
                maxheight = dd
                self.apPoint.height = maxheight - 600000
                self.apPoint.ev = math.sqrt(_vx * _vx + _vy * _vy)
                self.apPoint.name = "Ap"
                self.apPoint.tim = cnt * timb
                self.apPoint.lx = tx
                self.apPoint.ly = ty
            if dd < minheight:
                minheight = dd
                self.pePoint.height = minheight - 600000
                self.pePoint.ev = math.sqrt(_vx * _vx + _vy * _vy)
                self.pePoint.name = "Pe"
                self.pePoint.tim = cnt * timb
                self.pePoint.lx = tx
                self.pePoint.ly = ty
            bgvector = current_vector
            bglen = dd
            bgx = tx
            bgy = ty
        if minheight > 668000:
            self.onOrbit = 1
        else:
            self.onOrbit = 0


class Simulator(threading.Thread):
    phyobjs = []

    def addobj(self, obj):
        self.phyobjs.append(obj)

    def run(self):
        while True:
            for i in self.phyobjs:
                i.Calculate()

            time.sleep(0.01)


class Rocket(PhyObject):

    # Todo: 实现地球坐标系至火箭坐标系的变换
    engine_on = 0
    engine_throttle = 0
    engine_force = 0
    direction = 0  # clock order 0 for ↑
    si_sealevel = 0
    si_vacuum = 0
    fuel_speed = 0
    fuel = 0
    fuel_backup = 0
    fuel_perweight = 0

    def __init__(self, name, mass=0):
        self.name = name
        self.mass = mass
        f = open("rocket.txt", "r")
        lines = f.readlines()
        self.engine_force = float(lines[0]) * 1000
        self.si_sealevel = float(lines[1])
        self.si_vacuum = float(lines[2])
        self.fuel_speed = float(lines[3])
        self.fuel = float(lines[4])
        self.fuel_perweight = float(lines[5])
        self.mass = float(lines[6])
        self.fuel_backup = self.fuel
        f.close()

    def UserForcesCompute(self):
        # manage fuel
        if (self.fuel > 0 and self.engine_on > 0) or INFINITE_FUEL == 1:
            # compute engine'
            if INFINITE_FUEL == 0:
                self.fuel = (
                    self.fuel
                    - self.fuel_speed * sim_timebase * self.engine_throttle / 100
                )
                self.mass = (
                    self.mass
                    - self.fuel_speed
                    * sim_timebase
                    * self.fuel_perweight
                    * self.engine_throttle
                    / 100
                )
            angle = self.direction
            # todo: should consider computing the force's direction
            # angle_earth=self.orbitangle
            angle_earth = 0
            self.ax = (
                self.ax
                + self.engine_force
                * self.engine_throttle
                / 100
                * math.sin(angle + angle_earth)
                / self.mass
            )
            self.ay = (
                self.ay
                + self.engine_force
                * self.engine_throttle
                / 100
                * math.cos(angle + angle_earth)
                / self.mass
            )
        elif self.fuel <= 0:
            self.engine_on = 0


rocket = Rocket("rocket")
simulatorCtl = Simulator()

screen = None

rocket_image = None
rocket_image_s = pygame.transform.scale(
    pygame.image.load(r"resources/rocket.png"), (60, 93)
)
rocket_rect = rocket_image_s.get_rect().move(375, 360)

launchpad_image = pygame.transform.scale(
    pygame.image.load(r"resources/environment.png"), (2266, 600)
)
launchpad_rect = launchpad_image.get_rect().move(0, 0)

ground_image = pygame.transform.scale(
    pygame.image.load(r"resources/ground.png"), (800, 500)
)
ground_rect = ground_image.get_rect().move(0, 90)

launchshelf_image = pygame.transform.scale(
    pygame.image.load(r"resources/launchshelf.png"), (200, 400)
)
launchshelf_rect = launchshelf_image.get_rect().move(300, 270)

pimage = pygame.transform.scale(pygame.image.load(r"resources/particle.png"), (7, 7))

cloudimage = pygame.image.load(r"resources/cloud.png")

particlesys = None
spout_location = (400, 478)

fpsRate = 0
fpsLimit = 40

sound_engStart = None
sound_engStop = None
sound_engWorking = None
soud_explosion = None

orbit_Mode = False
showOrbitDirection = True
forceKeyboardCtl = False
tutorialMode = True
planet_image = pygame.transform.scale(
    pygame.image.load(r"resources/planet.png"), (200, 200)
)
planet_image_s = pygame.image.load(r"resources/planet.png")
planet_rect = planet_image.get_rect().move(300, 200)
zoom = 142 / 600000
trackrecord_cnt = 0
debugInfo = ""
bgdimg_s = pygame.transform.scale(
    pygame.image.load(r"resources/orbitbgd.png"), (800, 600)
)
bgdrect = bgdimg_s.get_rect()
bgdimg_n = bgdimg_s

arrowimg_s = pygame.transform.scale(pygame.image.load(r"resources/arrow.png"), (73, 56))


def change_alpha(img, alpha=255):
    width, height = img.get_size()
    for x in range(0, width):
        for y in range(0, height):
            r, g, b, old_alpha = img.get_at((x, y))
        if old_alpha > 0:
            img.set_at((x, y), (r, g, b, alpha))


def showTextLeftUp(str, column=0, color=(255, 255, 255)):
    fontobj = pygame.font.Font(r"resources/NotoSansHans-Regular.ttf", 16)
    # textSurfaceObj = fontobj.render(str, True, (255/100000*rocket.py,\
    # 255/100000*rocket.py, 255/100000*rocket.py))
    textSurfaceObj = fontobj.render(str, True, color)
    textSurfaceRect = textSurfaceObj.get_rect().move(10, column * 20 + 10)
    screen.blit(textSurfaceObj, textSurfaceRect)


def showRocketInfor(x, y):
    pygame.draw.aaline(screen, (255, 255, 255), (x, y), (x + 10, y))
    pygame.draw.aaline(screen, (255, 255, 255), (x + 10, y), (x + 20, y + 10))
    fontobj = pygame.font.Font(r"resources/NotoSansHans-Regular.ttf", 12)
    textSurfaceObj = fontobj.render(rocket.name, True, (255, 255, 255))
    textSurfaceRect = textSurfaceObj.get_rect().move(x + 20, y + 10)
    screen.blit(textSurfaceObj, textSurfaceRect)
    textSurfaceObj = fontobj.render(
        "速度:"
        + format(math.sqrt(rocket.vx * rocket.vx + rocket.vy * rocket.vy), ".1f")
        + " m/s",
        True,
        (255, 255, 255),
    )
    textSurfaceRect = textSurfaceObj.get_rect().move(x + 20, y + 25)
    screen.blit(textSurfaceObj, textSurfaceRect)
    textSurfaceObj = fontobj.render(
        "地表高度:" + format(rocket.height, ".1f") + " m", True, (255, 255, 255)
    )
    textSurfaceRect = textSurfaceObj.get_rect().move(x + 20, y + 40)
    screen.blit(textSurfaceObj, textSurfaceRect)


def showPtyInfor(p, order=0):
    if p.enable == 0 or rocket.height == 0:
        return
    x = int(400 + p.lx * zoom)
    y = int(300 - p.ly * zoom)

    pygame.draw.circle(screen, (200, 200, 200), (x, y), 3)
    # pygame.draw.aaline(screen, (255, 255, 255), (x, y), (580,  500+order*45))
    # pygame.draw.aaline(screen, (255, 255, 255),
    #                   (580,  500+order*45), (595,  500+order*45))
    fontobj = pygame.font.Font(r"resources/NotoSansHans-Regular.ttf", 12)
    textSurfaceObj = fontobj.render(p.name, True, (255, 255, 255))
    textSurfaceRect = textSurfaceObj.get_rect()
    if y >= 300:
        textSurfaceRect = textSurfaceObj.get_rect().move(x - 5, y + 2)
    else:
        textSurfaceRect = textSurfaceObj.get_rect().move(x + 5, y - 15)
    screen.blit(textSurfaceObj, textSurfaceRect)
    textSurfaceObj = fontobj.render(p.name, True, (255, 255, 255))
    textSurfaceRect = textSurfaceObj.get_rect().move(600, 500 + order * 45)
    screen.blit(textSurfaceObj, textSurfaceRect)
    textSurfaceObj = fontobj.render(
        "速度:" + format(p.ev, ".1f") + "m/s   地表:" + format(p.height, ".1f") + "m",
        True,
        (255, 255, 255),
    )
    textSurfaceRect = textSurfaceObj.get_rect().move(600, 500 + order * 45 + 15)
    screen.blit(textSurfaceObj, textSurfaceRect)
    textSurfaceObj = fontobj.render(
        "预计时间:" + format(p.tim / 60, ".1f") + " min", True, (255, 255, 255)
    )
    textSurfaceRect = textSurfaceObj.get_rect().move(600, 500 + order * 45 + 30)
    screen.blit(textSurfaceObj, textSurfaceRect)


def GameStart():
    global screen, simulatorCtl, particlesys, cloudsys, sound_engStart, sound_engStop, soud_explosion, sound_engWorking, tutorialMode
    # Graphics
    pygame.init()  # 初始化pygame
    pygame.key.set_repeat(70, 70)
    size = width, height = 800, 600  # 设置窗口大小
    screen = pygame.display.set_mode(size)  # 显示窗口
    pygame.display.set_caption("Rocket Orbiting Simulator")
    # physics
    simulatorCtl.addobj(rocket)
    simulatorCtl.start()
    particlesys = ParticleSys()
    particlesys.addParticlesEffect(
        PARTICLESYS_EFFECT_SPOUT,
        PARTICLE_NUMBER,
        406,
        407,
        PARTICLE_VELOCITY,
        3.14 + rocket.direction,
    )
    particlesys.start()
    sound_engStart = pygame.mixer.Sound(r"resources/sounds/elev_start.wav")
    sound_engStop = pygame.mixer.Sound(r"resources/sounds/elev_stop.wav")
    soud_explosion = pygame.mixer.Sound(r"resources/sounds/sound_explosion_debris1.wav")
    sound_engWorking = pygame.mixer.Sound(r"resources/sounds/sound_rocket_mini.wav")
    sound_engStart.set_volume(0.2)
    sound_engStop.set_volume(0.2)
    soud_explosion.set_volume(0.2)
    sound_engWorking.set_volume(0.2)
    pygame.mixer.init()
    pygame.mixer.music.load(r"resources/sounds/sound_ambience_nature.wav")
    screen.fill((0, 0, 0))
    showTextLeftUp("这是一个火箭发射物理模型", 0)
    showTextLeftUp("你需要使火箭成功进入轨道", 1)
    showTextLeftUp("注意：", 2)
    showTextLeftUp("天体模型参考了PC游戏《坎巴拉太空计划》中的Kerbin天体。", 3)
    showTextLeftUp("第一宇宙速度并非地球的7.9km/s 而是2.4km/s", 4)
    showTextLeftUp("程序现在进入演示模式 需要按照提示操作", 5)
    showTextLeftUp("节流阀显示的百分数是发动机功率的百分数", 6)
    showTextLeftUp("沿轨道顺向加速可以抬高轨道 逆向可以降低轨道", 7)
    showTextLeftUp("加速点提示的右水平方向是这个方向！沿屏幕方向水平向右[→]！", 8)
    showTextLeftUp("专有名词解释：", 9)
    showTextLeftUp("deltaV：火箭在真空下燃烧完所有燃料能得到的速度变化量", 10)
    showTextLeftUp("Vx Vy：沿绝对坐标系正交分解的速度矢量大小", 11)
    showTextLeftUp("程序中将有详细解析与提示。更多信息请参见文档。", 12)
    showTextLeftUp(
        "按T进入教程模式！！请认真观看程序执行，关注每一步变化。一旦出现提示更新必须马上执行。",
        13,
    )
    # 如果你能把飞船送入轨道，无论去太空中的任何地方，你都可以说自己已经走完了一半的道路。
    showTextLeftUp(
        "对于tutorial模式。如果错过提示更新，可能会导致轨道偏离预期等严重后果。请严格按照程序执行步骤。",
        14,
    )
    showTextLeftUp("按C进行自由任务。", 15)
    showTextLeftUp(
        "热键: [SPACE]：打开/关闭发动机 [Z]：最大节流阀 [X]：最小节流阀 [LSHIFT]：增大节流阀",
        16,
    )
    showTextLeftUp(
        "[LCTRL]：减小节流阀 [M]：进入轨道模式 [F]：无限燃料 [U]：一键入轨", 17
    )
    showTextLeftUp("[O]：时间加速 [P]：时间减速", 18)
    showTextLeftUp(
        "“如果你能把飞船送入轨道，无论去太空中的任何地方，你都可以说自己已经走完了一半的道路。”",
        20 + 1,
    )
    showTextLeftUp("引自《A Step Farther Out 》194页，作者 Jerry Pournelle", 20 + 2)
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    tutorialMode = False
                    return
                elif event.key == pygame.K_t:
                    tutorialMode = True
                    return


tipstep = 0
disableKey = False


def GetTips(r):
    global tipstep, rocke, rocket_image, orbit_Mode, disableKey, sim_timebase, zoom, forceKeyboardCtl
    if r.crashed == False and tipstep == 0:
        if r.height > 0:
            tipstep = 1
            rocket.direction = rocket.direction + 3.14 / 36
            rocket_image = pygame.transform.rotate(
                rocket_image, -rocket.direction * 180 / 3.14
            )
        rocket.engine_on = 1
        if orbit_Mode == True:
            showTextLeftUp(
                "轻按Z将油门设置到100%发射火箭。火箭将有适当的倾斜角度。这是正常的。",
                4,
                (200, 100, 100),
            )
        else:
            showTextLeftUp(
                "轻按Z将油门设置到100%发射火箭。火箭将有适当的倾斜角度。这是正常的。",
                5,
                (200, 100, 100),
            )
    elif tipstep == 1:
        if r.apPoint != None:
            if r.apPoint.height > 120000:
                tipstep = 2
                r.engine_throttle = 0
        if orbit_Mode == True:
            showTextLeftUp(
                "请保持当前状态继续上升。到达下一步（轨道远点在大气层外）时我们会自动关闭引擎。",
                4,
            )
            showTextLeftUp(
                "你需要上升到20,000米以上 此期间不要做任何操作 正在抬升火箭 请耐心等待（大概3分钟）",
                5,
            )
        else:
            showTextLeftUp(
                "请保持当前状态继续上升。到达下一步（轨道远点在大气层外）时我们会自动关闭引擎。",
                5,
            )
            showTextLeftUp(
                "你需要上升到20,000米以上 此期间不要做任何操作 正在抬升火箭 请耐心等待（大概3分钟）",
                6,
            )
    elif tipstep == 2:
        if r.height > 91000:
            tipstep = 3
        elif r.height > 87000:
            sim_timebase = 0.01
        if orbit_Mode == True:
            showTextLeftUp(
                "[无需开启引擎]最高点已经位于大气层外。1、按M进入轨道模式 2、轻按O键加快时间倍率",
                4,
            )
            showTextLeftUp(
                "在轨道模式（轻按M进入）下按H/N进行地图放大/缩小 请耐心等待 时间加速自动恢复后不要再加速",
                5,
            )
        else:
            showTextLeftUp(
                "[无需开启引擎]最高点已经位于大气层外。1、按M进入轨道模式 2、轻按O键加快时间倍率",
                5,
            )
            showTextLeftUp(
                "在轨道模式（轻按M进入）下按H/N进行地图放大/缩小 请耐心等待 时间加速自动恢复后不要再加速",
                6,
            )
    elif tipstep == 3:
        if r.direction >= 1.482 and r.direction <= 1.66:
            orbit_Mode = True
        if r.pePoint != None:
            if r.pePoint.height > 68000:
                tipstep = 4
                r.engine_throttle = 0
        if orbit_Mode == True:
            showTextLeftUp(
                "STEP1：1、轻按M进入火箭模式 2、按方向右键[→]将火箭旋转到右水平方向，到达角度后自动进入轨道模式。",
                4,
            )
            showTextLeftUp("STEP2:轻按Z加速。当入轨后，我们会自动关闭引擎。", 5)
        else:
            showTextLeftUp(
                "STEP1：1、轻按M进入火箭模式 2、按方向右键[→]将火箭旋转到右水平方向，到达角度后自动进入轨道模式。",
                5,
            )
            showTextLeftUp("STEP2:轻按Z加速。当入轨后，我们会自动关闭引擎。", 6)
    elif tipstep == 4:
        zoom = 142 / 600000
        if orbit_Mode == True:
            showTextLeftUp("你已进入轨道 演示部分已结束 关闭窗口结束程序", 4)
        else:
            showTextLeftUp("你已进入轨道 演示部分已结束 关闭窗口结束程序", 5)
        orbit_Mode = True
        disableKey = True


class OrbitCalcThread(threading.Thread):
    rcc = None
    flTyp = False

    def run(self):
        self.rcc.orbitCalc()
        self.flTyp = True


oct = None


def GameLoop():
    global screen, launchpad_image, launchpad_rect, rocket_image_s, rocket_image, rocket_rect, particlesys, launchshelf_rect, launchshelf_image, fpsRate, cloudlist, sound_engStop, sound_engStart, soud_explosion, sound_engWorking, ground_image, ground_rect, orbit_Mode, planet_image, planet_rect, planet_image_s, zoom, debugInfo, trackrecord_cnt, showOrbitDirection, bgdimg_s, bgdrect, bgdimg_n, sim_timebase, oct, disableKey, forceKeyboardCtl, tutorialMode
    fps_start = time.time()

    if oct == None:
        oct = OrbitCalcThread()
        oct.rcc = rocket
        oct.start()
    elif oct.flTyp == True:
        oct = OrbitCalcThread()
        oct.rcc = rocket
        oct.start()
    oct.join()
    # game-status
    if rocket.crashed == True:
        soud_explosion.play()
        showTextLeftUp("You Failed.Game Ends")
        pygame.display.flip()
        return
    if orbit_Mode == False:
        # Graphics
        if rocket.height < 59000:
            screen.fill(
                (
                    -100 / 68000 * rocket.height + 100,
                    -149 / 68000 * rocket.height + 149,
                    -237 / 68000 * rocket.height + 237,
                )
            )
        else:
            screen.fill((0, 0, 0))
            bgdimg_n = bgdimg_s
            # if rocket.height<69900:
            #    change_alpha(bgdimg_n,int(178/11000*rocket.height-877))
            screen.blit(bgdimg_n, bgdrect)

        if rocket.height < 600:
            launchpad_rect = launchpad_image.get_rect().move(
                -rocket.horizondisplacement, rocket.height
            )
            launchshelf_rect = launchshelf_image.get_rect().move(
                300 - rocket.horizondisplacement, 270 + rocket.height
            )
            ground_rect = launchpad_image.get_rect().move(0, 90 + rocket.height)
            screen.blit(ground_image, ground_rect)
            screen.blit(launchpad_image, launchpad_rect)
            screen.blit(launchshelf_image, launchshelf_rect)

        # draw clouds
        if rocket.height > GRAPHICS_CLOUD_DRAW_ALT and rocket.height < 16000:
            for cl in particlesys.clouds:
                if cl.y > -200 and cl.y < 600:
                    cloudrect = cloudimage.get_rect().move(cl.x, cl.y)
                    screen.blit(cloudimage, cloudrect)
                    # print("cloud "+str(cl.y)+" drawn")

        rocket_image = pygame.transform.rotate(
            rocket_image_s, -rocket.direction * 180 / 3.14
        )
        rocket_rect_n = rocket_image.get_rect(center=rocket_rect.center)
        screen.blit(rocket_image, rocket_rect_n)

        vy_str = ""
        a_str = ""
        vx_str = ""
        if rocket.vy >= 0:
            vy_str = format(abs(rocket.vy), ".2f") + " ↑"
        elif rocket.vy < 0:
            vy_str = "-" + format(abs(rocket.vx), ".2f") + " ↓"
        if rocket.ay >= 0:
            a_str = (
                format(
                    math.sqrt(rocket.ax * rocket.ax + rocket.ay * rocket.ay) / 9.8,
                    ".2f",
                )
                + " ↑"
            )
        elif rocket.ay < 0:
            a_str = (
                "-"
                + format(
                    math.sqrt(rocket.ax * rocket.ax + rocket.ay * rocket.ay) / 9.8,
                    ".2f",
                )
                + " ↓"
            )
        if rocket.vx >= 0:
            vx_str = format(abs(rocket.vx), ".2f")
        elif rocket.vx < 0:
            vx_str = "-" + format(abs(rocket.vx), ".2f")
        statusStr = (
            "Vy:"
            + vy_str
            + " m/s"
            + "   "
            + "Vx:"
            + vx_str
            + " m/s"
            + "   "
            + "加速度:"
            + a_str
            + " G"
            + "   "
            + "高度:"
            + format(rocket.height, ".2f")
            + " m"
            + "   "
            + "燃油:"
            + format(rocket.fuel, ".1f")
            + "/"
            + format(rocket.fuel_backup, ".1f")
            + "   "
            + "帧率:"
            + format(fpsRate, ".1f")
            + "   "
        )
        showTextLeftUp(statusStr)
        showTextLeftUp(
            "节流阀:"
            + str(rocket.engine_throttle)
            + "%  引擎:"
            + str(rocket.engine_on)
            + "  时间加速:"
            + str(int(sim_timebase / 0.01))
            + "x",
            1,
        )
        showTextLeftUp(
            "火箭参数  质量:"
            + format(rocket.mass, ".1f")
            + " kg  deltaV(v):"
            + format(
                rocket.si_vacuum
                * 9.8
                * math.log(
                    rocket.mass / (rocket.mass - (rocket.fuel * rocket.fuel_perweight)),
                    2.78,
                ),
                ".1f",
            )
            + " m/s",
            2,
        )

        if rocket.height < 68000:
            showTextLeftUp(
                "大气压:"
                + format(pressure / 1000, ".2f")
                + " kPa   空气阻力:"
                + format(rocket.air_dragforce / 1000, ".2f")
                + "kN",
                3,
            )
        else:
            showTextLeftUp("你已逃逸大气层", 3)
        showTextLeftUp(debugInfo, 4)
        # particle system
        """if particlesys!=None:
            particlesys.resume()
        elif particlesys!=None:
            particlesys.pause()"""

        if particlesys != None:
            for p in particlesys.particles:
                prect = pimage.get_rect().move(p.x - 3.5, p.y - 15)
                screen.blit(pimage, prect)
        """particledrawer=ParticleDrawer()
        particledrawer.start()
        particledrawer.join()"""
    else:
        screen.fill((25, 25, 112))
        pygame.draw.aaline(screen, (255, 255, 255), (10, 8), (10 + zoom * 600000, 8))
        pygame.draw.aaline(screen, (255, 255, 255), (10, 8), (10, 5))
        pygame.draw.aaline(
            screen, (255, 255, 255), (10 + zoom * 600000, 8), (10 + zoom * 600000, 5)
        )
        # rlp=244/267 #50/41
        rlp = 50 / 41
        planet_image = pygame.transform.scale(
            planet_image_s, (2 * int(zoom * 600000 * rlp), 2 * int(zoom * 600000 * rlp))
        )
        planet_rect = planet_image.get_rect().move(
            400 - int(zoom * 600000 * rlp), 300 - int(zoom * 600000 * rlp)
        )
        screen.blit(planet_image, planet_rect)
        # 400,219
        # r_image_p=zoom*600000 #radius per px
        locx = int(400 + zoom * rocket.px)
        locy = int(301 - zoom * rocket.py)
        pygame.draw.circle(screen, (200, 200, 200), (locx, locy), 5)
        if rocket.orbit_track.__len__() > 1 and oct != None:
            if oct.flTyp == True:
                for i in range(1, rocket.orbit_track.__len__()):
                    _fx = int(400 + zoom * rocket.orbit_track[i - 1][0])
                    _fy = int(301 - zoom * rocket.orbit_track[i - 1][1])

                    _bx = int(400 + zoom * rocket.orbit_track[i][0])
                    _by = int(301 - zoom * rocket.orbit_track[i][1])
                    # print("x1="+str(rocket.orbit_track[i-1][0])+"y1="+str(rocket.orbit_track[i-1][1])
                    #      + "x2="+str(rocket.orbit_track[i][0])+"y2="+str(rocket.orbit_track[i][1]))
                    pygame.draw.aaline(screen, (152, 245, 255), (_fx, _fy), (_bx, _by))
                    i = i + rocket.orbit_track.__len__() / 10000

        showTextLeftUp(format(zoom * 600000, ".1f") + "px per 600km")
        showTextLeftUp(
            "节流阀:"
            + str(rocket.engine_throttle)
            + "%  引擎:"
            + str(rocket.engine_on)
            + "  时间加速倍率:"
            + str(int(sim_timebase / 0.01))
            + "x",
            1,
        )
        showTextLeftUp(
            "deltaV(v):"
            + format(
                rocket.si_vacuum
                * 9.8
                * math.log(
                    rocket.mass / (rocket.mass - (rocket.fuel * rocket.fuel_perweight)),
                    2.78,
                ),
                ".1f",
            )
            + " m/s",
            2,
        )

        if rocket.height < 68000:
            showTextLeftUp(
                "大气压:"
                + format(pressure / 1000, ".2f")
                + " kPa   空气阻力:"
                + format(rocket.air_dragforce / 1000, ".2f")
                + "kN",
                3,
            )
        else:
            showTextLeftUp("你已逃逸大气层", 3)
        showTextLeftUp(debugInfo, 4)
        showRocketInfor(locx, locy)
        showPtyInfor(rocket.apPoint, 0)
        showPtyInfor(rocket.pePoint, 1)

    if showOrbitDirection == True:
        fontobj = pygame.font.Font(r"resources/NotoSansHans-Regular.ttf", 11)
        textSurfaceObj = fontobj.render("轨道顺向", True, (255, 255, 255))
        textSurfaceRect = textSurfaceObj.get_rect().move(10, 465)
        screen.blit(textSurfaceObj, textSurfaceRect)
        xpp = int(400 + 100 * rocket.tanangle_cos)
        ypp = int(300 - 100 * rocket.tanangle_sin)
        # xoff = int(xpp - 15*math.sin(rocket.tanangle - 1/4 * 3.14159))
        # yoff = int(ypp - 15*math.cos(rocket.tanangle - 1/4 * 3.14159))
        # pygame.draw.aaline(screen, (240, 240, 240), (400, 300), (xpp, ypp))
        # pygame.draw.aaline(screen, (240, 240, 240),
        #                   (xpp, ypp), (xoff, yoff))
        if rocket.tanangle_sin > 0:
            arrowimg = pygame.transform.rotate(
                arrowimg_s, (math.acos(rocket.tanangle_cos)) * 180 / 3.14
            )
        else:
            arrowimg = pygame.transform.rotate(
                arrowimg_s, (-math.acos(rocket.tanangle_cos)) * 180 / 3.14
            )
        arect = arrowimg.get_rect()
        arrowimg_rect = arrowimg.get_rect(center=arect.center).move(10, 480)
        screen.blit(arrowimg, arrowimg_rect)

    # Sound
    if rocket.height == 0:
        if pygame.mixer.music.get_busy() == False:
            pygame.mixer.music.play(1, 0)
            print("music1")
    else:
        if rocket.pePoint != None:
            if rocket.pePoint.height > 68000:
                if pygame.mixer.music.get_busy() == False:
                    pygame.mixer.music.pause()
                    pygame.mixer.music.load(
                        r"resources/sounds/Kevin MacLeod - Endless Space.mp3"
                    )
                    pygame.mixer.music.play(1, 0)
                    print("music2")
        else:
            pygame.mixer.music.pause()
        if rocket.engine_throttle > 0 and rocket.engine_on > 0:
            sound_engWorking.set_volume(0.2 * rocket.engine_throttle / 100)
            sound_engWorking.play()
        else:
            sound_engWorking.stop()

    # tracks
    """trackrecord_cnt = trackrecord_cnt + 1
    if trackrecord_cnt > TRACK_RECORD:
        rocket.orbit_track.append((rocket.px, rocket.GetAlt()))
        trackrecord_cnt = 0"""

    if tutorialMode:
        GetTips(rocket)

    pygame.display.flip()
    fps_end = time.time()
    fpsRate = 1 / (fps_end - fps_start)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # 如果单击关闭窗口，则退出
            print("Be about to exit")
            os._exit(0)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_v:
                forceKeyboardCtl = True

            if disableKey == False or forceKeyboardCtl == True:
                if event.key == pygame.K_SPACE:
                    if rocket.engine_on == 0:
                        rocket.engine_on = 1
                        sound_engStart.play()
                    else:
                        rocket.engine_on = 0
                        sound_engStop.play()
                elif event.key == pygame.K_z:
                    rocket.engine_throttle = 100
                elif event.key == pygame.K_x:
                    rocket.engine_throttle = 0
                elif event.key == pygame.K_LSHIFT:
                    if rocket.engine_throttle < 100:
                        if rocket.engine_throttle + 5 > 100:
                            rocket.engine_throttle = 100
                        else:
                            rocket.engine_throttle = rocket.engine_throttle + 5
                elif event.key == pygame.K_LCTRL:
                    if rocket.engine_throttle > 0:
                        if rocket.engine_throttle - 5 < 0:
                            rocket.engine_throttle = 0
                        else:
                            rocket.engine_throttle = rocket.engine_throttle - 5
                elif event.key == pygame.K_m:
                    if orbit_Mode == False:
                        orbit_Mode = True
                    else:
                        orbit_Mode = False
                elif event.key == pygame.K_f:
                    if INFINITE_FUEL == 0:
                        INFINITE_FUEL = 1
                        debugInfo = "无限燃油开启"
                    else:
                        INFINITE_FUEL = 0
                        debugInfo = "无限燃油禁用"
                elif event.key == pygame.K_o:
                    # time speed on
                    if sim_timebase < 0.30:
                        if (
                            rocket.engine_on == 1
                            and rocket.engine_throttle > 0
                            and rocket.fuel > 0
                        ):
                            return
                        sim_timebase = sim_timebase + 0.05
                elif event.key == pygame.K_p:
                    # time speed down
                    sim_timebase = 0.01
                elif event.key == pygame.K_u:
                    rocket.py = 680000
                    rocket.vx = 2400
                """elif event.key == pygame.K_i:
                    if showOrbitDirection == True:
                        showOrbitDirection = False
                    else:
                        showOrbitDirection = True"""
            if event.key == pygame.K_h:
                if zoom * 600000 < 350:
                    zoom = (zoom * 600000 + 10) / 600000
            if event.key == pygame.K_n:
                if zoom * 600000 > 20:
                    zoom = (zoom * 600000 - 10) / 600000
        # continuous pressure detect
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_LEFT]:
            if rocket.py != 0:
                rocket.direction = rocket.direction - 3.14 / 36
                rocket_image = pygame.transform.rotate(
                    rocket_image, -rocket.direction * 180 / 3.14
                )
        elif key_pressed[pygame.K_RIGHT]:
            if rocket.py != 0:
                rocket.direction = rocket.direction + 3.14 / 36
                rocket_image = pygame.transform.rotate(
                    rocket_image, -rocket.direction * 180 / 3.14
                )


# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    GameStart()
    while True:
        GameLoop()
    # 退出pygame
    pygame.quit()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
