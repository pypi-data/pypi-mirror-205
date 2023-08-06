from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'

PACKAGE_NAME = "pytorchgan"
DESCRIPTION = 'PytorchGAN是一个基于Pytorch框架的生成对抗网络（GAN）实现库。'
LONG_DESCRIPTION = 'PytorchGAN是一个基于Pytorch框架的生成对抗网络（GAN）实现库。GAN是一种用于生成模型的机器学习算法，其通过训练生成器和鉴别器来生成新的数据样本。PytorchGAN提供了许多经典的GAN模型实现，如DCGAN，WGAN，CGAN，CycleGAN等。PytorchGAN的主要优点之一是其使用Pytorch框架。Pytorch是一种动态图形框架，具有易于使用和调试的优点，同时也具有高度灵活性和可扩展性。因此，使用PytorchGAN可以更轻松地构建和训练GAN模型，并且可以利用Pytorch的自动微分功能来优化模型参数。'
AUTHOR_NAME = "Xuehang Cang"
AUTHOR_EMAIL = "xuehangcang@outlook.com"
PROJECT_URL = "https://github.com/xuehangcang/pytorchgan"
REQUIRED_PACKAGES = ["torch", "torchaudio", "torchaudio"]  # 第三方工具
PROJECT_KEYWORDS = ['pypi', 'python', 'Pytorch', 'GAN']  # 关键字

# 阅读更多关于分类器的信息  https://pypi.org/classifiers/
CLASSIFIERS = [
    "Programming Language :: Python :: 3",
    "Operating System :: Unix",
    "Operating System :: MacOS :: MacOS X",
    "Operating System :: Microsoft :: Windows"]

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    author=AUTHOR_NAME,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    url=PROJECT_URL,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=REQUIRED_PACKAGES,
    keywords=PROJECT_KEYWORDS,
    classifiers=CLASSIFIERS
)
