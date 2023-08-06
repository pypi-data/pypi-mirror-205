from setuptools import setup, find_packages

def readme():
    with open('README.md') as f:
        return f.read()

VERSION = '0.0.1'
DESCRIPTION = 'Drill-bits, handy tools for ML in Python'

# Setting up
setup(
        name="drill-bits", 
        version=VERSION,
        author="jiujiuche",
        author_email="jiujiuche@gmail.com",
        description=DESCRIPTION,
        long_description=readme(),
        packages=find_packages(),
        install_requires=[
            'numpy',
            'Pillow',
        ],
        zip_safe=False,
        keywords=['python', 'toolbox'],
        classifiers= [
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)