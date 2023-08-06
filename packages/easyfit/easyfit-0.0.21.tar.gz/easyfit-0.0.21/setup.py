from setuptools import setup, find_packages
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    author='Hisham Ali',
    author_email='hishamali98@gmail.com',
    description="Fit, Predict and Score many machine learning models with few lines of code and a single object",
    long_description= long_description,
    long_description_content_type='text/markdown',
    license='MIT License',
    name='easyfit',
    keywords=['EasyFit', 'easyfit', 'ezfit', 'EZfit'],
    # packages=find_packages('easyfit', 'easyfit.*'),
    packages=['easyfit'],
    version='0.0.21',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    setup_requires=['wheel'],
    install_requires=["scikit-learn", "pandas", "xgboost", "tqdm"]
)
