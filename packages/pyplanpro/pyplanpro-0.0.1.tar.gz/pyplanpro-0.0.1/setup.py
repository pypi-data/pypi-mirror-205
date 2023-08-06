from setuptools import setup, find_packages

setup(
    name='pyplanpro',
    version='0.0.1',
    author='Jacob Østergaard Nielsen',
    author_email='jaoe@oestergaard-as.dk',
    description='Task scheduler for python',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Oestergaard-A-S/PyPlanPro',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
    ],
    install_requires=[
        # List your package's dependencies here
    ],
)