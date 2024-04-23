import numpy as np
from ophyd import Component as Cpt
from ophyd import Device, Signal

import re
import os

import h5py
import numpy as np
from event_model import compose_resource
from ophyd import Component as Cpt
from ophyd import Device, Signal
from ophyd.sim import NullStatus, new_uid

from collections import deque
from pathlib import Path




class IceCream(Device):

    image = Cpt(Signal, kind="normal")
    pix_sum = Cpt(Signal, kind="hinted")
    eff_size = Cpt(Signal, kind="hinted")
    pos_x = Cpt(Signal, kind="normal")
    pos_y = Cpt(Signal, kind="normal")
    wid_x = Cpt(Signal, kind="hinted")
    wid_y = Cpt(Signal, kind="hinted")

    # exposure_time = Cpt(Signal, value=1000, kind="config")  # exposure time, in milliseconds
    # user_defined_name = Cpt(Signal, kind="config")
    # camera_model = Cpt(Signal, kind="config")
    # serial_number = Cpt(Signal, kind="config")
    # image_shape = Cpt(Signal, kind="config")
    # pixel_level_min = Cpt(Signal, kind="config")
    # pixel_level_max = Cpt(Signal, kind="config")
    # active_format = Cpt(Signal, kind="config")
    # payload_size = Cpt(Signal, kind="config")
    # grab_timeout = Cpt(Signal, value=5000, kind="config")

    def __init__(
        self,
        width=1,
        height=1,
        *args,
        **kwargs,
    ):
        """
        A class to instantiate a Basler ophyd object.
        """
        super().__init__(*args, **kwargs)

        self._asset_docs_cache = deque()

        self.width = width
        self.height = height


    def trigger(self):

        super().trigger()

        n_frames = 4

        image = 0.
        for i in range(n_frames):
            res = os.popen("pvget ice-cream/image").read()
            image += np.array(eval(re.compile(" (\[.+\])").findall(res)[0]), dtype=float).reshape(48, 50).T / n_frames

        pix_sum, es, x0, xw, y0, yw = get_beam_stats(image, threshold=0.1)

        bad = False

        if bad:
            pix_sum, es, x0, xw, y0, yw = np.nan, np.nan, np.nan, np.nan, np.nan, np.nan

        ny, nx = image.shape

        self.pix_sum.put(pix_sum)
        self.eff_size.put(es * np.sqrt(self.height * self.width / (nx * ny)))
        self.pos_x.put(x0 * self.width / nx)
        self.pos_y.put(y0 * self.height / ny)
        self.wid_x.put(xw * self.width / nx)
        self.wid_y.put(yw * self.height / ny)

        self.image.put(image)

        super().trigger()

        return NullStatus()

    def stage(self):
        ...

    def unstage(self):
        ...

    def collect_asset_docs(self):
        items = list(self._asset_docs_cache)
        self._asset_docs_cache.clear()
        for item in items:
            yield item


ice_cream = IceCream(name="ice_cream", width=2.5, height=2.4)