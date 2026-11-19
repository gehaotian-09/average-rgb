"""Calculate average RGB colors for 0.png through 1999.png."""

import argparse
import csv
from pathlib import Path

import matplotlib
import numpy as np
from PIL import Image, ImageStat

matplotlib.use("Agg")
import matplotlib.pyplot as plt


IMAGE_COUNT = 2000


def average_rgb(path):
    with Image.open(path) as image:
        if "A" not in image.getbands() and "transparency" not in image.info:
            return ImageStat.Stat(image.convert("RGB")).mean

        pixels = np.asarray(image.convert("RGBA"))
        weights = pixels[..., 3]
        total_weight = weights.sum(dtype=np.float64)
        if total_weight == 0:
            raise ValueError(f"{path.name}: the image is fully transparent")
        return [
            np.multiply(pixels[..., channel], weights, dtype=np.uint32).sum()
            / total_weight
            for channel in range(3)
        ]


def save_plot(colors, path):
    fig = plt.figure(figsize=(8, 8), layout="constrained")
    ax = fig.add_subplot(projection="3d")
    ax.scatter(
        *colors.T, c=colors / 255, s=14, edgecolors="#404040",
        linewidths=0.25, depthshade=False,
    )
    ticks = [0, 64, 128, 192, 255]
    ax.set(
        xlabel="Red (R)", ylabel="Green (G)", zlabel="Blue (B)",
        xlim=(0, 255), ylim=(0, 255), zlim=(0, 255),
        xticks=ticks, yticks=ticks, zticks=ticks,
        title=f"Average RGB colors ({len(colors):,} images)",
    )
    ax.set_box_aspect((1, 1, 1))
    ax.view_init(elev=24, azim=-55)
    fig.savefig(path, dpi=200)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("folder", nargs="?", type=Path, default=Path.cwd())
    args = parser.parse_args()
    paths = [args.folder / f"{index}.png" for index in range(IMAGE_COUNT)]
    missing = [path.name for path in paths if not path.is_file()]
    if missing:
        parser.error(
            f"{len(missing)} PNG file(s) missing in {args.folder.resolve()}. "
            f"First missing files: {', '.join(missing[:5])}"
        )

    rows = []
    for path in paths:
        try:
            rows.append(average_rgb(path))
        except (OSError, ValueError) as error:
            parser.exit(1, f"Could not process {path}: {error}\n")
    colors = np.asarray(rows)

    csv_path = args.folder / "average_rgb.csv"
    plot_path = args.folder / "average_rgb_distribution.png"
    with csv_path.open("w", encoding="utf-8", newline="") as output:
        writer = csv.writer(output)
        writer.writerow(["filename", "R", "G", "B"])
        for path, color in zip(paths, colors):
            writer.writerow([path.name, *(f"{channel:.6f}" for channel in color)])
    save_plot(colors, plot_path)
    print(f"Saved {csv_path.resolve()}")
    print(f"Saved {plot_path.resolve()}")


if __name__ == "__main__":
    main()
