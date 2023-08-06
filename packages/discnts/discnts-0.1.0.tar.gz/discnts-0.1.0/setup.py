from setuptools import setup, find_packages

setup(
    name='discnts',
    version='0.1.0',
    description='A library for applying discounts to orders in a cloud kitchen Django application',
    author='Meerath Nida Aman',
    author_email='nidaaman77@gmail.com',
    packages=find_packages(),
    install_requires=[
        'django>=3.0'
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
    ],
)
