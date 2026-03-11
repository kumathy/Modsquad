import { useState, useEffect, useRef } from "react";

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import {
  ScanSearch,
  Square,
  AlertTriangle,
  Volume2,
  Activity,
} from "lucide-react";

export default function StreamProcessor() {
  const [isStreaming, setIsStreaming] = useState(false);
  const [stats, setStats] = useState({
    profanitiesDetected: 0,
    wordsReplaced: 0,
    streamDuration: 0,
  });

  function toggleStreaming() {
    if (!isStreaming) {
      setStats({
        profanitiesDetected: 0,
        wordsReplaced: 0,
        streamDuration: 0,
      });
    }
    setIsStreaming(!isStreaming);
  }

  const intervalRef = useRef(null);

  useEffect(() => {
    if (isStreaming) {
      intervalRef.current = setInterval(() => {
        setStats((prev) => ({
          ...prev,
          streamDuration: prev.streamDuration + 1,
        }));
      }, 1000);
    }

    return () => clearInterval(intervalRef.current);
  }, [isStreaming]);

  function formatDuration(seconds) {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    return `${hours.toString().padStart(2, "0")}:${minutes
      .toString()
      .padStart(2, "0")}:${secs.toString().padStart(2, "0")}`;
  }

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Real-Time Stream Processing</CardTitle>
          <CardDescription>
            Monitor and censor your live stream here
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className=" flex items-center justify-between">
            <div className="flex items-center gap-4">
              <Button
                size="lg"
                variant={isStreaming ? "destructive" : "default"}
                onClick={toggleStreaming}
                className="min-w-[140px]"
              >
                {isStreaming ? (
                  <>
                    <Square className="w-5 h-5 mr-2" />
                    Stop Stream
                  </>
                ) : (
                  <>
                    <ScanSearch className="w-5 h-5 mr-2" />
                    Scan for OBS
                  </>
                )}
              </Button>

              {isStreaming && (
                <Badge
                  variant="destructive"
                  className="gap-2 px-3 py-1.5 text-sm animate-pulse"
                >
                  <Activity className="w-4 h-4" />
                  LIVE
                </Badge>
              )}
            </div>

            {isStreaming && (
              <div className="text-right">
                <p className="text-sm text-muted-foreground">Stream Duration</p>
                <p className="text-2xl font-mono font-semibold">
                  {formatDuration(stats.streamDuration)}
                </p>
              </div>
            )}
          </div>

          <Separator />

          {/* Stats */}
          <div className="grid grid-cols-3 gap-4">
            <div className="text-center p-4 rounded-lg bg-muted/30">
              <p className="text-3xl font-bold text-primary">
                {stats.profanitiesDetected}
              </p>
              <p className="text-sm text-muted-foreground mt-1">
                Profanities Detected
              </p>
            </div>
            <div className="text-center p-4 rounded-lg bg-muted/30">
              <p className="text-3xl font-bold text-primary">
                {stats.wordsReplaced}
              </p>
              <p className="text-sm text-muted-foreground mt-1">
                Words Replaced
              </p>
            </div>
            <div className="text-center p-4 rounded-lg bg-muted/30">
              <p className="text-3xl font-bold text-primary">
                {stats.profanitiesDetected > 0
                  ? (
                      (stats.wordsReplaced / stats.profanitiesDetected) *
                      100
                    ).toFixed(0)
                  : 0}
                %
              </p>
              <p className="text-sm text-muted-foreground mt-1">Success Rate</p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Detection Log */}
      <Card>
        <CardHeader>
          <CardTitle>Detection Log</CardTitle>
          <CardDescription>
            Real-time profanity detection and replacement events
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="text-center py-12 text-muted-foreground">
            <AlertTriangle className="w-12 h-12 mx-auto mb-4 opacity-50" />
            <p>No events yet. Start streaming to see detection events.</p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
