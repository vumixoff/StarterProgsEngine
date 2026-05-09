[Setup]
AppName=StarterProgsEngine
AppVersion=1.0
AppPublisher=StarterProgsEngine
DefaultDirName={autopf}\StarterProgsEngine
DefaultGroupName=StarterProgsEngine
OutputDir=installer
OutputBaseFilename=StarterProgsEngine_Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
SetupIconFile=rocket_new.ico
UninstallDisplayIcon={app}\StarterProgsEngine.exe

[Files]
Source: "dist\StarterProgsEngine.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\StarterProgsEngine"; Filename: "{app}\StarterProgsEngine.exe"
Name: "{autodesktop}\StarterProgsEngine"; Filename: "{app}\StarterProgsEngine.exe"

[Run]
Filename: "{app}\StarterProgsEngine.exe"; Description: "Запустить StarterProgsEngine"; Flags: nowait postinstall skipifsilent