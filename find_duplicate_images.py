#!/usr/bin/env python3
"""
Find near-duplicate images in a folder using perceptual hashing.
Groups duplicates and optionally removes extras (keeps one per group).

Usage:
  python find_duplicate_images.py /path/to/image/folder
  python find_duplicate_images.py . --threshold 8

Requires: pip install imagehash Pillow
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PIL import Image
import imagehash


# Common image extensions
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".tiff", ".tif"}


def get_image_paths(folder: Path) -> list[Path]:
    """Return sorted list of image file paths in folder (non-recursive)."""
    paths = []
    for p in folder.iterdir():
        if p.is_file() and p.suffix.lower() in IMAGE_EXTENSIONS:
            paths.append(p)
    return sorted(paths)


def compute_hashes(paths: list[Path]) -> dict[Path, imagehash.ImageHash]:
    """Compute perceptual hash (pHash) for each image. Skip unreadable files."""
    hashes = {}
    for path in paths:
        try:
            with Image.open(path) as img:
                # Convert to RGB if necessary (e.g. RGBA, P)
                if img.mode not in ("RGB", "L"):
                    img = img.convert("RGB")
                hashes[path] = imagehash.phash(img)
        except Exception as e:
            print(f"  [skip] {path.name}: {e}", file=sys.stderr)
    return hashes


def find_duplicate_groups(
    hashes: dict[Path, imagehash.ImageHash],
    threshold: int = 5,
) -> list[list[Path]]:
    """
    Group paths that are near-duplicates (Hamming distance <= threshold).
    Returns list of groups; each group is a list of paths that are duplicates of each other.
    """
    paths = list(hashes.keys())
    n = len(paths)
    # Union-Find would scale better; for moderate N, simple iteration is fine
    parent = list(range(n))

    def find(i: int) -> int:
        if parent[i] != i:
            parent[i] = find(parent[i])
        return parent[i]

    def union(i: int, j: int) -> None:
        pi, pj = find(i), find(j)
        if pi != pj:
            parent[pi] = pj

    for i in range(n):
        for j in range(i + 1, n):
            if hashes[paths[i]] - hashes[paths[j]] <= threshold:
                union(i, j)

    # Build groups: group_id -> list of indices
    groups_by_id: dict[int, list[int]] = {}
    for i in range(n):
        root = find(i)
        groups_by_id.setdefault(root, []).append(i)

    # Convert to list of path lists (only groups with more than one image)
    result = []
    for indices in groups_by_id.values():
        if len(indices) > 1:
            result.append([paths[i] for i in sorted(indices)])
    return result


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Find near-duplicate images in a folder and optionally remove extras.",
    )
    parser.add_argument(
        "folder",
        type=str,
        help="Path to the folder containing images",
    )
    parser.add_argument(
        "-t",
        "--threshold",
        type=int,
        default=5,
        help="Perceptual hash Hamming distance threshold (0=identical, 5–10 typical for near-dupes; default 5)",
    )
    args = parser.parse_args()

    folder = Path(args.folder).resolve()
    if not folder.is_dir():
        print(f"Error: not a directory: {folder}", file=sys.stderr)
        sys.exit(1)

    paths = get_image_paths(folder)
    if not paths:
        print(f"No image files found in {folder}")
        return

    print(f"Scanning {len(paths)} images in {folder} ...")
    hashes = compute_hashes(paths)
    if len(hashes) < 2:
        print("Need at least 2 images to check for duplicates.")
        return

    groups = find_duplicate_groups(hashes, threshold=args.threshold)

    if not groups:
        print("No duplicate groups found.")
        return

    print(f"\nFound {len(groups)} duplicate group(s):\n")
    for i, group in enumerate(groups, 1):
        print(f"  Group {i} ({len(group)} images):")
        for p in group:
            print(f"    - {p.name}")
        print()

    total_dupes = sum(len(g) - 1 for g in groups)
    print(f"Total duplicate images (can be removed): {total_dupes}")

    answer = input("\nRemove duplicates? Keep one image per group. [y/N]: ").strip().lower()
    if answer not in ("y", "yes"):
        print("No files removed.")
        return

    removed = 0
    for group in groups:
        # Keep the first (by path name); remove the rest
        keep, delete = group[0], group[1:]
        for p in delete:
            try:
                p.unlink()
                print(f"  Removed: {p.name}")
                removed += 1
            except Exception as e:
                print(f"  Failed to remove {p.name}: {e}", file=sys.stderr)
    print(f"\nRemoved {removed} duplicate image(s). Kept one per group.")


if __name__ == "__main__":
    main()
