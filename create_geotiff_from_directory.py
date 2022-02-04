
import argparse
import glob
import os
import subprocess

import time

ap = argparse.ArgumentParser()

ap.add_argument(dest="directory")
ap.add_argument("-o", "--output",
                help="Name of output GeoTIFF (default: directory + .tif)")
ap.add_argument("--overwrite", action="store_true")
ap.add_argument("--no-cleanup", action="store_true")


if not os.path.exists("/tmp/"):
    TMP_BASE = "tmp/"
else:
    TMP_BASE = "/tmp/"

TMP_DIR = os.path.join(TMP_BASE, str(time.time()).replace(".", "_"))

if not os.path.exists(TMP_DIR):
    os.mkdir(TMP_DIR)

args = ap.parse_args()

if args.output is None:
    out_file = os.path.split(args.directory.rstrip("/"))[1] + ".tif"
    print(out_file)
else:
    out_file = args.output


if not os.path.exists(os.path.dirname(out_file)):
    os.makedirs(os.path.dirname(out_file))

all_xyz_files = glob.glob(args.directory + "*.xyz")

print("STEP 1: Converting all xyz-files")

for xyz_file in all_xyz_files:
    print(xyz_file)
    tmp_tif = os.path.join(TMP_DIR, os.path.basename(
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

print("STEP 2: Merging temporary tif files")
merge_command = [
    "gdal_merge.py",
    "-o", out_file,
]
merge_command.extend(glob.glob(os.path.join(TMP_DIR, "*tif")))

subprocess.run(merge_command)

print("STEP 3: Cleaning temporary directory (TODO)")
# TODO
