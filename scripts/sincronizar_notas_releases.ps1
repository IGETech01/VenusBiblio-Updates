# Sincroniza as descricoes dos Releases com docs/releases/vX.Y.Z.md.
# Requer GitHub CLI autorizado na conta com permissao de manutencao do repo.
# Nao modifica tags, assets, publicacao ou chave privada.
param([string[]]$Versoes = @("v0.12.2", "v0.13.1", "v0.14.0"))
$ErrorActionPreference = 'Stop'
$repo = 'IGETech01/VenusBiblio-Updates'
$gh = (Get-Command gh -ErrorAction SilentlyContinue | Select-Object -First 1).Source
if (-not $gh) {
    $gh = @(
        "$env:ProgramFiles\GitHub CLI\gh.exe",
        "$env:LOCALAPPDATA\Programs\GitHub CLI\gh.exe",
        "$env:LOCALAPPDATA\Microsoft\WinGet\Links\gh.exe"
    ) | Where-Object { Test-Path -LiteralPath $_ -PathType Leaf } | Select-Object -First 1
}
if (-not $gh) { throw 'GitHub CLI nao localizado.' }
& $gh auth status
if ($LASTEXITCODE -ne 0) { throw 'gh nao autenticado.' }
$dir = Join-Path $env:TEMP ("VenusBiblio_Notas_" + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $dir -Force | Out-Null
try {
    foreach ($tag in $Versoes) {
        if ($tag -notmatch '^v\d+\.\d+\.\d+$') {
            throw "Versao invalida: $tag"
        }
        $arquivo = Join-Path $dir "$tag.md"
        $raw = "https://raw.githubusercontent.com/IGETech01/VenusBiblio-Updates/main/docs/releases/$tag.md"
        Invoke-WebRequest -Uri $raw -OutFile $arquivo
        if (-not (Test-Path $arquivo) -or (Get-Item $arquivo).Length -lt 120) {
            throw "Notas vazias ou ausentes: $tag"
        }
        & $gh release view $tag --repo $repo --json tagName | Out-Null
        if ($LASTEXITCODE -ne 0) { throw "Release inexistente: $tag" }
        & $gh release edit $tag --repo $repo --notes-file $arquivo
        if ($LASTEXITCODE -ne 0) { throw "Falha ao atualizar notas: $tag" }
        Write-Host "OK: descricao atualizada: $tag" -ForegroundColor Green
    }
    Write-Host 'Descricoes sincronizadas com o GitHub.' -ForegroundColor Green
}
finally {
    Remove-Item -LiteralPath $dir -Recurse -Force -ErrorAction SilentlyContinue
}
