#!/usr/bin/env python

from worldview_dl import download_image
import datetime
import pytz
import os

def test_module():
    t_now = datetime.datetime.now().replace(tzinfo=pytz.utc)
    t = t_now - datetime.timedelta(hours=2)

    download_image(
        fn="GOES_test.png",
        time=t,
        bbox=[10.,-60.,15.,-50.],
        layers=['GOES-East_ABI_Band2_Red_Visible_1km', 'Reference_Labels'],
        image_format="png",
        resolution=0.01,
    )


def test_cli():
    cmd = 'python -m worldview_dl.cli "2020-01-28 16:20" 10.,-60.,15.,-50. --image_type png'
    result = os.system(cmd)
    assert(0 == result)
