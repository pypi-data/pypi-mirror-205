from setuptools import setup, find_packages

setup(
    name = 'autoLinker',
    version = '1.0.1',
    keywords='',
    description = 'A quick Linker',
    license = 'MIT License',
    author = 'lin_zhe',
    author_email = 'mcwyzlele@163.com',
    packages = find_packages(),
    include_package_data = True,
    platforms = 'any',
    install_requires = [
        'pyautogui','keyboard'
    ],
)