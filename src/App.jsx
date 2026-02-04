import { useState } from "react";

import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Film, Radio, Settings2 } from "lucide-react";

export default function App() {
  return (
    <div className="min-h-screen">
      <header className="border-b">
        <div className="container mx-auto px-4 py-6">
          <h1 className="scroll-m-20 text-3xl font-bold tracking-tight text-balance">
            Modsquad
          </h1>
          <p className="leading-7 text-muted-foreground">
            Stream Moderation with AI-Powered Voice Cloning
          </p>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8">
        <Tabs defaultValue="vod" className="w-full">
          <TabsList className="grid w-full max-w-md grid-cols-3">
            <TabsTrigger value="vod" className="gap-2">
              <Film className="w-4 h-4" />
              VOD
            </TabsTrigger>
            <TabsTrigger value="real-time" className="gap-2">
              <Radio className="w-4 h-4" />
              Real-time
            </TabsTrigger>
            <TabsTrigger value="settings" className="gap-2">
              <Settings2 className="w-4 h-4" />
              Settings
            </TabsTrigger>
          </TabsList>
        </Tabs>
      </main>
    </div>
  );
}
