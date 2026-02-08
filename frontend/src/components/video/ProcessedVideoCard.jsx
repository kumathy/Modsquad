import { useState } from "react";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";

import {
  Upload,
  Play,
  Download,
  CheckCircle2,
  AlertCircle,
} from "lucide-react";

export default function ProcessedVideoCard({ video }) {
  return (
    <Card className="shadow-none">
      <CardContent className="pt-6">
        <div className="flex items-start justify-between gap-4">
          <div className="flex-1 space-y-3">
            <div className="flex items-center gap-3">
              <h4 className="font-medium">{video.name}</h4>
              {video.status === "completed" && (
                <Badge variant="default" className="gap-1">
                  <CheckCircle2 className="w-3 h-3" />
                  Completed
                </Badge>
              )}

              {video.status === "processing" && (
                <Badge variant="secondary">Processing</Badge>
              )}

              {video.status === "failed" && (
                <Badge variant="destructive" className="gap-1">
                  <AlertCircle className="w-3 h-3" />
                  Failed
                </Badge>
              )}
            </div>

            {video.status === "processing" && (
              <div className="space-y-2">
                <Progress value={video.progress} />
                <p className="flex justify-between items-center text-sm text-muted-foreground">
                  <span>Processing video and applying language control...</span>
                  <span className="font-medium"> {video.progress}%</span>
                </p>
              </div>
            )}

            {video.status === "completed" && (
              <div className="flex gap-6 text-sm">
                <div>
                  <span className="text-muted-foreground">
                    Profanities detecteds:{" "}
                  </span>
                  <span className="font-medium">
                    {video.profanitiesDetected}
                  </span>
                </div>
                <div>
                  <span className="text-muted-foreground">
                    Words replaced:{" "}
                  </span>
                  <span className="font-medium">{video.wordsReplaced}</span>
                </div>
                <div>
                  <span className="text-muted-foreground">Uploaded: </span>
                  <span className="font-medium">
                    {video.uploadedAt.toLocaleDateString()}
                  </span>
                </div>
              </div>
            )}
          </div>

          {video.status === "completed" && (
            <div className="flex gap-2">
              <Button variant="outline" size="sm">
                <Play className="w-4 h-4 mr-2" />
                Preview
              </Button>
              <Button size="sm">
                <Play className="w-4 h-4 mr-2" />
                Download
              </Button>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
