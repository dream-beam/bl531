print(f"Loading {__file__}")

# author: tmorris@bnl.gov
# November 2023
# as used at ALS



from blop import Agent, DOF, Objective

dofs = [
    DOF(device=m101_pitch, description="toroid pitch", search_domain=(0.7, 0.9), units="mm", tags=["toroid"]),
    DOF(device=m101_bend, description="toroid bend", search_domain=(2000, 5000), units="um", tags=["toroid"]),
    DOF(device=mono_angle, description="monochromator angle", search_domain=(25, 26), units="deg", tags=["mono"]),
    DOF(device=mono_height, description="monochromator height", search_domain=(40, 42), units="mm", tags=["mono"]),
]

# objectives = [
#     Objective(description="flux", name="diode_sample", target=-1500, min_snr=5e0),
# ]

ice_cream_objectives = [
    Objective(description="beam flux", name="ice_cream_pix_sum", target="max", trust_domain = (10000, np.inf), transform="log", max_noise=0.1, units="pA"),
    Objective(description="beam effective size", name="ice_cream_eff_size", target="min", transform="log", weight=2.0, max_noise=0.1, units="mm"),
    #Objective(description="beam width", name="ice_cream_wid_x", target="min", log=True, min_snr=1e2),
    #Objective(description="beam height", name="ice_cream_wid_y", target="min", log=True, min_snr=1e2),
]
basler_objectives = [
    Objective(description="beam sum", name="beam_sum", target="max", transform="log", max_noise=0.1, units="daq"),
    #Objective(description="beam width", name="beam_width_x", target="min", transform="log", max_noise=0.1, units="pixels"),
    #Objective(description="beam height", name="beam_width_y", target="min", transform="log", max_noise=0.1, units="pixels"),
    Objective(description="effective area", name="beam_eff_area", target="min", transform="log", weight=2, max_noise=0.1, units="pixels"),
]


dets=[
    # ice_cream
    basler_cam,
    ]

agent = Agent(
                dofs=dofs, 
                objectives=basler_objectives, 
                dets=[basler_cam], 
                digestion=basler_cam_digestion,
                db=db, 
                trigger_delay=0.1, 
                verbose=True
                )



exposure_dofs = [
    DOF(device=basler_cam.exposure_time, description="exposure time", search_domain=(10, 200), units="ms")
]

exposure_objectives = [
    Objective(description="beam max", name="beam_max", target=(3500, 4000), max_noise=0.1, units="daq"),
]


exposure_agent = Agent(
                dofs=exposure_dofs,
                objectives=exposure_objectives, 
                dets=[basler_cam], 
                digestion=basler_cam_digestion,
                db=db, 
                trigger_delay=0.1, 
                verbose=True
                )


agent.dofs.deactivate()
agent.dofs.activate(tag="toroid")

# # author: tmorris@bnl.gov
# # June 2023
# # as used at ALS

# # [0, 1] is for slicing (select from the explicit list)
# dofs = np.array([m101_pitch, m101_bend, mono_height, mono_angle])[[0, 1, 2, 3]]

# for dof in dofs:
#     dof.kind = "hinted"

# # bounds = np.array([(0, 0.1), (0, 10000)])

# # fid is for fiducials (set of good/ok parameters); 
# # #center of the exploration range
# fid_params = {
#     #"basler_cam_exposure_time": 100, 
#     "m101_pitch": 0.04, 
#     "m101_bend": 2800,
#     "mono_height": 40.6,
#     "mono_angle": 24,
#     }

# rel_bounds = {
#     #"basler_cam_exposure_time": [-1e-2, +1e-2],
#     "m101_pitch": [-2e-2, +2e-2],
#     "m101_bend": [-6e+2, +6e+2],
#     "mono_height": [-1e0, 1e0],
#     "mono_angle": [0, 6], 
# }

# # 4 x 2 arrays: 4 is dof, 2 is for min and max
# # r_ is array stacking
# hard_bounds = np.r_[[fid_params[dof.name] + np.array(rel_bounds[dof.name]) for dof in dofs]]

# #hard_bounds = np.array([[10., 200.], [0., 0.1], [2200., 3200.]])

# from bloptools.tasks import Task
# from bloptools.bayesian import Agent

# #make sure the digestion is passing something called with the same key as a product
# # kind is high or low
# # the lambda function is the fitness function (in this case log, for fitness function product)
# current_task = Task(key="current", kind="max", transform=lambda x: np.log(x))
# beam_peak_task = Task(key="peak", kind="max", transform=lambda x: np.log(x))
# beam_width_task = Task(key="x_width", kind="min", transform=lambda x: np.log(x))
# beam_height_task = Task(key="y_width", kind="min", transform=lambda x: np.log(x))

# boa = Agent(
#             dofs=dofs, # things which we move around
#             bounds=hard_bounds, # where we're allowed to move them
#             detectors=[basler_cam],
#             tasks=[beam_peak_task, beam_width_task, beam_height_task], # tasks for the optimizer
#             #tasks=[beam_peak_task], # tasks for the optimizer
#             digestion=digestion, # how to process the acquisition into task data
#             db=db, # a databroker instance
#             )

