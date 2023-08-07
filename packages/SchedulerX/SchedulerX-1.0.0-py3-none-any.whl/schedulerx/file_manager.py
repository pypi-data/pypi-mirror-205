SYSTEMD_SYSTEM_DIR = r"/etc/systemd/system"


class FileManager:
    """Class contains methods to manage files in the /etc/systemd/system
    directory"""

    def __init__(self, filename: str):
        self.filename = filename

    @property
    def file_full_path(self):
        # todo: try using another folder like systemd/system/salat
        return f"{SYSTEMD_SYSTEM_DIR}/{self.filename}"

    def create_file(self, content):
        """Create a file at /etc/systemd/system/ and add write permission to it

        Args:
            content (string): what to write at /etc/systemd/system/$filename
        """

        # create the file
        with open(f"{self.file_full_path}", "w") as service_file:
            service_file.write(content)


if __name__ == "__main__":
    file_manager = FileManager("ztest.txt")
    file_manager.create_file("hello world")
