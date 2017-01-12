from opsoro.console_msg import *
# Modules
from opsoro.Entity.Module import *
from opsoro.Entity.Module.Eye import Eye
from opsoro.Entity.Module.Eyebrow import Eyebrow
from opsoro.Entity.Module.Mouth import Mouth
from opsoro.Entity.Module.Wheel import Wheel
from opsoro.Entity.Group import Group
from opsoro.Entity.Group.WheelGroup import WheelGroup

#dof's
from opsoro.dof import DOF
from opsoro.dof.servo import Servo
from opsoro.dof.engine import Engine

MODULES = {'eye': Eye, 'eyebrow': Eyebrow, 'mouth': Mouth, 'wheel': Wheel}
GROUPS = {'group':Group,'wheelgroup': WheelGroup}


class Factory(object):
    """
        factory class for loading the entities from a config file
    """
    def __init__(self, data):
        """
            :param dict data:       data: the data from the config file
        """
        self.data = data
        self.groups = {}
        self.modules = {}
        self.entities = {} #these are the entities that will be returned to robot

    def _load_groups(self):
        if self.data and ("groups" in self.data):
            for g in self.data["groups"]:
                if ("type" in g) and (g["type"] in GROUPS):
                    group = GROUPS[g["type"]]()
                    if "tags" in g:
                        group.tags = g["tags"]
                    if "name" in g:
                        group.name = g["name"]
                    if "group" in g:
                        self.groups[g["group"]].add_module(group)
                    else:
                        self.entities[group.name] = group
                    self.groups[group.name] = group

    def _load_modules(self):
        if "modules" in self.data:
            for m in self.data["modules"]:
                if ("type" in m) and (m["type"] in MODULES):
                    module = MODULES[m["type"]]()
                    if "tags" in m:
                        module.tags = m["tags"]
                    if "name" in m:
                        module.name = m["name"]
                    if "dofs" in m:
                        module.dofs = self._load_dofs(m["dofs"])
                    if "group" in m:
                        self.groups[m["group"]].add_module(module)
                    else:
                        self.entities[module.name] = module
                    self.modules[module.name] = module

    def _load_dofs(self,dof_data):
        result = {}
        for d in dof_data:
            dof_name = ""
            if "name" in d:
                dof_name = d["name"]

            #MAPPING
            neutral = 0.0
            poly = None
            if 'mapping' in d:
                mapping_data = d['mapping']
                if 'neutral' in mapping_data:
                    neutral = mapping_data['neutral']
                if 'poly' in mapping_data:
                    poly = mapping_data['poly']

            dof = None
            #SERVO
            if 'servo' in d:
                dof = Servo(dof_name, neutral, poly)
                servo_data = d['servo']
                if 'pin' in servo_data and 'min' in servo_data and 'mid' in servo_data and 'max' in servo_data:
                    dof.config(servo_data['pin'],
                               servo_data['min'],
                               servo_data['mid'],
                               servo_data['max'], )
            #ENGINE
            elif 'engine' in d:
                    dof = Engine(dof_name, neutral, poly)
                    engine_data = d['engine']
                    if ('pin_a' in engine_data) and ('pin_b' in engine_data) and ('min_speed' in engine_data) and ('max_speed' in engine_data) and ('reverse' in engine_data):
                        dof.config(servo_data['pin_a'],
                                   servo_data['pin_b'],
                                   servo_data['min_speed'],
                                   servo_data['max_speed'],
                                   servo_data['reverse'], )
            #CONTINU SERVO (not in use)
            elif 'continu_servo' in d:
                        dof = ContinuServo(dof_name, neutral, poly)
                        servo_data = d['continu_servo']
                        if 'pin' in servo_data and 'forward_pers' in servo_data and 'mid' in servo_data and 'backward_pers' in servo_data:
                            dof.config(servo_data['pin'],
                                       servo_data['forward_pers'],
                                       servo_data['mid'],
                                       servo_data['backward_pers'],
                                       servo_data['reverse'])
            #NO SERVO OR ENGINE
            else:
                dof = DOF(dof_name, neutral, poly)


            result[dof_name] = dof
        return result

    def load_entities(self):
        """
            load the entities

            :return:            dictionary of entities (tree structure)
            :rtype:             dict
        """
        self._load_groups()
        self._load_modules()
        self._print_loading_result()
        return self.entities



    def _print_loading_result(self):
        """
        print in console the ammount of entities created from each type
        """
        result = {}
        for t in MODULES:
            instances = sum([isinstance(m,MODULES[t]) for m in self.modules.values()])
            if instances > 0:
                result[t] = instances
        for t in GROUPS:
            instances = sum([isinstance(g,GROUPS[t]) for g in self.groups.values()])
            if instances > 0:
                result[t] = instances
        print_info("Entities: " + str(result))
