import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name='statusDadosjusbr',
    version='0.3',
    author="Dadosjusbr",
    author_email="dadosjusbr@gmail.com",
    description="Contém os status de execução dos coletores do DadosjusBr",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dadosjusbr/status/",
    packages=['status'],
    classifiers=[
        "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
    ],
)
