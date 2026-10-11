<#
.SYNOPSIS
    Install or update KubeScope on Windows from the files of its GitHub release.

.DESCRIPTION
    irm https://raw.githubusercontent.com/dcotecnologia/kubescope/main/install.ps1 | iex

    It picks the latest release (or the one you name), checks the installer against
    the sha256 that GitHub publishes for it, and runs it silently for the current
    user, with no administrator rights. Run it again to update. On Linux use
    install.sh; there is no macOS package yet.

    To pass options, save the file and run it: .\install.ps1 -Version 0.1.0

.PARAMETER Version
    The release to install, for example 0.1.0. The default is the latest.

.PARAMETER Force
    Install even if that version is already installed.

.PARAMETER DryRun
    Show what would be done and change nothing.

.NOTES
    For tests and mirrors: KUBESCOPE_REPO (owner/name) and KUBESCOPE_API (the API
    URL, https only).
#>
[CmdletBinding()]
param(
    [string]$Version = 'latest',
    [switch]$Force,
    [switch]$DryRun
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
# A script run through `iex` must not call `exit`, which would close the user's
# window; `throw` stops it and shows the message.

$Repo = if ($env:KUBESCOPE_REPO) { $env:KUBESCOPE_REPO } else { 'dcotecnologia/kubescope' }
$Api = if ($env:KUBESCOPE_API) { $env:KUBESCOPE_API } else { 'https://api.github.com' }
# The AppId of the Inno Setup installer; its uninstall entry records the version.
$AppId = '{6E1D5B0A-4C2E-4F5C-9A57-3B8E0D6C7A11}'

if ($PSVersionTable.PSEdition -eq 'Core' -and -not $IsWindows) {
    throw "install.ps1 is for Windows. On Linux use install.sh: curl -fsSL https://raw.githubusercontent.com/$Repo/main/install.sh | sh"
}
if (-not [Environment]::Is64BitOperatingSystem) {
    throw 'Only 64-bit Windows packages are published.'
}
if (-not $Api.StartsWith('https://')) {
    throw 'KUBESCOPE_API must be an https URL.'
}
[Net.ServicePointManager]::SecurityProtocol =
    [Net.ServicePointManager]::SecurityProtocol -bor [Net.SecurityProtocolType]::Tls12

function Get-InstalledVersion {
    $entry = "Microsoft\Windows\CurrentVersion\Uninstall\${AppId}_is1"
    foreach ($root in 'HKCU:\Software', 'HKLM:\Software', 'HKLM:\Software\WOW6432Node') {
        $key = Join-Path $root $entry
        if (Test-Path $key) {
            return (Get-ItemProperty $key).DisplayVersion
        }
    }
    return $null
}

function Test-Newer([string]$A, [string]$B) {
    try {
        return ([version]$A) -gt ([version]$B)
    } catch {
        return $false
    }
}

$Version = $Version.TrimStart('v')
$url = if ($Version -eq 'latest') {
    "$Api/repos/$Repo/releases/latest"
} else {
    "$Api/repos/$Repo/releases/tags/v$Version"
}
try {
    $release = Invoke-RestMethod -Uri $url -Headers @{ 'User-Agent' = 'kubescope-install' }
} catch {
    throw "Could not read the release at $url (does that version exist? is GitHub rate limiting you?)"
}
$target = $release.tag_name.TrimStart('v')
$name = "KubeScope-$target-windows-x64-setup.exe"
$asset = $release.assets | Where-Object { $_.name -eq $name } | Select-Object -First 1
if (-not $asset) {
    throw "Release $($release.tag_name) has no file named $name."
}
$digest = if ($asset.PSObject.Properties['digest'] -and $asset.digest) {
    $asset.digest -replace '^sha256:', ''
} else {
    $null
}
if (-not $digest -and $env:KUBESCOPE_ALLOW_UNVERIFIED -ne '1') {
    throw "GitHub gives no sha256 for $name, so the download cannot be checked (set KUBESCOPE_ALLOW_UNVERIFIED=1 to go on anyway)."
}

$current = Get-InstalledVersion
if ($current -and -not $Force) {
    if ($current -eq $target) {
        Write-Host "KubeScope $current is already installed and up to date."
        return
    }
    if ($Version -eq 'latest' -and (Test-Newer $current $target)) {
        Write-Host "KubeScope $current is newer than the latest release ($target); nothing to do."
        return
    }
}
if ($current) {
    Write-Host "Updating KubeScope $current -> $target."
} else {
    Write-Host "Installing KubeScope $target."
}
Write-Host "  file:   $name"
Write-Host "  from:   $($asset.browser_download_url)"
Write-Host "  sha256: $(if ($digest) { $digest } else { 'not published' })"
Write-Host '  to:     your user account, with the installer run silently'
if ($DryRun) {
    Write-Host 'Dry run: nothing was downloaded or changed.'
    return
}

$file = Join-Path ([IO.Path]::GetTempPath()) $name
try {
    Write-Host 'Downloading...'
    $previous = $ProgressPreference
    $ProgressPreference = 'SilentlyContinue'  # the progress bar makes the download much slower
    try {
        Invoke-WebRequest -Uri $asset.browser_download_url -OutFile $file -UseBasicParsing
    } finally {
        $ProgressPreference = $previous
    }
    if ($digest) {
        $actual = (Get-FileHash -Path $file -Algorithm SHA256).Hash
        if ($actual -ne $digest.ToUpperInvariant()) {
            throw 'The sha256 of the download does not match what GitHub published; nothing was installed.'
        }
        Write-Host 'Checked the sha256.'
    }
    $process = Start-Process -FilePath $file -Wait -PassThru `
        -ArgumentList '/VERYSILENT', '/SUPPRESSMSGBOXES', '/NORESTART'
    if ($process.ExitCode -ne 0) {
        throw "The installer failed with exit code $($process.ExitCode)."
    }
    Write-Host 'Done. Start KubeScope from the Start menu.'
} finally {
    Remove-Item -Path $file -Force -ErrorAction SilentlyContinue
}
