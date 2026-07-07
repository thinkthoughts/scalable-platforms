"""
Minimal export helpers for notebook-generated PNGs.
"""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from .theme import ensure_results

def save_png(fig, name, dpi=300, outdir=None):
    outdir = Path(outdir) if outdir else ensure_results()
    outdir.mkdir(parents=True, exist_ok=True)
    path = outdir / f"{name}.png"
    fig.savefig(path, dpi=dpi, bbox_inches="tight")
    print(f"✓ Saved {path}")
    return path

def zip_results(repo_name="scalable-platforms", notebook=None, root=None):
    root = Path(root or ".").resolve()
    results = root / "results"
    suffix = f"-{notebook}" if notebook else ""
    zip_path = results / f"{repo_name}{suffix}.zip"
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(zip_path, "w", compression=ZIP_DEFLATED) as zf:
        for f in results.rglob("*"):
            if f.is_file() and f.resolve() != zip_path.resolve():
                zf.write(f, f.relative_to(root))
    print(f"✓ Created {zip_path}")
    return zip_path

def finalize_notebook(repo_name="scalable-platforms", notebook=None, root=None):
    return zip_results(repo_name=repo_name, notebook=notebook, root=root)
