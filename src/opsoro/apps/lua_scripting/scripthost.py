from __future__ import division

import sys
import time
import traceback

import lupa

from opsoro.animate import Animate, AnimatePeriodic
from opsoro.expression import Expression
from opsoro.hardware import Hardware
from opsoro.robot import Robot
from opsoro.sound import Sound
from opsoro.stoppable_thread import StoppableThread


def callback(fn):
    """
    Helper function to support callbacks in classes. Returns the first parameter
    if it is callable, returns a dummy function otherwise.

    Usage:
    callback(self.on_my_callback)()
    """

    def do_nothing(*args, **kwargs):
        pass

    if hasattr(fn, "__call__"):
        return fn
    else:
        return do_nothing


class ScriptHost(object):
    def __init__(self):
        self._script = ""
        self.is_running = False

        self.ui = ScriptUI()

        # Rising/falling edge dict
        self._rising_dict = {}
        self._falling_dict = {}

        self.runtime = None
        self.runtime_thread = None

        # Callbacks
        self.on_print = None
        self.on_error = None
        self.on_start = None
        self.on_stop = None

    def __del__(self):
        if self.is_running:
            self.stop_script()

    def setup_runtime(self):
        """
        Creates a new lua runtime and initializes all globals. Used by
        start_script(), should not be called directly.
        """
        # Create new lua instance
        self.runtime = lupa.LuaRuntime(unpack_returned_tuples=True)

        # Reset keys and button states
        self.ui._keys = {}
        self.ui._buttons = {}

        # Reset rising/falling edge dict
        self._rising_dict = {}
        self._falling_dict = {}

        # Set up API
        g = self.runtime.globals()

        g["Sound"] = Sound
        g["Expression"] = Expression
        g["Robot"] = Robot
        g["Hardware"] = LuaHardware(self.runtime)
        g["Animate"] = LuaAnimate
        g["AnimatePeriodic"] = LuaAnimatePeriodic

        g["UI"] = self.ui

        g["print"] = callback(self.on_print)
        g["sleep"] = self._sleep
        g["rising_edge"] = self._rising_edge
        g["falling_edge"] = self._falling_edge
        g["seconds"] = time.time

        # Basic Arduino functions
        g["delay"] = lambda t: self._sleep(t / 1000)
        g["min"] = min
        g["max"] = max
        g["abs"] = abs
        g["constrain"] = lambda x, a, b: max(a, min(x, b))
        g["map"] = lambda x, in_min, in_max, out_min, out_max: (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
        g["millis"] = lambda: time.time() * 1000.0

    def start_script(self, script):
        """
        Start a new script. This method will create a new runtime, pass the
        script to the runtime, and start a thread to continuously call the
        script's loop function. Can only be used if no other script is running.
        """
        # Check if running
        if self.is_running:
            raise RuntimeError("A script is already running!")

        self._script = script

        callback(self.on_start)()
        self.is_running = True

        # Initialize a new runtime
        self.setup_runtime()

        self.runtime_thread = StoppableThread(target=self._run)
        # self.runtime_thread.start();

    def stop_script(self):
        """
        Attempts to stop the current script. Returns immediately if no script is
        running. If a script is running, this method will send a stop signal to
        to the script thread, and then block until the thread is stopped. Note
        that the thread's stopped condition is only checked during sleep() and
        at the end of loop() calls, this function will not stop infinite loops.
        """
        if self.is_running and self.runtime_thread is not None:
            self.runtime_thread.stop()
            self.runtime_thread.join()

    def generate_lua_error(self, message):
        """
        If a script is running, this method will generate an error inside the
        script. Useful to signal script errors (e.g. bad parameter) to the user.
        """
        if self.is_running and self.runtime is not None:
            g = self.runtime.globals()
            g["error"](message)

    def _report_error(self, e):
        """
        Helper function that prefixes the type of error to the exception, and
        then sends the error message to the application through the on_error
        callback.
        """
        if type(e) == lupa.LuaSyntaxError:
            callback(self.on_error)("Syntax error: %s" % str(e))
        elif type(e) == lupa.LuaError:
            callback(self.on_error)("Lua error: %s" % str(e))
        else:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            tb_str = "".join(traceback.format_tb(exc_traceback)).replace(
                "\n", "<br>")
            callback(self.on_error)("Python error: %s<br>%s" %
                                    (str(e), tb_str))

    def _sleep(self, time):
        """
        Lua API
        Sleep function that pauses the thread for a number of seconds. This
        sleep function will return immediately if the thread's stop flag is set.
        This means that loop function should come to an end instantaneously,
        after which the thread is ended.
        """
        if self.runtime_thread is not None:
            self.runtime_thread.sleep(time)

    def _rising_edge(self, identifier, status):
        """
        Lua API
        Helper function to detect a rising edge of a signal (e.g. button, key,
        capacitive touch pad, etc). Identifier is an arbitrary string that is
        used to distinguish between different signals. Internally, it's used as
        a key for the dictionary that keeps track of different signals.

        Usage:
        if rising_edge("mybutton", UI:is_key_pressed("up")) then
                -- Do something
        end
        """
        last_status = False
        if identifier in self._rising_dict:
            last_status = self._rising_dict[identifier]

        self._rising_dict[identifier] = status
        return status and not last_status

    def _falling_edge(self, identifier, status):
        """
        Lua API
        Helper function to detect a falling edge of a signal (e.g. button, key,
        capacitive touch pad, etc). Identifier is an arbitrary string that is
        used to distinguish between different signals. Internally, it's used as
        a key for the dictionary that keeps track of different signals.

        Usage:
        if falling_edge("mybutton", UI:is_key_pressed("up")) then
                -- Do something
        end
        """
        last_status = False
        if identifier in self._falling_dict:
            last_status = self._falling_dict[identifier]

        self._falling_dict[identifier] = status
        return last_status and not status

    def _remove_lua_overlays(self):
        # for dofname, dof in Expression.dofs.iteritems():
        #     for overlay in dof.overlays:
        #         if lupa.lua_type(overlay) is not None:
        #             # It's a Lua value, remove it!
        #             dof.overlays.remove(overlay)
        pass

    def _run(self):
        """
        Called by the worker thread when the script is run. First attempts to
        call the script's setup function, then continuously calls the loop
        function. When the thread's stop flag is set, the loop breaks and the
        thread attempts to run the quit function. At any time, if the runtime
        encounters an error, the script is stopped, and the on_error and on_stop
        callbacks are triggered.
        """

        time.sleep(0.05)  # delay

        g = self.runtime.globals()

        # Evaluate code and run setup
        try:
            self.runtime.execute(self._script)
            if g["setup"] is not None:
                g["setup"]()
        except Exception as e:
            self.runtime_thread.stop()
            self._report_error(e)

        if g["loop"] is not None:
            # Continuously run loop, until thread is stopped
            while not self.runtime_thread.stopped():
                try:
                    g["loop"]()
                except Exception as e:
                    self._report_error(e)
                    self.runtime_thread.stop()
                # Delay not really necessary, but can be used to limit CPU time.
                # Without delay, this loop consumes about 70% CPU time on a RPi1.
                # else:
                # 	# 10ms breathing room between loops
                time.sleep(0.01)

        # Run quit
        if g["quit"] is not None:
            try:
                g["quit"]()
            except Exception as e:
                self._report_error(e)

        callback(self.on_stop)()
        self._remove_lua_overlays()
        self.is_running = False


class ScriptUI(object):
    def __init__(self):
        # Events
        self.on_init = None
        self.on_add_button = None
        self.on_add_key = None

        # Status dicts
        self._keys = {}
        self._buttons = {}

    def init(self):
        """
        Lua API
        Requests the application to initialize the UI through the on_init
        callback. The request is typically passed on to the client via websocket.
        """
        callback(self.on_init)()

    def add_button(self, name, caption, icon, toggle=False):
        """
        Lua API
        Adds a button to the client's UI. Request to client is sent through the
        on_add_button callback.
        """
        callback(self.on_add_button)(name, caption, icon, toggle)

    def add_key(self, key):
        """
        Lua API
        Adds a key listener to the client's UI.
        Request to client is sent through the on_add_key callback.
        """
        callback(self.on_add_key)(key)

    def set_key_status(self, key, status):
        """
        Used by the app to set the status of a key. Typically, key events are
        captured on the clientside using javascript and are transfered to the
        application using a websocket. The application is responsible for
        updating the key status in the ScriptUI class.
        """
        self._keys[key] = status

    def set_button_status(self, button, status):
        """
        Used by the app to set the status of a button. Typically, button events
        are captured on the clientside using javascript and are transfered to
        the application using a websocket. The application is responsible for
        updating the button status in the ScriptUI class.
        """
        self._buttons[button] = status

    def is_button_pressed(self, name):
        """
        Lua API
        Returns True if a button is pressed, False otherwise.
        """
        if name in self._buttons:
            return self._buttons[name]
        return False

    def is_key_pressed(self, key):
        """
        Lua API
        Returns True if a key is pressed, False otherwise.
        """
        if key in self._keys:
            return self._keys[key]
        return False


class LuaHardware(object):
    def __init__(self, runtime):
        # Workaround to convert lua tables to lists
        self.runtime = runtime

    def __getattr__(self, k):
        attr = getattr(Hardware, k)

        # Workaround to ignore the first parameter. When called from
        # lua, first param will be LuaHardware instance, which we do not
        # need.
        def ignore_one(ign, *args, **kwargs):
            return attr(*args, **kwargs)

        if hasattr(attr, "__call__"):
            return ignore_one
        else:
            return attr

    def cap_get_filtered_data(self):
        return self.runtime.table_from(Hardware.Capacitive.get_filtered_data())

    def cap_get_baseline_data(self):
        return self.runtime.table_from(Hardware.Capacitive.get_baseline_data())

    def ana_read_all_channels(self):
        return self.runtime.table_from(Hardware.Capacitive.get_baseline_data())

    def spi_command(self, cmd, params=None, returned=0, delay=0):
        if params is not None:
            params = list(params.values())
        return self.runtime.table_from(
            Hardware.SPI.command(cmd, params, returned, delay))

    def servo_set_all(self, pos_list):
        pos_list = list(pos_list.values())
        Hardware.Servo.set_all(post_list)


class LuaAnimate(object):
    def __init__(self, times, values):
        # Workaround to convert lua tables to lists
        self._a = Animate(list(times.values()), list(values.values()))

    @classmethod
    def new(cls, times, values):
        return LuaAnimate(times, values)

    def __call__(self):
        return self._a()

    def has_ended(self):
        return self._a.has_ended()


class LuaAnimatePeriodic(object):
    def __init__(self, times, values):
        # Workaround to convert lua tables to lists
        self._a = AnimatePeriodic(list(times.values()), list(values.values()))

    @classmethod
    def new(cls, times, values):
        return LuaAnimatePeriodic(times, values)

    def __call__(self):
        return self._a()

# NEW NEW NEW and untested
# install pyserial
# TODO: add to scripthost
# import serial
# import serial.tools.list_ports
#
# class ScriptSerial(object):
# 	def __init__(self):
# 		self._ser = None
# 		self.on_print = None
# 		setattr(self, "print", ScriptSerial.print_) # TODO: check
#
# 	def begin(self, baudrate=9600, port=None):
# 		ports = serial.tools.list_ports.comports()
#
# 		if len(ports) == 0:
# 			raise RuntimeError("No serial ports available!")
# 		elif len(ports) != 1:
# 			callback(self.on_print)("The following serial ports are available:")
# 			for p in ports:
# 				print callback(self.on_print)(p[0])
#
# 		self._ser = serial.Serial(baudrate=baudrate, port=port)
#
# 	def end(self):
# 		if self._ser:
# 			self._ser.close()
#
# 	def available(self):
# 		if self._ser:
# 			return self._ser.inWaiting()
# 		else:
# 			return 0
#
# 	def read(self, bytes):
# 		if not self._ser:
# 			return -1
# 		if self._ser.inWaiting() == 0:
# 			return -1
# 		return self._ser.read()
#
# 	def print_(self, s):
# 		if not self._ser:
# 			return 0
# 		return self._ser.write(bytes(s))
#
# 	def println(self, s):
# 		self.print_(s + "\n")
