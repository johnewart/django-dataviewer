from setuptools import setup, find_packages

setup(
    name='django-dataviewer',
    version='0.5.0',
    description='A Django application you can use to create views of your models and data.',
    long_description=open('README.rst').read(),
    author='John Ewart',
    author_email='john@johnewart.net',
    url='https://github.com/johnewart/django-dataviewer',
    download_url='https://github.com/johnewart/django-dataviewer/downloads',
    license='BSD',
    packages=find_packages(exclude=('ez_setup', 'tests', 'example')),
    tests_require=[
        'django>=1.1,<1.4',
    ],
    test_suite='runtests.runtests',
    include_package_data=True,
    zip_safe=False, 
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)