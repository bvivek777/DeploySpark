class JavaInstallationFailure(Exception):
    def __init__(self, port: int):
        super(JavaInstallationFailure, self).__init__("Fail to install Java on port {port}.".format(port=port))


class SparkInstallationFailure(Exception):
    def __init__(self, port: int):
        super(SparkInstallationFailure, self).__init__("Fail to install Spark on port {port}.".format(port=port))


class Python3InstallationFailure(Exception):
    def __init__(self, port: int):
        super(Python3InstallationFailure, self).__init__("Fail to install Python3 on port {port}.".format(port=port))

class ProfileFailure(Exception):
    def __init__(self, port: int):
        super(ProfileFailure, self).__init__("The profile does not work on port {port}.".format(port=port))

class Pip3InstallationException(Exception) :
    def __init__(self, port: int):
        super(Pip3InstallationException, self).__init__("pip3 not installed on port {port}.".format(port=port))

class PsutilInstallationException(Exception) :
    def __init__(self, port: int):
        super(PsutilInstallationException, self).__init__("psutil library not installed on port {port}.".format(port=port))
