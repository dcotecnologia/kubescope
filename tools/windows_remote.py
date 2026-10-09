"""Build the Windows packages on GitHub Actions and download them to dist/.

Needs the GitHub CLI (`gh`) logged in, and .github/workflows/release.yml
pushed. Usage: python tools/windows_remote.py [branch]   (default:
current branch)
"""

import json
import shutil
import subprocess
import sys
import time
from datetime import UTC, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = "release.yml"
ARTIFACT = "windows-packages"


def gh(*arguments: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["gh", *arguments], cwd=ROOT, check=check, capture_output=True, text=True
    )


def current_branch() -> str:
    result = subprocess.run(
        ["git", "branch", "--show-current"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip() or "main"


def find_run(branch: str, started: datetime) -> int:
    """The dispatched run appears a few seconds after the request."""
    deadline = time.monotonic() + 90
    while time.monotonic() < deadline:
        listing = gh(
            "run", "list", "--workflow", WORKFLOW, "--event", "workflow_dispatch",
            "--branch", branch, "--limit", "10", "--json", "databaseId,createdAt",
        )  # fmt: skip
        for run in json.loads(listing.stdout):
            created = datetime.fromisoformat(run["createdAt"].replace("Z", "+00:00"))
            if created >= started:
                return run["databaseId"]
        time.sleep(4)
    raise SystemExit("The workflow run did not show up; check the Actions tab")


def main() -> int:
    if shutil.which("gh") is None:
        raise SystemExit(
            "Install the GitHub CLI (https://cli.github.com) and run `gh auth login`"
        )
    branch = sys.argv[1] if len(sys.argv) > 1 else current_branch()

    if gh("workflow", "view", WORKFLOW, "--ref", branch, check=False).returncode != 0:
        raise SystemExit(
            f".github/workflows/{WORKFLOW} was not found on '{branch}' in GitHub.\n"
            "Commit and push the workflow first, then run this again."
        )

    started = datetime.now(UTC) - timedelta(seconds=5)
    print(f"Starting the Windows build on '{branch}'...")
    gh("workflow", "run", WORKFLOW, "--ref", branch, "-f", "target=windows")
    run_id = find_run(branch, started)
    print(f"Run {run_id}: https://github.com/{repository()}/actions/runs/{run_id}")

    watched = subprocess.run(
        ["gh", "run", "watch", str(run_id), "--exit-status"], cwd=ROOT, check=False
    )
    if watched.returncode != 0:
        raise SystemExit(
            "The Windows build failed; open the run link above for the log"
        )

    (ROOT / "dist").mkdir(exist_ok=True)
    gh("run", "download", str(run_id), "-n", ARTIFACT, "-D", str(ROOT / "dist"))
    for path in sorted((ROOT / "dist").glob("*windows*")):
        print(f"Downloaded {path} ({path.stat().st_size / 2**20:.0f} MiB)")
    return 0


def repository() -> str:
    result = gh("repo", "view", "--json", "nameWithOwner", "-q", ".nameWithOwner")
    return result.stdout.strip()


if __name__ == "__main__":
    raise SystemExit(main())
