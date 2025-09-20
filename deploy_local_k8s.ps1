# Stop on any error
$ErrorActionPreference = "Stop"

# Define paths
$manifestDir = ".\k8s-manifests"
$logDir = ".\logs"

# Ensure required directories exist
New-Item -ItemType Directory -Force -Path $manifestDir | Out-Null
New-Item -ItemType Directory -Force -Path $logDir | Out-Null

Write-Host "`n[Step 1] Checking for kubectl..."
if (-not (Get-Command kubectl -ErrorAction SilentlyContinue)) {
    Write-Host "Installing kubectl..." -ForegroundColor Yellow
    $kubectlUrl = "https://dl.k8s.io/release/v1.30.1/bin/windows/amd64/kubectl.exe"
    $kubectlPath = "$env:USERPROFILE\kubectl.exe"
    Invoke-WebRequest -Uri $kubectlUrl -OutFile $kubectlPath
    $env:PATH += ";$($env:USERPROFILE)"
}

Write-Host "`n[Step 2] Checking for kompose..."
if (-not (Get-Command kompose -ErrorAction SilentlyContinue)) {
    Write-Host "Installing kompose..." -ForegroundColor Yellow
    $komposeUrl = "https://github.com/kubernetes/kompose/releases/download/v1.31.2/kompose-windows-amd64.exe"
    $komposePath = "$env:USERPROFILE\kompose.exe"
    Invoke-WebRequest -Uri $komposeUrl -OutFile $komposePath
    $env:PATH += ";$($env:USERPROFILE)"
}

Write-Host "`n[Step 3] Setting Kubernetes context..."
kubectl config use-context docker-desktop

Write-Host "`n[Step 4] Building Docker images..."
docker build -t ai-analyst-agent:latest -f agents/Dockerfile .
docker build -t api-app:latest -f api_app/Dockerfile .

Write-Host "`n[Step 5] Tagging images with localhost prefix..."
docker tag ai-analyst-agent:latest localhost/ai-analyst-agent:latest
docker tag api-app:latest localhost/api-app:latest

Write-Host "`n[Step 6] Verifying local images..."
$images = @("localhost/ai-analyst-agent", "localhost/api-app")
foreach ($image in $images) {
    if (-not (docker images -q "$image:latest")) {
        Write-Host "❌ Missing image: $image:latest" -ForegroundColor Red
        exit 1
    } else {
        Write-Host "✅ Found image: $image:latest" -ForegroundColor Green
    }
}

Write-Host "`n[Step 7] Converting docker-compose to Kubernetes manifests..."
kompose convert --out $manifestDir

Write-Host "`n[Step 8] Patching deployment YAMLs with localhost image and imagePullPolicy: Never..."
Get-ChildItem -Path $manifestDir -Filter *deployment.yaml | ForEach-Object {
    Write-Host "Patching $($_.Name)..."
    $lines = Get-Content $_.FullName
    $patched = @()
    for ($i = 0; $i -lt $lines.Count; $i++) {
        $line = $lines[$i]
        if ($line -match '^\s*image:\s*(ai-analyst-agent|api-app):latest') {
            $indent = ($line -match '^(\s*)')[1]
            $imageName = $line -replace '^\s*image:\s*', ''
            $patched += "${indent}image: localhost/${imageName}"
            if ($i+1 -ge $lines.Count -or $lines[$i+1] -notmatch 'imagePullPolicy:') {
                $patched += "${indent}  imagePullPolicy: Never"
            }
        } else {
            $patched += $line
        }
    }
    Set-Content $_.FullName $patched
}

Write-Host "`n[Step 9] Saving logs from existing pods..."
foreach ($label in @("ai-analyst-agent", "api-app")) {
    $pods = kubectl get pods -l app=$label -o jsonpath='{.items[*].metadata.name}'
    foreach ($pod in $pods -split ' ') {
        if ($pod) {
            Write-Host "Saving logs for pod: $pod"
            kubectl logs $pod | Out-File "$logDir\$pod.log"
        }
    }
}

Write-Host "`n[Step 10] Cleaning up old deployments and pods..."
foreach ($label in @("ai-analyst-agent", "api-app")) {
    kubectl delete deployment $label --ignore-not-found
    kubectl delete pod -l app=$label --ignore-not-found
}

Write-Host "`n[Step 11] Reapplying Kubernetes manifests..."
Get-ChildItem -Path $manifestDir -Filter *.yaml | ForEach-Object {
    Write-Host "Applying $($_.Name)..."
    kubectl apply -f $_.FullName
}

Write-Host "`n[Step 12] Verifying pod startup..."
Start-Sleep -Seconds 5
kubectl get pods -w

Write-Host "`n✅ Deployment complete using local images."
