"""A setuptools based setup module.
See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
 
    name="TsProject",  # Required 项目名称
    version="1.0.0",  # Required 发布版本号
    description="TsProject Init: File POST to Cloud",  # Optional 项目简单描述
    long_description=long_description,  # Optional 详细描述
    long_description_content_type="text/markdown",  # 内容类型
    url="https://www.tsginkgo.cn/about",  # Optional github项目地址
    author="Kqy",  # Optional 作者
    author_email="2765301200@qq.com",  # Optional 作者邮箱
    classifiers=[  # Optional 分类器通过对项目进行分类来帮助用户找到项目, 以下除了python版本其他的 不需要改动
     
        "Development Status :: 3 - Alpha", 
        # Indicate who your project is intended for
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        # Pick your license as you wish
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
    ],
   
    keywords="Tsginkgo, Ksuser, Kqy",  # Optional 搜索关键字
 
    
    packages=find_packages(),  # Required
   
    python_requires=">=3.7, <4",  # python 版本要求
 
    install_requires=["requests"],  # Optional 第三方依赖库
   
    project_urls={  # Optional 和项目相关的 其他网页连接资源
        "Bug Reports": "https://www.tsginkgo.cn",
        "Funding": "https://www.tsginkgo.cn",
        "Say Thanks!": "https://www.tsginkgo.cn",
        "Source": "https://www.tsginkgo.cn/about",
    },
)