# from opsoro.hardware import Hardware
# from opsoro.dof.servo import Servo
from opsoro.dof import DOF
from opsoro.dof.servo import Servo
from opsoro.dof.engine import Engine
from opsoro.dof.continu_servo import ContinuServo
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
        self.dofs = {}
        # self.servos = []

        if data is not None:
            self.load_module(data)

    def apply_poly(self, r, phi, anim_time=-1):
        for name, dof in self.dofs.iteritems():
            dof.calc(r, phi, anim_time)

    def update(self):
        # index = 0
        updated = False
        for name, dof in self.dofs.iteritems():
            # dof.update(self.dofs[index].value)
            if dof.update():
                updated = True
        return updated

    def set_dof_value(self, dof_name, dof_value, anim_time=-1):
        if dof_name is None:
            for name, dof in self.dofs.iteritems():
                dof.set_value(dof_value, anim_time)
        else:
            self.dofs[dof_name].set_value(dof_value, anim_time)

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
            self.dofs = {}
            # self.servos = []
            for dof_data in data['dofs']:
                #DOF NAME
                if 'name' not in dof_data:
                    dof_data['name'] = ""
                dof_name = dof_data['name']

                #MAPPING
                neutral = 0.0
                poly = None
                if 'mapping' in dof_data:
                    mapping_data = dof_data['mapping']
                    if 'neutral' in mapping_data:
                        neutral = mapping_data['neutral']
                    if 'poly' in mapping_data:
                        poly = mapping_data['poly']

                dof = None
                #SERVO
                if 'servo' in dof_data:
                    dof = Servo(dof_name, neutral, poly)
                    servo_data = dof_data['servo']
                    if 'pin' in servo_data and 'min' in servo_data and 'mid' in servo_data and 'max' in servo_data:
                        dof.config(servo_data['pin'],
                                   servo_data['min'],
                                   servo_data['mid'],
                                   servo_data['max'], )
                #ENGINE
                elif 'engine' in dof_data:
                    dof = Engine(dof_name, neutral, poly)
                    engine_data = dof_data['engine']
                    if ('pin_a' in engine_data) and ('pin_b' in engine_data) and ('min_speed' in engine_data) and ('max_speed' in engine_data) and ('reverse' in engine_data):
                        dof.config(servo_data['pin_a'],
                                   servo_data['pin_b'],
                                   servo_data['min_speed'],
                                   servo_data['max_speed'],
                                   servo_data['reverse'], )
                #CONTINU SERVO
                elif 'continu_servo' in dof_data:
                        dof = ContinuServo(dof_name, neutral, poly)
                        servo_data = dof_data['continu_servo']
                        if 'pin' in servo_data and 'min' in servo_data and 'mid' in servo_data and 'max' in servo_data:
                            dof.config(servo_data['pin'],
                                       servo_data['min'],
                                       servo_data['mid'],
                                       servo_data['max'],
                                       servo_data['reverse'])
                #NO SERVO OR ENGINE
                else:
                    dof = DOF(dof_name, neutral, poly)

                self.dofs[dof.name] = dof

    def __str__(self):
        return str(self.name)
