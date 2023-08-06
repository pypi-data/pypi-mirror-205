from setuptools import setup, find_packages

with open('README.md') as readme:
    readme_content = readme.read()

setup(
    name='ankitrazorpay',
    version='0.2',
    packages=find_packages(),
    description='A simple calculator package',
    long_description=readme_content,
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    license='MIT',
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