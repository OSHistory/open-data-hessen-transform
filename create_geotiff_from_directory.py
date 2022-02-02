
import argparse
import glob
import os
import subprocess

import time

from cv2 import merge

ap = argparse.ArgumentParser()

ap.add_argument(dest="directory")
ap.add_argument("-o", "--output",
                help="Name des Auszugebenden GeoTIFFs (default: directory + .tif)")
ap.add_argument("--overwrite", action="store_true")
ap.add_argument("--no-cleanup", action="store_true")


TMP_DIR = os.path.join("/tmp/", str(time.time()).replace(".", "_"))
print(TMP_DIR)

if not os.path.exists(TMP_DIR):
    os.mkdir(TMP_DIR)

args = ap.parse_args()

print(args)

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
print(merge_command)
subprocess.run(merge_command)

print("STEP 3: Cleaning temporary directory")
# TODO
