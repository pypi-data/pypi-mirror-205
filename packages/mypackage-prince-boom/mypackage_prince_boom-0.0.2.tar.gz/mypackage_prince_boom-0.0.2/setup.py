from setuptools import setup

setup(
    name='mypackage_prince_boom',
    version='0.0.2',
    packages=['mypackage_prince_boom'],
    install_requires=[
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'mypackage_prince_boom = mypackage_prince_boom.__main__:main'
        ]
    },
    author='prince',
    author_email='princee.studio45creations@gmail.com',
    description='A short description of your package',
    url='https://github.com/prince7417/mypackage_prince_boom',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
