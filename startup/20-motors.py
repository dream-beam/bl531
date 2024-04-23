print(f"Loading {__file__}")

import ophyd
from ophyd import EpicsMotor
# ophyd.set_cl('caproto')

m101_pitch = EpicsMotor('bl531_esp300:m101_pitch_mm', name='m101_pitch')
m101_bend  = EpicsMotor('bl531_esp300:m101_bend_um', name='m101_bend')
mono_height = EpicsMotor('bl531_xps1:mono_height_mm', name='mono_height')
mono_angle = EpicsMotor('bl531_xps1:mono_angle_deg', name='mono_angle')