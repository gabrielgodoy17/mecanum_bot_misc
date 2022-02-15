import launch
import launch_ros
import os
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    pkg_share = launch_ros.substitutions.FindPackageShare(package='mecanum_bot_misc').find('mecanum_bot_misc')
    default_rviz_config_path = os.path.join(pkg_share, 'rviz/config.rviz')

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', LaunchConfiguration('rvizconfig')],
    )
   
    return launch.LaunchDescription([
        launch.actions.DeclareLaunchArgument(name='rvizconfig', default_value=default_rviz_config_path,
                                            description='Absolute path to rviz config file'),
        rviz_node
    ])