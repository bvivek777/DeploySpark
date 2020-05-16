from error_handler.Error_Handler import *;
import json;
# Installs the pre requisites For spark installation
# and Data CPU state collection
class Helper :

    def __init__(self, mode=1):
        super().__init__();
        self.mode = 1;
        with open("../commands.json") as install_commands :
            self.commands = json.load(install_commands);

    def check_install( self, connection, component, os = "ubuntu" ) -> bool :
        print("Checking installation for : "+component);
        try :
            version = connection.run(self.commands[os]["check"][component]);
            if component == "java" :
                version.stdout.split('"')[1].split(".")[0];
                if int(version) > 8 :
                    return True;
            if component == "pip3" :
                version = version.stdout.split(" ")[1].split(".")[0];
                if ( int(version) > 8 ) :
                    return True;
        except :
            pass
        print(component+": not installed");
        return False;

    def __install_pkg( self, connection, component, os ) :
        print("Installing "+component+" using package manager");
        connection.run( self.commands[os][component] );
        print(component+" installation complete");

    # install java on to remote machines
    def install_java( self, connection, os = "ubuntu" ) :
        # check if there is a previous version of java installed
        if ( self.check_install(connection, "java", os ) ) :
            return;
        try :
            if ( self.mode == 1 ) :
                self.__install_pkg(connection, "java", os );
            else :
                print("Using URL to get openjdk")
                # to install from disk
        except :
            raise JavaInstallationFailure;
    
    # install python3 if it doesnt exist
    def install_python3( self, connection, os = "ubuntu") :        
        if ( self.check_install(connection, "python3", os ) ) :
            return;
        try :
            if ( self.mode == 1 ) :
                self.__install_pkg( connection, "python3", os );
            else :
                print("Getting python3 from URL")
        except :        
            raise Python3InstallationFailure;
    
    # install pip3 and psutils
    def install_pip3 ( self, connection, os = "ubuntu") :
        if ( self.check_install(connection, "pip3", os)) :
            return;
        try :
            if ( self.mode == 1 ) :
                self.__install_pkg( connection, "pip3", os );
                connection.run( self.commands[os]["psutil"]);
            else :
                print("Upload pip from URL");
        except :
            raise Pip3InstallationException;
    
    def install_spark ( self, connection, os = "ubuntu") :
        print("Installing Spark")

    def upload_file(self, connection, file, dest) :
        print("Uploading "+file)
        

