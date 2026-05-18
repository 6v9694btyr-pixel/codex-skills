param(
    [string]$VaultPath = $PSScriptRoot
)

$ErrorActionPreference = "Stop"

$targets = @(
    @{
        Name = "codex"
        Source = Join-Path $VaultPath "codex"
        Destination = Join-Path $env:USERPROFILE ".codex\skills"
    },
    @{
        Name = "agents"
        Source = Join-Path $VaultPath "agents"
        Destination = Join-Path $env:USERPROFILE ".agents\skills"
    }
)

foreach ($target in $targets) {
    if (-not (Test-Path -LiteralPath $target.Source)) {
        continue
    }

    New-Item -ItemType Directory -Path $target.Destination -Force | Out-Null
    Get-ChildItem -LiteralPath $target.Source -Directory | ForEach-Object {
        $destination = Join-Path $target.Destination $_.Name
        if (Test-Path -LiteralPath $destination) {
            Remove-Item -LiteralPath $destination -Recurse -Force
        }
        Copy-Item -LiteralPath $_.FullName -Destination $destination -Recurse -Force
    }
}

Write-Host "Skills restored from $VaultPath"
