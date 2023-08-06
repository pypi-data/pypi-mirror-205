# -*- coding: utf-8 -*-
"""Utility to check soft dependency imports, and raise warnings or errors."""
import io
import sys
import warnings
from importlib import import_module
from inspect import isclass
from typing import List

from packaging.requirements import InvalidRequirement, Requirement
from packaging.specifiers import InvalidSpecifier, SpecifierSet

__author__: List[str] = ["fkiraly", "mloning"]


def _check_soft_dependencies(
    *packages,
    package_import_alias=None,
    severity="error",
    obj=None,
    suppress_import_stdout=False,
):
    """Check if required soft dependencies are installed and raise error or warning.

    Parameters
    ----------
    packages : str or list/tuple of str, or length-1-tuple containing list/tuple of str
        str should be package names and/or package version specifications to check.
        Each str must be a PEP 440 compatibe specifier string, for a single package.
        For instance, the PEP 440 compatible package name such as "pandas";
        or a package requirement specifier string such as "pandas>1.2.3".
        arg can be str, kwargs tuple, or tuple/list of str, following calls are valid:
        `_check_soft_dependencies("package1")`
        `_check_soft_dependencies("package1", "package2")`
        `_check_soft_dependencies(("package1", "package2"))`
        `_check_soft_dependencies(["package1", "package2"])`
    package_import_alias : dict with str keys and values, optional, default=empty
        key-value pairs are package name, import name
        import name is str used in python import, i.e., from import_name import ...
        should be provided if import name differs from package name
    severity : str, "error" (default), "warning", "none"
        behaviour for raising errors or warnings
        "error" - raises a `ModuleNotFoundException` if one of packages is not installed
        "warning" - raises a warning if one of packages is not installed
            function returns False if one of packages is not installed, otherwise True
        "none" - does not raise exception or warning
            function returns False if one of packages is not installed, otherwise True
    obj : python class, object, str, or None, default=None
        if self is passed here when _check_soft_dependencies is called within __init__,
        or a class is passed when it is called at the start of a single-class module,
        the error message is more informative and will refer to the class/object;
        if str is passed, will be used as name of the class/object or module
    suppress_import_stdout : bool, optional. Default=False
        whether to suppress stdout printout upon import.

    Raises
    ------
    ModuleNotFoundError
        error with informative message, asking to install required soft dependencies

    Returns
    -------
    boolean - whether all packages are installed, only if no exception is raised
    """
    if len(packages) == 1 and isinstance(packages[0], (tuple, list)):
        packages = packages[0]
    if not all(isinstance(x, str) for x in packages):
        raise TypeError("packages must be str or tuple of str")

    if package_import_alias is None:
        package_import_alias = {}
    msg = "package_import_alias must be a dict with str keys and values"
    if not isinstance(package_import_alias, dict):
        raise TypeError(msg)
    if not all(isinstance(x, str) for x in package_import_alias.keys()):
        raise TypeError(msg)
    if not all(isinstance(x, str) for x in package_import_alias.values()):
        raise TypeError(msg)

    if obj is None:
        class_name = "This functionality"
    elif not isclass(obj):
        class_name = type(obj).__name__
    elif isclass(obj):
        class_name = obj.__name__
    elif isinstance(obj, str):
        class_name = obj
    else:
        raise TypeError("obj must be a class, an object, a str, or None")

    for package in packages:
        try:
            req = Requirement(package)
        except InvalidRequirement:
            msg_version = (
                f"wrong format for package requirement string, "
                f'must be PEP 440 compatible requirement string, e.g., "pandas"'
                f' or "pandas>1.1", but found {package!r}'
            )
            raise InvalidRequirement(msg_version) from None

        package_name = req.name
        package_version_req = req.specifier

        # determine the package import
        if package_name in package_import_alias.keys():
            package_import_name = package_import_alias[package_name]
        else:
            package_import_name = package_name
        # attempt import - if not possible, we know we need to raise warning/exception
        try:
            if suppress_import_stdout:
                # setup text trap, import, then restore
                sys.stdout = io.StringIO()
                pkg_ref = import_module(package_import_name)
                sys.stdout = sys.__stdout__
            else:
                pkg_ref = import_module(package_import_name)
        # if package cannot be imported, make the user aware of installation requirement
        except ModuleNotFoundError as e:
            msg = (
                f"{e}. "
                f"{class_name} requires package {package!r} to be present "
                f"in the python environment, but {package!r} was not found. "
            )
            if obj is not None:
                msg = msg + (
                    f"{package!r} is a dependency of {class_name} and required "
                    f"to construct it. "
                )
            msg = msg + (
                f"Please run: `pip install {package}` to "
                f"install the {package} package. "
            )

            if severity == "error":
                raise ModuleNotFoundError(msg) from e
            elif severity == "warning":
                warnings.warn(msg, stacklevel=2)
                return False
            elif severity == "none":
                return False
            else:
                raise RuntimeError(
                    "Error in calling _check_soft_dependencies, severity "
                    'argument must be "error", "warning", or "none",'
                    f"found {severity!r}."
                ) from e

        # now we check compatibility with the version specifier if non-empty
        if package_version_req != SpecifierSet(""):
            pkg_env_version = pkg_ref.__version__

            msg = (
                f"{class_name} requires package {package!r} to be present "
                f"in the python environment, with version {package_version_req}, "
                f"but incompatible version {pkg_env_version} was found. "
            )
            if obj is not None:
                msg = msg + (
                    f"{package!r}, with version {package_version_req},"
                    f"is a dependency of {class_name} and required to construct it. "
                )

            # raise error/warning or return False if version is incompatible
            if pkg_env_version not in package_version_req:
                if severity == "error":
                    raise ModuleNotFoundError(msg)
                elif severity == "warning":
                    warnings.warn(msg, stacklevel=2)
                elif severity == "none":
                    return False
                else:
                    raise RuntimeError(
                        "Error in calling _check_soft_dependencies, severity argument"
                        f' must be "error", "warning", or "none", found {severity!r}.'
                    )

    # if package can be imported and no version issue was caught for any string,
    # then obj is compatible with the requirements and we should return True
    return True


