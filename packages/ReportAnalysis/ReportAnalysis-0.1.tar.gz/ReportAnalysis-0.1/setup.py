from setuptools import setup, find_packages

setup(
    name='ReportAnalysis',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'nltk',
    ],
    entry_points={
        'console_scripts': [
            'report_analysis = report_analysis.analyzer:analyze_report'
        ]
    },
    author='Al Mustafiz Bappy',
    author_email='almustafizbappy@gmail.com',
    description='A package for analyzing reports using NLTK',
    keywords='nltk report analysis',
    url='https://github.com/bappy-3/ReportAnalysis'
)
