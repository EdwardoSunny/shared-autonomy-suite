import hid
import threading
import numpy as np
from .utils import convert, rotation_matrix
from .spacemouse_config import SpaceMouseConfig


class SpaceMouse:
    def __init__(self, config: SpaceMouseConfig):
        print("Opening SpaceMouse device")
        self.pos_sensitivity = config.pos_sensitivity
        self.rot_sensitivity = config.rot_sensitivity
        self.verbose = config.verbose
        self.vendor_id = config.vendor_id
        self.product_id = config.product_id
        self.device = hid.device()

        self.device.open(self.vendor_id, self.product_id)

        print("Manufacturer: %s" % self.device.get_manufacturer_string())
        print("Product: %s" % self.device.get_product_string())

        self.x, self.y, self.z = 0, 0, 0
        self.roll, self.pitch, self.yaw = 0, 0, 0

        self._display_controls()

        self.grasp = 0.0

        self._control = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self._reset_state = 0
        self.rotation = np.array([[-1.0, 0.0, 0.0],
                                  [0.0, 1.0, 0.0],
                                  [0.0, 0.0, -1.0]])
        self._enabled = True

        self.lock = threading.Lock()

        self._running = True
        self.thread = threading.Thread(target=self.run)
        self.thread.daemon = True
        self.thread.start()

    @staticmethod
    def _display_controls():
        def print_command(char, info):
            char += " " * (30 - len(char))
            print("{}\t{}".format(char, info))

        print("")
        print_command("Control", "Command")
        print_command("Right button", "reset simulation")
        print_command("Left button", "toggle gripper open/close")
        print_command("Move mouse laterally", "move arm horizontally in x-y plane")
        print_command("Move mouse vertically", "move arm vertically")
        print_command("Twist mouse about an axis", "rotate arm about a corresponding axis")
        print("")

    def _reset_internal_state(self):
        self.rotation = np.array([[-1.0, 0.0, 0.0],
                                  [0.0, 1.0, 0.0],
                                  [0.0, 0.0, -1.0]])
        self.x, self.y, self.z = 0, 0, 0
        self.roll, self.pitch, self.yaw = 0, 0, 0
        self._control = np.zeros(6)
        self.grasp = 0.0

    def start_control(self):
        self._reset_internal_state()
        self._reset_state = 0
        self._enabled = True

    def get_controller_state(self):
        with self.lock:
            control = np.array(self._control.copy())
            grasp = self.grasp

        dpos = control[:3] * 0.05 * self.pos_sensitivity
        roll, pitch, yaw = control[3:] * 0.05 * self.rot_sensitivity

        drot1 = rotation_matrix(pitch, [1.0, 0, 0])
        drot2 = rotation_matrix(roll, [0, 1.0, 0])
        drot3 = rotation_matrix(yaw, [0, 0, 1.0])

        self.rotation = self.rotation.dot(drot1.dot(drot2.dot(drot3)))

        return dict(
            dpos=dpos,
            rotation=self.rotation,
            raw_drotation=np.array([roll, pitch, yaw]),
            grasp=grasp,
            reset=self._reset_state,
        )

    def run(self):
        while self._running:
            d = self.device.read(13)
            if d is not None and self._enabled:
                if self.verbose:
                    print(f"Raw HID data: {d}")

                if self.product_id == 50741:
                    if d[0] == 1:
                        self.y = convert(d[1], d[2])
                        self.x = convert(d[3], d[4])
                        self.z = convert(d[5], d[6]) * -1.0

                    elif d[0] == 2:
                        self.roll = -convert(d[5], d[6])
                        self.pitch = convert(d[1], d[2])
                        self.yaw = convert(d[3], d[4])

                        with self.lock:
                            self._control = [
                                self.x,
                                self.y,
                                self.z,
                                self.yaw,
                                self.pitch,
                                self.roll,
                            ]
                        if self.verbose:
                            print(f"Control values: {self._control}")
                else:
                    if d[0] == 1:
                        self.y = convert(d[1], d[2])
                        self.x = convert(d[3], d[4])
                        self.z = convert(d[5], d[6]) * -1.0

                        self.roll = convert(d[7], d[8])
                        self.pitch = convert(d[9], d[10])
                        self.yaw = convert(d[11], d[12])

                        with self.lock:
                            self._control = [
                                self.x,
                                self.y,
                                self.z,
                                self.roll,
                                self.pitch,
                                self.yaw,
                            ]
                        if self.verbose:
                            print(f"Control values: {self._control}")

                if d[0] == 3:
                    if d[1] == 1:
                        with self.lock:
                            if self.grasp == 0.0:
                                self.grasp = 1.0
                            else:
                                self.grasp = 0.0
                        if self.verbose:
                            state = "closed" if self.grasp == 1.0 else "opened"
                            print(f"Gripper toggled to: {state}")
                    elif d[1] == 2:
                        self._reset_state = 1
                        self._enabled = False
                        self._reset_internal_state()

    @property
    def control(self):
        return np.array(self._control)

    @property
    def control_gripper(self):
        if self.grasp == 1.0:
            return "close"
        else:
            return "open"

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._running = False
        self.thread.join(timeout=0.5)
        try:
            self.device.close()
        except Exception as e:
            print("Error closing HID device:", e)
