print(f"Loading {__file__}")

import bluesky.plan_stubs as bps
import bluesky.plans as bp
import databroker
import matplotlib.pyplot as plt
from bluesky import RunEngine
from bluesky.callbacks.best_effort import BestEffortCallback
from databroker import Broker

from bluesky.utils import ProgressBarManager


plt.ion()

# Enable interactive mode
# ss

db = Broker.named("temp")
# db = Broker.named("local")
# try:
#     databroker.assets.utils.install_sentinels(db.reg.config, version=1)
# except Exception:
#     pass


RE = RunEngine({})
RE.subscribe(db.insert)

bec = BestEffortCallback()
bec.disable_plots()
RE.subscribe(bec)
RE.waiting_hook = ProgressBarManager()