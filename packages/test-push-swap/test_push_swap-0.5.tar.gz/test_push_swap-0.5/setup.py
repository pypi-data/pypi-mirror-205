from setuptools import setup

setup(
    name='test_push_swap',
    version='0.5',
    packages=['test_push_swap'],
    url='https://github.com/hu8813/tester_push_swap',
    license='MIT',
    author='hueseyin kaya aydin',
    author_email='huaydin@student.42vienna.com',
    description='A tester for the push swap project',
    entry_points={
        'console_scripts': [
            'test_push_swap=test_push_swap.post_install:main'
        ]
    }
)

