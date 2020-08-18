import json
import sys
import traceback

class Helper :

    def __init__(self, mode=1):
        super().__init__()
        self.mode = 1
        with open("./commands.json") as install_commands :
            self.commands = json.load(install_commands)

    def check_install( self, connection, component, os = "ubuntu" ) -> bool:
        print("Checking installation for : "+component)
        try :
            version = connection.run(self.commands[os]["check"][component])
            if component == "JAVA" :
                version.stdout.split('"')[1].split(".")[0]
                if int(version) > 8 :
                    return True
            if component == "pip3" :
                version = version.stdout.split(" ")[1].split(".")[0]
                if ( int(version) > 8 ) :
                    return True
            return True
        except :
            pass
        print(component+": not installed")
        return False

    def __install_pkg( self, connection, component, os ) -> bool:
        try :
            print("Installing "+component+" using package manager")
            connection.run( self.commands[os]["package"][component] )
            print(component+" installation complete")
            return True
        except Exception as e:
            print(e)
            print("Error installing "+component)
            return False

    def __check_file( self, connection, path, directory ) -> str, bool:
        try :
            directory = directory.split("/")
            directory = directory[len(directory)-1]
            connection.run("[[ -f "+path+directory+" ]] && echo 'true' || error")
            return directory, True
        except :
            return directory, False

    def download_and_install_tar( self, connection, component, os="ubuntu", install_path = ".", method="fs" ) -> bool:
        if ( not component in self.commands["Download"] ):
            print(" Download link for "+component+" not found in commands.json")
            return
        if ( self.check_install(connection, component, os) ):
            return
        path = "/opt/"
        proc_file = ""        
        try :
            print("Check for pre installed version")
            if method == "fs" and component in self.commands["Upload"]:
                print("Uploading Tar file") 
                file_name = self.commands["Upload"][component]
                proc_file, status = self.__check_file(connection, path, file_name)
                if ( status ):
                    print("File already exists")
                else:
                    self.upload_file(connection, file_name, path)
            elif component in self.commands["Download"]:                
                file_name = self.commands["Download"][component]
                proc_file = file_name[len(file_name)-1]
                connection.run("cd "+path)
                print("Downloading Tar file")            
                connection.run("wget -c "+self.commands["Download"][component])
            else:
                raise Exception("component command not found") 
            print("Installing "+component )
            self.install_tar(connection, component, proc_file, os, install_path)            
            return True
        except :
            print("Error Installing "+component)
            print(traceback.format_exc())
            return False
    
    def install_tar(self, connection, component, file_name, os, install_path=".") -> bool:
        print("Extracting and Installing "+component)
        path = "/opt/"
        full_path = path+file_name
        try:
            connection.run("cd "+path)
            connection.run("tar xvf "+full_path+" -C "+install_path)
            connection.run("export "+component+"_HOME="+full_path)
            connection.run("export PATH=$PATH:"+component+"_HOME/bin")
            connection.run("echo 'export "+component+"_HOME="+full_path+"' >> ~/.bashrc")
            connection.run("echo 'export PATH=$PATH:"+component+"_HOME="+full_path+"' >> ~/.bashrc")
            print("Installed "+component)
        except:
            print("Error extracting "+component)

    def install_package( self, connection, component, os="ubuntu" ) -> bool:
        if ( not component in self.commands[os]["package"] ):
            print(" command not found for "+component+" in commands.json ")
            return
        if ( self.check_install(connection, component, os) ):
            return
        res = self.__install_pkg(connection, component, os)
        return res and self.check_install(connection, component, os)

    def upload_file(self, connection, upload, dest) -> bool :
        print("Uploading "+upload)
        try :
            connection.put(upload, dest)
            return True
        except :
            return False
    
    def remove_package( self, connection, component, os ) -> bool:
        try :
            print("Installing "+component+" using package manager")
            connection.run( self.commands[os]["remove"][component] )
            print(component+" removal complete")
            return True
        except :
            print("Error removing "+component)
            return False