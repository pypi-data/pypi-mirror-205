import setuptools

setuptools.setup(
    name='local-logger-python-backend-setup-name',
    version='0.0.3',
    author="Circles",
    author_email="info@circles.zone",
    description="PyPI Package for Circles Local Python Logger functions",
    long_description="This is a package for sharing common Logger\
                    function used in different repositories",
    long_description_content_type="text/markdown",
    url="https://github.com/circles-zone/local-logger-python-backend",
    packages=setuptools.find_packages(),
    install_requires=['mysql.connector.pooling'],
    classifiers=[
     "Programming Language :: Python :: 3",
     "License :: Other/Proprietary License",
     "Operating System :: OS Independent",
    ],
 )
