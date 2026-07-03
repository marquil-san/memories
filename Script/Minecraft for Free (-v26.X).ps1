# Requires admin privileges
$ErrorActionPreference = "Stop"

function Force-ReplaceDll {
    param (
        [string]$SourcePath,
        [string]$DestinationPath
    )

    $fileName = Split-Path $DestinationPath -Leaf
    Write-Host "`n Deleting $fileName if it exists..."

    try {
        Remove-Item -Force -Path $DestinationPath
        Write-Host "Deleted $fileName"
    } catch {
        Write-Warning "⚠️ Could not delete $fileName — may be protected or in use"
    }

    Write-Host "Copying $fileName..."
    try {
        Copy-Item -Force -Path $SourcePath -Destination $DestinationPath
        Write-Host "Copied $fileName"
    } catch {
        Write-Error "Failed to copy ${fileName}: $_"
    }
}

$Source32 = "Replace with path where you downloaded"
$Source64 = "Replace with path where you downloaded"
$Dest32 = "C:\Windows\System32\Windows.ApplicationModel.Store.dll"
$Dest64 = "C:\Windows\SysWOW64\Windows.ApplicationModel.Store.dll"

Force-ReplaceDll -SourcePath $Source32 -DestinationPath $Dest32
Force-ReplaceDll -SourcePath $Source64 -DestinationPath $Dest64
