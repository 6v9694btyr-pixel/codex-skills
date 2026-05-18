param(
    [string]$VaultPath = "",
    [string]$GitRemote = "",
    [switch]$Push
)

$ErrorActionPreference = "Stop"

function Resolve-StrictPath([string]$Path) {
    if (Test-Path -LiteralPath $Path) {
        return (Resolve-Path -LiteralPath $Path).Path
    }
    return [System.IO.Path]::GetFullPath($Path)
}

function Copy-SkillDirectory([string]$Source, [string]$Destination, [string]$VaultRoot) {
    $resolvedVault = Resolve-StrictPath $VaultRoot
    $resolvedDestination = [System.IO.Path]::GetFullPath($Destination)

    if (-not $resolvedDestination.StartsWith($resolvedVault, [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "Refusing to write outside vault: $resolvedDestination"
    }

    if (Test-Path -LiteralPath $Destination) {
        Remove-Item -LiteralPath $Destination -Recurse -Force
    }

    New-Item -ItemType Directory -Path $Destination -Force | Out-Null
    Get-ChildItem -LiteralPath $Source -Force |
        Copy-Item -Destination $Destination -Recurse -Force

    Get-ChildItem -LiteralPath $Destination -Directory -Recurse -Force -Filter "__pycache__" -ErrorAction SilentlyContinue |
        Remove-Item -Recurse -Force
    Get-ChildItem -LiteralPath $Destination -File -Recurse -Force -ErrorAction SilentlyContinue |
        Where-Object { $_.Extension -in @(".pyc", ".pyo") } |
        Remove-Item -Force
}

if ($VaultPath.Trim().Length -eq 0) {
    if ($env:CODEX_SKILL_VAULT -and $env:CODEX_SKILL_VAULT.Trim().Length -gt 0) {
        $VaultPath = $env:CODEX_SKILL_VAULT
    } elseif ($PSScriptRoot -and $PSScriptRoot.Trim().Length -gt 0) {
        $VaultPath = $PSScriptRoot
    } else {
        $VaultPath = (Get-Location).Path
    }
}

$vaultFullPath = [System.IO.Path]::GetFullPath($VaultPath)
New-Item -ItemType Directory -Path $vaultFullPath -Force | Out-Null
New-Item -ItemType Directory -Path (Join-Path $vaultFullPath "codex") -Force | Out-Null
New-Item -ItemType Directory -Path (Join-Path $vaultFullPath "agents") -Force | Out-Null

if ($PSCommandPath) {
    Copy-Item -LiteralPath $PSCommandPath -Destination (Join-Path $vaultFullPath "sync-codex-skills.ps1") -Force
}

$sources = @(
    @{
        Name = "codex"
        Path = Join-Path $env:USERPROFILE ".codex\skills"
        InstallRoot = "%USERPROFILE%\.codex\skills"
        Exclude = @(".system")
    },
    @{
        Name = "agents"
        Path = Join-Path $env:USERPROFILE ".agents\skills"
        InstallRoot = "%USERPROFILE%\.agents\skills"
        Exclude = @()
    }
)

$manifest = @()

foreach ($source in $sources) {
    if (-not (Test-Path -LiteralPath $source.Path)) {
        continue
    }

    $targetRoot = Join-Path $vaultFullPath $source.Name
    Get-ChildItem -LiteralPath $source.Path -Directory | ForEach-Object {
        if (-not ($source.Exclude -contains $_.Name)) {
            $destination = Join-Path $targetRoot $_.Name
            Copy-SkillDirectory -Source $_.FullName -Destination $destination -VaultRoot $vaultFullPath

            $vaultRelativePath = Join-Path $source.Name $_.Name
            $installRelativePath = Join-Path $source.InstallRoot $_.Name
            $manifest += [PSCustomObject]@{
                source = $source.Name
                name = $_.Name
                vaultRelativePath = $vaultRelativePath
                installPath = $installRelativePath
                syncedAt = (Get-Date).ToString("o")
            }
        }
    }
}

$manifestPath = Join-Path $vaultFullPath "manifest.json"
$manifest | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $manifestPath -Encoding UTF8

$restoreScript = @'
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
'@

Set-Content -LiteralPath (Join-Path $vaultFullPath "restore-codex-skills.ps1") -Value $restoreScript -Encoding UTF8

$readme = @'
# Codex Skill Vault

This folder mirrors personal skills from:

- `%USERPROFILE%\.codex\skills`
- `%USERPROFILE%\.agents\skills`

Bundled system skills are skipped. Run `restore-codex-skills.ps1` on another Windows computer to copy these skills back into that user's default local locations.

To restore on another Windows computer:

```powershell
powershell -ExecutionPolicy Bypass -File .\restore-codex-skills.ps1
```

To sync this computer into the current vault folder:

```powershell
powershell -ExecutionPolicy Bypass -File .\sync-codex-skills.ps1
```

To sync to a specific NAS or backup folder:

```powershell
powershell -ExecutionPolicy Bypass -File .\sync-codex-skills.ps1 -VaultPath "D:\path\to\CodexSkillVault"
```

To also push to GitHub, provide a remote repository URL:

```powershell
powershell -ExecutionPolicy Bypass -File .\sync-codex-skills.ps1 -VaultPath "D:\path\to\CodexSkillVault" -GitRemote "https://github.com/OWNER/REPO.git" -Push
```
'@

Set-Content -LiteralPath (Join-Path $vaultFullPath "README.md") -Value $readme -Encoding UTF8

$git = Get-Command git -ErrorAction SilentlyContinue
if ($git) {
    $gitSafePath = $vaultFullPath.Replace("\", "/")
    & git config --global --add safe.directory $gitSafePath

    Push-Location $vaultFullPath
    try {
        if (-not (Test-Path -LiteralPath ".git")) {
            & git init | Out-Null
        }

        & git config user.name "Codex Skill Sync"
        & git config user.email "codex-skill-sync@local"

        if ($GitRemote.Trim().Length -gt 0) {
            $remoteNames = @(& git remote)
            if ($remoteNames -contains "origin") {
                & git remote set-url origin $GitRemote
            } else {
                & git remote add origin $GitRemote
            }
        }

        & git add .
        $status = (& git status --porcelain)
        if ($status) {
            & git commit -m "Sync Codex skills" | Out-Null
        }

        if ($Push) {
            if ($GitRemote.Trim().Length -eq 0 -and -not (& git remote get-url origin 2>$null)) {
                throw "No GitHub remote configured. Re-run with -GitRemote."
            }
            & git branch -M main
            & git push -u origin main
        }
    }
    finally {
        Pop-Location
    }
}

Write-Host "Skill vault synced: $vaultFullPath"
