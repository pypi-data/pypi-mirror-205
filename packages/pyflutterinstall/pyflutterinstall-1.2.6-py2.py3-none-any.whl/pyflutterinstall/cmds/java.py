"""
Command stub for sdkmanager
"""

import os
import sys

from pyflutterinstall.config import config_load
from pyflutterinstall.trampoline import trampoline

JAVA_DIR = config_load().get("JAVA_DIR", None)

COMMAND = "java"


def find_default_path_or_none() -> str | None:
    """Find default path"""
    if JAVA_DIR is None:
        return None
    jdk_folders = os.listdir(JAVA_DIR)
    if not jdk_folders:
        return None
    if len(jdk_folders) > 1:
        jdk_folders.sort()
        jdk_folders.reverse()
    base_java_dir = os.path.join(JAVA_DIR, jdk_folders[0])
    if sys.platform == "darwin":
        java_bin = os.path.join(base_java_dir, "Contents", "Home", "bin")
    else:
        java_bin = os.path.join(base_java_dir, "bin")
    return java_bin


def main(argv: list[str] | None = None) -> int:
    """Main"""
    java_bin = trampoline(COMMAND, args=argv, default_path=find_default_path_or_none())
    assert os.path.exists(java_bin), f"java_bin {java_bin} does not exist"
    return 0


if __name__ == "__main__":
    sys.exit(main())
