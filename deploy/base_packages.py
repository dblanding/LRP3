from pyinfra.operations import apt

base_packages = apt.packages(
    name="Install python pip and i2c tools",
    packages=["python3-pip", "python3-smbus", "i2c-tools", "python3-ujson", "python3-numpy"],
    _sudo=True,
    )
