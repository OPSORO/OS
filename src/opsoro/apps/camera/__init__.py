from __future__ import with_statement

import argparse
import datetime
import math
import os
import random
import time
from functools import partial

import cv2
import imutils
from flask import (Blueprint, flash, redirect, render_template, request,
                   send_from_directory, url_for)

from opsoro.console_msg import *
from opsoro.expression import Expression
from opsoro.hardware import Hardware
from opsoro.robot import Robot
from opsoro.sound import Sound
from opsoro.stoppable_thread import StoppableThread


def constrain(n, minn, maxn): return max(min(maxn, n), minn)


get_path = partial(os.path.join, os.path.abspath(os.path.dirname(__file__)))

config = {
    'full_name':            'Camera',
    'author':               'OPSORO',
    'icon':                 'fa-info',
    'color':                'green',
    'difficulty':           1,
    'tags':                 ['camera', 'developer'],
    'allowed_background':   True,
    'multi_user':           True,
    'connection':           0,
    'activation':           1
}
config['formatted_name'] = config['full_name'].lower().replace(' ', '_')

loop_t = None
camera = None
firstFrame = None
fast = None

img_blur = 7
img_threshold = 40
img_dilate = 5
img_min_area = 200
view_width = 200


view_min_x = math.floor(view_width / 4)
view_max_x = view_width - view_min_x
view_range_x = view_max_x - view_min_x
single_view_range = math.floor(view_width / 3)
single_half_view_range = single_view_range / 2
eyes_center_1_x = math.floor(view_width / 2.1)
eyes_center_2_x = math.floor(view_width / 1.9)

view_ranges = [[view_min_x, view_min_x + single_view_range],
               [eyes_center_1_x - single_half_view_range, eyes_center_1_x + single_half_view_range],
               [eyes_center_2_x - single_half_view_range, eyes_center_2_x + single_half_view_range],
               [view_max_x - single_view_range, view_max_x]]


def look_at(x):
    # print_info('detection: %i' % x)
    for value in range(4):
        eye_index = value + 1
        eye_hor_value = constrain(x, view_ranges[value][0], view_ranges[value][1])
        eye_hor_dof_value = (eye_hor_value - (view_ranges[value][0] + single_half_view_range)) / single_half_view_range
        Robot.set_dof(['eye', str(eye_index), 'horizontal'], eye_hor_dof_value, random.random())


def look_random():
    random_face = str(random.randint(1, 4))
    # Robot.set_dof([random_face], -2, -1)
    # Robot.set_dof([], 2, -1)
    # # open eyes
    rnd_time = 0.1 + random.random()
    Robot.set_dof(['eye', random_face, 'lid'], random.random(), rnd_time)
    loop_t.sleep(rnd_time * 2)
    # look left
    rnd_pos = random.random()
    rnd_time = 0.1 + random.random()
    Robot.set_dof(['eye', 'left', random_face, 'horizontal'], random.choice([-1, 1]) * rnd_pos, rnd_time)
    Robot.set_dof(['eye', 'right', random_face, 'horizontal'], random.choice([-1, 1]) * rnd_pos, rnd_time)
    loop_t.sleep(rnd_time * 2)
    # look right
    rnd_pos = random.random()
    rnd_time = 0.1 + random.random()
    Robot.set_dof(['eye', 'left', random_face, 'horizontal'], random.choice([-1, 1]) * rnd_pos, rnd_time)
    Robot.set_dof(['eye', 'right', random_face, 'horizontal'], random.choice([-1, 1]) * rnd_pos, rnd_time)
    # Robot.set_dof(['eye', random_face, 'horizontal'], -1, 0.2)
    loop_t.sleep(rnd_time * 2)
    # look straight
    rnd_time = 0.1 + random.random()
    Robot.set_dof(['eye', random_face, 'horizontal'], 0, rnd_time)
    loop_t.sleep(rnd_time * 2)
    # close eyes
    rnd_time = 0.1 + random.random()
    Robot.set_dof(['eye', random_face, 'lid'], -1, rnd_time)
    loop_t.sleep(rnd_time * 2)


