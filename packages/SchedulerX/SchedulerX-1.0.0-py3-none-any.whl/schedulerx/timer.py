from schedulerx import ServiceManager
from schedulerx import CommandHandler
from schedulerx import FileManager


class TimerManager:
    """

    Args:
        service_manager (ServiceManager): service manager instance linked to
        to this timer instance
        description (str): timer_description
    """

    def __init__(
        self,
        filename: str,
        on_calendar: str,
        service_manager: ServiceManager,
        description: str = "",
    ) -> None:

        self.filename = filename
        self.description = description
        self.on_calendar = on_calendar
        self.service_manager: ServiceManager = service_manager

        self.file_manager = FileManager(filename=self.filename)
        self.command_handler = CommandHandler()

    def create_timer(self):
        self.file_manager.create_file(self._get_timer_text())

    def _get_timer_text(self):
        return f"""[Unit]
Description={self.description}
Requires={self.service_manager.filename}


[Timer]
OnCalendar={self.on_calendar}
Unit={self.service_manager.filename}

[Install]
WantedBy=multi-user.target
"""

    def start_timer(self):
        # reload daemon process
        self.command_handler.run_shell_command("systemctl daemon-reload")
        # start timer
        self.command_handler.run_shell_command(
            f"systemctl start {self.filename}"
        )

    def enable_timer(self):

        # self.logger.debug("enable timer")
        self.command_handler.run_shell_command(
            f"systemctl enable {self.filename}"
        )


if __name__ == "__main__":
    title = "tes"
    sm = ServiceManager(f"{title}.service", "siir tzft from tmer")
    sm.create_service_file()
    tm = TimerManager(f"{title}.timer",
                      on_calendar="12:12:12", service_manager=sm)
    tm.create_timer()
    # os.remove(f"/etc/systemd/system/{title}.service")
    # os.remove(f"/etc/systemd/system/{title}.timer")
