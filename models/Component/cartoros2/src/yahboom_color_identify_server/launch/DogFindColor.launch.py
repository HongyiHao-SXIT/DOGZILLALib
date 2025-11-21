from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():

    yahboom_color_identify_server_node = Node(
        package='yahboom_color_identify_server',
        executable='yahboom_color_identify_server',
        output='screen'
    )

    xgo_nav2_send_goal_node = Node(
        package='xgo_nav2_send_goal',
        executable='xgo_nav2_send_goal',
        output='screen'
    )

    return LaunchDescription(
        [
            yahboom_color_identify_server_node,
            xgo_nav2_send_goal_node,
        ]
    )
