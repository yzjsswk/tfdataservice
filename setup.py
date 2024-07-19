from setuptools import setup, find_packages

setup(
    name='touchfish',
    version='1.0.4',
    description='data service and python sdk for touchfish #6cc92702e32f55e9446da17e86f8d8e150c87d82',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='yzjsswk',
    author_email='yzjsswk@gmail.com',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
    install_requires=[
        'yfunc',
        'PyYAML',
        'whoosh',
        'flask',
        'requests',
        'PyMuPDF'
    ],
)
