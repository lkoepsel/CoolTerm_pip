from setuptools import setup, find_packages

setup(
    name='CoolTerm',
    version='0.1',
    # This tells setuptools to include any directories, and subdirectories,
    # which include an __init__.py file
    packages=find_packages(),
    install_requires=[],
    # Metadata
    author='Your Name',
    author_email='your.email@example.com',
    description='CoolTerm scripting capabilities',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    # Use the URL to the github repo or wherever your code is hosted
    url='https://github.com/lkoepsel/CoolTerm_pip',
    # Descriptive keywords to help find your package
    keywords='CoolTerm serial scripting',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        # Pick a topic relevant for your package
        'Topic :: Software Development :: Communications',
        'License :: OSI Approved :: MIT License',  # Again, pick a license
        # Specify the Python versions you support here
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.12',
    ],
)
