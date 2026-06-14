$ScriptDir = $PSScriptRoot
$DevPath = Split-Path $ScriptDir -Parent

function Test-FileLocked {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path
    )

    if (!(Test-Path -LiteralPath $Path)) {
        return $false
    }

    $stream = $null
    try {
        $stream = [System.IO.File]::Open(
            $Path,
            [System.IO.FileMode]::Open,
            [System.IO.FileAccess]::ReadWrite,
            [System.IO.FileShare]::None
        )
        return $false
    }
    catch [System.IO.IOException] {
        return $true
    }
    finally {
        if ($null -ne $stream) {
            $stream.Close()
        }
    }
}

function Write-StateLockDetails {
    param(
        [Parameter(Mandatory = $true)]
        [string]$TerraformDirectory
    )

    $lockInfoPath = Join-Path $TerraformDirectory ".terraform.tfstate.lock.info"
    if (Test-Path -LiteralPath $lockInfoPath) {
        try {
            $lockInfo = Get-Content -LiteralPath $lockInfoPath -Raw | ConvertFrom-Json
            Write-Host "Terraform lock details:" -ForegroundColor Yellow
            Write-Host "  Lock ID:   $($lockInfo.ID)" -ForegroundColor Yellow
            Write-Host "  Operation: $($lockInfo.Operation)" -ForegroundColor Yellow
            Write-Host "  Who:       $($lockInfo.Who)" -ForegroundColor Yellow
            Write-Host "  Created:   $($lockInfo.Created)" -ForegroundColor Yellow
        }
        catch {
            Write-Host "Terraform lock info file exists but could not be parsed: $lockInfoPath" -ForegroundColor Yellow
        }
    }

    $terraformProcesses = Get-Process -Name terraform -ErrorAction SilentlyContinue
    if ($terraformProcesses) {
        Write-Host "Running Terraform process IDs:" -ForegroundColor Yellow
        $terraformProcesses | ForEach-Object {
            Write-Host "  $($_.Id)" -ForegroundColor Yellow
        }
    }
}

function Invoke-Terraform {
    param(
        [Parameter(Mandatory = $true)]
        [string[]]$Arguments
    )

    & terraform @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "terraform $($Arguments -join ' ') failed with exit code $LASTEXITCODE."
    }
}

Write-Host "Terraform dev path: $DevPath" -ForegroundColor Cyan

if (!(Test-Path (Join-Path $DevPath "main.tf"))) {
    Write-Host "ERROR: main.tf not found in: $DevPath" -ForegroundColor Red
    exit 1
}

Push-Location $DevPath

try {
    $statePath = Join-Path $DevPath "terraform.tfstate"
    if (Test-FileLocked -Path $statePath) {
        Write-Host "ERROR: Terraform state file is locked: $statePath" -ForegroundColor Red
        Write-StateLockDetails -TerraformDirectory $DevPath
        Write-Host "Close the other Terraform command, or stop the listed terraform.exe process if it is stale, then rerun this script." -ForegroundColor Yellow
        throw "Terraform state file is locked."
    }

    Invoke-Terraform -Arguments @("init")
    Invoke-Terraform -Arguments @("plan", "-destroy", "-out", "destroy.tfplan")

    Write-Host ""
    $confirm = Read-Host "Type DESTROY to continue"

    if ($confirm -ne "DESTROY") {
        Write-Host "Destroy cancelled." -ForegroundColor Yellow
        exit 0
    }

    Invoke-Terraform -Arguments @("apply", "destroy.tfplan")

    Write-Host "Terraform destroy completed." -ForegroundColor Green
}
finally {
    Pop-Location
}
