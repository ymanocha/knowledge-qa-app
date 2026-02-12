# Deployment Guide: Free Hosting 🚀

You can host this entire application for free using **Render** (Backend) and **Vercel** (Frontend).

## Prerequisites
1. A **GitHub** account.
2. Push your code to a new GitHub repository.

---

## 1. Backend Deployment (Render)
Render offers a "Web Service" free tier that is perfect for this FastAPI backend.

1. Create a free account on [Render](https://render.com).
2. Click **New +** > **Blueprint**.
3. Connect your GitHub repository.
4. Render will detect the `render.yaml` file automatically.
5. **Environment Variables**: When prompted, add your `GOOGLE_API_KEY`.
6. **Note**: The free tier service "sleeps" after 15 minutes of inactivity. The first request after a break may take ~30 seconds to wake up.

---

## 2. Frontend Deployment (Vercel)
Vercel is the gold standard for hosting Vite/React applications.

1. Create a free account on [Vercel](https://vercel.com).
2. Click **Add New** > **Project**.
3. Import your GitHub repository.
4. **Project Settings**:
   - **Root Directory**: Select `frontend`.
   - **Framework Preset**: Vite (detected automatically).
5. **Environment Variables**:
   - Add `VITE_API_URL`: Set this to your Render backend URL (e.g., `https://knowledge-qa-backend.onrender.com`).
6. Click **Deploy**.

---

## 3. Post-Deployment (Final Step)
Once your Vercel URL is live (e.g., `https://my-rag-app.vercel.app`):
1. Go back to your **Render Dashboard**.
2. Go to **Environment Settings** for your backend service.
3. Update `ALLOWED_ORIGINS` to match your Vercel URL. This ensures CORS allows your frontend to talk to the backend.

---

## ⚠️ Free Tier Limitations
- **Ephemeral Storage**: On Render's free tier, the `storage.json` file is reset every time the server restarts or sleeps. This means your uploaded documents will disappear after a few hours of inactivity.
- **Waking Up**: The backend takes a moment to "wake up" on the first request.

**Enjoy your live Private Knowledge Q&A!**
