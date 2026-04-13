import { createRoot } from "react-dom/client";
import { ThemeProvider } from "next-themes";
import App from "/src/App.jsx";
import "/src/index.css";

const root = createRoot(document.getElementById("root"));
root.render(
  <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
    <App />
  </ThemeProvider>
);
