from setuptools import setup, find_packages

setup(
    name='aassddee',
    version='0.0.2',
    description='for fun',
    author='Yizhan',
    author_email='boy87511@gmail.com',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    keywords='iris sklearn',
    install_requires=[
        'pandas',
        'scikit-learn',
    ],
)
