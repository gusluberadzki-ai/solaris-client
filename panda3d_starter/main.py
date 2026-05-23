from pathlib import Path
from math import sin

from direct.gui.DirectGui import DirectFrame, DirectLabel
from direct.actor.Actor import Actor
from direct.gui.OnscreenText import OnscreenText
from direct.showbase.ShowBase import ShowBase
from direct.showbase.ShowBaseGlobal import globalClock
from panda3d.core import (
    CardMaker,
    AmbientLight,
    DirectionalLight,
    LineSegs,
    TransparencyAttrib,
    TextNode,
    Vec3,
    WindowProperties,
    loadPrcFile,
)

loadPrcFile(str(Path(__file__).with_name("settings.prc")))
WEAPON_MODEL_PATH = Path(__file__).with_name("fps_animated_carbine_static.glb")


class StarterGame(ShowBase):
    def __init__(self):
        super().__init__()

        self.disableMouse()
        self.setBackgroundColor(0.88, 0.9, 0.94, 1)

        self.move_speed = 10
        self.sprint_speed = 16
        self.mouse_sensitivity = 0.1
        self.player_height = 1.8
        self.pitch = 0
        self.selected_slot = 0
        self.weapon_recoil = 0.0
        self.weapon_flash = 0.0
        self.weapon_time = 0.0
        self.reload_timer = 0.0
        self.reload_duration = 1.0
        self.reloading = False
        self.reload_offset = 0.0
        self.reload_turn = 0.0
        self.keys = {
            "forward": False,
            "backward": False,
            "left": False,
            "right": False,
            "sprint": False,
        }

        self.accept("escape", self.userExit)
        self.accept("w", self.set_key, ["forward", True])
        self.accept("w-up", self.set_key, ["forward", False])
        self.accept("s", self.set_key, ["backward", True])
        self.accept("s-up", self.set_key, ["backward", False])
        self.accept("a", self.set_key, ["left", True])
        self.accept("a-up", self.set_key, ["left", False])
        self.accept("d", self.set_key, ["right", True])
        self.accept("d-up", self.set_key, ["right", False])
        self.accept("shift", self.set_key, ["sprint", True])
        self.accept("shift-up", self.set_key, ["sprint", False])
        self.accept("mouse1", self.fire_weapon)
        self.accept("r", self.reload_weapon)
        self.accept("1", self.select_slot, [0])
        self.accept("2", self.select_slot, [1])
        self.accept("3", self.select_slot, [2])

        self.player = self.render.attachNewNode("player")
        self.player.setPos(0, -18, self.player_height)
        self.camera.reparentTo(self.player)
        self.camera.setPos(0, 0, 0)

        self.setup_mouse()
        self.setup_lights()
        self.build_world()
        self.build_viewmodel()
        self.add_ui()
        self.select_slot(0)

        self.taskMgr.add(self.update, "update")

    def setup_mouse(self):
        props = WindowProperties()
        props.setCursorHidden(True)
        self.win.requestProperties(props)
        self.make_borderless_fullscreen()
        self.center_mouse()

    def make_borderless_fullscreen(self):
        display_width = self.pipe.getDisplayWidth()
        display_height = self.pipe.getDisplayHeight()

        if display_width <= 0 or display_height <= 0:
            return

        props = WindowProperties()
        props.setUndecorated(True)
        props.setOrigin(0, 0)
        props.setSize(display_width, display_height)
        self.win.requestProperties(props)

    def center_mouse(self):
        if self.win is None:
            return
        x = self.win.getXSize() // 2
        y = self.win.getYSize() // 2
        self.win.movePointer(0, x, y)

    def setup_lights(self):
        ambient = AmbientLight("ambient")
        ambient.setColor((0.55, 0.58, 0.63, 1))
        ambient_np = self.render.attachNewNode(ambient)
        self.render.setLight(ambient_np)

        sun = DirectionalLight("sun")
        sun.setColor((1.0, 0.96, 0.9, 1))
        sun_np = self.render.attachNewNode(sun)
        sun_np.setHpr(-35, -55, 0)
        self.render.setLight(sun_np)

    def build_world(self):
        self.tile_size = 6
        self.terrain_radius = 14
        self.terrain_tiles = {}
        self.terrain_grid = None
        self.last_player_tile = None
        self.ground_cell = CardMaker("ground_cell")
        self.ground_cell.setFrame(0, self.tile_size, 0, self.tile_size)
        self.update_terrain(force=True)

    def update_terrain(self, force=False):
        player_x = self.player.getX()
        player_y = self.player.getY()
        center_x = int(player_x // self.tile_size)
        center_y = int(player_y // self.tile_size)
        if self.last_player_tile == (center_x, center_y) and not force:
            return
        self.last_player_tile = (center_x, center_y)
        wanted_tiles = set()

        for dx in range(-self.terrain_radius, self.terrain_radius + 1):
            for dy in range(-self.terrain_radius, self.terrain_radius + 1):
                wanted_tiles.add((center_x + dx, center_y + dy))

        for coord in list(self.terrain_tiles.keys()):
            if coord not in wanted_tiles:
                self.terrain_tiles[coord].removeNode()
                del self.terrain_tiles[coord]

        for coord in wanted_tiles:
            if coord in self.terrain_tiles:
                continue
            tx, ty = coord
            tile = self.render.attachNewNode(self.ground_cell.generate())
            tile.setP(-90)
            tile.setPos(tx * self.tile_size, ty * self.tile_size + self.tile_size, 0)
            if (tx + ty) % 2 == 0:
                tile.setColor(0.36, 0.40, 0.34, 1)
            else:
                tile.setColor(0.30, 0.34, 0.29, 1)
            self.terrain_tiles[coord] = tile

        if self.terrain_grid is not None:
            self.terrain_grid.removeNode()
            self.terrain_grid = None

        grid = LineSegs("terrain_grid")
        grid.setThickness(1.0)
        grid.setColor(0.10, 0.13, 0.08, 1)
        min_x = (center_x - self.terrain_radius) * self.tile_size
        max_x = (center_x + self.terrain_radius + 1) * self.tile_size
        min_y = (center_y - self.terrain_radius) * self.tile_size + self.tile_size
        max_y = (center_y + self.terrain_radius + 1) * self.tile_size + self.tile_size

        for i in range(-self.terrain_radius, self.terrain_radius + 2):
            line_x = (center_x + i) * self.tile_size
            grid.moveTo(line_x, min_y, 0.03)
            grid.drawTo(line_x, max_y, 0.03)

        for i in range(-self.terrain_radius, self.terrain_radius + 2):
            line_y = (center_y + i) * self.tile_size + self.tile_size
            grid.moveTo(min_x, line_y, 0.03)
            grid.drawTo(max_x, line_y, 0.03)

        self.terrain_grid = self.render.attachNewNode(grid.create())

    def make_tiled_ground(self, size, tile_size):
        cell = CardMaker("ground_cell")
        cell.setFrame(0, tile_size, 0, tile_size)

        for x in range(-size, size, tile_size):
            for y in range(-size, size, tile_size):
                tile = self.render.attachNewNode(cell.generate())
                tile.setP(-90)
                tile.setPos(x, y + tile_size, 0)

                if (x // tile_size + y // tile_size) % 2 == 0:
                    tile.setColor(0.975, 0.975, 0.98, 1)
                else:
                    tile.setColor(0.955, 0.96, 0.968, 1)

        grid = LineSegs("ground_grid")
        grid.setThickness(1.0)
        grid.setColor(0.65, 0.68, 0.74, 1)

        for value in range(-size, size + tile_size, tile_size):
            grid.moveTo(value, -size, 0.02)
            grid.drawTo(value, size, 0.02)
            grid.moveTo(-size, value, 0.02)
            grid.drawTo(size, value, 0.02)

        self.render.attachNewNode(grid.create())

    def add_ui(self):
        self.top_text = OnscreenText(
            text="WASD move   Shift sprint   Mouse look   Esc quit",
            pos=(0, 0.84),
            fg=(0.18, 0.2, 0.24, 1),
            bg=(0.95, 0.96, 0.98, 0.8),
            scale=0.042,
            align=TextNode.ACenter,
            mayChange=False,
        )
        self.build_hotbar()

    def build_hotbar(self):
        self.hotbar_slots = []
        slot_names = ["1  Pulse", "2  Empty", "3  Empty"]
        slot_width = 0.18
        start_x = -slot_width

        for index, name in enumerate(slot_names):
            x = start_x + index * slot_width
            frame = DirectFrame(
                parent=self.aspect2d,
                frameColor=(0.82, 0.85, 0.9, 0.75),
                frameSize=(-0.075, 0.075, -0.045, 0.045),
                pos=(x, 0, -0.74),
            )
            label = DirectLabel(
                parent=frame,
                text=name,
                text_scale=0.036,
                text_fg=(0.18, 0.2, 0.24, 1),
                text_align=TextNode.ACenter,
                frameColor=(0, 0, 0, 0),
                pos=(0, 0, -0.012),
            )
            self.hotbar_slots.append((frame, label))

        self.update_hotbar()

    def update_hotbar(self):
        for index, (frame, label) in enumerate(self.hotbar_slots):
            if index == self.selected_slot:
                frame["frameColor"] = (0.99, 0.99, 1.0, 0.95)
                label["text_fg"] = (0.08, 0.1, 0.14, 1)
            else:
                frame["frameColor"] = (0.82, 0.85, 0.9, 0.72)
                label["text_fg"] = (0.26, 0.28, 0.32, 1)

    def build_viewmodel(self):
        self.viewmodel_root = self.camera.attachNewNode("viewmodel_root")
        self.viewmodel_root.setPos(0.38, 0.92, -0.5)
        self.viewmodel_root.setHpr(0, -2, 0)
        self.viewmodel_root.setLightOff(1)
        self.viewmodel_root.setDepthWrite(False)
        self.viewmodel_root.setDepthTest(False)

        self.hand_root = None

        self.gun_root = self.viewmodel_root.attachNewNode("gun_root")
        self.gun_root.setPos(0, 0, 0)
        self.gun_root.setHpr(0, 0, 0)

        self.weapon_actor = None
        self.weapon_model = None
        self.weapon_hands = None
        self.weapon_bolt = None
        self.weapon_trigger = None
        if WEAPON_MODEL_PATH.exists():
            try:
                actor = Actor(str(WEAPON_MODEL_PATH))
                if not actor.isEmpty():
                    self.weapon_actor = actor
                    self.weapon_model = actor
            except Exception:
                self.weapon_actor = None

            if self.weapon_model is None or (hasattr(self.weapon_model, "isEmpty") and self.weapon_model.isEmpty()):
                loaded_weapon = self.loader.loadModel(str(WEAPON_MODEL_PATH))
                if not loaded_weapon.isEmpty():
                    self.weapon_model = self.extract_weapon_part(loaded_weapon, "**/carbine")
                    self.weapon_hands = self.extract_weapon_part(loaded_weapon, "**/Null")
            if self.weapon_model is not None and hasattr(self.weapon_model, "isEmpty") and self.weapon_model.isEmpty():
                self.weapon_model = None
                self.weapon_actor = None
            if self.weapon_model is not None:
                self.weapon_model.reparentTo(self.gun_root)
                self.weapon_model.setScale(0.012)
                self.weapon_model.setHpr(0, 90, 0)
                self.weapon_model.setPos(0.22, 0.38, -0.24)
                self.weapon_model.setLightOff(1)
                self.weapon_model.setDepthWrite(False)
                self.weapon_model.setDepthTest(False)
                self.weapon_model.setTwoSided(True)

                if self.weapon_hands is not None:
                    self.hand_root = self.weapon_hands
                    self.hand_root.reparentTo(self.gun_root)
                    self.hand_root.setScale(0.012)
                    self.hand_root.setHpr(0, 90, 0)
                    self.hand_root.setPos(0.22, 0.38, -0.24)
                    self.hand_root.setLightOff(1)
                    self.hand_root.setDepthWrite(False)
                    self.hand_root.setDepthTest(False)
                    self.hand_root.setTwoSided(True)

                self.weapon_bolt = self.weapon_model.find("**/bolt")
                self.weapon_trigger = self.weapon_model.find("**/trigger")

        if self.weapon_model is None:
            self.hand_root = self.viewmodel_root.attachNewNode("hand_root")
            self.hand_root.setPos(0.12, -0.05, -0.02)
            skin = (0.82, 0.74, 0.68, 1)
            glove = (0.18, 0.19, 0.22, 1)
            self.add_viewmodel_part(self.hand_root, "palm", (0, 0, 0), (0.16, 0.08, 0.2), skin, "cube")
            self.add_viewmodel_part(self.hand_root, "wrist", (-0.05, -0.02, -0.14), (0.11, 0.07, 0.12), glove, "cube")
            self.add_viewmodel_part(self.hand_root, "thumb", (0.1, -0.04, 0.02), (0.04, 0.035, 0.11), skin, "cube")
            self.add_viewmodel_part(self.hand_root, "fingers", (-0.04, 0.02, 0.16), (0.12, 0.045, 0.08), skin, "cube")
            body = (0.9, 0.91, 0.94, 1)
            dark = (0.14, 0.16, 0.2, 1)
            accent = (0.45, 0.55, 0.7, 1)
            self.add_viewmodel_part(self.gun_root, "slide", (0, 0.2, 0.1), (0.11, 0.34, 0.09), body, "cube")
            self.add_viewmodel_part(self.gun_root, "barrel", (0, 0.49, 0.08), (0.05, 0.12, 0.05), dark, "cube")
            self.add_viewmodel_part(self.gun_root, "frame", (0, 0.08, -0.03), (0.1, 0.22, 0.08), dark, "cube")
            self.add_viewmodel_part(self.gun_root, "grip", (0, -0.05, -0.18), (0.07, 0.1, 0.18), body, "cube")
            self.add_viewmodel_part(self.gun_root, "core", (0, 0.03, 0.02), (0.035, 0.1, 0.05), accent, "cube")

        flash = CardMaker("muzzle_flash")
        flash.setFrame(-0.06, 0.06, -0.06, 0.06)
        self.muzzle_flash = self.gun_root.attachNewNode(flash.generate())
        self.muzzle_flash.setPos(0, 0.64, 0.08)
        self.muzzle_flash.setTransparency(TransparencyAttrib.MAlpha)
        self.muzzle_flash.setColor(1.0, 0.9, 0.65, 0)
        self.muzzle_flash.setBillboardPointEye()
        self.muzzle_flash.setDepthWrite(False)
        self.muzzle_flash.setDepthTest(False)

    def extract_weapon_part(self, loaded_weapon, pattern):
        part = loaded_weapon.find(pattern)
        if part.isEmpty():
            return None
        extracted = part.copyTo(self.render)
        extracted.setPos(0, 0, 0)
        extracted.setHpr(0, 0, 0)
        return extracted

    def add_viewmodel_part(self, parent, name, pos, scale, color, shape):
        model_name = "models/misc/rgbCube" if shape == "cube" else "models/misc/sphere"
        part = self.loader.loadModel(model_name)
        part.reparentTo(parent)
        part.setName(name)
        part.setPos(*pos)
        part.setScale(*scale)
        part.setColor(*color)
        part.setTextureOff(1)
        part.setMaterialOff(1)
        part.setLightOff(1)
        part.setDepthWrite(False)
        part.setDepthTest(False)
        return part

    def set_key(self, key, value):
        self.keys[key] = value

    def select_slot(self, index):
        self.selected_slot = index
        if index == 0:
            self.gun_root.show()
            if self.hand_root is not None:
                self.hand_root.show()
        else:
            self.gun_root.hide()
            if self.hand_root is not None:
                self.hand_root.hide()
        self.update_hotbar()

    def fire_weapon(self):
        if self.selected_slot != 0:
            return
        self.weapon_recoil = 1.0
        self.weapon_flash = 1.0
        if self.weapon_actor is not None:
            anim_names = list(self.weapon_actor.getAnimNames())
            if "fire" in anim_names:
                self.weapon_actor.play("fire")
            elif anim_names:
                self.weapon_actor.play(anim_names[0])

    def reload_weapon(self):
        if self.selected_slot != 0 or self.reloading:
            return
        self.reloading = True
        self.reload_timer = 0.0
        if self.weapon_actor is not None:
            anim_names = list(self.weapon_actor.getAnimNames())
            if "reload" in anim_names:
                self.weapon_actor.play("reload")
            elif anim_names:
                self.weapon_actor.play(anim_names[0])

    def update(self, task):
        dt = globalClock.getDt()
        if not self.mouseWatcherNode.hasMouse():
            return task.cont

        if self.win.getProperties().getForeground():
            pointer = self.win.getPointer(0)
            center_x = self.win.getXSize() // 2
            center_y = self.win.getYSize() // 2

            dx = pointer.getX() - center_x
            dy = pointer.getY() - center_y

            self.player.setH(self.player.getH() - dx * self.mouse_sensitivity)
            self.pitch = max(-85, min(85, self.pitch - dy * self.mouse_sensitivity))
            self.camera.setP(self.pitch)
            self.center_mouse()

        move = Vec3(0, 0, 0)
        forward = self.render.getRelativeVector(self.player, Vec3(0, 1, 0))
        right = self.render.getRelativeVector(self.player, Vec3(1, 0, 0))
        forward.setZ(0)
        right.setZ(0)

        if forward.lengthSquared() > 0:
            forward.normalize()
        if right.lengthSquared() > 0:
            right.normalize()

        if self.keys["forward"]:
            move += forward
        if self.keys["backward"]:
            move -= forward
        if self.keys["right"]:
            move += right
        if self.keys["left"]:
            move -= right

        if move.lengthSquared() > 0:
            move.normalize()
            speed = self.sprint_speed if self.keys["sprint"] else self.move_speed
            self.player.setPos(self.player.getPos() + move * speed * dt)

        self.update_terrain()

        self.player.setZ(self.player_height)
        self.update_viewmodel(dt, move.lengthSquared() > 0)
        return task.cont

    def update_viewmodel(self, dt, is_moving):
        self.weapon_time += dt
        self.weapon_recoil = max(0.0, self.weapon_recoil - dt * 6.5)
        self.weapon_flash = max(0.0, self.weapon_flash - dt * 10.0)

        if self.selected_slot != 0:
            return

        bob_speed = 9 if is_moving else 2
        bob_amount = 0.028 if is_moving else 0.01
        bob_x = sin(self.weapon_time * bob_speed) * bob_amount
        bob_z = abs(sin(self.weapon_time * bob_speed * 0.5)) * bob_amount * 1.6
        recoil_push = self.weapon_recoil * 0.12
        recoil_pitch = self.weapon_recoil * 9

        if self.reloading:
            self.reload_timer += dt
            progress = min(1.0, self.reload_timer / self.reload_duration)
            self.reload_offset = sin(progress * 3.14159) * 0.12
            self.reload_turn = sin(progress * 3.14159) * 10.0
            if progress >= 1.0:
                self.reloading = False
                self.reload_offset = 0.0
                self.reload_turn = 0.0
        else:
            self.reload_offset = 0.0
            self.reload_turn = 0.0

        self.viewmodel_root.setPos(0.38 + bob_x, 0.92 - recoil_push, -0.5 - bob_z - self.reload_offset)
        self.viewmodel_root.setHpr(self.reload_turn * 0.1, -2 + recoil_pitch + self.reload_turn * 0.3, bob_x * -12)
        self.gun_root.setHpr(self.reload_turn * 0.6, recoil_pitch * 0.8, self.reload_turn * -0.2)

        if self.hand_root is not None:
            hand_pitch = -10 - recoil_pitch * 0.35
            self.hand_root.setHpr(-8, hand_pitch, 8)

        if self.weapon_bolt is not None and not self.weapon_bolt.isEmpty():
            self.weapon_bolt.setY(10.0093 - self.weapon_recoil * 1.6)
        if self.weapon_trigger is not None and not self.weapon_trigger.isEmpty():
            self.weapon_trigger.setP(-self.weapon_recoil * 18)

        flash_alpha = self.weapon_flash * 0.9
        self.muzzle_flash.setColor(1.0, 0.92, 0.7, flash_alpha)
        self.muzzle_flash.setScale(1 + self.weapon_flash * 0.8)


if __name__ == "__main__":
    game = StarterGame()
    game.run()
