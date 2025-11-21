import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    
    #nav2_yaml = os.path.join(get_package_share_directory('localization_server'), 'config', 'amcl_config.yaml')
    nav2_yaml = "~/cartoros2/src/localization_server/config/amcl_config.yaml"
    #map_file = os.path.join(get_package_share_directory('map_server'), 'config', 'turtlebot_area.yaml')
    map_file = "~/cartoros2/mymap2.yaml"
    
    #planner
    base_url = "~/cartoros2/src/localization_server/config/"
    controller_yaml = base_url + "controller.yaml"
    bt_navigator_yaml = base_url + "bt_navigator.yaml"
    planner_yaml = base_url + "planner_server.yaml"
    recovery_yaml = base_url + "recovery.yaml"
    
    
    	
    return LaunchDescription([
        Node(
            package='nav2_map_server',
            executable='map_server',
            name='map_server',
            output='screen',
            parameters=[{'use_sim_time': True}, 
                        {'yaml_filename':map_file},
                        {'use_map_topic':True},
                        {'publish_full_map':True},
                        {'publish_map_metadata':True},
                        {'publish_frequency':100.0}]
        ),
            
        #Node(
        #    package='nav2_amcl',
        #    executable='amcl',
        #    name='amcl',
        #    output='screen',
        #    parameters=[nav2_yaml],
            

            
           
        ),
        
        Node(
            package='nav2_controller',
            executable='controller_server',
            name='controller_server',
            output='screen',
            parameters=[controller_yaml]),

        Node(
            package='nav2_planner',
            executable='planner_server',
            name='planner_server',
            output='screen',
            parameters=[planner_yaml]),
            
        Node(
            package='nav2_recoveries',
            executable='recoveries_server',
            name='recoveries_server',
            parameters=[recovery_yaml],
            output='screen'),

        Node(
            package='nav2_bt_navigator',
            executable='bt_navigator',
            name='bt_navigator',
            output='screen',
            parameters=[bt_navigator_yaml]),
            

        Node(
            package='nav2_lifecycle_manager',
            executable='lifecycle_manager',
            name='lifecycle_manager_navigation',
            output='screen',
            parameters=[{'use_sim_time': True},
                        {'autostart': True},
                        {'node_names': ['map_server','amcl',
                        'planner_server','controller_server',
                        'recoveries_server', 'bt_navigator']}]
        )
    ])
