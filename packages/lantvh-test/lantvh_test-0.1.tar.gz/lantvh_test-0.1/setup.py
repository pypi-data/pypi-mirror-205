from setuptools import setup

setup(
    name='lantvh_test',
    version='0.1',
    description='SDK example',
    author='lantvh',
    author_email='lantvh@vpi.pvn.vn',
    entry_points={
        'console_scripts': [
            'lantvh=lantvh:excel_processing',
        ],
    },
    py_modules=['lantvh'],
   
    install_requires=[
        'pandas>=1.3.0'
    ],
)
