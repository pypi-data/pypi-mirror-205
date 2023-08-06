import os
import sys

from setuptools import setup, Extension

if sys.version_info < (3, 8):
    raise SystemError("This package is for Python 3.8 and above.")

here = os.path.dirname(__file__)

# Get the long description from the README file
with open(os.path.join(here, "README.markdown"), encoding="utf-8") as fp:
    long_description = fp.read()

setup_kwargs = {}

ext_files = [
    "src/mmapbitarray.c",
    "src/bloomfilter.c",
    "src/md5.c",
    "src/primetester.c",
    "src/MurmurHash3.c",
]

if os.name == "nt":
    ext_files.extend(
        [
            "src/win/io_win.c",
            "src/win/mman.c",
            # 'src/win/getopt.c',
        ]
    )

# Branch out based on `--cython` in `argv`. Specifying `--cython` will try to cythonize source whether
# Cython module is available or not (`force_cythonize`).
cythonize = True
force_cythonize = False

if "--cython" in sys.argv:
    force_cythonize = True
    sys.argv.remove("--cython")

# Always try to cythonize `pybloomer.pyx` if Cython is available
# or if `--cython` was passed
try:
    from Cython.Distutils import build_ext
except ModuleNotFoundError:
    if force_cythonize:
        print(
            "Cannot Cythonize: Cython module not found. "
            "Hint: to build pybloomfilter using the distributed "
            "source code, simply run 'python setup.py install'."
        )
        sys.exit(1)
    cythonize = False

if cythonize:
    ext_files.append("src/pybloomer.pyx")
    setup_kwargs["cmdclass"] = {"build_ext": build_ext}
else:
    # Use `pybloomfilter.c` distributed with the package.
    # Note that we let the exception bubble up if `pybloomfilter.c` doesn't exist.
    ext_files.append("src/pybloomer.c")

ext_modules = [Extension("pybloomer", ext_files)]

setup(
    name="pybloomer",
    version="0.6.0",
    author="Dr. Masroor Ehsan",
    author_email="masroore+pypi@gmail.com",
    url="https://github.com/masroore/pybloomer",
    description="A fast implementation of Bloom filter for Python built on mmap",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT License",
    test_suite="tests.test_all",
    ext_modules=ext_modules,
    python_requires=">=3.8, <4",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: C",
        "Programming Language :: Cython",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    **setup_kwargs
)
