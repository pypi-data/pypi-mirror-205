from setuptools import setup

setup(
    name='vtb_biname',
    version='0.1',
    description='A binary organization/ individual name classification library for PySpark',
    url='https://github.com/NguyenThaoVi0702/vtb_biname',
    author='Nguyen Thao Vi',
    author_email='vinguyen7202@gmail.com',
    packages=['vtb_biname'],
    install_requires=[
        'pandas',
        'scikit-learn',
        'joblib',
        'pyspark'
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