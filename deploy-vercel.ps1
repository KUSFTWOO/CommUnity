# CommUnity Vercel 배포 스크립트
# 사용법: PowerShell에서 .\deploy-vercel.ps1

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

Write-Host "=== CommUnity Vercel 배포 ===" -ForegroundColor Cyan

# Vercel CLI 확인
if (-not (Get-Command vercel -ErrorAction SilentlyContinue)) {
    Write-Host "Vercel CLI가 없습니다. 설치: npm i -g vercel" -ForegroundColor Red
    exit 1
}

$vercelVersion = vercel --version 2>&1 | Select-Object -First 1
Write-Host "Vercel CLI: $vercelVersion"

# 로그인 확인
$whoami = vercel whoami 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "`nVercel 로그인이 필요합니다. 브라우저에서 인증을 완료하세요." -ForegroundColor Yellow
    vercel login
}

Write-Host "`n로그인 계정:" -ForegroundColor Green
vercel whoami

Write-Host "`nDATABASE_URL 확인..." -ForegroundColor Cyan
$envList = vercel env ls 2>&1 | Out-String
if ($envList -notmatch "DATABASE_URL") {
    Write-Host "경고: DATABASE_URL이 없습니다. Neon/Supabase 등 PostgreSQL 연결 후 재배포하세요." -ForegroundColor Yellow
    Write-Host "  약관: https://vercel.com/twoo00-5507s-projects/~/integrations/accept-terms/neon?source=cli" -ForegroundColor Yellow
    Write-Host "  설치: vercel integration add neon" -ForegroundColor Yellow
}

Write-Host "`n프로덕션 배포를 시작합니다..." -ForegroundColor Cyan
vercel deploy --prod --yes

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n배포 완료!" -ForegroundColor Green
} else {
    Write-Host "`n배포 실패. 로그를 확인하세요." -ForegroundColor Red
    exit $LASTEXITCODE
}
