"""Main module."""
import requests
import pendulum
import datetime


BASE_URL = "https://wvs.earthdata.nasa.gov/api/v1/snapshot?REQUEST=GetSnapshot&TIME={time}&BBOX={bbox}&CRS=EPSG:4326&LAYERS={layers}&FORMAT={format}&WIDTH={width}&HEIGHT={height}"
# example arguments:
#  time: 2020-01-29T12:10:00Z
#  bbox: 10.177734375,-60.1875,16.41796875,-53.5166015625
#  layers: GOES-East_ABI_Band2_Red_Visible_1km,Reference_Labels
#  format: image/tiff
#  width: 1518
#  height: 1420

def download_image(fn, time, bbox, layers, image_format, resolution):
    """
    example arguments:
     time: datetime(2020-01-29T12:10:00Z)
     bbox: [10.177734375, -60.1875, 16.41796875, -53.5166015625]
     layers: ["GOES-East_ABI_Band2_Red_Visible_1km", "Reference_Labels"]
     image_format: "tiff"
     resolution: 0.01 (deg/pixel)
    """

    if len(bbox) != 4:
        raise Exception("`bbox` should be a list of [lat_S, lon_W, lat_N, lon_E]")

    if time.tzinfo is None:
        raise Exception("The provided timestamp doesn't contain timezone info")

    # round time to nearest second
    time = time - datetime.timedelta(microseconds=time.microsecond)

    dlon = bbox[2]-bbox[0]
    dlat = bbox[3]-bbox[1]
    width, height = int(dlat/resolution), int(dlon/resolution)

    url = BASE_URL.format(
        time=pendulum.instance(time).to_iso8601_string(),
        bbox=",".join([str(v) for v in bbox]),
        layers=",".join(layers),
        format="image/{}".format(image_format),
        width=width,
        height=height
    )
    r = requests.get(url)

    if r.status_code == 200:
        if 'xml' in r.text[:40]:
            print(url)
            raise Exception(r.content)
        else:
            with open(fn, 'wb') as fh:
                fh.write(r.content)
    else:
        raise Exception(r.status)
