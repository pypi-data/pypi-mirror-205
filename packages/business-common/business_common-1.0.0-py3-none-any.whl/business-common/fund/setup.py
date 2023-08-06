from setuptools import setup, find_packages

setup(
    name='business-common',
    version='1.0.0',
    description='fund evaluation description',
    author='刘殿欢乐',
    author_email='liudhl@investoday.com.cn',
    url= 'http://192.168.14.111/investoday-open/pypi/business-common',
    packages=['business-common/fund'], # 要打包的项目文件夹
    include_package_data=True, # 自动打包文件夹内所有数据
    install_requires=[
        'numpy',
        'pandas',
        'pyhdfs',
        'pymssql',
        'datetime',
        'sqlalchemy',
    ]
)