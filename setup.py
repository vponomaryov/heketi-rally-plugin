from setuptools import setup


setup(
    name='heketi_rally_plugin',
    version='0.0.1',
    description='Heketi plugin for OpenStack Rally project',
    license='Apache License (2.0) or LGPLv3+',
    author='Valerii Ponomarov',
    author_email='kiparis.kh@gmail.com',
    url='https://github.com/vponomaryov/heketi-rally-plugin',
    install_requires=['rally>=0.11.2', 'heketi>=3.0.0', 'requests'],
    classifiers=[
        'Intended Audience :: Information Technology',
        'Intended Audience :: QA Engineers',
        'License :: OSI Approved :: Apache License 2.0',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: System :: Filesystems',
        'Topic :: System :: Distributed Computing',
    ],
)
