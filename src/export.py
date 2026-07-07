"""
src.export

Minimal export helpers for notebook-generated PNGs and artifact ZIPs.

Typical usage
-------------
from src.paths import get_paths
from src.export import save_png, package_artifacts

PATHS = get_paths("00_context")

save_png(fig, "00_specification_chain", PATHS)

zip_path = package_artifacts(
    PATHS,
    notebook_name="00_context",
)
"""

from __future__ import annotations

from pathlib import Path
from shutil import copy2
from zipfile import ZIP_DEFLATED, ZipFile


# ============================================================================
# Figure export
# ============================================================================

def save_png(
    fig,
    name: str,
    paths,
    dpi: int = 300,
    save_to_repo_figures: bool = True,
    save_to_results: bool = True,
) -> dict[str, Path]:
    """
    Save a matplotlib figure as PNG.

    By default, saves the same PNG to:

        figures/<name>.png
        results/<notebook>/figures/<name>.png

    Parameters
    ----------
    fig
        Matplotlib figure.
    name
        Filename stem, without .png.
    paths
        RepoPaths object from src.paths.get_paths().
    dpi
        Export resolution.
    save_to_repo_figures
        Save to top-level figures/.
    save_to_results
        Save to notebook-specific results figures directory.

    Returns
    -------
    dict[str, Path]
        Dictionary of saved file paths.
    """

    saved = {}

    filename = f"{name}.png"

    if save_to_repo_figures:
        paths.figures.mkdir(parents=True, exist_ok=True)
        repo_path = paths.figures / filename
        fig.savefig(repo_path, dpi=dpi, bbox_inches="tight")
        saved["figures"] = repo_path
        print(f"✓ Saved {repo_path}")

    if save_to_results:
        paths.figures_results.mkdir(parents=True, exist_ok=True)
        results_path = paths.figures_results / filename
        fig.savefig(results_path, dpi=dpi, bbox_inches="tight")
        saved["results"] = results_path
        print(f"✓ Saved {results_path}")

    return saved


# ============================================================================
# File collection helpers
# ============================================================================

def _safe_relative(path: Path, root: Path) -> Path:
    """
    Return path relative to root when possible, otherwise return filename.
    """

    try:
        return path.relative_to(root)
    except ValueError:
        return Path(path.name)


def _write_path_to_zip(
    zf: ZipFile,
    item: Path,
    root: Path,
    exclude: set[Path] | None = None,
) -> None:
    """
    Add a file or directory to a zip archive.
    """

    exclude = {p.resolve() for p in (exclude or set())}
    item = Path(item)

    if item.is_dir():
        for path in item.rglob("*"):
            if not path.is_file():
                continue
            if path.resolve() in exclude:
                continue
            zf.write(path, _safe_relative(path, root))

    elif item.exists() and item.is_file():
        if item.resolve() in exclude:
            return
        zf.write(item, _safe_relative(item, root))


# ============================================================================
# Artifact packaging
# ============================================================================

def package_artifacts(
    paths,
    notebook_name: str,
    include_site: bool = True,
    include_src: bool = True,
    include_figures: bool = True,
    include_results: bool = True,
    include_project_files: bool = True,
) -> Path:
    """
    Package notebook artifacts into a ZIP file.

    Creates:

        results/<notebook_name>/<notebook_name>_artifacts.zip

    Includes, by default:

        notebooks/<notebook_name>.ipynb
        figures/
        results/<notebook_name>/
        site/
        src/
        README.md
        requirements.txt
        LICENSE
        .gitignore

    Parameters
    ----------
    paths
        RepoPaths object from src.paths.get_paths().
    notebook_name
        Notebook identifier, e.g. "00_context".
    include_site
        Include site/ folder.
    include_src
        Include src/ folder.
    include_figures
        Include top-level figures/ folder.
    include_results
        Include notebook-specific results folder.
    include_project_files
        Include README, requirements, LICENSE, and .gitignore.

    Returns
    -------
    Path
        Path to created ZIP file.
    """

    zip_path = paths.notebook_results / f"{notebook_name}_artifacts.zip"
    zip_path.parent.mkdir(parents=True, exist_ok=True)

    notebook_path = paths.notebooks / f"{notebook_name}.ipynb"
    fallback_notebook_path = Path.cwd() / f"{notebook_name}.ipynb"

    items: list[Path] = []

    if notebook_path.exists():
        items.append(notebook_path)
    elif fallback_notebook_path.exists():
        items.append(fallback_notebook_path)

    if include_figures:
        items.append(paths.figures)

    if include_results:
        items.append(paths.notebook_results)

    if include_site:
        items.append(paths.site)

    if include_src:
        items.append(paths.src)

    if include_project_files:
        for path in [
            paths.readme,
            paths.requirements,
            paths.license,
            paths.gitignore,
        ]:
            if path.exists():
                items.append(path)

    with ZipFile(zip_path, "w", compression=ZIP_DEFLATED) as zf:
        for item in items:
            _write_path_to_zip(
                zf=zf,
                item=item,
                root=paths.repo,
                exclude={zip_path},
            )

    print(f"✓ Created {zip_path}")
    print(f"✓ Size: {zip_path.stat().st_size:,} bytes")

    return zip_path


# ============================================================================
# Notebook display helper
# ============================================================================

def display_download(path: Path) -> None:
    """
    Display a download link in Jupyter / Colab when possible.
    """

    path = Path(path)

    try:
        from IPython.display import FileLink, display

        display(FileLink(str(path)))
    except Exception:
        print(path)

    try:
        from google.colab import files

        files.download(str(path))
    except Exception:
        pass


def finalize_notebook(
    paths,
    notebook_name: str,
    display: bool = True,
) -> Path:
    """
    Package notebook artifacts and optionally display a download link.
    """

    zip_path = package_artifacts(paths, notebook_name=notebook_name)

    if display:
        display_download(zip_path)

    return zip_path
