# Copies example images from dataset/training into the webapp public assets/examples folder
# Usage (PowerShell):
#   .\scripts\copy_examples.ps1 -MaxPerClass 5
param(
    [int]$MaxPerClass = 5
)

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Resolve-Path "$root\.."
$srcBase = Join-Path $repoRoot 'dataset\training'
$destBase = Join-Path $repoRoot 'webapp\public\assets\images\examples'

if (-not (Test-Path $destBase)) {
    New-Item -ItemType Directory -Path $destBase | Out-Null
}

$manifest = @()

# Sensitive - pull from diverse categories (computerscreen, creditcards, idcard)
$sensSrc = Join-Path $srcBase 'sensitive'
if (Test-Path $sensSrc) {
    # computerscreen examples
    Get-ChildItem -Path $sensSrc -Filter 'computerscreen*' -File | Select-Object -First $MaxPerClass | ForEach-Object {
        $dstName = "sensitive_computerscreen_$($_.Name)"
        Copy-Item -Path $_.FullName -Destination (Join-Path $destBase $dstName) -Force
        $manifest += "assets/images/examples/$dstName"
    }
    # creditcards examples
    Get-ChildItem -Path $sensSrc -Filter 'creditcards*' -File | Select-Object -First $MaxPerClass | ForEach-Object {
        $dstName = "sensitive_creditcard_$($_.Name)"
        Copy-Item -Path $_.FullName -Destination (Join-Path $destBase $dstName) -Force
        $manifest += "assets/images/examples/$dstName"
    }
    # idcard examples
    Get-ChildItem -Path $sensSrc -Filter 'idcard*' -File | Select-Object -First $MaxPerClass | ForEach-Object {
        $dstName = "sensitive_idcard_$($_.Name)"
        Copy-Item -Path $_.FullName -Destination (Join-Path $destBase $dstName) -Force
        $manifest += "assets/images/examples/$dstName"
    }
}

# Non-sensitive
$nsSrc = Join-Path $srcBase 'nonsensitive'
if (Test-Path $nsSrc) {
    Get-ChildItem -Path $nsSrc -File | Select-Object -First $MaxPerClass | ForEach-Object {
        $dstName = "nonsensitive_$($_.Name)"
        Copy-Item -Path $_.FullName -Destination (Join-Path $destBase $dstName) -Force
        $manifest += "assets/images/examples/$dstName"
    }
}

# Save manifest.json in the examples folder (relative paths from webapp/public root)
$manifestPath = Join-Path $destBase 'manifest.json'
$manifest | ConvertTo-Json | Out-File -Encoding UTF8 $manifestPath

Write-Host "Copied examples to: $destBase"
Write-Host "Manifest written to: $manifestPath"
Write-Host "Run the demo server (python -m http.server 8000) from webapp/public and open the page to see example buttons."