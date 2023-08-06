import sys
from subprocess import call
from subprocess import check_output

import pdm_bump
import pdoc
from acb.actions import dump
from acb.actions import load
from addict import Dict as adict
from aiopath import AsyncPath
from pydantic import BaseModel

for mod in (pdm_bump, pdoc):
    pass


# Crackerjack


class Crakerjack(BaseModel):
    path: AsyncPath = AsyncPath(".")
    pkg_path: AsyncPath = AsyncPath.cwd()
    pkg_name: str = "crackerjack"

    async def update_pkg_configs(self) -> None:
        poetry_pip_env = False
        # root_files = [file async for file in self.pkg_path.iterdir() if (
        #     "poetry" or "Pip") in file.name]
        # if len(root_files):
        #     poetry_pip_env = True
        #     for file in root_files:
        #         await file.unlink()
        for config in (".gitignore", ".pre-commit-config.yaml", ".libcst.codemod.yaml"):
            config_path = self.path / config
            config_pkg_path = self.pkg_path / config
            # if poetry_pip_env:
            #     await config_pkg_path.unlink()
            config_text = await config_path.read_text()
            await config_pkg_path.write_text(
                config_text.replace("crackerjack", self.pkg_name)
            )
        toml_file = "pyproject.toml"
        toml_path = self.path / toml_file
        pkg_toml_path = self.pkg_path / toml_file
        if not await pkg_toml_path.exists():
            call(["pdm", "init"])
        installed_pkgs = check_output(
            ["pdm", "list", "--freeze"],
            universal_newlines=True,
        ).splitlines()
        if not len([pkg for pkg in installed_pkgs if "pre-commit" in pkg]):
            call(["pdm", "add", "-d", "pre_commit"])
            call(["pre-commit", "install"])
        toml = await load.toml(toml_path)
        pkg_toml = await load.toml(pkg_toml_path)
        if poetry_pip_env:
            del pkg_toml.tool.poetry
        pkg_toml.tool = toml.tool
        await dump.toml(pkg_toml, pkg_toml_path)

    async def process(
        self,
        options: adict[str, str | bool],
    ) -> None:
        imp_dir = self.pkg_path / "__pypackages__"
        sys.path.append(str(imp_dir))
        self.pkg_name = self.pkg_path.stem.lower()
        print("\nCrackerjacking...\n")
        await self.update_pkg_configs()
        try:
            call(["pre-commit", "run", "--all-files"])
        except Exception as err:
            raise err
        if options.publish:
            call(["pdm", "bump", options.publish])
            call(["pdm", "publish"])


crackerjack_it = Crakerjack().process
