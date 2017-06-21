import sys
import time
import json
import threading
import traceback
import collections
from abc import abstractmethod

from . import finiteloop

try:
    import Queue as queue
except ImportError:
    import queue

from . import exception
from . import _find_first_key, flavor_router

#
# class StoppableDaemon(threading.Thread):
#     def __init__(self, *args, **kwargs):
#         super(StoppableDaemon, self).__init__(*args, **kwargs)
#         self.daemon = True
#         self._shutdown = threading.Event()
#
#     def stop(self):
#         self._shutdown.set()


# class RunForeverAsThread(object):
#
#     def run_as_thread(self, *args, **kwargs):
#         t = threading.Thread(target=self.run_forever, args=args, kwargs=kwargs)
#         t.daemon = True
#         t.start()
#
#     @abstractmethod
#     def run_forever(self):
#         pass


class CollectLoop(finiteloop.StoppableDaemon):
    def __init__(self, handle, *args, **kwargs):
        super(CollectLoop, self).__init__(*args, **kwargs)
        self._handle = handle
        self._inqueue = queue.Queue()

    @property
    def input_queue(self):
        return self._inqueue

    def run(self):
        while not self._shutdown.isSet():
            try:
                msg = self._inqueue.get(block=True, timeout=5)
                self._handle(msg)
            except queue.Empty:
                pass
            except:
                traceback.print_exc()


class GetUpdatesLoop(finiteloop.StoppableDaemon):
    def __init__(self, bot, on_update, relax=0.1, timeout=20, allowed_updates=None, *args, **kwargs):
        super(GetUpdatesLoop, self).__init__(*args, **kwargs)
        self._bot = bot
        self._update_handler = on_update
        self._relax = relax
        self._timeout = timeout
        self._allowed_upd = allowed_updates

    def run(self):
        offset = None  # running offset
        # allowed_upd = allowed_updates
        while not self._shutdown.isSet():
            try:
                result = self._bot.getUpdates(offset=offset,
                                              timeout=self._timeout,
                                              allowed_updates=self._allowed_upd)

                # Once passed, this parameter is no longer needed.
                allowed_upd = None

                if len(result) > 0:
                    # No sort. Trust server to give messages in correct order.
                    for update in result:
                        self._update_handler(update)
                        offset = update['update_id'] + 1

            except exception.BadHTTPResponse as e:
                traceback.print_exc()

                # Servers probably down. Wait longer.
                if e.status == 502:
                    time.sleep(30)
            except:
                traceback.print_exc()
            finally:
                time.sleep(self._relax)


def _dictify3(data):
    if type(data) is bytes:
        return json.loads(data.decode('utf-8'))
    elif type(data) is str:
        return json.loads(data)
    elif type(data) is dict:
        return data
    else:
        raise ValueError()


def _dictify27(data):
    if type(data) in [str, unicode]:
        return json.loads(data)
    elif type(data) is dict:
        return data
    else:
        raise ValueError()

_dictify = _dictify3 if sys.version_info >= (3,) else _dictify27


def _extract_message(update):
    key = _find_first_key(update, ['message',
                                   'edited_message',
                                   'channel_post',
                                   'edited_channel_post',
                                   'callback_query',
                                   'inline_query',
                                   'chosen_inline_result',
                                   'shipping_query',
                                   'pre_checkout_query'])
    return key, update[key]


def _infer_handler_function(bot, h):
    if h is None:
        return bot.handle
    elif isinstance(h, dict):
        return flavor_router(h)
    else:
        return h


class MessageLoop(object):
    def __init__(self, bot, handle=None):
        self._bot = bot
        self._handle = _infer_handler_function(bot, handle)
        self._collectloop = None
        self._updatesloop = None

    def start_threads(self, *args, **kwargs):
        """
        :type relax: float
        :param relax: seconds between each :meth:`.getUpdates`

        :type timeout: int
        :param timeout:
            ``timeout`` parameter supplied to :meth:`.getUpdates`, controlling
            how long to poll.

        :type allowed_updates: array of string
        :param allowed_updates:
            ``allowed_updates`` parameter supplied to :meth:`.getUpdates`,
            controlling which types of updates to receive.

        Calling this method will block forever. Use :meth:`.run_as_thread` to
        run it non-blockingly.
        """
        self._collectloop = CollectLoop(self._handle)
        self._updatesloop = GetUpdatesLoop(self._bot,
                                           lambda update:
                                           self._collectloop.input_queue.put(_extract_message(update)[1]),
                                           *args, **kwargs)
        # feed events to collect loop
        self._bot.scheduler.on_event(self._collectloop.input_queue.put)
        self._bot.scheduler.run_as_thread()

        # self._updatesloop.run_as_thread(*args, **kwargs)
        self._updatesloop.start()
        self._collectloop.start()  # blocking --> not anymore!

    def stop_threads(self):
        try:
            self._collectloop.stop()
            self._updatesloop.stop()
            self._bot.scheduler.stop()
            # self._collectloop = None
            # self._updatesloop = None
        except BaseException as e:
            print("Can't stop threads that weren't started [%s]" % str(e))
            raise


