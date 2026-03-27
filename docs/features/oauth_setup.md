# OAuth Setup Guide

## Google Cloud Console

1. Go to [console.cloud.google.com](https://console.cloud.google.com)
2. Create a new project or select an existing one
3. Go to **APIs & Services → OAuth consent screen**
   - User type: **External**
   - App name: `Second Brain`
   - User support email: your email
   - Developer contact: your email
   - Save and continue (remaining fields are optional)
4. Go to **APIs & Services → Credentials**
   - Click **+ Create Credentials → OAuth 2.0 Client ID**
   - Application type: **Web application**
   - Name: `Second Brain`
   - Under **Authorized redirect URIs** add:
     - `http://localhost:8000/api/auth/google/callback` (local)
     - `https://your-app.railway.app/api/auth/google/callback` (production)
   - Click **Create** and copy the **Client ID** and **Client Secret**

## GitHub

1. Go to [github.com/settings/developers](https://github.com/settings/developers)
2. Click **New OAuth App**
3. Fill in the form:
   - Application name: `Second Brain`
   - Homepage URL: `http://localhost:8000`
   - Authorization callback URL: `http://localhost:8000/api/auth/github/callback`
   - Click **Register application**
4. Copy the **Client ID**
5. Click **Generate a new client secret** and copy it
6. For production, create a separate OAuth App with:
   - Homepage URL: `https://your-app.railway.app`
   - Authorization callback URL: `https://your-app.railway.app/api/auth/github/callback`

## Environment Variables

Add to `.env` (local) and Railway dashboard (production):

```env
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret
APP_BASE_URL=http://localhost:8000  # or https://your-app.railway.app in production
```
