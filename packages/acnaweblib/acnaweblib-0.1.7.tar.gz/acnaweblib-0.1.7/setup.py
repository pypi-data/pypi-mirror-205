from setuptools import setup, find_packages

def readme():
    with open('README.rst') as f:
        return f.read()

requirements = []

setup(
    name='acnaweblib',
    version='0.1.7',
    description='Short description',
    long_description=readme(),
    author='Antonio Carlos de Lima Junior',
    author_email='antonioclj.ac@gmail.com',
    url='https://github.com/acnaweb/acnaweb-lib',
    packages=find_packages(include=['acnaweblib', 'acnaweblib.*']),
    install_requires=requirements,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Text Processing :: Linguistic',
      ],
    keywords='funniest joke comedy flying circus',
    license='MIT',
)
