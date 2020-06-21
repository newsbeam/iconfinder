from distutils.core import setup

setup(
    name='nm_iconfinder',
    packages=['nm_iconfinder'],
    version='0.1.2',
    license='ISC',
    description='Find icons of a website given a URL',
    author='newsmail.today',
    author_email='us@newsmail.today',
    url='https://github.com/newsmail-today/iconfinder',
    keywords=['icon', 'favicon', 'newsmail'],
    install_requires=[
        "beautifulsoup4",
        "lxml",
        "Pillow",
        "requests",
    ],
    classifiers=[
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
)
