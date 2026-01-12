# Production Deployment Checklist - Image Upload Fix

## Pre-Deployment

- [ ] All code changes committed to Git
- [ ] `.env` file created locally with B2 credentials (for testing)
- [ ] Local image upload tested and working
- [ ] Check server logs show successful uploads

## Deployment Steps

### 1. Push Code to Git
```bash
cd C:\Users\HomePC\Desktop\erp-prod
git add -A
git commit -m "Fix: Configure B2 cloud storage for image uploads on production"
git push origin main
```

### 2. Configure Vercel Environment Variables
Go to: **Vercel Dashboard → Your Project → Settings → Environment Variables**

Add these variables (set for **Production**):
```
B2_KEY_ID = [your_b2_key_id]
B2_APPLICATION_KEY = [your_b2_application_key]
B2_BUCKET_NAME = [your_bucket_name]
B2_ENDPOINT_URL = https://s3.us-east-005.backblazeb2.com
```

- [ ] B2_KEY_ID added
- [ ] B2_APPLICATION_KEY added
- [ ] B2_BUCKET_NAME added
- [ ] B2_ENDPOINT_URL added

### 3. Redeploy on Vercel
- [ ] Go to **Deployments** tab
- [ ] Find the latest deployment
- [ ] Click **Redeploy** button (or push new code to trigger auto-deploy)

## Post-Deployment Verification

### Test in Production
1. Go to https://flash-backend-sabir.vercel.app/
2. Log in with test account
3. Try to upload an image
4. Verify image appears and loads correctly

### Check Vercel Logs
- [ ] Go to Deployments → Latest → Logs
- [ ] Look for: `Uploading file:` message
- [ ] Look for: `File uploaded successfully:` message
- [ ] No error messages about B2 credentials

### Alternative: Check Backend Logs
If Vercel logs don't show upload messages, check if there's a separate backend logs view

## Rollback Plan

If something goes wrong:
```bash
# Revert the last commit
git revert HEAD
git push origin main
```

Then remove the environment variables from Vercel and redeploy.

## Success Indicators

✅ Images upload without error
✅ Server logs show upload progress
✅ Image URLs are returned correctly  
✅ Images load from B2 cloud storage
✅ Frontend displays images properly

## Troubleshooting

If uploads still fail after deployment:

1. **Verify credentials** - Log in to Backblaze account and check key/bucket
2. **Check Vercel logs** - Look for specific error messages
3. **Re-add environment variables** - Sometimes they need to be re-entered
4. **Restart deployment** - Sometimes helps with environment variable propagation

See `docs/IMAGE_UPLOAD_TROUBLESHOOTING.md` for detailed debugging steps.
