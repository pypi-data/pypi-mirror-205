from setuptools import setup, find_packages

with open("./README.md", "r", encoding="utf-8") as e:
    long_description = e.read()

print(long_description)


setup(
    name='Routing_flet', 
    version='0.0.2',
    author='Dxsxsx',
    description='Enrutamiento y login requerido facil con flet',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Dxsxsx/Routing_flet',
    download_url='https://github.com/Dxsxsx/Routing_flet',
    requires=['flet'],
    project_urls = {
        "Bug Tracker":"https://github.com/Dxsxsx/Routing_flet/releases"
    },
    classifiers={
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    },
    package_dir={"":"src"},
    packages=find_packages(where='src'),
    python_requires=">=3.6",
)

""" 
py -m pip install --upgrade build
py -m build

py -m pip install --upgrade twine
py -m twine upload --repository pypi dist/*
 """