from setuptools import setup, find_packages

setup(
    name='SoundGraph',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'matplotlib',
        'SpeechRecognition',
        'pyaudio'
    ],
    entry_points={
        'console_scripts': [
            'sound_graph = sound_graph:main'
        ]
    },
    author='Al Mustafiz Bappy',
    author_email='almustafizbappy@gmail.com',
    description='Real-time audio visualization tool',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/bappy-3/sound-graph',
    license='MIT'
)
