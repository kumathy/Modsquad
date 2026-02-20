# <p align="center">ModSquad</p>

<p align="center">
    VOD + Real-time language control tool for streaming
</p>

## Running Locally

### Prerequisites

- [Node.js](https://nodejs.org/) v18 or higher
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Python 3.12](https://www.python.org/downloads/release/python-3120/)
- npm

### 1. Clone the repository

```bash
git clone https://github.com/kumathy/ModSquad.git && cd ModSquad
```

### 2. Start the frontend

From the project root, install dependencies:

```bash
cd frontend && npm install
```

Start dev server and Electron in two separate terminals:

```bash
# Terminal 1 — Vite dev server
npm run dev

# Terminal 2 — Electron
npm run start
```

### 3. Start the backend

In another separate terminal, from the project root:

```bash
docker compose up --build
```

This builds the Python environment and starts the FastAPI server at `http://localhost:8000`. The `--build` flag is only needed the first time or after changes to `requirements.txt`/`Dockerfile`. After that, just run:

```bash
docker compose up
```

To stop the backend:

```bash
docker compose down
```

## Internal Development Guide

### Tech Stack

- **React** - UI framework
- **Vite** - Build tool and dev server
- **Electron** - Desktop app wrapper
- **shadcn/ui** - Component library
- **Tailwind CSS** - CSS framework
- **FastAPI** - Backend API
- **OpenAI Whisper** - Speech-to-text transcription
- **MoviePy** - Video/audio processing
- **Docker** - Backend environment and dependency management

### Project Structure

```
ModSquad/
├── docker-compose.yml                 # Docker orchestration
├── frontend/
│   ├── src/
│   │   ├── App.jsx                    # Main app component
│   │   ├── components/
│   │   │   ├── video/                 # Video processing components
│   │   │   └── ui/                    # shadcn components
│   │   ├── index.jsx                  # React entry point
│   │   └── lib/
│   ├── index.html                     # HTML entry point
│   └── main.cjs                       # Electron main process
├── backend/
│   ├── utils/                         # Backend utility functions
│   ├── main.py                        # FastAPI entry point
│   ├── requirements.txt               # Python dependencies
│   └── Dockerfile                     # Backend container definition
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

### How Docker works

Our backend has a heavy dependency stack (ffmpeg, PyTorch, Whisper, MoviePy) that is difficult to install consistently across machines with different OSes. Docker solves this by packaging the backend and all its dependencies into a container, essentially  an isolated computer that we can all use to run the backend, solving the "But it works on my machine" problem.

```
docker-compose.yml       ← orchestrates the backend container
backend/Dockerfile       ← specifications for building the backend environment
backend/requirements.txt ← Python packages to be installed inside the container
```

The frontend runs outside Docker and communicates with the containerized backend over HTTP at `localhost:8000`.

> [!NOTE]
> Please run `docker compose up --build` after modifying `requirements.txt` or `Dockerfile`

### Adding Python packages
Only list direct dependencies in `requirements.txt` (Only whatever you're importing in `.py` files)

**Steps to add a new package:**

1. Install it into your local venv (for VS Code intellisense):
   ```bash
   pip install <package>
   ```

2. Check the installed version:
   ```bash
   pip show <package>
   ```

3. Manually add it to `backend/requirements.txt`:
   ```
   package-name==1.2.3
   ```

4. Rebuild the Docker container so it installs inside it too:
   ```bash
   docker compose up --build
   ```

> [!WARNING]
> Do not use `pip freeze > requirements.txt`. This dumps all sub-dependencies with pinned versions in the file and makes it difficult to maintain.

### Documentation

[React](https://react.dev) • [shadcn/ui](https://ui.shadcn.com/docs) • [Tailwind CSS](https://tailwindcss.com/docs) • [FastAPI](https://fastapi.tiangolo.com/) • [Docker](https://docs.docker.com/)
