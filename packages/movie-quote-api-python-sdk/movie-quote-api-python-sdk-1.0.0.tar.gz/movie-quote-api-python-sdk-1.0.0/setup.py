from setuptools import setup, find_packages

setup(
    name='movie-quote-api-python-sdk',
    version='1.0.0',
    description='Python SDK for the Movie Quote API',
    author='Ashish Sharda',
    author_email='ashishjsharda@gmail.com',
    url='https://github.com/yourusername/movie-quote-api-python-sdk',
    packages=find_packages(),
    install_requires=['requests'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
