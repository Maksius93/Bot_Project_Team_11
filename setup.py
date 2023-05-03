from setuptools import setup, find_namespace_packages

setup(
    name='botik',
    version='0.1',
    author='TBG',
    author_email='TBG',
    description='Bot helper, add and save phone number, email, adress, date to birthday, sort some trash folder ',
    packages=find_namespace_packages(),
    entry_points = {'console_scripts': ['Hello = bot.src_with_classes:main']},
    install_requires=[
        'transliterate'
        
    ],
)