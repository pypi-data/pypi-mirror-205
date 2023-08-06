from setuptools import setup, find_packages

setup(
    name='test-push-swap',
    version='0.5',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'test_push_swap = test_push_swap.pstester:main'
        ]
    },
    install_requires=[],
    author='hueseyin kaya aydin',
    author_email='huaydin@student.42vienna.com',
    description='A tester for the push swap project',
    url='https://github.com/hu8813/tester_push_swap',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)

