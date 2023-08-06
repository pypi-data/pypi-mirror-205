from setuptools import setup

setup(
    name = 'aggdirect_route_estimation_calculator',         # How you named your package folder (MyLib)
    packages = ['aggdirect_route_estimation_calculator'],
    version = '0.4',
    description = 'Route Estimation Calculator functions',
    author = 'Chinmoy Das',
    author_email = '',
    url = '',   # Provide either the link to your github or to your website
    keywords = ['Route Estimation Calculator', 'Route Calculator' , 'AGGDIRECT'],   # Keywords that define your package best
    install_requires=['polyline'],
    classifiers=[
        'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',      # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',   # Again, pick a license
        'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    ],
)