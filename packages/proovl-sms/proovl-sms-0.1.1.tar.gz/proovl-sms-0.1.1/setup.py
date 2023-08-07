from setuptools import setup, find_packages

setup(
    name='proovl-sms',
    version='0.1.1',
    author='Tomas',
    author_email='',
    description='A Python library for sending SMS messages using Proovl API',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://www.proovl.com',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Communications :: Telephony',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
