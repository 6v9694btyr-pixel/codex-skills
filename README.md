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