def Loop():
    global camera
    global firstFrame
    global fast

    eye_lids = [random.random(), random.random(), random.random(), random.random()]
    last_active = time.time()
    active_count = 0
    start_time = time.time()
    next_random = time.time() + 5
    prev_random = 5
    inactive = False

    time.sleep(0.05)  # delay
    while not loop_t.stopped():
        if camera is None:
            continue
        (grabbed, frame) = camera.read()

        # if the frame could not be grabbed, then we have reached the end of the video
        if not grabbed:
            continue

        # resize the frame, convert it to grayscale, and blur it
        frame = imutils.resize(frame, width=view_width)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # gray = cv2.GaussianBlur(gray, (img_blur, img_blur), 255)

        # if the first frame is None, initialize it
        if firstFrame is None:
            firstFrame = gray
            continue

        # compute the absolute difference between the current frame and first frame
        frameDelta = cv2.absdiff(firstFrame, gray)
        thresh = cv2.threshold(frameDelta, img_threshold, 255, cv2.THRESH_BINARY)[1]

        # dilate the thresholded image to fill in holes, then find contours on thresholded image
        thresh = cv2.dilate(thresh, None, iterations=img_dilate)
        thresh = cv2.erode(thresh, None, iterations=img_dilate)
        (cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2:]

        largest_area = 0
        largest_c = None
        # loop over the contours
        for c in cnts:
            # if the contour is too small, ignore it
            area = cv2.contourArea(c)
            if area < img_min_area:
                continue
            if area > largest_area:
                largest_area = area
                largest_c = c

        if not inactive:
            for value in range(4):
                Robot.set_dof(['eye', str(value + 1), 'lid'], eye_lids[value], 0.2)

        if largest_c is not None:
            # only on detection update firstframe
            firstFrame = gray

            (x, y, w, h) = cv2.boundingRect(largest_c)
            if w > h:
                # print('out of view')
                continue
            center_x = x + w / 2
            # center_y = y + h / 2
            if center_x < view_min_x or center_x > view_max_x:
                # print('out of view')
                continue

            if inactive:
                print_info('active and snap!')
                cv2.imwrite("snaps/start-snap-" + str(last_active) + ".jpg", frame)
                active_count = 0
                Robot.auto_enable_servos = False
                inactive = False
                for value in range(4):
                    eye_lids.append(random.random())
                    Robot.set_dof(['eye', str(value + 1), 'lid'], eye_lids[value], random.random() * 2)

            last_active = time.time()
            active_count += 1
            # if active_count % 30 == 0:
            #     cv2.imwrite("snaps/snap-" + str(last_active) + ".jpg", frame)

            look_at(center_x)

            if random.randint(0, 10) >= 10:
                wink_face = str(random.randint(0, 4))
                Robot.set_dof(['eye', random.choice(['left', 'right', '']), str(wink_face), 'lid'], -1, 0.2)

        if not inactive:
            if time.time() - last_active > 20:
                print_info('inactive')
                inactive = True
                Robot.auto_enable_servos = True
                prev_random = random.randint(10, 30)
                next_random = time.time() + prev_random
                Robot.set_dof(['eye', 'lid'], -1, 1)

        else:
            if time.time() - next_random > 0:
                prev_random = random.randint(prev_random, prev_random + 30)
                next_random = time.time() + prev_random
                print_info('RANDOM! %i' % next_random)
                look_random()
            loop_t.sleep(1)

        loop_t.sleep(0.01)


def setup_pages(apps):
    app_bp = Blueprint(config['formatted_name'], __name__, template_folder='templates', static_folder='static')
    # Public function declarations
    # app_bp.add_url_rule('/demo',    'demo',     apps.app_api(demo),       methods=['GET', 'POST'])

    @app_bp.route('/')
    @apps.app_view
    def index():
        data = {
            'actions': {},
            'data': [],
        }
        action = request.args.get('action', None)
        if action != None:
            data['actions'][action] = request.args.get('param', None)

        return apps.render_template(config['formatted_name'] + '.html', **data)
    apps.register_app_blueprint(app_bp)


def setup(server):
    pass


def start(server):
    try:
        global loop_t
        global camera
        global fast

        camera = cv2.VideoCapture(0)
        print('camera 0')
        time.sleep(0.25)

        # Initiate FAST object with default values
        # fast = cv2.FastFeatureDetector_create()
        fast = cv2.FastFeatureDetector()
        loop_t = StoppableThread(target=Loop)

    except Exception as e:
        print(e)


def stop(server):
    global loop_t
    global camera
    if loop_t is not None:
        loop_t.stop()
    if camera is not None:
        camera.release()
    pass
