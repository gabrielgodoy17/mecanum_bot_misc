import launch
import launch_ros
import os
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.actions import DeclareLaunchArgument

def generate_launch_description():
    pkg_share = FindPackageShare(package='mecanum_bot_misc').find('mecanum_bot_misc')
    slam_pkg_share = FindPackageShare(package='slam_toolbox').find('slam_toolbox')
    bot_pkg_share = FindPackageShare(package='mecanum_bot').find('mecanum_bot')
    slam_pkg_share = FindPackageShare(package='slam_toolbox').find('slam_toolbox')
    default_rviz_config_path = os.path.join(pkg_share, 'rviz/config.rviz')

    ekf_params_file = os.path.join(bot_pkg_share, 'config/ekf.yaml')
    offline_params_file = os.path.join(slam_pkg_share, '/config/mapper_params_offline.yaml')
    online_async_params_file = os.path.join(slam_pkg_share, '/config/mapper_params_online_async.yaml')
    online_sync_params_file = os.path.join(slam_pkg_share, 'config/mapper_params_online_sync.yaml')

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', LaunchConfiguration('rvizconfig')],
    )

    robot_localization_node = Node(
        package='robot_localization',
        executable='ekf_node',
        name='ekf_filter_node',
        parameters=[ekf_params_file]
    )

    slam_node = Node(
        parameters=[offline_params_file],
        package='slam_toolbox',
        executable='sync_slam_toolbox_node',
        name='slam_toolbox'
    )
   
    return launch.LaunchDescription([
        DeclareLaunchArgument(name='rvizconfig', default_value=default_rviz_config_path,
                                            description='Absolute path to rviz config file'),
        rviz_node,
        robot_localization_node,
        slam_node
    ])