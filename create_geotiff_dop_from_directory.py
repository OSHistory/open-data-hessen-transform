
import argparse
import glob
import os
import subprocess
import sys
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
else:
    out_file = args.output

if os.path.exists(out_file):
    if not args.overwrite:
        print(f"Fatal: File {out_file} exists, use --overwrite option.")
        sys.exit(1)

if not os.path.exists(os.path.dirname(out_file)):
    os.makedirs(os.path.dirname(out_file))

print("STEP 1: Merging jpg files (gdal_merge.py)")
merge_command = [
    "gdal_merge.py",
    "-co", "COMPRESS=JPEG", 
    "-co", "PHOTOMETRIC=YCBCR",
    "-co", "TILED=YES",
    "-o", out_file
]

merge_command.extend(glob.glob(args.directory + "*.jpg"))

subprocess.run(merge_command)

print("Step 2: Generating overviews")
gdaladdo_command = [
    "gdaladdo",
    "--config", "COMPRESS_OVERVIEW JPEG",
    "--config", "PHOTOMETRIC_OVERVIEW YCBCR",
    "--config", "INTERLEAVE_OVERVIEW PIXEL",
    "-r", "average",
    out_file,
    "2", "4", "8", "16"
]

subprocess.run(gdaladdo_command)
