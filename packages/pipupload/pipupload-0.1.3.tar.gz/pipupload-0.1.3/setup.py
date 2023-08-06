# from distutils.core import  setup
# import setuptools
# packages = ['pipupload']# 唯一的包名，自己取名
# setup(name='pipupload',
# 	version='1.0',
# 	author='cl',
#     packages=packages,
#     package_dir={'requests': 'requests'},)


from setuptools import setup, find_packages

setup(
    name="pipupload",
    version="0.1.3",
    keywords=["pip", "pip_test", "python", "layUI"],
    description="pip_test",
    long_description="pipupload",
    license="MIT",
    url="https://github.com/MrClin/python_pip_install.git",
    author="cl",
    author_email="cl459134@163.com",

    # packages=find_packages(),  # 这个参数是导入目录下的所有__init__.py包
    packages=['pipupload'],
    # 这里一定一定要把自己的所有包放在setup。py文件的同级目录下，比如UIMonkey2077，不能写成['utils','services'....],这样会在site-package目录下生成分散的目录

    include_package_data=True,
    platforms="any",
    # install_requires=['uiautomator2', 'tornado'],
    python_requires='>=3.5',
    zip_safe=True,

    # 定义命令行窗口  启动模块的入口（把模块当成工具）
    # entry_points={
    #     'console_scripts': [
    #         'UIMonkey2077 = UIMonkey2077.__main__:main'
    #     ]
    # }
    )


