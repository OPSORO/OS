from opsoro.console_msg import *
# Modules
from opsoro.module import *
from opsoro.module.eye import Eye
from opsoro.module.eyebrow import Eyebrow
from opsoro.module.mouth import Mouth
from opsoro.module.wheel import Wheel
from opsoro.module.group import Group
from opsoro.module.group.wheelGroup import WheelGroup

#dof's
from opsoro.dof import DOF
from opsoro.dof.servo import Servo
from opsoro.dof.engine import Engine

MODULES = {'eye': Eye, 'eyebrow': Eyebrow, 'mouth': Mouth, 'wheel': Wheel, 'wheelgroup': WheelGroup}

class ModuleFactory(object):
    def __init__(self, data):
        """
            data: the data from the config file (tag: modules)
        """
        self.data = data
        self.modules = []



    def load_modules(self):
        """
            load the modules
        """
        if (self.modules is None) or (self.modules == []):
            self.modules = []
            for mdata in self.data:
                m = self._load_module(mdata)
                if m is not None:
                    self.modules = self.modules + [m]
            #load the modules into the groupmodules
            for mod in self.modules:
                if isinstance(mod,Group):
                    for m in self.modules:
                        if m.name in mod.module_names:
                            mod.modules += [m]
        print str(self.modules)
        return self.modules

    def _load_module(self,mdata):
        result = None
        if mdata['type'] in MODULES:

            result = MODULES[mdata['type']](mdata)

            result.name = (mdata['name'] if 'name' in mdata else "")
            result.tags = (mdata['tags'] if 'tags' in mdata else [])

            result.position = {}
            result.size = {}
            if 'canvas' in mdata:
                print_todo("moduleFactory: canvas")

            if 'dofs' in mdata:
                self.dofs = {}
                # self.servos = []
                for dof_data in mdata['dofs']:
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
                    # #CONTINU SERVO
                    # elif 'continu_servo' in dof_data:
                    #         dof = ContinuServo(dof_name, neutral, poly)
                    #         servo_data = dof_data['continu_servo']
                    #         if 'pin' in servo_data and 'forward_pers' in servo_data and 'mid' in servo_data and 'backward_pers' in servo_data:
                    #             dof.config(servo_data['pin'],
                    #                        servo_data['forward_pers'],
                    #                        servo_data['mid'],
                    #                        servo_data['backward_pers'],
                    #                        servo_data['reverse'])
                    #NO SERVO OR ENGINE
                    else:
                        dof = DOF(dof_name, neutral, poly)

                    result.dofs[dof.name] = dof

            if 'modls' in mdata:
                result.module_names = mdata['modls']
        return result

    def count_Types(self):
        """
        count the number of instances of each module class

            return: dictionary with key:module type, value: number of instances
        """
        modules = self.load_modules()
        result = {}
        for t in MODULES:
            instances = sum([isinstance(m,MODULES[t]) for m in modules])
            if instances > 0:
                result[t] = instances
        return result
