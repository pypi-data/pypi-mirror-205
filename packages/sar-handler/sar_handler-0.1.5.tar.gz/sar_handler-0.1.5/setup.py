from setuptools import find_packages, setup
from pathlib import Path


this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='sar_handler',
    packages=find_packages(include=['sar_handler']),
    version='0.1.5',
    description='Handler SAR images',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Felecort',
    # author_email="@gmail.com",
    url="https://github.com/Felecort/SAR_Handler",
    license='MIT',
    install_requires=["numpy",
                      "Pillow",
                      "scipy",
                      "tqdm",
                      "torch",
                      ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests',
)
