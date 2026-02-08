# <p align="center">ModSquad</p>

<p align="center">
    VOD + Real-time language control tool for streaming
</p>

## Tech Stack

- **React** - UI framework
- **Vite** - Build tool and dev server
- **Electron** - Desktop app wrapper
- **shadcn/ui** - Component library
- **Tailwind CSS** - CSS framework
- **FastAPI** - Backend API

### Project Structure

```
ModSquad/
├── frontend/
│   ├── src/
│   │   ├── App.jsx                  # Main app component
│   │   ├── components/              # ← Create custom components here
│   │   │   └── ui/                  # ← shadcn components go here (don't modify)
│   │   ├── index.css
│   │   ├── index.jsx                # React entry point
│   │   └── lib/
│   │       └── utils.js             # Utility functions
│   ├── index.html                   # HTML entry point
│   ├── main.cjs                     # Electron main process
│   ├── package.json
│   ├── tailwind.config.js
│   ├── vite.config.js
│   └── components.json
├── backend/
│   ├── utils/                       # Backend utility functions
│   ├── main.py                      # FastAPI entry point
│   └── requirements.txt
├── README.md
└── .gitignore
```

## Running Locally

### Prerequisites

- Node.js (v18 or higher)
- Python (v3.8 or higher)
- npm
- pip

1. **Clone the repository**

```bash
   git clone https://github.com/kumathy/ModSquad.git && cd ModSquad
```

2. **Frontend Setup**

```bash
   # Navigate to frontend
   cd frontend

   # Install dependencies
   npm install

   # Start development server
   npm run dev
```

In a **separate terminal**, start Electron:

```bash
   npm run start
```

4. **Backend Setup**

In yet another **separate terminal**:

```bash
   # Navigate to backend
   cd backend

   # Create virtual environment
   python3 -m venv venv

   # Activate virtual environment
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   # Install dependencies
   pip install -r requirements.txt

   # Start FastAPI server
   uvicorn main:app --reload
```

## Internal Development Guide

### Installing `shadcn/ui` Components

Run this command from the **project root**:

```bash
npx shadcn@latest add [component-name]
```

Example:

```bash
npx shadcn@latest add button
npx shadcn@latest add card
npx shadcn@latest add tabs
```

This will automatically put the components in `src/components/ui/`

### Documentation

[React](https://react.dev) • [shadcn/ui](https://ui.shadcn.com/docs) • [Tailwind CSS](https://tailwindcss.com/docs) • [FastAPI](https://fastapi.tiangolo.com/)
