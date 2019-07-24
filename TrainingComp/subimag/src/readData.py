#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from PIL import Image
import requests
from StringIO import StringIO
from SuironIO import SuironIO
from clock import Clock
import json
import numpy
from threading import Lock

with open('./settings.json') as d:
    SETTINGS = json.load(d)

suironio = SuironIO(id=0, width=SETTINGS['width'], height=SETTINGS['height'], depth=SETTINGS['depth'])
suironio.init_saving()
lock = Lock()
clck=Clock(suironio, 0.01)
clck.start()



def callback(data):

    lock.acquire()
    if (not suironio.check_lock()):

#    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
        response = requests.get('http://10.108.95.102:8080/?action=snapshot')
        img = Image.open(StringIO(response.content))
        response.close()
        turn = abs((data.angular.z/8)-0.15)
        speed  = (data.linear.x/14)+0.15   
        s={}
        s['motor']=speed
        s['servo']=turn
        print("Recording Inputs...")
        suironio.record_inputs(s, numpy.array(img))
        suironio.unlock()

    lock.release()
    print("releasing")


def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('listener', anonymous=True)
    sub=rospy.Subscriber("cmd_vel", Twist, callback, queue_size=1, tcp_nodelay=True, buff_size=2**24)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    while  not rospy.is_shutdown():
        try:
            listener() 
        except KeyboardInterrupt:
            break

    print('Saving file...')
    clck.stop()
