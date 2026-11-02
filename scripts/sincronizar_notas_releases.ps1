# Sincroniza as descricoes dos Releases existentes com docs/releases/vX.Y.Z.md.
# Sem parametros: detecta automaticamente as versoes que estao publicadas.
# Nao cria, exclui, assina, publica nem modifica assets ou tags.
param([string[]]$Versoes)
$ErrorActionPreference = 'Stop'
$repo = 'IGETech01/VenusBiblio-Updates'

$comando = Get-Command gh -ErrorAction SilentlyContinue
$gh = if ($comando) { $comando.Source } else { $null }
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

$json = & $gh release list --repo $repo --limit 100 --json tagName
if ($LASTEXITCODE -ne 0) { throw 'Nao foi possivel listar os Releases.' }
$existentes = @($json | ConvertFrom-Json | ForEach-Object { $_.tagName })
if (-not $Versoes -or $Versoes.Count -eq 0) {
    $Versoes = @($existentes | Where-Object { $_ -match '^v\d+\.\d+\.\d+$' })
}
$pasta = Join-Path $env:TEMP ("VenusBiblio_Notas_" + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $pasta -Force | Out-Null
try {
    $total = 0
    foreach ($tag in $Versoes) {
        if ($tag -notmatch '^v\d+\.\d+\.\d+$') {
            throw "Versao invalida: $tag"
        }
        if ($existentes -notcontains $tag) {
            Write-Warning "Release $tag nao existe no GitHub; ignorando."
            continue
        }
        $arquivo = Join-Path $pasta "$tag.md"
        $url = "https://raw.githubusercontent.com/IGETech01/VenusBiblio-Updates/main/docs/releases/$tag.md"
        try {
            Invoke-WebRequest -Uri $url -OutFile $arquivo -UseBasicParsing
        }
        catch {
            Write-Warning "Notas de $tag nao encontradas; ignorando."
            continue
        }
        if ((Get-Item -LiteralPath $arquivo).Length -lt 120) {
            throw "Notas vazias ou incompletas: $tag"
        }
        & $gh release edit $tag --repo $repo --notes-file $arquivo
        if ($LASTEXITCODE -ne 0) { throw "Falha ao atualizar notas: $tag" }
        $total += 1
        Write-Host "OK: descricao sincronizada para $tag" -ForegroundColor Green
    }
    Write-Host "Sincronizacao concluida ($total descricoes)." -ForegroundColor Green
}
finally {
    Remove-Item -LiteralPath $pasta -Recurse -Force -ErrorAction SilentlyContinue
}
