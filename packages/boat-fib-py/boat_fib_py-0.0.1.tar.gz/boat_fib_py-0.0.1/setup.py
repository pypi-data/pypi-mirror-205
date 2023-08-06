from setuptools import find_packages,setup

with open("README.md","r") as fh:
    long_description = fh.read()

setup(
    name="boat_fib_py",
    version="0.0.1",
    author="zhongjunhang",
    author_email="836914541@qq.com",
    description="Calc a fib number",
    long_description=long_description,
    url="https://github.com/zhongjunhang/boat-fib-py",
    install_requires=[],
    packages=find_packages(exclude=("tests",)),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'fib-number = boat_fib_py.cmd.fib_numb:fib_numb',
        ]
    }
)