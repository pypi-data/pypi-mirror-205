# from schedulerx import ServiceTimerManager

# service_timer = ServiceTimerManager(
#     service_filename="shutdown.service",
#     service_description="shutdown at midnight",
#     command="shutdown now",
#     timer_filename="shutdown.timer",
#     timer_description="shutdown at midnight timer",
#     on_calendar="@daily",
# )


# service_timer.schedule()


import os
if not os.path.exists("logg"):

    os.mkdir("logg")

file_abspath = os.path.abspath("logg/test.py")
print(file_abspath)
with open(file_abspath, "w") as f:
    pass
