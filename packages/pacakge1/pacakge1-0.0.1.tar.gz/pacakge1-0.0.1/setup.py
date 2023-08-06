import setuptools

setuptools.setup(
    name="pacakge1",
    packages=['package1'],
    py_modules=['package1.another_package'],
    install_requires=[],
    version="0.0.1",
    author="Ubaid Shaikh",
    author_email="shaikhubaid769@gmail.com",
    description="A package for importing modules as top-level",
    long_description="",
    long_description_content_type="text/markdown",
    url="https://github.com/Shaikh-Ubaid/lpython_packages",
    classifiers=[ # Classifiers give pip metadata about your project. See https://pypi.org/classifiers/ for a list of available classifiers.
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
