# Deployment Guide - Downloads Organizer

## 🚀 Railway Deployment

### Prerequisites
- GitHub repository with your code
- Railway account (free at railway.app)

### Step 1: Deploy Backend to Railway

1. **Go to Railway.app** and sign in with GitHub
2. **Click "New Project"** → "Deploy from GitHub repo"
3. **Select your repository** (organizer)
4. **Configure the service:**
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Step 2: Environment Variables

Add these environment variables in Railway dashboard:

```
DOWNLOADS_PATH=/app/downloads
SECRET_KEY=your-production-secret-key-change-this
DEBUG=False
ENVIRONMENT=production
```

### Step 3: Deploy Frontend to Vercel

1. **Go to Vercel.com** and sign in with GitHub
2. **Import your repository**
3. **Configure:**
   - **Root Directory**: `frontend`
   - **Framework**: Next.js
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`

### Step 4: Environment Variables for Frontend

In Vercel dashboard, add:

```
API_URL=https://your-railway-app.railway.app
NEXT_PUBLIC_API_URL=https://your-railway-app.railway.app
```

### Step 5: Update CORS Settings

In your Railway backend, add this environment variable:

```
CORS_ORIGINS=https://your-vercel-app.vercel.app,https://your-railway-app.railway.app
```

## 🔧 Alternative: Single Platform Deployment

### Option A: Railway (Full Stack)
- Deploy both frontend and backend to Railway
- Use Railway's static site hosting for frontend

### Option B: Render (Full Stack)
- Deploy both services to Render
- Use Render's static site hosting

## 📝 Post-Deployment

1. **Test your API** at `https://your-app.railway.app/api/docs`
2. **Test your frontend** at `https://your-app.vercel.app`
3. **Verify file organization** works in production

## 🛠️ Troubleshooting

### Common Issues:
- **CORS errors**: Update CORS_ORIGINS environment variable
- **File access**: Ensure DOWNLOADS_PATH is accessible
- **Build failures**: Check build logs in Railway dashboard

### Logs:
- **Railway**: View logs in Railway dashboard
- **Vercel**: View logs in Vercel dashboard
- **Local**: `railway logs` or `vercel logs`
