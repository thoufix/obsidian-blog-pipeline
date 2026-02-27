# PowerShell Script for Windows - Obsidian Blog Image Processor
# 
# WORKFLOW:
#   Obsidian Git plugin auto-commits .md files every 10 minutes
#   This script processes images and ensures they're committed with the .md files
#
# USAGE:
#   powershell -ExecutionPolicy Bypass -File "C:\Users\AI\deploy-blog.ps1"

# Set variables
$postsPath = "D:\Sandbox\Dev\obsidian-blog-pipeline\hugo-site\content\posts"
$myrepo = "https://github.com/thoufix/obsidian-blog-pipeline.git"
$projectRoot = "D:\Sandbox\Dev\obsidian-blog-pipeline"

# Set error handling
$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

# Change to project root
Set-Location $projectRoot

# Check for required commands
if (-not (Get-Command 'git' -ErrorAction SilentlyContinue)) {
    Write-Error "Git is not installed or not in PATH."
    exit 1
}

# Check for Python command (python or python3)
if (Get-Command 'python' -ErrorAction SilentlyContinue) {
    $pythonCommand = 'python'
} elseif (Get-Command 'python3' -ErrorAction SilentlyContinue) {
    $pythonCommand = 'python3'
} else {
    Write-Error "Python is not installed or not in PATH."
    exit 1
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Obsidian Blog - Image Processor" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Process images with Python script
Write-Host "[1/3] Processing image links..." -ForegroundColor Yellow
if (-not (Test-Path "scripts\images.py")) {
    Write-Error "Python script images.py not found."
    exit 1
}

try {
    & $pythonCommand scripts\images.py
    Write-Host "  Image processing complete!" -ForegroundColor Green
} catch {
    Write-Error "Failed to process image links."
    exit 1
}

# Step 2: Check Git repository
Write-Host "[2/3] Checking Git repository..." -ForegroundColor Yellow
if (-not (Test-Path ".git")) {
    Write-Host "Initializing Git repository..." -ForegroundColor Yellow
    git init
    git remote add origin $myrepo
} else {
    $remotes = git remote
    if (-not ($remotes -contains 'origin')) {
        Write-Host "Adding remote origin..." -ForegroundColor Yellow
        git remote add origin $myrepo
    } else {
        Write-Host "  Git repository ready." -ForegroundColor Green
    }
}

# Step 3: Stage, commit, and push
Write-Host "[3/3] Staging and pushing changes..." -ForegroundColor Yellow
$hasChanges = (git status --porcelain) -ne ""
if (-not $hasChanges) {
    Write-Host "  No changes to commit (Obsidian Git may have already committed)." -ForegroundColor Gray
} else {
    git add .
    
    $commitMessage = "Blog update: images processed on $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
    git commit -m "$commitMessage"
    Write-Host "  Committed: $commitMessage" -ForegroundColor Green
    
    git push origin master
    Write-Host "  Push complete!" -ForegroundColor Green
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  Done! Woodpecker will deploy!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "What happens next:" -ForegroundColor Cyan
Write-Host "  1. Woodpecker CI on Pi 5 detects the push"
Write-Host "  2. Hugo builds the site (on Pi 5)"
Write-Host "  3. Site deploys to blog.pilab.space"
Write-Host ""
Write-Host "Monitor: https://github.com/thoufix/obsidian-blog-pipeline/actions" -ForegroundColor Cyan
Write-Host ""
