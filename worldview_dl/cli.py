"""Console script for worldview_dl."""
import argparse
import sys

import dateutil.parser
import pytz

from .worldview_dl import download_image

def _bbox_arg(s):
    bbox = [float(v) for v in s.split(',')]

    if len(bbox) != 4:
        raise Exception("`bbox` should be a list of [lat_S, lon_W, lat_N, lon_E]")
    return bbox

def _parse_utc_timedate(s):
    d = dateutil.parser.parse(s)
    return d.replace(tzinfo=pytz.utc)


def main():
    """Console script for worldview_dl."""
    parser = argparse.ArgumentParser()
    parser.add_argument('time', type=_parse_utc_timedate, help="timestamp (UTC)")
    parser.add_argument('bbox', type=_bbox_arg)
    parser.add_argument('--layers', nargs='+',
        default=['GOES-East_ABI_Band2_Red_Visible_1km', 'Reference_Labels']
    )
    parser.add_argument('--image_type', default='tiff')
    # 1px ~ 1km ~ 1/100 deg
    parser.add_argument('--resolution', default=1.0/100, type=float)

    args = parser.parse_args()

    fn = "GOES_{time}.{ext}".format(
        time=args.time.isoformat(),
        ext=args.image_type
    )

    download_image(
        fn=fn,
        time=args.time,
        bbox=args.bbox,
        layers=args.layers,
        image_format=args.image_type,
        resolution=args.resolution,
    )
    print("Image downloaded to `{}`".format(fn))


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
