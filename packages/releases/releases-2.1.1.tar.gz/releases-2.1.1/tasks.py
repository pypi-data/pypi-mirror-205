from os.path import join

from invocations import docs, checks, ci
from invocations.pytest import test, integration, coverage
from invocations.packaging import release

from invoke import Collection


ns = Collection(test, integration, coverage, release, docs, ci, checks.blacken)
ns.configure(
    {
        "packaging": {
            "sign": True,
            "wheel": True,
            "changelog_file": join(
                docs.ns.configuration()["sphinx"]["source"], "changelog.rst"
            ),
        },
    }
)
