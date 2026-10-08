; Inno Setup script. Build with: iscc /DAppVersion=0.1.0 packaging\windows\kubescope.iss
; Expects the PyInstaller output in dist\KubeScope (see KubeScope.spec).

#ifndef AppVersion
  #define AppVersion "0.0.0"
#endif

[Setup]
AppId={{6E1D5B0A-4C2E-4F5C-9A57-3B8E0D6C7A11}
AppName=KubeScope
AppVersion={#AppVersion}
AppPublisher=DCO Tecnologia
AppPublisherURL=https://github.com/dcotecnologia/kubescope
DefaultDirName={autopf}\KubeScope
DefaultGroupName=KubeScope
UninstallDisplayIcon={app}\KubeScope.exe
SetupIconFile=..\..\src\kubescope\assets\icon.ico
LicenseFile=..\..\LICENSE
OutputDir=..\..\dist
OutputBaseFilename=KubeScope-{#AppVersion}-windows-x64-setup
Compression=lzma2
SolidCompression=yes
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "..\..\dist\KubeScope\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\KubeScope"; Filename: "{app}\KubeScope.exe"
Name: "{autodesktop}\KubeScope"; Filename: "{app}\KubeScope.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\KubeScope.exe"; Description: "{cm:LaunchProgram,KubeScope}"; Flags: nowait postinstall skipifsilent
