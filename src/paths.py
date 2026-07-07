"""
src.paths

Shared repository path utilities for the Scalable Platforms notebooks.

Typical usage
-------------
from src.paths import get_paths

PATHS = get_paths("00_context")

print(PATHS.repo_name)
print(PATHS.figures)
print(PATHS.figures_results)
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


# ============================================================================
# Repository path container
# ============================================================================

@dataclass(frozen=True)
class RepoPaths:
    """Repository directory structure."""

    # Repository root
    repo: Path

    # Source
    src: Path

    # Repository folders
    notebooks: Path
    figures: Path
    papers: Path

    # Results
    results: Path
    notebook_results: Path
    figures_results: Path

    # Website
    site: Path
    reports: Path
    images: Path
    css: Path
    js: Path

    # ------------------------------------------------------------------
    # Convenience properties
    # ------------------------------------------------------------------

    @property
    def repo_name(self) -> str:
        """Repository name."""
        return self.repo.name

    @property
    def readme(self) -> Path:
        return self.repo / "README.md"

    @property
    def requirements(self) -> Path:
        return self.repo / "requirements.txt"

    @property
    def license(self) -> Path:
        return self.repo / "LICENSE"

    @property
    def gitignore(self) -> Path:
        return self.repo / ".gitignore"


# ============================================================================
# Repository discovery
# ============================================================================

def find_repo_root(start: Path | None = None) -> Path:
    """
    Locate the repository root.

    Searches upward until a directory containing ``src/`` is found.

    Works whether executed from

        repo/
        repo/notebooks/
        repo/notebooks/tmp/
        repo/results/
        Google Colab copies
    """

    current = (start or Path.cwd()).resolve()

    for candidate in [current] + list(current.parents):
        if (candidate / "src").exists():
            return candidate

    raise RuntimeError(
        "Unable to locate repository root. "
        "Expected to find a directory containing 'src/'."
    )


# ============================================================================
# Build directory structure
# ============================================================================

def get_paths(notebook: str = "00_context") -> RepoPaths:
    """
    Return repository paths and create directories if necessary.

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
    figures_results = notebook_results / "figures"

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
        figures_results,
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
        figures_results=figures_results,
        site=site,
        reports=reports,
        images=images,
        css=css,
        js=js,
    )


# ============================================================================
# Pretty printing
# ============================================================================

def print_paths(paths: RepoPaths) -> None:
    """Print repository paths."""

    print("\nRepository")
    print("-" * 60)
    print(f"repo              : {paths.repo}")
    print(f"repo_name         : {paths.repo_name}")

    print("\nSource")
    print("-" * 60)
    print(f"src               : {paths.src}")

    print("\nRepository folders")
    print("-" * 60)
    print(f"notebooks         : {paths.notebooks}")
    print(f"figures           : {paths.figures}")
    print(f"papers            : {paths.papers}")

    print("\nResults")
    print("-" * 60)
    print(f"results           : {paths.results}")
    print(f"notebook_results  : {paths.notebook_results}")
    print(f"figures_results   : {paths.figures_results}")

    print("\nWebsite")
    print("-" * 60)
    print(f"site              : {paths.site}")
    print(f"reports           : {paths.reports}")
    print(f"images            : {paths.images}")
    print(f"styles            : {paths.css}")
    print(f"javascript        : {paths.js}")

    print("\nProject files")
    print("-" * 60)
    print(f"README            : {paths.readme}")
    print(f"requirements      : {paths.requirements}")
    print(f"LICENSE           : {paths.license}")
    print(f".gitignore        : {paths.gitignore}")

    print()


# ============================================================================
# Example
# ============================================================================

if __name__ == "__main__":

    PATHS = get_paths("00_context")

    print_paths(PATHS)
