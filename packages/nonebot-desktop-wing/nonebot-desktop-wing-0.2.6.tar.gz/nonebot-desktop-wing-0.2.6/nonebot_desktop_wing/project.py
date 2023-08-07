from __future__ import annotations
import asyncio
from pathlib import Path
import sys
from typing import (
    TYPE_CHECKING, Iterable, List, Literal, Optional, Tuple, Union, overload
)

from dotenv.main import DotEnv

from nonebot_desktop_wing.constants import WINDOWS
from nonebot_desktop_wing.lazylib import nb_cli
from nonebot_desktop_wing.molecules import perform_pip_install

if TYPE_CHECKING:
    from importlib.metadata import Distribution
    from nb_cli.config import Driver, Adapter, ConfigManager
    from subprocess import Popen


def find_python(fp: Union[str, Path]) -> str:
    """Find a python executable in a directory."""
    pfp = Path(fp)
    veexec = (
        pfp / ".venv"
        / ("Scripts" if WINDOWS else "bin")
        / ("python.exe" if WINDOWS else "python")
    )
    return str(veexec) if veexec.exists() else sys.executable


def distributions(*fp: str) -> Iterable[Distribution]:
    from importlib import metadata
    if fp:
        return metadata.distributions(path=list(fp))
    return metadata.distributions()


def getdist(root: Union[str, Path]) -> Iterable[Distribution]:
    """Get packages installed in a directory."""
    return (
        distributions(
            *(str(si) for si in Path(root).glob(".venv/**/site-packages"))
        )
    )


@overload
def create(
    fp: str,
    drivers: List[Driver],
    adapters: List[Adapter],
    dev: bool,
    usevenv: bool,
    index: Optional[str] = None,
    new_win: Literal[False] = False,
    catch_output: bool = False
) -> Popen[bytes]:
    ...


@overload
def create(
    fp: str,
    drivers: List[Driver],
    adapters: List[Adapter],
    dev: bool,
    usevenv: bool,
    index: Optional[str] = None,
    new_win: Literal[True] = True
) -> Tuple[Popen[bytes], str]:
    ...


def create(
    fp: str,
    drivers: List[Driver],
    adapters: List[Adapter],
    dev: bool,
    usevenv: bool,
    index: Optional[str] = None,
    new_win: bool = False,
    catch_output: bool = False
) -> Union[Popen[bytes], Tuple[Popen[bytes], str]]:
    """
    Create a new NoneBot project.

    - fp: `str`                 - path to target project (must be empty or not
                                  exist)
    - drivers: `List[Driver]`   - drivers to be installed.
    - adapters: `List[Adapter]` - adapters to be installed.
    - dev: `bool`               - whether to use a profile for developing
                                  plugins.
    - usevenv: `bool`           - whether to create a virtual environment.
    - index: `Optional[str]`    - index url for downloading packages.
    - new_win: `bool`           - whether to create a new window.
    - catch_output: `bool`      - whether to catch output stdout and stderr.

    - return:                   - the process running commands (and temp
                                  script path if `new_win` is set `True`).
        - `Popen[bytes] if new_win == False`
        - `(Popen[bytes], str) if new_win == True`
    """
    p = Path(fp)
    if p.exists():
        p.rmdir()
    nb_cli.handlers.create_project(
        "simple" if dev else "bootstrap",
        {
            "nonebot": {
                "project_name": p.name,
                "drivers": [d.dict() for d in drivers],
                "adapters": [a.dict() for a in adapters],
                "use_src": True
            }
        },
        str(p.parent)
    )
    dri_real = [d.project_link for d in drivers]
    adp_real = [a.project_link for a in adapters]
    dir_name = p.name.replace(" ", "-")
    venv_dir = p / ".venv"

    if usevenv:
        from venv import create as create_venv
        create_venv(venv_dir, prompt=dir_name, with_pip=True)

    pyexec = find_python(p)

    return perform_pip_install(
        pyexec, "nonebot2", *dri_real, *adp_real,
        index=index or "",
        new_win=new_win,  # type: ignore
        catch_output=catch_output
    )


def get_builtin_plugins(pypath: str) -> List[str]:
    """Get built-in plugins, using python in an environment."""
    return asyncio.run(
        nb_cli.handlers.list_builtin_plugins(python_path=pypath)
    )


def find_env_file(fp: Union[str, Path]) -> List[str]:
    """Find all dotenv files in a directory."""
    return [p.name for p in Path(fp).glob(".env*")]


def get_env_config(ep: Union[str, Path], config: str) -> Optional[str]:
    return DotEnv(ep).get(config)


def recursive_find_env_config(
    fp: Union[str, Path], config: str
) -> Optional[str]:
    """
    Recursively find a config in dotenv files.

    - fp: `Union[str, Path]`    - project directory.
    - config: `str`             - config string.

    - return: `Optional[str]`   - value of the config.
    """
    pfp = Path(fp)
    cp = pfp / ".env"
    if not cp.is_file():
        # Default profile is 'prod' if main profile does not exist.
        return get_env_config(pfp / ".env.prod", config)
    # Use main profile.
    glb = DotEnv(cp).dict()
    if config in glb:
        # Config in main profile.
        return glb[config]
    env = glb.get("ENVIRONMENT", None)  # Get specified profile.
    return env and get_env_config(pfp / f".env.{env}", config)


def recursive_update_env_config(
    fp: Union[str, Path], config: str, value: str
) -> None:
    """
    Recursively edit a config in dotenv files.

    - fp: `Union[str, Path]`    - project directory.
    - config: `str`             - config string.
    - value: `str`              - new value of the config.
    """
    pfp = Path(fp)
    cp = pfp / ".env"
    if not cp.is_file():
        # Default profile is 'prod' if main profile does not exist.
        cp = pfp / ".env.prod"
        useenv = DotEnv(cp).dict()
    else:
        # Use main profile.
        useenv = DotEnv(cp).dict()
        if config not in useenv:
            env = get_env_config(cp, "ENVIRONMENT")
            if env:
                # Specified profile is usable.
                cenv = DotEnv(pfp / f".env.{env}").dict()
                if config in cenv:
                    cp = pfp / f".env.{env}"
                    useenv = cenv

    useenv.update({config: value})

    with open(cp, "w") as f:
        f.writelines(f"{k}={v}\n" for k, v in useenv.items() if k and v)


def get_toml_config(basedir: Union[str, Path]) -> ConfigManager:
    """Get project TOML manager for a project."""
    basepath = Path(basedir)
    return nb_cli.config.ConfigManager(find_python(basepath), basepath / "pyproject.toml")