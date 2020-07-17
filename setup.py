from setuptools import setup, find_packages, Extension
from os.path import join, dirname

setup(
    name='audiocorpusbuilder',              
    version=audiocorpusbuilder.__version__,                         
    description='command-line package for automatical creation of russian language audio corpus (pairs speech-text) from YouTube audiotracks and subtitles',
    url='https://github.com/dangrebenkin/audiocorpusbuilder',
    author='Daniel Grebenkin',
    author_email = 'd.grebenkin@g.nsu.ru',
    license='Apache License Version 2.0',
    keywords=['dataset', 'librosa', 'youtube-dl', 'youtube'],     
    packages = find_packages(), 
    platforms = 'Linux',
    entry_points ={ 
        'console_scripts': [ 
            'acbr = audiocorpusbuilder.core:main'
        ]
    },
    install_requires=[
        'audioread >= 2.0.0',
        'numpy >= 1.15.0',
        'packaging >= 18',
        'scipy >= 1.0.0',
        'scikit-learn >= 0.14.0, != 0.19.0',
        'joblib >= 0.14',
        'decorator >= 3.0.0',
        'resampy >= 0.2.2',
        'numba == 0.48',
        'soundfile >= 0.9.0',
        'pooch >= 1.0',
        'librosa>=0.7.0',
        'youtube-dl>=2020.1.1'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',  
        'Programming Language :: Python :: 3.8']            
) 

