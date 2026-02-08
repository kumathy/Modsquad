import { useState } from "react";

import VideoUploadCard from "@/components/video/VideoUploadCard";
import ProcessedVideoCard from "@/components/video/ProcessedVideoCard";

export default function VideoProcessor() {
  const [processedVideos, setProcessedVideos] = useState([]);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);

  return (
    <div>
      <VideoUploadCard
        isUploading={isUploading}
        uploadProgress={uploadProgress}
      />
      <ProcessedVideoCard />
    </div>
  );
}
