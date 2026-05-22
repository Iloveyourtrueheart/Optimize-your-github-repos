"""
GitHub 项目优化器
一键优化你的 GitHub 项目（代码 + README）
"""

from setuptools import setup, find_packages

setup(
    name="github-optimizer",
    version="1.0.0",
    description="GitHub 项目优化器 - 一键优化你的 GitHub 项目（代码 + README）",
    long_description=open("README.md", "r", encoding="utf-8").read() if __import__("os").path.exists("README.md") else "",
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/YOUR_USERNAME/github-optimizer",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "anthropic>=0.18.0",
        "PyGithub>=2.1.1",
        "GitPython>=3.1.40",
        "click>=8.1.0",
        "tqdm>=4.66.0",
        "python-dotenv>=1.0.0",
    ],
    entry_points={
        "console_scripts": [
            "github-optimize=cli:cli",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="github, optimizer, readme, claude, ai",
    project_urls={
        "Bug Reports": "https://github.com/YOUR_USERNAME/github-optimizer/issues",
        "Source": "https://github.com/YOUR_USERNAME/github-optimizer",
    },
)
