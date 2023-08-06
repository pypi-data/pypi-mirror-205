from setuptools import find_packages, setup

setup(
    name='netbox-subnet-allocator',
    version='0.2',
    description='A NetBox plugin for managing the allocation of subnets',
    install_requires=[],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)

