from distutils.core import setup
import setuptools

packages = ['xincshi']  # 唯一的包名，自己取名, import 导入的名字
setup(name='xincshi-hello',  # name 是第三方库名， pip install 的名字
      version='3.0',   #版本号，
      author='xincshi',
      packages=packages,
      package_dir={'requests': 'requests'}, )