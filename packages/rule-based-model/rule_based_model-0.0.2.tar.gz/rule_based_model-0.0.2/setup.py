from setuptools import setup, find_packages

setup(
    name='rule_based_model',
    version='0.0.2',
    license="apache-2.0",
    author='Liang',
    author_email='liang@marketshriek.com',
    description='A rule based model to detect stock company name listed in oslo børs',
    url="https://github.com/Market-Shriek/rule-based-model",
    project_urls={
        "Repo": "https://github.com/Market-Shriek/rule-based-model",
        "Bug Tracker": "https://github.com/Market-Shriek/rule-based-model/issues",
    },
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    package_data={'rule_based_model': ['match_A.pkl', 'first_word.pkl', 'first_2word.pkl', 'first_3word.pkl']},
    python_requires=">=3.7",
    install_requires=[
       "pyahocorasick == 2.0.0"
    ]
)