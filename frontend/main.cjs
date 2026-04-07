const { app, BrowserWindow } = require("electron/main");
const path = require("path");
const { spawn } = require("child_process");
const http = require("http");
const fs = require("fs");

const isDev = !app.isPackaged;
let backendProcess = null;

function getBackendPath() {
  if (isDev) return null;

  const backendDir = path.join(process.resourcesPath, "backend");
  if (process.platform === "win32") {
    return path.join(backendDir, "modsquad-backend.exe");
  }
  return path.join(backendDir, "modsquad-backend");
}

function startBackend() {
  const backendPath = getBackendPath();
  if (!backendPath) return null;

  const userDataPath = app.getPath("userData");
  const uploadsDir = path.join(userDataPath, "uploads");
  const dataDir = path.join(userDataPath, "data");
  const hfHome = path.join(userDataPath, "models");

  // Ensure directories exist
  for (const dir of [uploadsDir, dataDir, hfHome]) {
    fs.mkdirSync(dir, { recursive: true });
  }

  const child = spawn(backendPath, [], {
    env: {
      ...process.env,
      UPLOAD_DIR: uploadsDir,
      DATA_DIR: dataDir,
      HF_HOME: hfHome,
      MPLCONFIGDIR: path.join(userDataPath, "matplotlib"),
    },
    stdio: ["ignore", "pipe", "pipe"],
  });

  child.stdout.on("data", (d) => console.log("[backend]", d.toString()));
  child.stderr.on("data", (d) => console.error("[backend]", d.toString()));

  child.on("error", (err) => {
    console.error("Failed to start backend:", err);
  });

  return child;
}

function waitForBackend(timeoutMs = 120000) {
  const start = Date.now();

  return new Promise((resolve, reject) => {
    function poll() {
      if (Date.now() - start > timeoutMs) {
        return reject(new Error("Backend failed to start within timeout"));
      }

      const req = http.get("http://localhost:8000/", (res) => {
        resolve();
      });
      req.on("error", () => {
        setTimeout(poll, 500);
      });
      req.end();
    }
    poll();
  });
}

function killBackend() {
  if (backendProcess && !backendProcess.killed) {
    backendProcess.kill();
    backendProcess = null;
  }
}

async function createWindow() {
  const win = new BrowserWindow({
    width: 1200,
    height: 800,
  });

  if (isDev) {
    win.loadURL("http://localhost:5173");
  } else {
    win.loadFile(path.join(__dirname, "dist", "index.html"));
  }
}

app.whenReady().then(async () => {
  if (!isDev) {
    backendProcess = startBackend();
    try {
      await waitForBackend();
    } catch (err) {
      console.error(err.message);
    }
  }

  createWindow();

  app.on("activate", () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on("before-quit", killBackend);

app.on("window-all-closed", () => {
  killBackend();
  if (process.platform !== "darwin") {
    app.quit();
  }
});
