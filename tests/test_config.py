import os
import subprocess
import sys


def test_runtime_home_is_independent_from_package_installation(tmp_path):
    environment = os.environ.copy()
    environment["FLIGHTLAB_HOME"] = str(tmp_path)
    result = subprocess.run(
        [sys.executable, "-c", "from flightlab.config import ROOT; print(ROOT)"],
        env=environment,
        check=True,
        capture_output=True,
        text=True,
    )
    assert result.stdout.strip() == str(tmp_path.resolve())
