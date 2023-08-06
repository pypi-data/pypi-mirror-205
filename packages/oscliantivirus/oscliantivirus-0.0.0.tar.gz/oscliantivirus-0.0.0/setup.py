from setuptools import setup, find_packages
import atexit, os

with open("readme.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    # name=['oscliantivirus', 'oscliantivirus'],#name='oscliantivirus',
    name='oscliantivirus',
    version='0.0.0',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'oscliantivirus = oscliantivirus.__main__:main'
        ]
    },
    author='Juste Elysée MALNADILA',
    author_email='malandilajusteelysee@gmail.com',
    description=''' 👨‍💻🛠️
"oscliantivirus" is an advanced antivirus package designed for both developers and standard users to provide custom security features for their systems.''',
    # long_description=''' this is a Python package designed to facilitate the importation of missing modules during coding. Rather than requiring manual importation of modules that have not been previously utilized, "oscliantivirus" enables automatic detection and importation of such modules in real-time. This feature streamlines the coding process by eliminating the need for users to manually manage imports, allowing them to focus on writing code without distraction. "oscliantivirus" is available for installation via PyPI using pip.''',
    # long_description=open('README.rst').read(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/yourusername/oscliantivirus',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        # 'Programming Language :: Python :: 3.6',
        # 'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
    python_requires='>=3.8'
    # Project_description='dfgldfgkmdlfkgfdmlk'
)

def print_welcome_message():
    print("Thank you for installing my_module!")
    print("We hope you find it useful.")

atexit.register(print_welcome_message)
print("(*) oscliantivirus to serve you well, thank you!")