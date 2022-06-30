import os
from setuptools import setup
from glob import glob

package_name = 'mecanum_bot_misc'

setup(
    name=package_name,
    version='1.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name + '/rviz'), glob('rviz/*.rviz')),
        (os.path.join('share', package_name + '/launch'), glob('launch/*.launch.py')),
        (os.path.join('share', package_name + '/config'), glob('config/*.yaml')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='gabriel',
    maintainer_email='godoygabriel07@gmail.com',
    description='Additional package for riz and teleop mecanum robot',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'teleop = mecanum_bot_misc.teleop:main'
        ],
    },
)
