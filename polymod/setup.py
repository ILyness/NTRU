# Available at setup time due to pyproject.toml
from pybind11.setup_helpers import Pybind11Extension, build_ext
from setuptools import setup

__version__ = "1.0.0"

# Define the C++ extension
ext_modules = [
    Pybind11Extension(
        "polymod",                # The name of the module importable in Python
        ["src/polymod.cpp"],   # The source file
        define_macros=[("VERSION_INFO", __version__)],
    ),
]

setup(
    name="polymod",
    version=__version__,
    description="Convolution Polynomial Library designed to support necessary operations for the NTRU cryptosystem.",
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
    python_requires=">=3.12",
)
