import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="common-cols-project",
    version="0.1.3",
    author="Elena García Mañes",
    author_email="elenagarciamanes@example.com",
    description="Given a list of data frames, finds common columns between all pairs of data frames.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ElenaGarciaManes?tab=repositories",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
