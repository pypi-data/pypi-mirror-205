from schedulerx import FileManager


class ServiceManager:
    """Service class manages: create the service file
    Args:
        filename (string): name of the service file with extension
        command (string): command to run
    """

    def __init__(
        self,
        filename: str,
        command: str,
        description: str = "",
    ):
        self.filename: str = filename
        self.description = description
        self.command = command

    def create_service_file(self):
        self.file_manager = FileManager(self.filename)
        self.file_manager.create_file(content=self._get_service_text())

    def _get_service_text(self):
        return f"""[Unit]
Description={self.description}


[Service]
ExecStart={self.command}

[Installer]
WantedBy=multi-user.target
"""


if __name__ == "__main__":
    service_manager = ServiceManager(
        filename="test.service", command="siir tkhra"
    )
    service_manager.create_service_file()
