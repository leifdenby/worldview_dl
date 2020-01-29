"""Console script for worldview_dl."""
import argparse
import sys

import dateutil.parser
import pytz
import tqdm
import datetime
import math

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
    parser.add_argument('--end-time', default=None, type=_parse_utc_timedate)

    args = parser.parse_args()

    if args.end_time is None:
        times = [args.time]
        wrap = lambda t: t
    else:
        t_len = args.end_time - args.time
        dt = datetime.timedelta(seconds=60*10)
        N = int(math.ceil(t_len/dt))
        times = [args.time + n*dt for n in range(N+1)]
        wrap = lambda t: tqdm.tqdm(t)

    for t in wrap(times):

        fn = "GOES_{time}.{ext}".format(
            time=t.isoformat(),
            ext=args.image_type
        )

        download_image(
            fn=fn,
            time=t,
            bbox=args.bbox,
            layers=args.layers,
            image_format=args.image_type,
            resolution=args.resolution,
        )
        if len(times) == 1:
            print("Image downloaded to `{}`".format(fn))


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
