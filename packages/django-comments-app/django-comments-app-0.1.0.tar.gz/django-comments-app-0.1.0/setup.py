from setuptools import setup, find_packages

setup(
    name='django-comments-app',
    version='0.1.0',
    description='A reusable Django app for comments',
    author='Usmonbek Ravshanov',
    author_email='usmonbekravshanov@gmail.com',
    packages=find_packages(),
    install_requires=[
        'Django>=3.2',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Framework :: Django :: 3.2',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
