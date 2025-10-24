# Meesho Clone - Exact Redesign Deployment Script
# This script deploys the new Navbar and Home pages

Write-Host "🚀 DEPLOYING EXACT MEESHO REDESIGN..." -ForegroundColor Cyan

# Navigate to frontend
cd "d:\Friends\meeshoo\meeshoo\frontend\src"

# Replace Navbar.js
Write-Host "📝 Replacing Navbar.js..." -ForegroundColor Yellow
Copy-Item -Path "components\Navbar_final.js" -Destination "components\Navbar.js" -Force
Write-Host "✅ Navbar.js replaced!" -ForegroundColor Green

# Replace Home.js
Write-Host "📝 Replacing Home.js..." -ForegroundColor Yellow
Copy-Item -Path "pages\Home_v3_exact.js" -Destination "pages\Home.js" -Force
Write-Host "✅ Home.js replaced!" -ForegroundColor Green

Write-Host ""
Write-Host "✅ DEPLOYMENT COMPLETE!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Next steps:" -ForegroundColor Cyan
Write-Host "1. Restart frontend: cd d:\Friends\meeshoo\meeshoo\frontend && yarn start" -ForegroundColor White
Write-Host "2. Hard refresh phone: Ctrl+Shift+R" -ForegroundColor White
Write-Host "3. Enjoy your Meesho clone! 🎉" -ForegroundColor White
