"""Keep native framework routing aligned with the actual production entry point."""

import importlib
import json
import tomllib
from pathlib import Path

from fastapi import FastAPI


def test_native_vercel_entrypoint() -> None:
    root = Path(__file__).resolve().parents[2]
    config = json.loads((root / "vercel.json").read_text())
    project = tomllib.loads((root / "pyproject.toml").read_text())
    module_name, variable = project["tool"]["vercel"]["entrypoint"].split(":")
    assert config["framework"] == "fastapi"
    assert "rewrites" not in config
    assert "routes" not in config
    entrypoint = module_name.replace(".", "/") + ".py"
    function = config["functions"][entrypoint]
    assert (root / function["includeFiles"]).is_file()
    assert isinstance(getattr(importlib.import_module(module_name), variable), FastAPI)
