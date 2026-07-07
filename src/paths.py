"""
src.paths

Shared repository path utilities for the Scalable Platforms notebooks.

Every notebook should begin with:

    from src.paths import get_paths

    PATHS = get_paths("00_context")

which returns all commonly used repository directories and creates them
when necessary.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


# ---------------------------------------------------------------------
# Path container
# ---------------------------------------------------------------------

@dataclass(frozen=True)
class RepoPaths:
    """Repository directory structure."""

    repo: Path

    src: Path
    notebooks: Path
    figures: Path
    papers: Path

    results: Path
    notebook_results: Path

    site: Path
    reports: Path

    images: Path
    css: Path
    js: Path


# ---------------------------------------------------------------------
# Repository discovery
# ---------------------------------------------------------------------

def find_repo_root(start: Path | None = None) -> Path:
    """
    Locate the repository root.

    Works whether executed from:

        repo/
        repo/notebooks/
        repo/notebooks/tmp/
        Colab copies

    The repository root is identified by the presence of
    the src/ directory.
    """

    current = (start or Path.cwd()).resolve()

    for candidate in [current] + list(current.parents):
        if (candidate / "src").exists():
            return candidate

    raise RuntimeError(
        "Unable to locate repository root containing 'src/'."
    )


# ---------------------------------------------------------------------
# Build directory structure
# ---------------------------------------------------------------------

def get_paths(notebook: str = "00_context") -> RepoPaths:
    """
    Create and return repository paths.

    Parameters
    ----------
    notebook
        Notebook identifier, e.g.

            00_context
            07_optical_tweezer_scaling
            13_hyperfine_coherence
    """

    repo = find_repo_root()

    src = repo / "src"
    notebooks = repo / "notebooks"
    figures = repo / "figures"
    papers = repo / "papers"

    results = repo / "results"
    notebook_results = results / notebook

    site = repo / "site"
    reports = site / "reports"

    images = site / "images"
    css = site / "styles"
    js = site / "js"

    directories = [
        notebooks,
        figures,
        papers,
        results,
        notebook_results,
        site,
        reports,
        images,
        css,
        js,
    ]

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

    return RepoPaths(
        repo=repo,
        src=src,
        notebooks=notebooks,
        figures=figures,
        papers=papers,
        results=results,
        notebook_results=notebook_results,
        site=site,
        reports=reports,
        images=images,
        css=css,
        js=js,
    )


# ---------------------------------------------------------------------
# Convenience
# ---------------------------------------------------------------------

def print_paths(paths: RepoPaths) -> None:
    """Pretty-print repository paths."""

    print()

    print("Repository")
    print("----------")
    print(f"repo        : {paths.repo}")
    print(f"src         : {paths.src}")
    print(f"notebooks   : {paths.notebooks}")
    print(f"figures     : {paths.figures}")
    print(f"papers      : {paths.papers}")

    print()

    print("Results")
    print("-------")
    print(f"results     : {paths.results}")
    print(f"notebook    : {paths.notebook_results}")

    print()

    print("Website")
    print("-------")
    print(f"site        : {paths.site}")
    print(f"reports     : {paths.reports}")
    print(f"images      : {paths.images}")
    print(f"styles      : {paths.css}")
    print(f"javascript  : {paths.js}")

    print()


# ---------------------------------------------------------------------
# Typical notebook entry point
# ---------------------------------------------------------------------

if __name__ == "__main__":

    PATHS = get_paths("00_context")
    print_paths(PATHS)