def _check_python_version(obj, package=None, msg=None, severity="error"):
    """Check if system python version is compatible with requirements of obj.

    Parameters
    ----------
    obj : BaseObject descendant
        used to check python version
    package : str, default = None
        if given, will be used in error message as package name
    msg : str, optional, default = default message (msg below)
        error message to be returned in the `ModuleNotFoundError`, overrides default
    severity : str, "error" (default), "warning", or "none"
        whether the check should raise an error, a warning, or nothing

    Returns
    -------
    compatible : bool, whether obj is compatible with system python version
        check is using the python_version tag of obj

    Raises
    ------
    ModuleNotFoundError
        User friendly error if obj has python_version tag that is
        incompatible with the system python version. If package is given,
        error message gives package as the reason for incompatibility.
    """
    est_specifier_tag = obj.get_class_tag("python_version", tag_value_default="None")
    if est_specifier_tag in ["None", None]:
        return True

    try:
        est_specifier = SpecifierSet(est_specifier_tag)
    except InvalidSpecifier:
        msg_version = (
            f"wrong format for python_version tag, "
            f'must be PEP 440 compatible specifier string, e.g., "<3.9, >= 3.6.3",'
            f" but found {est_specifier_tag!r}"
        )
        raise InvalidSpecifier(msg_version) from None

    # python sys version, e.g., "3.8.12"
    sys_version = sys.version.split(" ")[0]

    if sys_version in est_specifier:
        return True
    # now we know that est_version is not compatible with sys_version

    if not isinstance(msg, str):
        msg = (
            f"{type(obj).__name__} requires python version to be {est_specifier},"
            f" but system python version is {sys.version}."
        )

        if package is not None:
            msg += (
                f" This is due to python version requirements of the {package} package."
            )

    if severity == "error":
        raise ModuleNotFoundError(msg)
    elif severity == "warning":
        warnings.warn(msg, stacklevel=2)
    elif severity == "none":
        return False
    else:
        raise RuntimeError(
            "Error in calling _check_python_version, severity "
            f'argument must be "error", "warning", or "none", found {severity!r}.'
        )
    return True
