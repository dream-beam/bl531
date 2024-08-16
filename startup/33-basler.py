from pathlib import PurePath

from nslsii.ad33 import SingleTriggerV33
from ophyd import Component as C

from ophyd import EpicsSignalRO
from ophyd.areadetector import AreaDetector, ImagePlugin
from ophyd.areadetector.filestore_mixins import (
    FileStoreIterativeWrite,
    FileStorePluginBase,
)
from ophyd.areadetector.plugins import TIFFPlugin_V33


class TSTFileStoreTIFF(FileStorePluginBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filestore_spec = "AD_TIFF"  # spec name stored in resource doc
        self.stage_sigs.update(
            [
                ("file_template", "%s%s_%6.6d.tiff"),
                ("file_write_mode", "Single"),
            ]
        )
        # 'Single' file_write_mode means one image : one file.
        # It does NOT mean that 'num_images' is ignored.

    def get_frames_per_point(self):
        return self.parent.cam.num_images.get()

    def stage(self):
        super().stage()
        # this over-rides the behavior is the base stage
        self._fn = self._fp

        resource_kwargs = {
            "template": "%s%s_%6.6d.tiff",
            "filename": self.file_name.get(),
            "frame_per_point": self.get_frames_per_point(),
        }
        self._generate_resource(resource_kwargs)


class TSTTIFFPlugin(TIFFPlugin_V33, TSTFileStoreTIFF, FileStoreIterativeWrite):
    pass


base = "/mnt/data531/BL531"


class TSTBasler(AreaDetector):
    image = C(ImagePlugin, "image1:")
    tiff = C(
        TSTTIFFPlugin,
        "TIFF1:",
        write_path_template=f"{base}/%Y/%m/%d/",
        read_path_template=f"{base}/%Y/%m/%d/",
        read_attrs=[],
        root=base,
    )
    stats = C(EpicsSignalRO, "Stats1:Total_RBV")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.stage_sigs.update([(self.cam.trigger_mode, "Internal")])

    def make_data_key(self):
        source = "PV:{}".format(self.prefix)
        # This shape is expected to match arr.shape for the array.
        shape = (
            self.cam.array_size.array_size_y.get(),
            self.cam.array_size.array_size_x.get(),
        )
        return dict(
            shape=shape,
            source=source,
            dtype="array",
            dtype_str="|u1",
            external="FILESTORE:",
        )


class TSTBaslerSingleTrigger(SingleTriggerV33, TSTBasler):
    pass


def display_last_image_bas_cam():
    from PIL import Image

    Image.fromarray(
        tiled_client.values().last().primary["external"]["bas1_image"].read()[0]
    ).show()


bas1_pv_prefix = "BL531acA1920:"



basler_cam = TSTBaslerSingleTrigger(bas1_pv_prefix, name="bas1", read_attrs=["tiff"])

basler_cam.stats.kind = "hinted"