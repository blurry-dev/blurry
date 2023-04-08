import nox


@nox.session(python=["3.11", "3.10"])
def tests(session):
    session.install("pytest", ".")
    session.run("pytest")


@nox.session(python=["3.11", "3.10"])
def lint(session):
    session.install("flake8", ".")
    session.run("flake8", "blurry", "tests")


@nox.session(python=["3.11", "3.10"])
def typecheck(session):
    session.install("pyright", ".")
    session.run("pyright")
