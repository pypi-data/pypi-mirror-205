from setuptools import setup, find_packages

setup(
    name='wansec',
    version='1.1',
    description='None',
    author='Aoda',
    author_email='febyzamsee@gmail.com',
    packages=find_packages(),
    install_requires=[
        'requests>=2.29.0',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.11',
    ],
)
