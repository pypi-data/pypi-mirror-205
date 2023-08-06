from setuptools import setup
import setuptools

setup(
    name='SqrtS',
    version='0.0.1',
    author='cemeye',
    author_email='caomingyang2022@163.com',
    url='https://pypi.org/project/SqrtS',
    description='python magic GUI package',
    # 需要打包的目录，只有这些目录才能 from import
    packages=setuptools.find_packages(),
    package_data={
        '': ['*.zip'],
        'bandwidth_reporter': ['*.zip']
    },
    # 安装此包时需要同时安装的依赖包
    install_requires=['pywin32', "pillow", "pyautogui", "pygame", "keyboard"],
)
