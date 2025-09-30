# ----------------------------------------
# PowerShell Script: push-adk-web.ps1
# Builds and pushes adk-web image to Google Artifact Registry using OAuth2
# ----------------------------------------

# Configurable values
$serviceName = "adk-web"
$imageTag = "asia-south1-docker.pkg.dev/ai-analyst-for-startup-eval/ai-analyst-ui/adk-web:latest"
$registry = "asia-south1-docker.pkg.dev"
$projectId = "ai-analyst-for-startup-eval"
$gcloudInstallerUrl = "https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe"
$installerPath = "$env:TEMP\GoogleCloudSDKInstaller.exe"

Write-Host "`n[Step 1] Checking for gcloud CLI..." -ForegroundColor Cyan
if (-not (Get-Command gcloud -ErrorAction SilentlyContinue)) {
    Write-Host "`n[Info] gcloud CLI not found. Downloading installer..." -ForegroundColor Yellow
    Invoke-WebRequest -Uri $gcloudInstallerUrl -OutFile $installerPath
    Write-Host "`n[Info] Launching Google Cloud SDK installer..." -ForegroundColor Yellow
    Start-Process -FilePath $installerPath -Wait

    Write-Host "`n[Info] Please complete the installation and restart this script." -ForegroundColor Yellow
    exit 1
}

Write-Host "`n[Step 2] Verifying gcloud login..." -ForegroundColor Cyan
$account = gcloud auth list --filter=status:ACTIVE --format="value(account)"
if (-not $account) {
    Write-Host "`n[Info] No active account found. Launching login flow..." -ForegroundColor Yellow
    gcloud auth login
    $account = gcloud auth list --filter=status:ACTIVE --format="value(account)"
    if (-not $account) {
        Write-Host "`n[Error] Login failed. Cannot proceed." -ForegroundColor Red
        exit 1
    }
}

Write-Host "`n[Step 3] Setting project..." -ForegroundColor Cyan
gcloud config set project $projectId
if ($LASTEXITCODE -ne 0) {
    Write-Host "`n[Error] Failed to set project." -ForegroundColor Red
    exit 1
}

Write-Host "`n[Step 4] Authenticating Docker with OAuth2 token..." -ForegroundColor Cyan
$token = gcloud auth print-access-token
if (-not $token) {
    Write-Host "`n[Error] Failed to retrieve access token." -ForegroundColor Red
    exit 1
}
$loginCommand = "docker login -u oauth2accesstoken --password-stdin https://$registry"
$processInfo = New-Object System.Diagnostics.ProcessStartInfo
$processInfo.FileName = "docker"
$processInfo.Arguments = "login -u oauth2accesstoken --password-stdin https://$registry"
$processInfo.RedirectStandardInput = $true
$processInfo.UseShellExecute = $false
$processInfo.CreateNoWindow = $true
$process = [System.Diagnostics.Process]::Start($processInfo)
$process.StandardInput.WriteLine($token)
$process.StandardInput.Close()
$process.WaitForExit()
if ($process.ExitCode -ne 0) {
    Write-Host "`n[Error] Docker login failed." -ForegroundColor Red
    exit 1
}

Write-Host "`n[Step 5] Building and pushing multi-architecture image using docker buildx bake..." -ForegroundColor Cyan

docker buildx version 2>$null
if (-not $?) {
	Write-Host "`n[Info] docker buildx not found. Creating a builder instance..." --ForegroundColor Yellow
	$createBuilder = docker buildx create --use --name mybuilder
	if (-not $createBuilder) {
		Write-Host "`n[Error] Failed to create docker buildx builder." --ForegroundColor Red
		exit 1
	}
}

docker buildx bake $serviceName --push
if (-not $?) {
    Write-Host "`n[Error] Docker bake failed to build and push image." -ForegroundColor Red
    exit 1
}

Write-Host "`n[Success] Multi-architecture image pushed successfully to Artifact Registry!" -ForegroundColor Green

Write-Host "`n[Step 6] Listing image tags..." -ForegroundColor Cyan
gcloud artifacts docker tags list asia-south1-docker.pkg.dev/ai-analyst-for-startup-eval/ai-analyst-ui/adk-web
