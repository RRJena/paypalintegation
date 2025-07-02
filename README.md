# 💳 PayPal Payment Integration (FastAPI + React)

This project demonstrates a working PayPal payment flow using:

- 🚀 **FastAPI** backend for creating and capturing PayPal orders/subscriptions
- 💻 **React + TailwindCSS (Vite)** frontend for user interface
- 💰 Fully integrated **PayPal Sandbox Checkout** & **Subscriptions**

---

## 📁 Project Structure

```
project-root/
│
├── backend/fastapi_app           ← FastAPI project
│   └── main.py
│   └── .env
│
├── frontend/react_frontend          ← React project (Vite + Tailwind)
│   └── src/
│   └── index.html
│   └── package.json
│
└── README.md
```

---

## ⚙️ Requirements

- Node.js (>= 18)
- Python 3.10+
- pip / pipenv
- PayPal Developer account: https://developer.paypal.com

---

## 🛠️ Setup Instructions

### 1. 🔧 Backend (FastAPI)

#### A. Install dependencies

```bash
cd backend/fastapi_app
pip install fastapi uvicorn httpx python-dotenv
```

#### B. Create `.env` file

```ini
PAYPAL_CLIENT_ID=your_sandbox_client_id
PAYPAL_CLIENT_SECRET=your_sandbox_secret
PAYPAL_API_BASE=https://api-m.sandbox.paypal.com
```

Get your credentials from: https://developer.paypal.com/dashboard/applications/sandbox

#### C. Run FastAPI server

```bash
uvicorn main:app --reload --port 8000
```

The backend will be available at: [http://localhost:8000](http://localhost:8000)

---

### 2. 💻 Frontend (React + Vite + TailwindCSS)

#### A. Install dependencies

```bash
cd frontend/react_frontend     
npm install
```

#### B. Run Vite dev server

```bash
npm run dev
```

The frontend will be available at: [http://localhost:5173](http://localhost:5173)

---

## 🚀 How It Works

1. User enters amount & clicks **Pay One-Time** or **Subscribe**
2. Frontend sends request to FastAPI
3. FastAPI creates a PayPal order / plan
4. User is redirected to PayPal for approval
5. After approval, user is redirected back to frontend
6. Frontend **auto-captures** the payment using `order_id`

---

## 🔁 Supported PayPal Flows

| Feature        | Supported | Notes                                      |
|----------------|-----------|--------------------------------------------|
| One-Time Pay   | ✅        | `/pay/one-time` + `/pay/capture/:id`       |
| Subscriptions  | ✅        | `/pay/recurring`                           |
| Auto Capture   | ✅        | Frontend reads `token` and triggers capture |
| Webhooks       | 🔄        | Optional – can be added                     |

---

##  Testing With Sandbox

- Login to [PayPal Sandbox](https://sandbox.paypal.com) using:
  - **Personal sandbox account** for approving payments
  - **Business account** receives funds and is linked to your app

You can create sandbox accounts at: https://developer.paypal.com/dashboard/accounts

---

## Build Frontend (for production)

```bash
cd frontend
npm run build
```

The static files will be output to `dist/`

---

## Useful Links

- [PayPal API Docs](https://developer.paypal.com/docs/api/overview/)
- [FastAPI Docs](https://fastapi.tiangolo.com)
- [Vite + React](https://vitejs.dev/guide/)
- [TailwindCSS](https://tailwindcss.com)

---

## ✅ Status: Fully Working Sandbox Demo








