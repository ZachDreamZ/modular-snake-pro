; Inno Setup Script for Snake Gradient
; Run with: iscc installer.iss

#define MyAppName "Snake Gradient"
#define MyAppVersion "0.0.7"
#define MyAppPublisher "Modular Snake Pro"
#define MyAppURL "https://github.com/anomalyco/modular-snake-pro"
#define MyAppExeName "SnakeGradient.exe"

[Setup]
AppId={{B8A3C9D1-E2F4-4A5B-9C7D-8E1F2A3B4C5D}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
OutputDir=installer_output
OutputBaseFilename=SnakeGradient_Setup_v{#MyAppVersion}
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
UninstallDisplayIcon={app}\{#MyAppExeName}

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: checkedonce

[Files]
Source: "dist\SnakeGradient\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\SnakeGradient\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[UninstallRun]
Filename: "{app}\data\cleanup.bat"; Flags: runhidden skipifdoesntexist

[Code]
function InitializeSetup: Boolean;
begin
  Result := True;
end;
