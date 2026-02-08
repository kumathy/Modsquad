# <p align="center">ModSquad</p>

<p align="center">
    VOD + Real-time language control tool for streaming
</p>

## Running Locally

### Prerequisites

- Node.js (v18 or higher)
- npm

1. **Clone the repository**

```bash
   git clone https://github.com/kumathy/ModSquad.git && cd ModSquad
```

2. **Install dependencies**

```bash
   cd frontend
   npm install
```

3. **Start development server**

```bash
   npm run dev
```

4. **In another terminal, start the Electron app**

```bash
   npm run start
```

## Internal Development Guide

### Tech Stack

- **React** - UI framework
- **Vite** - Build tool and dev server
- **Electron** - Desktop app wrapper
- **shadcn/ui** - Component library
- **Tailwind CSS** - CSS framework

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
