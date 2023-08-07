import sys

from setuptools import setup

platform = {"darwin": "mac", "win32": "win"}.get(sys.platform, "unix")


setup(
    name=f"libtukaan-{platform}",
    version="0.1.4",
    license="MIT",
    author="rdbende",
    author_email="rdbende@proton.me",
    description="Binary extensions for Tukaan",
    url="https://tukaan.github.io",
    project_urls={
        "Source": "https://github.com/tukaan/libtukaan",
        "Documentation": "https://tukaan.github.io/docs",
        "Tracker": "https://github.com/tukaan/libtukaan/issues",
    },
    python_requires=">=3.7",
    packages=["libtukaan"],
    package_data={"libtukaan": [f"{platform}/*.*"]},
)
