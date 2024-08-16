print(f"Loading {__file__}")

from PIL import Image
import scipy as sp
import epics
import time as ttime


class SAXSDetector(Device):
    image = Cpt(Signal, kind="normal")
    profile = Cpt(Signal, kind="normal")
    filename = Cpt(Signal, kind="normal")

    def __init__(
        self,
        center,
        *args,
        **kwargs,
    ):
        """
        A class to instantiate a Basler ophyd object.
        """
        super().__init__(*args, **kwargs)

        self.center = center

    def trigger(self):

        epics.caput("13PIL1:cam1:Acquire", 1)

        ttime.sleep(3)

        filename_ascii = epics.caget('13PIL1:cam1:FullFileName_RBV')
        self.filename.put(bytes(filename_ascii).decode()[:-1])

        image = np.array(Image.open(self.filename.get())).clip(max=1e3)
        self.image.put(image)

        ny, nx = image.shape
        x, y = np.arange(nx), np.arange(ny)
        X, Y = np.meshgrid(x, y)
        Z = (X - self.center[0]) + 1j * (Y - self.center[1])
        R = np.abs(Z)

        bins = np.linspace(0, 500, 256)

        mask = image > -1

        profile = sp.stats.binned_statistic(R[mask], image[mask], statistic="mean", bins=bins).statistic

        self.profile.put(profile)

        super().trigger()

        return NullStatus()

    def stage(self):
        super().stage()
        
    def unstage(self):
        super().unstage()


#saxs = SAXSDetector(name="saxs", center=[445, 588])