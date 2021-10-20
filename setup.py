from setuptools import setup

setup(
    name='FXQuotationSpider',
    version='0.7',
    packages=['FXQuotationSpider'],
    url='',
    license='',
    author='SevenNi',
    author_email='',
    description='Easy API to get foreign exchange rate from Bank of China.',

    install_requires=['requests', 'scrapy', 'tqdm', 'prettytable', 'numpy', 'matplotlib', ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

)
