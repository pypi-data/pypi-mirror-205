from setuptools import setup


with open("README.md", 'r') as f:
    long_description = f.read()


setup(
    name="cashman",
    version="0.0.0",  # SemVer... Major, Minor, Patch
    description="A cli tool to track personal expenses",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LordUbuntu/cash-man",
    keywords=["python", "expense tracker", "personal finance", "finance", "cli"],
    license="Unlicense",
    author="Jacobus Burger",
    author_email="therealjacoburger@gmail.com",
    packages=["cashman"],
    install_requires=["rich==13.3.4", "click==8.1.3"],
    extras_require={
        "dev": ["pytest>=7.2", "twine>=4.0.2"],
    },
    python_requires=">=3.10",
    platforms=["any"],
    py_modules=["cashman"],
    entry_points={
        "console_scripts": ["cashman=cashman.__main__:main"],
    },
    classifiers=[
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
        "Topic :: Utilities",
        "Environment :: Console",
    ],
)
