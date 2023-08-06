from setuptools import setup, find_packages
import atexit

setup(
    # name=['selfetch', 'Selfetch'],#name='selfetch',
    name='selfetch',
    version='0.0.0.0',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'selfetch = selfetch.__main__:main'
        ]
    },
    author='Juste Elysée MALNADILA',
    author_email='malandilajusteelysee@gmail.com',
    description=''' 👨‍💻"selfetch" is a Python package that automatically imports missing modules on-the-fly, saving time and effort during coding 🛠️⌛''',
    long_description=''' this is a Python package designed to facilitate the importation of missing modules during coding. Rather than requiring manual importation of modules that have not been previously utilized, "selfetch" enables automatic detection and importation of such modules in real-time. This feature streamlines the coding process by eliminating the need for users to manually manage imports, allowing them to focus on writing code without distraction. "selfetch" is available for installation via PyPI using pip.''',
    url='https://github.com/yourusername/selfetch',
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
print("(*) selfetch to serve you well, thank you!")