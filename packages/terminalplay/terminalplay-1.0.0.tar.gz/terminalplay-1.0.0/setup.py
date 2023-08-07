from setuptools import setup, find_packages

setup(
    name='terminalplay',
    version='1.0.0',
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
      description="Play videos on your terminal; Works on windows as well as linux",
      long_description="""
      The video played will also have color and sound :)
      Videos be converted into easily readable frames which will be printed on the terminal (This 
      conversion will only take place once).
      """,
      platforms= ["windows","linux"]
)