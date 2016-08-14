#!/usr/bin/env python
#
# AutoPilot :: Sourav Badami :: http://www.souravbadami.me
# Script: AutoSleep
# Description: This script automatically detects when theres no one nearby and
#              sends the system to sleep mode.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS-IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
import os
import time
import cv2
import sys
import time
from gi.repository import Notify
import threading
import ctypes

DELTA_COUNT_THRESHOLD = 1000
STILL_TIME = 0

# Set sleep trigger time in seconds (Default: 30 minutes)
STT = 1800

def delta_images(t0, t1, t2):
    d1 = cv2.absdiff(t2, t0)
    return d1
    
def started():
    """
    Get's triggered when the application starts and notifies user.
    """
    global timer_thread
    Notify.init("Started")
    #Shows Notification on the desktop
    Notify.Notification.new("\nAutoPilot"," The system has been taken over by AutoPilot.").show()
    os.system("shutdown now -h")
    
started()
    
def timeout():
    """
    Triggers the notification and system process on timeout.
    """
    global timer_thread
    Notify.init("AutoPilot")
    #Shows Notification on the desktop
    Notify.Notification.new("\nAutoPilot"," System going down to sleep mode.").show()
    #os.system("shutdown now -h")
    
def start_timer():
    """
    Starts the timer when there's no one around.
    """
    global STILL_TIME
    while STILL_TIME != 0:
        STILL_TIME = STILL_TIME + 1
        #print(STILL_TIME-1, "Seconds")
        if STILL_TIME/2 == STT:
            timeout()
        time.sleep(1)

for cn in range(0,3):
    cam = cv2.VideoCapture(cn)
    if cam.isOpened():
        break
if not cam.isOpened():
    sys.stderr.write('ERROR: Did not open a camera.\n')
    sys.exit(1)
    
print ("Running with camera number %d." % cn)
print type(cam)
print str(cam)

cam.set(3,640)
cam.set(4,480)

winName = "AutoPilot"
cv2.namedWindow(winName, cv2.CV_WINDOW_AUTOSIZE)

t_minus = cam.read()[1]
t_now = cam.read()[1]
t_plus = cam.read()[1]
t_now = cv2.resize(t_now, (640, 480))
t_minus = cv2.resize(t_minus, (640, 480))
t_plus = cv2.resize(t_plus, (640, 480))

delta_count_last = 1

while True:
    delta_view = delta_images(t_minus, t_now, t_plus)

    retval, delta_view = cv2.threshold(delta_view, 16, 255, 3)
    cv2.normalize(delta_view, delta_view, 0, 255, cv2.NORM_MINMAX)
    img_count_view = cv2.cvtColor(delta_view, cv2.COLOR_RGB2GRAY)
    delta_count = cv2.countNonZero(img_count_view)
    delta_view = cv2.flip(delta_view, 1)
    cv2.putText(
    delta_view, "UM-PID: %d"%(
    delta_count), (5, 15), cv2.FONT_HERSHEY_PLAIN, 0.8, (255,255,255))
    cv2.putText(
    delta_view, "Pilot Status: Activated", (10, 450), cv2.FONT_HERSHEY_PLAIN, 0.8, (255,255,255))
    # Credits
    cv2.putText(
    delta_view, "Developer: Sourav Badami", (390, 450), cv2.FONT_HERSHEY_PLAIN, 0.8, (255,255,255))
    cv2.putText(
    delta_view, "Blog: http://www.souravbadami.me", (390, 460), cv2.FONT_HERSHEY_PLAIN, 0.8, (255,255,255))    
    cv2.imshow(winName, delta_view)

    if (
    delta_count_last < DELTA_COUNT_THRESHOLD
     and delta_count >= DELTA_COUNT_THRESHOLD):
        STILL_TIME = 0
        sys.stdout.flush()
    elif delta_count_last >= DELTA_COUNT_THRESHOLD and delta_count < DELTA_COUNT_THRESHOLD:
        STILL_TIME = 1
        timer_thread = threading.Thread(target=start_timer)
        timer_thread.start()
        sys.stdout.flush()
        
    now=time.time()
    
    delta_count_last = delta_count

    t_minus = t_now
    t_now = t_plus
    t_plus = cam.read()[1]
    t_plus = cv2.blur(t_plus,(8,8))
    t_plus = cv2.resize(t_plus, (640, 480))

    key = cv2.waitKey(10)
    if key == 0x1b or key == ord('q'):
        cv2.destroyWindow(winName)
        break
        
