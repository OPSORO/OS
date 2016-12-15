# import os
# from functools import partial
#
# import yaml
# try:
#     from yaml import CLoader as Loader, CDumper as Dumper
# except ImportError:
#     from yaml import Loader, Dumper
#
# get_path = partial(os.path.join, os.path.abspath(os.path.dirname(__file__)))
#
# from opsoro.hardware import Hardware
# from opsoro.console_msg import *
# # Modules
# from opsoro.modules.eye import Eye
# from opsoro.modules.mouth import Mouth
# from opsoro.modules.eyebrow import Eyebrow
# MODULES = {'eye': Eye, 'eyebrow': Eyebrow, 'mouth': Mouth}
#
# import json
#
#
# class _Modules(object):
#     def __init__(self):
#         self.modules = []
#         self.data = {}
#         self.current_file = None
#
#     def apply_poly(self, r, phi):
#         for module in self.modules:
#             module.apply_poly(r, phi)
#
#     def update(self):
#         for module in self.modules:
#             module.update()
#
#     def setPosition(self, module_name, dof_name):
#         for module in self.modules:
#             module.update()
#
#     def load_modules(self, file):
#         # Load modules from file
#         if file is None:
#             return False
#         try:
#             with open(get_path("../config/" + file)) as f:
#                 self.data = f.read()
#
#             if self.data is None or len(self.data) == 0:
#                 print_warning("Config contains no data: " + file)
#                 return False
#             self.data = json.loads(self.data)
#
#             self.current_file = file
#         except IOError:
#             self.data = {}
#             print_warning("Could not open " + file)
#             return False
#
#         # Create all module-objects from data
#         self.modules = []
#         modules_count = {}
#         for module_data in self.data['modules']:
#             if module_data['module'] in MODULES:
#
#                 # Create module object
#                 module = MODULES[module_data['module']](module_data)
#
#                 # Count different modules
#                 if module_data['module'] not in modules_count:
#                     modules_count[module_data['module']] = 0
#                 modules_count[module_data['module']] += 1
#                 self.modules.append(module)
#
#         # print module feedback
#         print_info("Modules loaded [" + file + "]: " + str(modules_count))
#
#         return True
#
#     def save_modules(self, file=None):
#         # Save modules to yaml file
#         if file is None:
#             file = self.current_file
#         if file is None:
#             return False
#
#         try:
#             with open(get_path("../config/" + file), "w") as f:
#                 f.write(
#                     yaml.dump(
#                         self.data, default_flow_style=False, Dumper=Dumper))
#             self.current_file = file
#             print_info("Modules saved: " + file)
#             return True
#         except IOError:
#             print_warning("Could not save " + file)
#         return False
#
#
# Modules = _Modules()
