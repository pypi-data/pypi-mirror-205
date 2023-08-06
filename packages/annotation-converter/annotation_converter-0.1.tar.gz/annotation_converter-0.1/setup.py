from setuptools import setup, find_packages

setup(
    name='annotation_converter',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        
        'Flask'
    ],
    entry_points={
        'console_scripts': [
            'annotation_converter=annotation_converter.__main__:main'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
