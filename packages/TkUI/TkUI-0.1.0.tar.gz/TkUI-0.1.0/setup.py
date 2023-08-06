import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="TkUI",
    version="0.1.0",
    author="iamxcd",
    author_email="iamxcd@gmail.com",
    description="TkUI,是基于tkinter的Canvas模块开发的,具有现代化风格的UI库",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/iamxcd/tk-ui",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
)
