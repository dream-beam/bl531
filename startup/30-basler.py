# author: tmorris@bnl.gov
# June 2023
# as used at ALS

use_basler_cam = True

if use_basler_cam:

    from datetime import datetime
    import matplotlib.pyplot as plt

    import bluesky.plans as bp
    from bluesky.callbacks import best_effort
    from bluesky.run_engine import RunEngine
    from databroker import Broker
    from ophyd.utils import make_dir_tree

    import ophyd_basler
    from ophyd_basler.basler_handler import BaslerCamHDF5Handler
    from ophyd_basler.basler_camera import BaslerCamera

    ophyd_basler.available_devices()

    #cam num sets the camera we use 
    basler_cam = BaslerCamera(cam_num=1, verbose=True, name="basler_cam", pixel_format="Mono12")
    basler_cam.exposure_time.put(25)

    ip = get_ipython()

    # To disable napari callback, comment out next line:
    ip.run_line_magic("run",  "-i ~/src/ophyd-basler/examples/napari_basler.py")

    # basler_cam.active_format.put("BayerGB12")

    db.reg.register_handler("BASLER_CAM_HDF5", BaslerCamHDF5Handler, overwrite=True)

    root_dir = "/tmp/basler"
    _ = make_dir_tree(datetime.now().year, base_path=root_dir)

    # make objects
    import numpy as np



    # from ophyd import AreaDetector, SingleTrigger

    # class MyDetector(SingleTrigger, AreaDetector):
    #     pass

    # prefix = 'BL531acA5427:'
    # basler_cam = MyDetector(prefix, name="basler_cam")


