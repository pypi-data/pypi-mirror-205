import setuptools

setuptools.setup(
    name="CommonlyTools",
    version="2.1.1",
    author="MaxPython110331",
    author_email="max.gamil110331@gmail.com",
    description="You will use Python easily!",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/maxgamil110331/CommonlyTools",                                         
    packages=["commonlytools"],
    keywords="CommonlyTools",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["requests", "datetime"],
    python_requires=">=3.6"
)