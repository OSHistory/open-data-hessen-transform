# README

Simple python scripts to transform data from the OpenData-Geo Portal
in Hessen [https://gds.hessen.de/](https://gds.hessen.de/). Transforms `.xyz` files to GeoTIFs and
ALKIS data to geopackage for facilitated data access.

This script assumes that `gdal`-utilities and `ogr2ogr` are present and in your
python path.

## Create Geopackage from ALKIS data

The script iterates and exports all layers defined in the config file `config.yaml`.

Copy the example file `config.example.yaml` to `config.yaml` and remove or add layers.

For a list of all available layers simply run:

```bash
ogrinfo path/to/ALKIS/your_alkis_file.xml
```

You can specify an optional extent, if you are only interested in a subset of the data

```bash
python3 create_geopackage_from_alkis.py \
    # extent (min_x, min_y, max_x, max_y) in EPSG:25832 (here Sachsenhausen)
    -e 497712.819 5673706.531 505244.836 5679252.480 \
    -i path/to/the/alkis/file.xml \
    -o path/to/your_geopackage.gpkg \
    --overwrite
```

## Create GeoTIFFs from xzy data

Unzip the downloaded file to a directory, then point the script there and specify an output Geopackage:

```bash
python3 create_geotiff_from_directory.py path/to/your/unzipped/DGM/ -o path/to/xyz_dgm.tif
```

## Create GeoTIFFs from single jpg files

Unzip the downloaded file to a directory, then point the script there and specify an output Geopackage:

```bash
python3 create_geotiff_from_directory.py path/to/your/unzipped/DOP/ -o path/to/xyz_dop.tif
```

## TODO:

- add extent option to GeoTIFF creation
- Check extent of files before merging (if extent used)
- Better ALKIS to geopackage conversion (use `-mapFieldType`)
- Possibly use existing NAS Tools
- dop and DEM Scripts are essentially the same (except for the .xyz / .jpg part) -> should share most of the
  code base
- move configuration options (like compression etc.) to `config.yaml`
