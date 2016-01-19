from setuptools import setup

DESCRIPTION = 'Script to test effectivness of image compression tools'

setup(
    author="Marko Samastur",
    author_email="markos@gaivo.net",
    name='squeeze',
    version='0.1.0',
    description=DESCRIPTION,
    long_description=DESCRIPTION,
    url='https://github.com/samastur/compression_tests',
    platforms=['OS Independent'],
    license='MIT License',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Multimedia :: Graphics',
        'Topic :: Utilities',
    ],
    install_requires=[
        'pyimagediet>=1.1.0',
        'Click>=6.2',
    ],
    include_package_data=True,
    packages=['squeeze'],
    entry_points={
        'console_scripts': ['sqz=squeeze.squeeze:squeeze']
    },
    zip_safe=False
)
