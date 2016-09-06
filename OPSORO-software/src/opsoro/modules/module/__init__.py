from opsoro.hardware import Hardware
from opsoro.hardware.servo import Servo
from opsoro.console_msg import *

import numpy as np
from scipy import interpolate

import math
import cmath

constrain = lambda n, minn, maxn: max(min(maxn, n), minn)


class Module(object):
    def __init__(self, data=None):
        self.name = ""
        self.position = {}
        self.size = {}
        self.dofs = []
        self.servos = []

        if data is not None:
            self.load_module(data)

    def apply_poly(self, phi, r):
        for dof in self.dofs:
            dof.calc(phi, r)

    def update(self):
        index = 0
        for servo in self.servos:
            if servo.pin < 0 or servo.pin > 15:
                continue  # Skip invalid pins

            servo.dof_to_us(self.dofs[index].value)
            servo.update()

            index += 1

    def load_module(self, data):
        if 'name' in data:
            self.name = data['name']
        else:
            self.name = ""

        self.position = {}
        self.size = {}

        if 'canvas' in data:
            canvas_data = data['canvas']
            if 'pos' in canvas_data:
                self.position = canvas_data['pos']
            if 'size' in canvas_data:
                self.size = canvas_data['size']

        if 'dofs' in data:
            self.dofs = []
            self.servos = []
            for dof_data in data['dofs']:
                if 'name' not in dof_data:
                    dof_data['name'] = ""
                dof_name = self.name + "_" + dof_data['name']

                if 'servo' in dof_data:
                    servo_data = dof_data['servo']
                    if 'pin' in servo_data and 'min' in servo_data and 'mid' in servo_data and 'max' in servo_data:
                        self.servos.append(
                            Servo(servo_data['pin'], servo_data[
                                'min'], servo_data['mid'], servo_data['max'],
                                  dof_name))

                neutral = 0.0
                poly = None
                if 'mapping' in dof_data:
                    mapping_data = dof_data['mapping']
                    if 'neutral' in mapping_data:
                        neutral = mapping_data['neutral']
                    if 'poly' in mapping_data:
                        poly = mapping_data['poly']

                self.dofs.append(DOF(dof_name, neutral, poly))

    def __str__(self):
        return str(self.name)


class DOF(object):
    def __init__(self, name, neutral=0.0, poly=None):
        self.name = name
        self.value = neutral

        # Dict to store any extra data from YAML files
        self.data = {}

        # List of overlay functions
        # def my_overlay(dofpos, dof):
        #   new_dof_pos = dofpos
        #   return my_new_pos
        self.overlays = []

        self._phis = None
        self._dofs = None
        self._neutral = None
        self._interp_poly = None

        self.set_control_polygon(neutral, poly)

    def __repr__(self):
        return "DOF(name=%s, neutral=%.2f, poly={...})" \
         % (self.name, self._neutral)

    def set_control_polygon(self, neutral=0.0, poly=None):
        def deg_to_rad_minpi_pluspi(deg):
            # Convert to [0, 360[
            deg = deg % 360.0
            # Convert to [-180, 180[
            if deg >= 180.0:
                deg = deg - 360.0
            # Convert to radians
            rad = deg * math.pi / 180.0
            return float(rad)

        self._neutral = constrain(neutral, -1.0, 1.0)

        if poly is None or len(poly) == 0:
            self._phis = np.array([])
            self._dofs = np.array([])
            self._interp_poly = lambda x: self._neutral
        else:
            # The control polygon has one or more DOF values
            # keys = np.linspace(0, 360, 21)[0:20]
            # phis = map(deg_to_rad_minpi_pluspi, keys)
            # phis = np.linspace(0, math.pi, 10)[0:10] + np.linspace(0, -math.pi,
            #                                                        10)[0:10]
            phis = np.linspace(-math.pi, math.pi, 20)[0:20]
            dofs = map(lambda x: float(x), poly)

            # print(phis)
            # print(dofs)
            # #
            # # First point in the control polygon.
            # # To be appended at the end to simulate looparound behavior
            # a_phi = phis[0]
            # a_dof = dofs[0]
            #
            # # Last point in the control polygon.
            # # To be prepended at the beginning to simulate looparound behavior
            # b_phi = phis[19]
            # b_dof = dofs[19]
            #
            # phis = [b_phi - 2 * math.pi] + phis + [a_phi + 2 * math.pi]
            # dofs = [b_dof] + dofs + [a_dof]
            # #
            # print(phis)
            # print(dofs)

            # Sort lists
            indexes = range(len(phis))
            indexes.sort(key=phis.__getitem__)
            sorted_phis = map(phis.__getitem__, indexes)
            sorted_dofs = map(dofs.__getitem__, indexes)

            # Convert to numpy arrays
            self._phis = np.array(sorted_phis)
            self._dofs = np.array(sorted_dofs)

            # print(self._phis)
            # print(self._dofs)

            # Create interpolation instance
            self._interp_poly = interpolate.interp1d(
                sorted_phis, sorted_dofs, kind="linear")

    def calc(self, phi, r):
        # Calculate DOF position at max intensity
        dof_at_max_r = self._interp_poly(phi)

        # Interpolate between neutral DOF pos and max intensity DOF pos
        self.value = self._neutral + (r * (dof_at_max_r - self._neutral))

        # Execute overlays
        for overlay_fn in self.overlays:
            try:
                self.value = overlay_fn(self.value, self)
            except TypeError:
                # Not a callable object, or function does not take 2 args
                pass

        return self.value

    def add_overlay(self, fn):
        self.overlays.append(fn)

    def remove_overlay(self, fn):
        self.overlays.remove(fn)

    def clear_overlays(self):
        self.overlays = []
