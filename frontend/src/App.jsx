import { useState } from "react";

import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";

import VideoProcessor from "@/components/video/VideoProcessor";

import { Film, Radio, Settings2 } from "lucide-react";

export default function App() {
  return (
    <div className="flex flex-col min-h-screen">
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

          <div className="mt-8">
            <TabsContent value="vod" className="space-y-6">
              <div>
                <h2 className="text-2xl font-semibold tracking-tight mb-2">
                  VOD Processing
                </h2>
                <p className="text-muted-foreground">
                  Upload your videos/recorded streams to receive a censored
                  version with AI-cloned voice replacement.
                </p>
              </div>
              <VideoProcessor />
            </TabsContent>

            <TabsContent value="real-time">
              <div>
                <h2 className="text-2xl font-semibold tracking-tight mb-2">
                  Real-time Stream Monitoring
                </h2>
                <p className="text-muted-foreground">Coming soon!</p>
              </div>
            </TabsContent>

            <TabsContent value="settings">
              <div>
                <h2 className="text-2xl font-semibold tracking-tight mb-2">
                  Settings
                </h2>
                <p className="text-muted-foreground">Coming soon!</p>
              </div>
            </TabsContent>
          </div>
        </Tabs>
      </main>

      <footer className="border-t mt-auto">
        <div className="container mx-auto px-4 py-6">
          <div className="text-sm text-muted-foreground">
            <p>© 2026 Modsquad. AI-powered stream moderation.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
