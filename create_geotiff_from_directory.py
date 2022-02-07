
import argparse
import glob
import os
import subprocess
import tempfile
import sys

import time

ap = argparse.ArgumentParser()

ap.add_argument(dest="directory")
ap.add_argument("-o", "--output",
                help="Name of output GeoTIFF (default: directory + .tif)")
ap.add_argument("--overwrite", action="store_true")
ap.add_argument("--no-cleanup", action="store_true")


TMP_DIR = tempfile.TemporaryDirectory(prefix="hessen_open_data_")

args = ap.parse_args()

if args.output is None:
    out_file = os.path.split(args.directory.rstrip("/"))[1] + ".tif"
    print(out_file)
else:
    out_file = args.output


if not os.path.exists(os.path.dirname(out_file)):
    os.makedirs(os.path.dirname(out_file))

if os.path.exists(out_file):
    if args.overwrite == False:
        print(f"Fatal: File {out_file} exists (use --overwrite)")
        sys.exit(1)
    else:
        print(f"Deleting old file {out_file}")
        os.remove(out_file)

all_xyz_files = glob.glob(args.directory + "*.xyz")

print("STEP 1: Converting all xyz-files")

for xyz_file in all_xyz_files:
    print(xyz_file)
    tmp_tif = os.path.join(TMP_DIR.name, os.path.basename(
        xyz_file.replace(".xyz", ".tif")))
    tmp_tif_warped = tmp_tif.replace(".tif", "_warped.tif")

    print("STEP 1.1: Transform xyz to .tif")
    subprocess.run([
        "gdal_translate",
        "-a_srs", "EPSG:25832",
        xyz_file,
        tmp_tif
    ])
    # Warping is necessary or gdal_merge.py will fail
    print("STEP 1.2: Warping")
    subprocess.run([
        "gdalwarp",
        "-s_srs", "EPSG:25832",
        "-t_srs", "EPSG:25832",
        "-ot", "Float32",
        tmp_tif,
        tmp_tif_warped
    ])
    os.remove(tmp_tif)

print("STEP 2.1: Merging temporary tif files")
merge_command = [
    "gdal_merge.py",
    "-co", "COMPRESS=PACKBITS",
    "-o", out_file,
]
merge_command.extend(glob.glob(os.path.join(TMP_DIR.name, "*tif")))

subprocess.run(merge_command)

print("STEP 2.2: Genearting overview")
overview_command = ["gdaladdo",
                    "--config", "COMPRESS_OVERVIEW", "PACKBITS",
                    "--config", "INTERLEAVE_OVERVIEW", "PIXEL",
                    "-r", "average",
                    out_file,
                    "2", "4", "8", "16"
                    ]

print(" ".join(overview_command))

subprocess.run(overview_command)
