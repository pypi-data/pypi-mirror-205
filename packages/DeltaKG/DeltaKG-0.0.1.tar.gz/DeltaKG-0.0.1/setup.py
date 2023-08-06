# coding: utf-8
import setuptools
from os import path
this_directory = path.abspath(path.dirname(__file__))

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except:
    long_description = ""

setuptools.setup(
    name='DeltaKG',
    version='0.0.1',
    description='A library for dynamically editing PLM-based KG embeddings.',
    author='Bozhong Tian',
    author_email='tbozhong@zju.edu.cn',
    url='https://github.com/zjunlp/PromptKG/tree/main/deltaKG',
    install_requires=[],
    # install_requires=['dataclasses==0.8', 'transformers==4.26.1', 'activations==0.1.0', 'flax==0.3.4',
    #                   'utils==1.0.1', 'pytorch_lightning==1.3.1', 'jsonlines', 'higher', 'allennlp', 'file_utils==0.0.1'],
    keywords='knowledge graph embedding edit',
    long_description=long_description,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6"
)
