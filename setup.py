import os
import textwrap

from setuptools import setup

BUILD_RUST_EXTENSION = bool(os.environ.get("UNBLOB_BUILD_RUST_EXTENSION", False))
RUST_DEBUG = bool(os.environ.get("UNBLOB_RUST_DEBUG", False))

setuptools_kwargs = {}

if BUILD_RUST_EXTENSION:
    try:
        from setuptools_rust import Binding, RustExtension

        python_version = "38"

        setuptools_kwargs.update(
            dict(
                rust_extensions=[
                    RustExtension(
                        target="unblob._rust",
                        debug=RUST_DEBUG,
                        path="rust/Cargo.toml",
                        binding=Binding.PyO3,
                        py_limited_api=True,
                        features=[
                            f"pyo3/abi3-py{python_version}",
                            "pyo3/extension-module",
                        ],
                    )
                ],
                options={
                    "bdist_wheel": {"py_limited_api": f"cp{python_version}"},
                },
            )
        )
    except ModuleNotFoundError:
        print(
            textwrap.dedent(
                """
                    ####################### WARNING ######################
                    Required dependency, setuptools-rust cannot be found.
                    It can be installed by issuing =poetry install= first.
                    ####################### WARNING ######################
                    """
            )
        )
        raise

setup(**setuptools_kwargs)
