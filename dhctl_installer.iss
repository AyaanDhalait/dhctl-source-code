[Setup]
AppName=dhctl
AppVersion=1.0
DefaultDirName={pf}\dhctl
DefaultGroupName=dhctl
OutputDir=.
OutputBaseFilename=dhctlInstaller
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\dhctl.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\dhctl"; Filename: "{app}\dhctl.exe"
Name: "{commondesktop}\dhctl"; Filename: "{app}\dhctl.exe"

[Tasks]
Name: "addtopath"; Description: "Add dhctl to PATH"; Flags: unchecked

[Registry]
Root: HKCU; Subkey: "Environment"; ValueType: expandsz; ValueName: "Path"; \
ValueData: "{olddata};{app}"; Tasks: addtopath