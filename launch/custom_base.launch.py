import launch
import os
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.actions import DeclareLaunchArgument

def generate_launch_description():
    pkg_share = FindPackageShare(package='mecanum_bot_misc').find('mecanum_bot_misc')
    bot_pkg_share = FindPackageShare(package='mecanum_bot').find('mecanum_bot')

    
    default_rviz_config_path = os.path.join(pkg_share, 'rviz/config.rviz')
    default_model_path = os.path.join(bot_pkg_share, 'description/mecanum_bot_description.urdf')
    # ekf_params_file = os.path.join(bot_pkg_share, 'config/ekf.yaml')
    # custom_slam_params_file = os.path.join(pkg_share, 'config/custom_slam_params.yaml')

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', LaunchConfiguration('rvizconfig')],
    )

    # robot_localization_node = Node(
    #     package='robot_localization',
    #     executable='ekf_node',
    #     name='ekf_filter_node',
    #     parameters=[ekf_params_file]
    # )

    # slam_node = Node(
    #     parameters=[
    #         custom_slam_params_file
    #     ],
    #     package='slam_toolbox',
    #     executable='async_slam_toolbox_node',
    #     name='slam_toolbox',
    #     output='screen'
    # )

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': Command(['xacro ', LaunchConfiguration('model')])}],
        arguments=[default_model_path]
    )

    joint_state_publisher_node = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        parameters=[{'source_list': ['wheels_joint_state']}]
    )

    direction_mapper_node = Node(
        package='mecanum_bot',
        executable='direction_mapper',
        name='direction_mapper'
    )

    fwd_kinematics_node = Node(
        package='mecanum_bot',
        executable='fwd_kinematics',
        name='fwd_kinematics'
    )

    inv_kinematics_node = Node(
        package='mecanum_bot',
        executable='inv_kinematics',
        name='inv_kinematics'
    )

    # wheels_joint_update_node = Node(
    #     package='mecanum_bot',
    #     executable='wheels_joint_update',
    #     name='wheels_joint_update'
    # )

    wheels_speed_broadcaster = Node(
        package='mecanum_bot',
        executable='wheels_speed_broadcaster',
        name='wheels_speed_broadcaster'
    )

    # tf2_node = Node(
    #     package='tf2_ros',
    #     executable='static_transform_publisher',
    #     name='static_tf_pub_laser',
    #     arguments=['0', '0', '0.02','0', '0', '0', '1','base_link','laser_frame'],
    # )

    return launch.LaunchDescription([
        DeclareLaunchArgument(
            name='rvizconfig', 
            default_value=default_rviz_config_path,
            description='Absolute path to rviz config file'),
        DeclareLaunchArgument(
            name='model', 
            default_value=default_model_path,
            description='Absolute path to robot urdf file'),
        rviz_node,
        robot_state_publisher_node,
        joint_state_publisher_node,
        direction_mapper_node,
        fwd_kinematics_node,
        inv_kinematics_node,
        # wheels_joint_update_node,
        wheels_speed_broadcaster
        # tf2_node
        # robot_localization_node,
        # slam_node
    ])
