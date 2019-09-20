import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="killerasteroids",
    author="Henrik Petersson",
    author_email="henrik@tutamail.com",
    description="Shoot 'em up game created with pygame",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    package_data={"": ["*.wav", "*.ogg", "*.ttf", "*.png"]},
    python_requires=">=3.7.4",
    entry_points={
        "console_scripts": ["killerasteroids = killerasteroids.__main__:main"]
    },
)
