import setuptools

# Open the requirements file and dump them
with open("requirements.txt") as file:
    requirements = file.read().splitlines()
# Do the same with the dev requirements
with open("requirements-dev.txt") as file:
    extras = {"dev": file.read().splitlines()}


setuptools.setup(
    name="tokki",
    version="0.1",
    author="Hannele Ruiz",
    author_email="lemon@justalemon.ml",
    description="Set of Asynchronous APIs for various services.",
    url="https://github.com/ChomusukeBot/Tokki",
    packages=["tokki"],
    install_requires=requirements,
    extras_require=extras,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
