#!/usr/bin/env python

import math
import rospy
import serial
from serial.threaded import LineReader, ReaderThread
import sys
import math

# These can only be imported after the main ROS imports because they set up the import paths
import std_msgs.msg
import sensor_msgs.msg
import geometry_msgs.msg


class Mpu9250Reader(LineReader):

    TERMINATOR = b'\n'

    def __init__(self, *args, **kwargs):
        self.acc = (0, 0, 0)
        self.mag = (0, 0, 0)
        self.gyro = (0, 0, 0)
        self.orientation = (0, 0, 0, 0)
        super(Mpu9250Reader, self).__init__(*args, **kwargs)

    def handle_line(self, data):
        # Strip off the \n
        line = data.strip()

        if line.startswith('ACC:'):
            self.acc = map(float, line.split(':')[1].split(','))
        if line.startswith('GYRO:'):
            self.gyro = map(float, line.split(':')[1].split(','))
        if line.startswith('MAG:'):
            self.mag = map(float, line.split(':')[1].split(','))
        if line.startswith('ORI:'):
            self.orientation = map(float, line.split(':')[1].split(','))



def run():
    rospy.init_node('mpu9250_arduino')

    imu_raw_data_publisher = rospy.Publisher('imu/data', sensor_msgs.msg.Imu, queue_size=1)
    imu_mag_publisher = rospy.Publisher('imu/mag', sensor_msgs.msg.MagneticField, queue_size=1)

    ser = serial.Serial('/dev/ttyUSB1', 38400, timeout=5)
    with ReaderThread(ser, Mpu9250Reader) as protocol:
        while not rospy.is_shutdown():
            # Convert acc from g to m/s^2
            acc = map(lambda x: x * 9.81, protocol.acc)
            # Convert gyro from deg/s to rad/s
            gyro = map(lambda x: x * (math.pi / 180), protocol.gyro)
            # Convert mag from G to T
            mag = map(lambda x: x / 1000, protocol.mag)

            imu_raw_data_publisher.publish(
                    sensor_msgs.msg.Imu(
                        header=std_msgs.msg.Header(frame_id='imu'),
                        orientation=geometry_msgs.msg.Quaternion(*protocol.orientation),
                        linear_acceleration=geometry_msgs.msg.Vector3(*acc),
                        angular_velocity=geometry_msgs.msg.Vector3(*gyro)))
            imu_mag_publisher.publish(
                    sensor_msgs.msg.MagneticField(
                        magnetic_field=geometry_msgs.msg.Vector3(*mag)))

            rospy.sleep(0.5)

if __name__ == '__main__':
    try:
        run()
    except rospy.ROSInterruptException:
        pass

