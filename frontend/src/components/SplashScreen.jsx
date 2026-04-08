import { useEffect } from "react";
import { Loader2 } from "lucide-react";
import { API_URL } from "@/config";

export default function SplashScreen({ onReady }) {
  useEffect(() => {
    let cancelled = false;
    async function poll() {
      while (!cancelled) {
        try {
          const res = await fetch(`${API_URL}/`);
          if (res.ok) {
            onReady();
            return;
          }
        } catch {}
        await new Promise((r) => setTimeout(r, 1000));
      }
    }
    poll();
    return () => { cancelled = true; };
  }, [onReady]);

  return (
    <div className="flex items-center justify-center min-h-screen">
      <Loader2 className="h-10 w-10 animate-spin text-muted-foreground" />
    </div>
  );
}
