from launch import LaunchDescription
#from launch.actions
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
from launch.substitutions import LaunchConfiguration
import os


def generate_launch_description():

    
  
    carto = IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(
                get_package_share_directory("xgo_bringup"),
                "",
                "Catographer_vanjee.launch.py",
            )),
        )
    
    
    tf_ros_bas_foot_publish = Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='static_transform_publisher',
            arguments=['0', '0', '0.5', '0', '0', '0', '1', 'base_footprint', 'base_link']
    )
    
    tf_ros_laser_publish = Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='static_transform_publisher',
            arguments=['0', '0', '0', '0', '0', '0', '1', 'map', 'vanjee']
    )
    #[LaunchConfiguration(variable_name='scanner')

    
    
    
    rviz_display_node = Node(
        package='rviz2',
        executable="rviz2",
        output="screen"
    )

    return LaunchDescription(
        [
            carto,
            #tf_ros_publish,
            #tf_ros_bas_foot_publish,
            #tf_ros_laser_publish,
            DeclareLaunchArgument(
            name='wlr_720', default_value='wlr_720',
            description='Namespace for sample topics'
        ),
            
            Node(
        package='pointcloud_to_laserscan',
        executable='pointcloud_to_laserscan_node',
        remappings=[('cloud_in', [LaunchConfiguration(variable_name='wlr_720'), '/cloud_points']),
                    ('scan',[LaunchConfiguration(variable_name='wlr_720'), '/scan'])],
        parameters=[{
                'transform_tolerance': 0.01,
                'min_height': 0.0,
                'max_height': 1.0,
                'angle_min': 0.0,  # -M_PI/2
                'angle_max': 3.14,  # M_PI/2
                'angle_increment': 0.00349,  # M_PI/360.0
                'scan_time': 0.1,
                'range_min': 0.5,
                'range_max': 120.0,
                'use_inf': True,
                'inf_epsilon': 1.0
            }],
        output="screen"
    ),
            
            
            #pointclound_to_laserscan_node
        ]
    )
