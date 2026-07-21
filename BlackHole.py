from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from direct.task import Task
import math
import random
class BlackHoleApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.disableMouse()

        # Background
        self.setBackgroundColor(0, 0, 0)

        # =========================
        # CAMERA SETTINGS
        # =========================

        self.camera_distance = 45
        self.camera_angle_x = 0
        self.camera_angle_y = 15

        self.mouse_sensitivity = 0.2

        self.last_mouse_x = 0
        self.last_mouse_y = 0
        self.mouse_held = False

        self.accept("mouse1", self.start_mouse)
        self.accept("mouse1-up", self.stop_mouse)

        self.accept("wheel_up", self.zoom_in)
        self.accept("wheel_down", self.zoom_out)

        # =========================
        # LIGHTING
        # =========================

        ambient = AmbientLight("ambient")
        ambient.setColor((0.2, 0.2, 0.25, 1))
        ambient_np = render.attachNewNode(ambient)
        render.setLight(ambient_np)

        point = PointLight("point")
        point.setColor((2, 1.5, 0.8, 1))
        point_np = render.attachNewNode(point)
        point_np.setPos(0, 0, 0)
        render.setLight(point_np)

        # =========================
        # BLACK HOLE CORE
        # =========================

        self.blackhole = loader.loadModel("models/smiley")
        self.blackhole.reparentTo(render)
        self.blackhole.setScale(4)
        self.blackhole.setColor(0, 0, 0, 1)

        # =========================
        # GLOWING EVENT HORIZON
        # =========================

        self.glow = loader.loadModel("models/smiley")
        self.glow.reparentTo(render)
        self.glow.setScale(5.5)

        self.glow.setTransparency(TransparencyAttrib.MAlpha)
        self.glow.setColor(1, 0.5, 0.1, 0.15)

        # =========================
        # ACCRETION DISK PARTICLES
        # =========================

        self.particles = []

        for i in range(500):

            particle = loader.loadModel("models/smiley")
            particle.reparentTo(render)

            radius = random.uniform(6, 14)
            angle = random.uniform(0, 2 * math.pi)
            height = random.uniform(-0.5, 0.5)

            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            z = height

            particle.setPos(x, y, z)

            particle.setScale(random.uniform(0.05, 0.18))

            r = random.uniform(0.8, 1.0)
            g = random.uniform(0.3, 0.7)
            b = random.uniform(0.0, 0.2)

            particle.setColor(r, g, b, 1)

            speed = random.uniform(0.4, 1.6)

            self.particles.append({
                "node": particle,
                "radius": radius,
                "angle": angle,
                "height": height,
                "speed": speed
            })

        # =========================
        # STARS
        # =========================

        self.create_stars()

        # =========================
        # UPDATE LOOP
        # =========================

        self.taskMgr.add(self.update_scene, "updateScene")

    # ====================================
    # STAR FIELD
    # ====================================

    def create_stars(self):

        for _ in range(400):

            star = loader.loadModel("models/smiley")
            star.reparentTo(render)

            x = random.uniform(-150, 150)
            y = random.uniform(-150, 150)
            z = random.uniform(-150, 150)

            star.setPos(x, y, z)

            star.setScale(random.uniform(0.02, 0.07))

            brightness = random.uniform(0.7, 1.0)

            star.setColor(
                brightness,
                brightness,
                brightness,
                1
            )

    # ====================================
    # MOUSE CAMERA
    # ====================================

    def start_mouse(self):

        if self.mouseWatcherNode.hasMouse():

            mpos = self.mouseWatcherNode.getMouse()

            self.last_mouse_x = mpos.getX()
            self.last_mouse_y = mpos.getY()

            self.mouse_held = True

    def stop_mouse(self):

        self.mouse_held = False

    # ====================================
    # ZOOM
    # ====================================

    def zoom_in(self):

        self.camera_distance -= 2

        if self.camera_distance < 10:
            self.camera_distance = 10

    def zoom_out(self):

        self.camera_distance += 2

        if self.camera_distance > 100:
            self.camera_distance = 100

    # ====================================
    # MAIN UPDATE LOOP
    # ====================================

    def update_scene(self, task):

        dt = globalClock.getDt()

        # =========================
        # CAMERA ROTATION
        # =========================

        if self.mouse_held and self.mouseWatcherNode.hasMouse():

            mpos = self.mouseWatcherNode.getMouse()

            dx = mpos.getX() - self.last_mouse_x
            dy = mpos.getY() - self.last_mouse_y

            self.camera_angle_x -= dx * 100 * self.mouse_sensitivity
            self.camera_angle_y += dy * 100 * self.mouse_sensitivity

            self.camera_angle_y = max(
                -85,
                min(85, self.camera_angle_y)
            )

            self.last_mouse_x = mpos.getX()
            self.last_mouse_y = mpos.getY()

        # =========================
        # SPHERICAL CAMERA
        # =========================

        rad_x = math.radians(self.camera_angle_x)
        rad_y = math.radians(self.camera_angle_y)

        cam_x = (
            self.camera_distance
            * math.cos(rad_y)
            * math.sin(rad_x)
        )

        cam_y = (
            -self.camera_distance
            * math.cos(rad_y)
            * math.cos(rad_x)
        )

        cam_z = (
            self.camera_distance
            * math.sin(rad_y)
        )

        self.camera.setPos(cam_x, cam_y, cam_z)

        self.camera.lookAt(0, 0, 0)

        # =========================
        # ROTATE GLOW
        # =========================

        self.glow.setH(
            self.glow.getH() + 10 * dt
        )

        # =========================
        # PARTICLE MOTION
        # =========================

        for p in self.particles:

            p["angle"] += p["speed"] * dt

            radius = p["radius"]
            angle = p["angle"]

            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            z = p["height"]

            p["node"].setPos(x, y, z)

            # Spiral inward
            p["radius"] -= 0.003

            # Reset
            if p["radius"] < 5:

                p["radius"] = random.uniform(10, 14)

                p["angle"] = random.uniform(
                    0,
                    2 * math.pi
                )

        return Task.cont

# ====================================
# RUN APP
# ====================================

app = BlackHoleApp()
app.run()
