import setuptools
from setuptools import setup

setup(
    name='porter-depthai',
    version='0.1.0',    
    description='Scripts for depthai and cv2 cameras',
    url='https://github.com/porteratzo/my_depthai',
    author='Omar Montoya',
    author_email='omar.alfonso.montoya@hotmail.com',
    license='MIT License',
    packages=setuptools.find_packages(),
    install_requires=['matplotlib',
                      'numpy',
                      'porter-bench[csv]',
                      'opencv-python',
                      'depthai',
                      ],
    extras_require={
    },
    classifiers=[
        'Operating System :: POSIX :: Linux', 
        'Programming Language :: Python :: 3',
    ],
)