from setuptools import setup

setup(name='eeg_blinks',
      version='0.0.3',
      description='make life easier',
      author='rpb',
      packages=['eeg_blinks','eeg_blinks.utilities',
                  'eeg_blinks.vislab','eeg_blinks.viz'],
      long_description='Get EOG from EEG signal recording',
      install_requires=['seaborn']
      )
