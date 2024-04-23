print(f"Loading {__file__}")

diode_sample = ophyd.EpicsSignal('bl201-beamstop:current', name='diode_sample')
