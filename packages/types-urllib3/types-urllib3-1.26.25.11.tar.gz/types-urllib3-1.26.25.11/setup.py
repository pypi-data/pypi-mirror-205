from setuptools import setup

name = "types-urllib3"
description = "Typing stubs for urllib3"
long_description = '''
## Typing stubs for urllib3

This is a PEP 561 type stub package for the `urllib3` package. It
can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`urllib3`. The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/urllib3. All fixes for
types and metadata should be contributed there.

*Note:* The `urllib3` package includes type annotations or type stubs
since version 2.0.0. Please uninstall the `types-urllib3`
package if you use this or a newer version.


See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `2dd268d74aaebe4819f55ecb13c03e352bad13a4`.
'''.lstrip()

setup(name=name,
      version="1.26.25.11",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/urllib3.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['urllib3-stubs'],
      package_data={'urllib3-stubs': ['__init__.pyi', '_collections.pyi', 'connection.pyi', 'connectionpool.pyi', 'contrib/__init__.pyi', 'contrib/socks.pyi', 'exceptions.pyi', 'fields.pyi', 'filepost.pyi', 'packages/__init__.pyi', 'packages/ssl_match_hostname/__init__.pyi', 'packages/ssl_match_hostname/_implementation.pyi', 'poolmanager.pyi', 'request.pyi', 'response.pyi', 'util/__init__.pyi', 'util/connection.pyi', 'util/queue.pyi', 'util/request.pyi', 'util/response.pyi', 'util/retry.pyi', 'util/ssl_.pyi', 'util/timeout.pyi', 'util/url.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
