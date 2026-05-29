# Supabase/PostgreSQL DATABASE_URL을 Vercel Production에 등록합니다.
# 사용법:
#   $env:DATABASE_URL = "postgresql://postgres.[ref]:[password]@...pooler.supabase.com:6543/postgres"
#   .\scripts\set-vercel-database.ps1
#
# Supabase: Project Settings → Database → Connection string (URI) → Transaction pooler

param(
    [string]$DatabaseUrl = $env:DATABASE_URL
)

$ErrorActionPreference = "Stop"
Set-Location (Split-Path $PSScriptRoot -Parent)

if (-not $DatabaseUrl) {
    Write-Host "DATABASE_URL이 비어 있습니다." -ForegroundColor Red
    Write-Host "Supabase 예시 (프로젝트 ref: ijzifreevyhgndqasokn):"
    Write-Host '  postgresql://postgres.ijzifreevyhgndqasokn:[PASSWORD]@aws-0-ap-northeast-2.pooler.supabase.com:6543/postgres'
    exit 1
}

Write-Host "Vercel에 DATABASE_URL 등록 중..." -ForegroundColor Cyan
echo $DatabaseUrl | vercel env add DATABASE_URL production --force
echo $DatabaseUrl | vercel env add DATABASE_URL preview --force

Write-Host "재배포 중..." -ForegroundColor Cyan
vercel deploy --prod --yes

Write-Host "완료." -ForegroundColor Green
