from setuptools import setup, find_packages

setup(
    name='classreg',
    version='0.0.1',
    description='data analysis',
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
    keywords='data analysis',
    install_requires=[
        'pandas',
        'matplotlib',
        'statsmodels',
        'scikit-learn',
    ],
)
