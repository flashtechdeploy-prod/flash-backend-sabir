# Image Upload Troubleshooting Guide

## Problem
Image uploads work locally but fail in production (Vercel deployment at `https://flash-backend-sabir.vercel.app/`).

## Root Cause
The application uses **Backblaze B2 cloud storage** for file uploads. The issue occurs because:

1. **B2 credentials were hardcoded** with empty/default values in the code
2. **Environment variables were not properly configured** on the production server (Vercel)
3. Missing error logging made it difficult to diagnose the issue

## Solution

### Step 1: Get Backblaze B2 Credentials
If you don't have a Backblaze B2 account:
1. Sign up at https://www.backblaze.com/b2/cloud-storage/
2. Create a bucket (e.g., "flash-erp-new")
3. Generate application key with read/write permissions

### Step 2: Configure Environment Variables on Vercel

Add the following environment variables to your Vercel project:

```
B2_KEY_ID=your_actual_b2_key_id
B2_APPLICATION_KEY=your_actual_b2_application_key
B2_BUCKET_NAME=your_bucket_name
B2_ENDPOINT_URL=https://s3.us-east-005.backblazeb2.com
```

**Steps to add on Vercel:**
1. Go to Vercel Dashboard → Your Project → Settings → Environment Variables
2. Add each variable above
3. Make sure they're available for Production environment
4. Redeploy the application

### Step 3: Update Local .env File

Create a `.env` file in the `flash-backend-sabir` directory (or copy from `.env.example`):

```env
# Database Configuration
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=your_db_host
DB_NAME=flashnew
DB_PORT=5432

# Backblaze B2 Configuration (REQUIRED)
B2_KEY_ID=your_actual_b2_key_id
B2_APPLICATION_KEY=your_actual_b2_application_key
B2_BUCKET_NAME=your_bucket_name
B2_ENDPOINT_URL=https://s3.us-east-005.backblazeb2.com

# CORS Origins
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173

# Other Settings
SECRET_KEY=your-secret-key-here
DEBUG=true
```

### Step 4: Test Locally

```bash
cd flash-backend-sabir
python -m uvicorn app.main:app --reload
```

Try uploading an image - check the terminal for detailed error logs.

## Code Changes Made

### 1. `app/core/config.py`
- Changed B2 credentials from hardcoded values to environment variables
- Added empty defaults so they can be read from `.env` or Vercel environment variables

### 2. `app/core/upload_helper.py`
- Added validation to check if B2 credentials are configured
- Provides clear error message if credentials are missing
- Added region specification for better S3 compatibility

### 3. `app/api/routes/core/upload.py`
- Added logging to track upload progress
- Added better error handling and debugging information
- Changed `storage_type` from "local" to "b2"

### 4. `app/api/routes/client/router.py`
- Added logging for client document uploads
- Added error handling with detailed logging

## Verification Checklist

- [ ] B2 account created with bucket
- [ ] Application key generated with read/write permissions
- [ ] Environment variables added to Vercel project
- [ ] `.env` file created locally with B2 credentials
- [ ] Backend redeployed on Vercel
- [ ] Test file upload locally - check server logs for success
- [ ] Test file upload on production - should now work

## Debugging Tips

### If uploads still fail:

1. **Check Vercel logs:**
   ```
   Dashboard → Project → Deployments → Latest → Logs
   ```

2. **Check local logs:**
   When running locally, look for:
   ```
   Uploading file: filename.jpg to folder: uploads
   File uploaded successfully: file_... -> https://s3.us-east-005.backblazeb2.com/...
   ```

3. **Verify B2 credentials:**
   - Log in to Backblaze account
   - Check that application key has read/write permissions
   - Verify bucket name matches

4. **Test B2 connection:**
   In Python:
   ```python
   import boto3
   client = boto3.client(
       "s3",
       endpoint_url="https://s3.us-east-005.backblazeb2.com",
       aws_access_key_id="YOUR_KEY_ID",
       aws_secret_access_key="YOUR_APP_KEY"
   )
   response = client.list_buckets()
   print(response)
   ```

## File Upload Flow

1. User uploads image → Frontend sends to `/api/core/upload`
2. Backend validates file
3. File is uploaded to Backblaze B2
4. File metadata is saved to PostgreSQL database
5. Frontend receives file URL and displays image

## Notes

- All image uploads go to Backblaze B2 cloud storage (not local filesystem)
- URLs are public and accessible from anywhere
- Uploaded files are organized by date and unique ID
- Original filename is preserved in database metadata
