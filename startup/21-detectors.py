print(f"Loading {__file__}")
from ophyd import Device, EpicsSignal, Component as Cpt

class BeamStopCurrent(Device):
    prec = Cpt(EpicsSignal, ".PREC")
    current = Cpt(EpicsSignal, "")


beamstop_current_device = BeamStopCurrent("bl201-beamstop:current", name="beamstop")
beamstop_current_device.prec.put(3)  # This is needed for LiveTable (via BestEffortCallback) to print the values with proper number of decimal values
beamstop_current = beamstop_current_device.current
beamstop_current.kind = "hinted"



