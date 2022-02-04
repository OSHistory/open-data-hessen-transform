
import argparse
import glob
import os
import subprocess
import yaml
import sys

import time

ap = argparse.ArgumentParser()

ap.add_argument("-i", "--input-file", required=True,
                help="Input ALKIS-File (.xml) to process")
ap.add_argument("-o", "--output", required=True,
                help="Name des Auszugebenden Geopackage")
ap.add_argument("-e", "--extent", help="Extent to clip to",
                nargs="+", type=float)
ap.add_argument("-c", "--config-file",
                help="Configuration file (e.g. layers to include)", default="config.yaml")
ap.add_argument("--overwrite", action="store_true")
ap.add_argument("--no-cleanup", action="store_true")

args = ap.parse_args()

if not os.path.exists(args.config_file):
    print(f"Fatal: Config File ({args.config_file}) does not exist")
    sys.exit(1)

with open(args.config_file) as fh:
    config = yaml.load(fh, Loader=yaml.FullLoader)

if os.path.exists(args.output) and not args.overwrite:
    print("Fatal: File exists (use --overwrite)")
    sys.exit(1)

if not os.path.exists(os.path.dirname(args.output)):
    os.makedirs(os.path.dirname(args.output))

for layer_idx, layer in enumerate(config['include']):
    print(f"\tExporting {layer}")
    conversion_call = ["ogr2ogr", args.output,
                       args.input_file, layer,
                       "-nlt", "PROMOTE_TO_MULTI"]
    if args.extent:
        conversion_call.append("-clipsrc")
        conversion_call.extend([str(num) for num in args.extent])

    # first iteration
    if not layer_idx:
        if args.overwrite:
            conversion_call.append("-overwrite")
    else:
        conversion_call.append("-append")
    subprocess.run(conversion_call)
