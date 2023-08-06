from setuptools import setup, find_packages

def readme():
    with open('README.md') as f:
        return f.read()

requirements = []

setup(
    name='acnaweblib',
    version='0.1.10',
    description='Short description',
    long_description=readme(),
    long_description_content_type="text/markdown",
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
