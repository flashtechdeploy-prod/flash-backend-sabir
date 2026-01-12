# Flash ERP API Test Script - After Employee2 Removal
# Tests Employee CRUD and Related Table Endpoints

Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "  FLASH ERP API ENDPOINT TESTING" -ForegroundColor Cyan
Write-Host "  (After Employee2 Table Consolidation)" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

$baseUrl = "http://localhost:8000"

# Login
Write-Host "[AUTH] Logging in..." -ForegroundColor Yellow
try {
    $login = Invoke-RestMethod -Uri "$baseUrl/api/auth/login" -Method POST -Body "username=superadmin&password=string" -ContentType "application/x-www-form-urlencoded"
    $headers = @{Authorization = "Bearer $($login.access_token)"}
    Write-Host "[AUTH] Login successful!" -ForegroundColor Green
    Write-Host ""
} catch {
    Write-Host "[AUTH] Login FAILED: $_" -ForegroundColor Red
    exit 1
}

$passed = 0
$failed = 0

function Test-Endpoint {
    param($name, $url, $method = "GET")
    Write-Host "  $name ... " -NoNewline
    try {
        $response = Invoke-RestMethod -Uri "$baseUrl$url" -Method $method -Headers $headers -ErrorAction Stop
        Write-Host "PASS" -ForegroundColor Green
        $script:passed++
        return $response
    } catch {
        Write-Host "FAIL - $($_.Exception.Message)" -ForegroundColor Red
        $script:failed++
        return $null
    }
}

# ============== EMPLOYEE CRUD TESTS ==============
Write-Host "[EMPLOYEES - CRUD]" -ForegroundColor Cyan
Test-Endpoint "GET /api/employees/" "/api/employees/"
Test-Endpoint "GET /api/employees/by-db-id/1" "/api/employees/by-db-id/1"
Test-Endpoint "GET /api/employees/kpis" "/api/employees/kpis"
Test-Endpoint "GET /api/employees/departments/list" "/api/employees/departments/list"
Test-Endpoint "GET /api/employees/designations/list" "/api/employees/designations/list"
Test-Endpoint "GET /api/employees/allocated/active" "/api/employees/allocated/active"
Write-Host ""

# ============== ATTENDANCE TESTS ==============
Write-Host "[ATTENDANCE]" -ForegroundColor Cyan
Test-Endpoint "GET /api/attendance/summary" "/api/attendance/summary"
Write-Host ""

# ============== PAYROLL TESTS ==============
Write-Host "[PAYROLL]" -ForegroundColor Cyan
Test-Endpoint "GET /api/payroll/payment-status" "/api/payroll/payment-status"
Test-Endpoint "GET /api/payroll/sheet-entries" "/api/payroll/sheet-entries"
Write-Host ""

# ============== CLIENT MANAGEMENT TESTS ==============
Write-Host "[CLIENT MANAGEMENT]" -ForegroundColor Cyan
Test-Endpoint "GET /api/client-management/clients" "/api/client-management/clients"
Test-Endpoint "GET /api/client-management/statistics" "/api/client-management/statistics"
Write-Host ""

# ============== ADVANCES TESTS ==============
Write-Host "[ADVANCES]" -ForegroundColor Cyan
Test-Endpoint "GET /api/advances/employees/1/summary" "/api/advances/employees/1/summary"
Test-Endpoint "GET /api/advances/employees/1/advances" "/api/advances/employees/1/advances"
Write-Host ""

# ============== INVENTORY TESTS ==============
Write-Host "[INVENTORY]" -ForegroundColor Cyan
Test-Endpoint "GET /api/general-inventory/items" "/api/general-inventory/items"
Test-Endpoint "GET /api/restricted-inventory/items" "/api/restricted-inventory/items"
Test-Endpoint "GET /api/inventory-assignments/" "/api/inventory-assignments/"
Write-Host ""

# ============== FINANCE TESTS ==============
Write-Host "[FINANCE]" -ForegroundColor Cyan
Test-Endpoint "GET /api/finance/accounts" "/api/finance/accounts"
Test-Endpoint "GET /api/expenses/" "/api/expenses/"
Write-Host ""

# ============== SUMMARY ==============
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "  TEST SUMMARY" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "  PASSED: $passed" -ForegroundColor Green
Write-Host "  FAILED: $failed" -ForegroundColor $(if ($failed -gt 0) { "Red" } else { "Green" })
Write-Host ""

if ($failed -eq 0) {
    Write-Host "  All tests passed! Employee2 removal successful." -ForegroundColor Green
} else {
    Write-Host "  Some tests failed. Please review the errors above." -ForegroundColor Yellow
}
