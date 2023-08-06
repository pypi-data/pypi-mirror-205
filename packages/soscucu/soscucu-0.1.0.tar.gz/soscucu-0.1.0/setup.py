from setuptools import setup, find_packages
import os
import shutil

# 이전 빌드 파일 삭제
dist_path = 'dist'
if os.path.exists(dist_path):
    shutil.rmtree(dist_path)
setup(
    name="soscucu",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    author="Choongin",
    author_email="choongin.lee@kaist.ac.kr",
    description="A simple greeting package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/greeting",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)