class Webhook(finiteloop.StoppableDaemon):
    def __init__(self, bot, handle=None, *args, **kwargs):
        super(Webhook, self).__init__(*args, **kwargs)
        self._bot = bot
        self._collectloop = CollectLoop(_infer_handler_function(bot, handle))

    def run_forever(self):
        # feed events to collect loop
        self._bot.scheduler.on_event(self._collectloop.input_queue.put)
        self._bot.scheduler.run_as_thread()

        self._collectloop.start()

    def feed(self, data):
        update = _dictify(data)
        self._collectloop.input_queue.put(_extract_message(update)[1])

    def stop(self):
        self._collectloop.stop()
        super(Webhook, self).stop()


class Orderer(finiteloop.StoppableDaemon):
    def __init__(self, on_ordered_update, maxhold=3, *args, **kwargs):
        super(Orderer, self).__init__(*args, **kwargs)
        self._on_ordered_update = on_ordered_update
        self._inqueue = queue.Queue()
        self._maxhold = maxhold

    @property
    def input_queue(self):
        return self._inqueue

    def run(self):
        def handle(update):
            self._on_ordered_update(update)
            return update['update_id']

        # Here is the re-ordering mechanism, ensuring in-order delivery of updates.
        max_id = None                 # max update_id passed to callback
        buffer = collections.deque()  # keep those updates which skip some update_id
        qwait = 5                  # how long to wait for updates,
                                      # because buffer's content has to be returned in time.

        while not self._shutdown.isSet():
            try:
                update = self._inqueue.get(block=True, timeout=qwait)

                if max_id is None:
                    # First message received, handle regardless.
                    max_id = handle(update)

                elif update['update_id'] == max_id + 1:
                    # No update_id skipped, handle naturally.
                    max_id = handle(update)

                    # clear contagious updates in buffer
                    if len(buffer) > 0:
                        buffer.popleft()  # first element belongs to update just received, useless now.
                        while 1:
                            try:
                                if type(buffer[0]) is dict:
                                    max_id = handle(buffer.popleft())  # updates that arrived earlier, handle them.
                                else:
                                    break  # gap, no more contagious updates
                            except IndexError:
                                break  # buffer empty

                elif update['update_id'] > max_id + 1:
                    # Update arrives pre-maturely, insert to buffer.
                    nbuf = len(buffer)
                    if update['update_id'] <= max_id + nbuf:
                        # buffer long enough, put update at position
                        buffer[update['update_id'] - max_id - 1] = update
                    else:
                        # buffer too short, lengthen it
                        expire = time.time() + self._maxhold
                        for a in range(nbuf, update['update_id']-max_id-1):
                            buffer.append(expire)  # put expiry time in gaps
                        buffer.append(update)

                else:
                    pass  # discard

            except queue.Empty:
                # debug message
                # print('Timeout')

                # some buffer contents have to be handled
                # flush buffer until a non-expired time is encountered
                while not self._shutdown.isSet():       # TODO: maybe replace with self._shutdown.isSet() ??
                    try:
                        if type(buffer[0]) is dict:
                            max_id = handle(buffer.popleft())
                        else:
                            expire = buffer[0]
                            if expire <= time.time():
                                max_id += 1
                                buffer.popleft()
                            else:
                                break  # non-expired
                    except IndexError:
                        break  # buffer empty
            except:
                traceback.print_exc()
            finally:
                qwait = 5
                # try:
                #     # don't wait longer than next expiry time
                #     qwait = buffer[0] - time.time()
                #     if qwait < 0:
                #         qwait = 0
                # except IndexError:
                    # buffer empty, can wait forever


                # debug message
                # print ('Buffer:', str(buffer), ', To Wait:', qwait, ', Max ID:', max_id)


class OrderedWebhook(finiteloop.StoppableDaemon):
    def __init__(self, bot, handle=None, maxhold=3, *args, **kwargs):
        super(OrderedWebhook, self).__init__(*args, **kwargs)
        self._bot = bot
        self._collectloop = CollectLoop(_infer_handler_function(bot, handle))
        self._orderer = Orderer(lambda update:
                                self._collectloop.input_queue.put(_extract_message(update)[1]),
                                maxhold=maxhold)

    def run(self):  # args moved to c'tor!
        """
        :type maxhold: float
        :param maxhold:
            The maximum number of seconds an update is held waiting for a
            not-yet-arrived smaller ``update_id``. When this number of seconds
            is up, the update is delivered to the message-handling function
            even if some smaller ``update_id``\s have not yet arrived. If those
            smaller ``update_id``\s arrive at some later time, they are discarded.

        Calling this method will block forever. Use :meth:`.run_as_thread` to
        run it non-blockingly.
        """
        # feed events to collect loop
        self._bot.scheduler.on_event(self._collectloop.input_queue.put)
        self._bot.scheduler.run_as_thread()

        self._orderer.start()
        self._collectloop.start()

        self._shutdown.wait()

        self._collectloop.stop()
        self._orderer.stop()
        self._bot.scheduler.stop()

    def feed(self, data):
        """
        :param data:
            One of these:

            - ``str``, ``unicode`` (Python 2.7), or ``bytes`` (Python 3, decoded using UTF-8)
              representing a JSON-serialized `Update <https://core.telegram.org/bots/api#update>`_ object.
            - a ``dict`` representing an Update object.
        """
        update = _dictify(data)
        self._orderer.input_queue.put(update)
