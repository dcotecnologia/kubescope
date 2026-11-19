import ast
from pathlib import Path

import kubescope.sdk as sdk

SDK = Path(sdk.__file__).parent


def test_the_sdk_imports_nothing_of_the_app() -> None:
    offenders: list[str] = []
    for path in SDK.glob("*.py"):
        for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
            if isinstance(node, ast.Import):
                modules = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom):
                modules = [node.module or ""]
            else:
                continue
            offenders += [
                f"{path.name}: {module}"
                for module in modules
                if module.split(".")[0] == "kubescope"
                and module.split(".")[:2] != ["kubescope", "sdk"]
            ]

    assert offenders == []


def test_every_name_the_sdk_exports_exists() -> None:
    assert all(hasattr(sdk, name) for name in sdk.__all__)
    assert sdk.API_VERSION == "0"
    assert set(sdk.EVENTS) == {
        sdk.CONTEXT_CHANGED,
        sdk.THEME_CHANGED,
        sdk.LANGUAGE_CHANGED,
        sdk.SHUTDOWN,
    }
