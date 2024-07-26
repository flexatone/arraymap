import setuptools
import typing as tp
import site
import os


AM_VERSION = "0.3.0"

# with open("README.rst") as file:
#     LONG_DESCRIPTION = file.read()


def get_ext_dir(*components: tp.Iterable[str]) -> tp.Sequence[str]:
    dirs = []
    for sp in site.getsitepackages():
        fp = os.path.join(sp, *components)
        if os.path.exists(fp):
            dirs.append(fp)
    return dirs


extension = setuptools.Extension(
    "arraymap",
    ["arraymap.c"],
    include_dirs=get_ext_dir("numpy", "_core", "include"),
    library_dirs=get_ext_dir("numpy", "_core", "lib"),
    define_macros=[("AM_VERSION", AM_VERSION)],
    libraries=["npymath"],
)

setuptools.setup(
    # name="arraymap",
    # version=AM_VERSION,
    # description="Dictionary-like lookup from NumPy array values to their integer positions",
    # long_description=LONG_DESCRIPTION,
    # python_requires=">=3.9",
    # install_requires=["numpy>=1.19.5"],
    # url="https://github.com/static-frame/arraymap",
    # author="Christopher Ariza, Brandt Bucher",
    # license="MIT",
    # classifiers=[
    #     "Development Status :: 5 - Production/Stable",
    #     "Intended Audience :: Developers",
    #     "Topic :: Software Development",
    #     "License :: OSI Approved :: MIT License",
    #     "Operating System :: MacOS :: MacOS X",
    #     "Operating System :: Microsoft :: Windows",
    #     "Operating System :: POSIX",
    #     "Programming Language :: Python :: 3.9",
    #     "Programming Language :: Python :: 3.10",
    #     "Programming Language :: Python :: 3.11",
    #     "Programming Language :: Python :: 3.12",
    # ],
    ext_modules=[extension],
)
