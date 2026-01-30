import { createRoot } from "react-dom/client";
import App from "/src/App.jsx";
import "/src/index.css";

const root = createRoot(document.getElementById("root"));
root.render(<App />);
