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
import { toast } from "sonner";
import { API_URL } from "@/config";

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
      // Upload file and get job ID
      onUploadProgress(5, videoId, "Uploading...");
      const response = await fetch(`${API_URL}/process-video`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Upload failed");
      }

      const { job_id } = await response.json();
      onUploadProgress(10, videoId, "Starting processing...");

      // Listen for processing progress via SSE
      await new Promise((resolve, reject) => {
        const es = new EventSource(`${API_URL}/process-video/${job_id}/progress`);

        es.addEventListener("progress", (e) => {
          const { progress, stage } = JSON.parse(e.data);
          const labels = {
            transcribing: "Transcribing audio...",
            filtering: "Filtering words...",
            censoring: "Censoring video...",
          };
          onUploadProgress(progress, videoId, labels[stage] || stage);
        });

        es.addEventListener("complete", (e) => {
          es.close();
          const data = JSON.parse(e.data);
          toast.success("Video processed successfully");
          onUploadComplete(data, videoId);
          setFile(null);
          const input = document.getElementById("video-upload");
          if (input) input.value = "";
          resolve();
        });

        es.addEventListener("error", (e) => {
          es.close();
          try {
            const { detail } = JSON.parse(e.data);
            reject(new Error(detail));
          } catch {
            reject(new Error("Processing failed"));
          }
        });
      });
    } catch (err) {
      console.error("Error:", err);
      toast.error(err.message);
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
            Upload your video to get an automatically censored version
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
