print(f"Loading {__file__}")

# author: tmorris@bnl.gov
# November 2023
# as used at ALS



from blop import Agent, DOF, Objective
from blop.digestion import beam_stats_digestion

dofs = [
    # DOF(device=m101_pitch, description="toroid pitch", search_domain=(0.78, 0.8), units="mm", tags=["toroid"]),
    # DOF(device=m101_bend, description="toroid bend", search_domain=(2000, 4000), units="um", tags=["toroid"], travel_expense=10.),
    DOF(device=mono_angle, description="monochromator angle", search_domain=(29, 30), units="deg", tags=["mono"]),
    # DOF(device=mono_height, description="monochromator height", search_domain=(43, 44), units="mm", tags=["mono"]),
]

beamstop_objectives = [
    Objective(description="flux", name="beamstop_current", target=(-5, -4)),
]

ice_cream_objectives = [
    Objective(description="beam flux", name="ice_cream_pix_sum", target="max", trust_domain = (10000, np.inf), transform="log", max_noise=0.1, units="pA"),
    Objective(description="beam effective size", name="ice_cream_eff_size", target="min", transform="log", weight=2.0, max_noise=0.1, units="mm"),
    #Objective(description="beam width", name="ice_cream_wid_x", target="min", log=True, min_snr=1e2),
    #Objective(description="beam height", name="ice_cream_wid_y", target="min", log=True, min_snr=1e2),
]
basler_objectives = [
    Objective(description="beam sum", name="sum", target="max", transform="log", max_noise=0.1, units="daq"),
    #Objective(description="beam width", name="beam_width_x", target="min", transform="log", max_noise=0.1, units="pixels"),
    #Objective(description="beam height", name="beam_width_y", target="min", transform="log", max_noise=0.1, units="pixels"),
    #Objective(description="effective area", name="beam_eff_area", target="min", transform="log", weight=2, max_noise=0.1, units="pixels"),
    Objective(description="area", name="area", target="min", transform="log", trust_domain=(10, 1e7), max_noise=0.1, units="pixels"),
]

saxs_objectives = [
    Objective(description="saxs peak", name="saxs_peak", target="max", transform="log", max_noise=0.1, units="daq"),
    Objective(description="saxs width", name="saxs_width", target="min", transform="log", max_noise=0.1, units="daq"),
]


agent = Agent(
                dofs=dofs,
                objectives=basler_objectives,
                detectors=[basler_cam],
                digestion=beam_stats_digestion,
                digestion_kwargs={"image_key": "bas1_image"},
                db=db,
                trigger_delay=0.1,
                verbose=True
                )


# agent = Agent(
#                 dofs=dofs,
#                 objectives=ice_cream_objectives,
#                 dets=[ice_cream],
#                 digestion=diamond_cam_digestion,
#                 db=db,
#                 trigger_delay=2,
#                 verbose=True
#                 )

# agent = Agent(
#                 dofs=dofs,
#                 objectives=saxs_objectives,
#                 dets=[saxs],
#                 digestion=saxs_digestion,
#                 db=db,
#                 trigger_delay=2,
#                 verbose=True
#                 )

# agent = Agent(
#                 dofs=dofs,
#                 objectives=beamstop_objectives,
#                 dets=[beamstop_current],
#                 db=db,
#                 trigger_delay=2,
#                 verbose=True
#                 )

# agent.dofs.deactivate()
# agent.dofs.activate(tag="toroid")
#agent.dofs.mono_height.activate()
# exposure_dofs = [
#     DOF(device=basler_cam.exposure_time, description="exposure time", search_domain=(10, 200), units="ms")
# ]

# exposure_objectives = [
#     Objective(description="beam max", name="beam_max", target=(3500, 4000), max_noise=0.1, units="daq"),
# ]


# exposure_agent = Agent(
#                 dofs=exposure_dofs,
#                 objectives=exposure_objectives,
#                 dets=[basler_cam],
#                 digestion=basler_cam_digestion,
#                 db=db,
#                 trigger_delay=0.1,
#                 verbose=True
#                 )


#agent.dofs.deactivate()

## for basler_objectives, find the pitch and bend to get large beam sum and small area
#agent.dofs.activate(tag="toroid")


# for beamstop_objectives, change angle to see the edge
#agent.dofs.mono_angle.activate()
