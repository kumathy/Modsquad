const params = new URLSearchParams(window.location.search);
const BACKEND_PORT = params.get("port") || 8000;
export const API_URL = `http://localhost:${BACKEND_PORT}`;
