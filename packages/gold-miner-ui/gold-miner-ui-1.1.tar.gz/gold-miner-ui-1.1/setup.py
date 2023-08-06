import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gold-miner-ui",
    version="1.1",
    author="Wes Hardaker",
    author_email="opensource@hardakers.net",
    description="A UI plugin that adds graphical extensions to gold-miner",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/isi-apropos/gold-miner-ui",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "gold-miner",
        "PyQt5",
        "pyqtgraph",
        "matplotlib",
        "multikeygraph",
        "jinja2",
        "roc_utils",
        "pyaml",
    ],
    entry_points={
        "console_scripts": [
            "gold-miner-auditor = apropos.goldminer.tools.auditor:main",
            "gold-miner-tande = apropos.goldminer.tools.tande:main",
            "gold-miner-fingerprint = apropos.goldminer.tools.fingerprinter:main",
        ]
    },
    python_requires=">=3.6",
    test_suite="nose.collector",
    tests_require=["nose"],
    package_data={
        "apropos.goldminer.reports": [
            "template.md",
            "summary-template.md",
            "template.html",
            "header.html",
            "navbar.html",
            "navbar-summary.html",
            "report.css",
            "hardhat.svg",
            "cancel.svg",
            "check.svg",
        ],
    },
)
