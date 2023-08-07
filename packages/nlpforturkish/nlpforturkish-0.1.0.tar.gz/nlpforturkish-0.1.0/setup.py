from setuptools import setup

setup(
    name='nlpforturkish',
    version='0.1.0',
    description='The aim of the NLPforTurkish library is to assist people interested in artificial intelligence by supporting the Turkish NLP area, which will benefit many people, particularly those who want to work on Turkish NLP.',
    author='Furkan Kesgin',
    author_email='furkan_bfk@hotmail.com',
    packages=['nlpforturkish'],
    install_requires=[
        'pandas',
        'scikit-learn',
        'matplotlib',
        'lazypredict',
        'tweepy'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
