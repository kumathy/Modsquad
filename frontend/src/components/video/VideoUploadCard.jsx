import { useState } from "react";

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Upload, Loader2 } from "lucide-react";

const API_URL = "http://localhost:8000";

export default function VideoUploadCard({
  onUploadStart,
  onUploadComplete,
  onUploadProgress,
  onUploadError,
}) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  function handleFileChange(event) {
    const selectedFile = event.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
    }
  }

  async function handleUpload() {
    if (!file) {
      return;
    }

    setLoading(true);

    const videoId = onUploadStart(file);

    const formData = new FormData();
    formData.append("file", file);

    try {
      // Simulate progress
      let currentProgress = 0;
      const progressInterval = setInterval(() => {
        if (currentProgress < 90) {
          currentProgress = Math.min(currentProgress + 10, 90);
          onUploadProgress(currentProgress, videoId);
        }
      }, 1000);

      const response = await fetch(`${API_URL}/process-video`, {
        method: "POST",
        body: formData,
      });

      clearInterval(progressInterval);

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Processing failed");
      }

      const data = await response.json();
      console.log("Processing complete:", data);

      // Update to completed
      onUploadComplete(data, videoId);

      // Reset form
      setFile(null);
      document.getElementById("video-upload").value = "";
    } catch (err) {
      console.error("Error:", err);

      // Mark as failed in the video card
      onUploadError(err.message, videoId);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-6">
      <Card className="shadow-none">
        <CardHeader>
          <CardTitle>Upload Video</CardTitle>
          <CardDescription>
            Upload your video and get a censored version with AI-powered voice
            replacement
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex items-center justify-center w-full">
            <label
              htmlFor="video-upload"
              className="flex flex-col items-center justify-center w-full h-64 border-2 border-dashed rounded-lg cursor-pointer bg-muted/50 hover:bg-muted/80 transition-colors"
            >
              <div className="flex flex-col items-center justify-center pt-5 pb-6">
                <Upload className="w-12 h-12 mb-4 text-muted-foreground" />
                <p className="mb-2 text-sm text-muted-foreground">
                  <span className="font-semibold">Click to upload</span> or drag
                  and drop
                </p>
                <p className="text-xs text-muted-foreground">
                  File format: MP4, MOV, AVI, MP3, WAV
                </p>
              </div>
              <input
                id="video-upload"
                type="file"
                className="hidden"
                accept="video/*,audio/*"
                onChange={handleFileChange}
                disabled={loading}
              />
            </label>
          </div>

          {/* Show selected file */}
          {file && (
            <>
              <div className="p-3 bg-muted rounded-lg">
                <p className="text-sm font-medium">{file.name}</p>
                <p className="text-xs text-muted-foreground">
                  {(file.size / (1024 * 1024)).toFixed(2)} MB
                </p>
              </div>

              {/* Upload Button */}
              <Button
                onClick={handleUpload}
                disabled={loading}
                className="w-full"
                size="lg"
              >
                {loading ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Processing...
                  </>
                ) : (
                  <>
                    <Upload className="mr-2 h-4 w-4" />
                    Process Video
                  </>
                )}
              </Button>
            </>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
