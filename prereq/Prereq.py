from prereq.Helper import Helper;
from error_handler import Error_Handler as e;

class Prereq :

    def __init__(self):
        super().__init__();
        self.exceptions = [
            e.JavaInstallationFailure,
            e.Pip3InstallationException,
            e.Python3InstallationFailure,
            e.SparkInstallationFailure,
            e.WgetInstallationException
        ]

    def install_prereqs(self, connection, os="ubuntu" ) :
        helper = Helper()
        helper.download_and_install_tar(connection, component="JAVA", os="ubuntu")
        helper.download_and_install_tar(connection, component="SPARK", os="ubuntu")
        helper.install_package(connection, "python3", os)
        helper.install_package(connection, "pip3", os)
        helper.install_package(connection, "psutil", os)