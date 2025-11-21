from sensor_msgs.msg import JointState
import time
from math import pi
import rclpy
from rclpy.node import Node
import DOGZILLALib as dog

control = dog.DOGZILLA()

"""
"lf_hip_joint", 左边肩部关节
"lf_lower_leg_joint",  左边前腿底部关节
"lf_upper_leg_joint", 左边前腿上部关节


"lh_lower_leg_joint", 左边后腿底部关节
"lh_upper_leg_joint", 左边后腿上部电机
"lh_hip_joint", 左边臀部关节

"rf_hip_joint", 右边肩部电机
"rf_lower_leg_joint", 右边前腿底部关节
"rf_upper_leg_joint", 右边前腿上部关节

"rh_hip_joint", 右边臀部关节
"rh_lower_leg_joint", 右边后腿底部关节
"rh_upper_leg_joint" 右边后腿上部关节
"""


class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('yahboomcar_joint_state')
        self.dogControl = dog.DOGZILLA()
        self.publisher_ = self.create_publisher(JointState, '/joint_states', 10)
        self.timer_period = 0.05  # seconds
        self.timer = self.create_timer(self.timer_period, self.timer_callback)
        self.i = 0
        self.last_state = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    def timer_callback(self):
        try:
            msg = JointState()
            t = self.get_clock().now()
            msg.header.stamp = t.to_msg()
            msg.name = ["lf_upper_leg_joint", "lf_lower_leg_link",  "lf_hip_joint",
                        "lh_upper_leg_joint", "lh_lower_leg_joint",  "lh_hip_joint",
                        "rf_upper_leg_joint", "rf_lower_leg_joint",  "rf_hip_joint",
                        "rh_upper_leg_joint", "rh_lower_leg_joint",   "rh_hip_joint"]

            angle = self.dogControl.read_motor()
            print(angle)
            msg.position = [angle[0] * pi / 180, 0 - angle[1] * pi / 180, angle[2] * pi / 180,
                            angle[3] * pi / 180, 0 - angle[4] * pi / 180, angle[5] * pi / 180,
                            0 - angle[6] * pi / 180, angle[7] * pi / 180, angle[8] * pi / 180,
                            0 - angle[9] * pi / 180, angle[10] * pi / 180, angle[11] * pi / 180]

            # msg.position = [-0.74, 0.3, 0.0,
            #                 0.0, 0.0, 0.0,
            #                 0.0, 0.0, 0.0,
            #                 0.0, 0.0, 0.0]
            dt = 1
            msg.velocity = [(angle[0] * pi / 180 - self.last_state[0] * pi / 180) / self.timer_period,
                            (angle[1] * pi / 180 - self.last_state[1] * pi / 180) / self.timer_period,
                            (angle[2] * pi / 180 - self.last_state[2] * pi / 180) / self.timer_period,
                            (angle[3] * pi / 180 - self.last_state[3] * pi / 180) / self.timer_period,
                            (angle[4] * pi / 180 - self.last_state[4] * pi / 180) / self.timer_period,
                            (angle[5] * pi / 180 - self.last_state[5] * pi / 180) / self.timer_period,
                            (angle[6] * pi / 180 - self.last_state[6] * pi / 180) / self.timer_period,
                            (angle[7] * pi / 180 - self.last_state[7] * pi / 180) / self.timer_period,
                            (angle[8] * pi / 180 - self.last_state[8] * pi / 180) / self.timer_period,
                            (angle[9] * pi / 180 - self.last_state[9] * pi / 180) / self.timer_period,
                            (angle[10] * pi / 180 - self.last_state[10] * pi / 180) / self.timer_period,
                            (angle[11] * pi / 180 - self.last_state[11] * pi / 180) / self.timer_period,
                            ]

            self.last_state = angle

            msg.effort = [float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                          float("nan"),
                          float("nan"), float("nan"), float("nan"), float("nan"), float("nan")]

            self.publisher_.publish(msg)
        except IndexError:
            self.get_logger().error(f'获取舵机状态失败', throttle_duration_sec=1)
            pass


def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()

    rclpy.spin(minimal_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
