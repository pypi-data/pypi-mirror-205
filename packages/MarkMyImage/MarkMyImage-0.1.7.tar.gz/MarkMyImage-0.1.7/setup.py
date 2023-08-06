from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="MarkMyImage",
    version="0.1.7",
    description="Add a watermark to all images in a folder.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Lomezno",
    author_email="dbwspain@gmail.com",
    packages=find_packages(),
    install_requires=["Pillow", "pyheif"],
    entry_points={
        "console_scripts": [
            "mmi=MarkMyImage:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.6",
)
