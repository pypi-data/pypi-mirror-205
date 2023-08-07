from setuptools import setup, find_packages


with open("README.rst", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setup(
    name='terminalplay',
    version='1.0.21',
    license='MIT',
    author="Merwin JD",
    author_email='merwin@fbi.ac',
    packages=find_packages('terminalplay/src'),
    package_dir={'': 'terminalplay/src'},
    url='https://github.com/merwin-asm/Terminal_Play',
    keywords='terminalplay, play videos, terminal',
    install_requires=[
          'moviepy',
          'playsound',
          'rich',
          'sty',
          'opencv-python'
      ],
      description="Play videos on your terminal; Works on windows as well as linux;The video played will also have color and sound :)",
          long_description = long_description,
    long_description_content_type = "text/markdown",
      platforms= ["windows","linux"],
    project_urls = {
        "Bug Tracker": "https://github.com/merwin-asm/Terminal_Play/issues",
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

      
)