import sys
from setuptools import setup
setup(
    name = "gatewayManager",
    version = "1.0",
    author="ScratchNest",
    author_email = "info@scratchnest.com",
    description = "Python module for implementing BLE IoT gateway application",
    url='https://github.com/ScratchnestMPU/Gateway_POC/tree/master/gatewaySoftware',
    keywords= ["Bluetooth","BLE","IoT","IoT gateway"],
    packages=["src","gdm"],
    package_data={
        'src': ['mydatabasenew.db', 'require.txt', 'bluez-src.tgz', 'bluepy-helper.c', 'version.h', 'Makefile']
    },
    entry_points={
        'console_scripts': [
            'main=src.main:main',
            'gdm=gdm.run:main',
        ]
    },
    requires=['flask','bluepy','paho-mqtt','sqlite3','json']
)
