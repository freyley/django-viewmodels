from setuptools import setup
import subprocess
import os.path

setup(
    name='django-viewmodels',
    version='0.3.0',
    description='Class based views for Django with automatic viewmodel rendering',
    author='Jeff Schwaber, Chris Pitzer, LoFi Art',
    author_email='freyley@gmail.com',
    url='',
    packages=['djviewmodels'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    zip_safe=False,
    #test_suite='tests.runtests.runtests',
    package_data={
        'djviewmodels': [
            '*.py',
        ]
    },
)
