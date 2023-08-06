import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-bootstrapless-synthesizer",
    "version": "2.3.1",
    "description": "Generate directly usable AWS CloudFormation template with aws-cdk v2.",
    "license": "Apache-2.0",
    "url": "https://github.com/aws-samples/cdk-bootstrapless-synthesizer.git",
    "long_description_content_type": "text/markdown",
    "author": "wchaws",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/aws-samples/cdk-bootstrapless-synthesizer.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_bootstrapless_synthesizer",
        "cdk_bootstrapless_synthesizer._jsii"
    ],
    "package_data": {
        "cdk_bootstrapless_synthesizer._jsii": [
            "cdk-bootstrapless-synthesizer@2.3.1.jsii.tgz"
        ],
        "cdk_bootstrapless_synthesizer": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.7",
    "install_requires": [
        "aws-cdk-lib>=2.0.0, <3.0.0",
        "aws-cdk.aws-batch-alpha>=2.8.0.a0, <3.0.0",
        "constructs>=10.0.5, <11.0.0",
        "jsii>=1.72.0, <2.0.0",
        "publication>=0.0.3",
        "typeguard~=2.13.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
