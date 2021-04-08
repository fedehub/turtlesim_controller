# Copyright 2016 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# Import ROS modules
#
import rclpy
from rclpy.node import Node
# Import ROS Messages and Services
from geometry_msgs.msg import Twist
# from geometry_msgs.msg import Pose (ask)
from turtlesim.msg import Pose
from turtlesim.srv import Kill
from turtlesim.srv import Spawn


class overallcontroller(Node):

    def __init__(self):
        super().__init__('overallcontroller')

        # initialize the client1
        # initialize self.req1
        self.client_1 = self.create_client(Kill, '/kill')
        while not self.client_1.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req1 = Kill.Request()

        # initialize the client2
        # initialize self.req2

        self.client_2 = self.create_client(Spawn, '/spawn')
        while not self.client_2.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req2 = Spawn.Request()

        # initialize publisher and subscriber
        self.publisher_ = self.create_publisher(Twist, '/ciccia/cmd_vel', 10)

    	# subscriber
    	self.subscribtion = self.create_subscribtion(
    	    Pose,
    	    '/ciccia/pose',
    	    self.ciccia_clbk,
    	    10)
    	# for avoiding warning
    	self.subscription

    def send_request(self):
        # set req1
        self.req1.name = 'turtle1'
        # call service 1
        self.future = self.client_1.call_async(self.req1)

    def send_request2(self):
        # set req2
        self.req2.x = 2
        self.req2.y = 5
        self.req2.tetha = 0
        self.req2.name = 'ciccia'
        # call service2
        self.future = self.client_2.call_async(self.req2)

    # publish a velocity message when something is received
    def ciccia_clbk(self, msg):
       # declare a message of Twist type
       msgTwist = Twist()

       if(msg.x > 9.0):
            msgTwist.linear.x = 1.0
            msgTwist.angular.z = 1.0
        elif(msg.x<1.5):
            msgTwist.linear.x=1.0
            msgTwist.angular.z=-1.0
        else:
            msgTwist.linear.x=1.0
            msgTwist.angular.z=0.0
            
        self.publisher_.publish(msgTwist)


def main(args=None):
    # init the node
    rclpy.init(args=args)
    
    
    # call services 1 and 2
    controller = overallcontroller()
    controller.send_request()
    # 
    controller.send_request2()
    
    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    rclpy.spin(controller)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
