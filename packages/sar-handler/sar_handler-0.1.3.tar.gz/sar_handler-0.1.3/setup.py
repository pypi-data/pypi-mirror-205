from setuptools import find_packages, setup

setup(
    name='sar_handler',
    packages=find_packages(include=['sar_handler']),
    version='0.1.3',
    description='Handler SAR images',
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
