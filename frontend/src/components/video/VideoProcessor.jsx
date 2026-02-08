import { useState } from "react";

import VideoUploadCard from "@/components/video/VideoUploadCard";
import ProcessedVideoCard from "@/components/video/ProcessedVideoCard";

export default function VideoProcessor() {
  const [processedVideos, setProcessedVideos] = useState([
    {
      name: "test_video_1.mp4",
      status: "completed",
      profanitiesDetected: 8,
      wordsReplaced: 8,
      uploadedAt: new Date("2026-02-08T10:30:00"),
      progress: 100,
    },
    {
      name: "stream_2025_02_05.mp4",
      status: "processing",
      profanitiesDetected: 3,
      wordsReplaced: 0,
      uploadedAt: new Date("2026-02-05T11:45:00"),
      progress: 65,
    },
    {
      name: "epic_minecraft_parkour_montage.mp4",
      status: "failed",
      profanitiesDetected: 0,
      wordsReplaced: 0,
      uploadedAt: new Date("2026-02-03T12:00:00"),
      progress: 0,
    },
  ]);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);

  const ProcessedVideoCards = processedVideos.map((video, videoIndex) => {
    return <ProcessedVideoCard key={videoIndex} video={video} />;
  });

  return (
    <div className="space-y-4">
      <VideoUploadCard
        isUploading={isUploading}
        uploadProgress={uploadProgress}
      />
      <div>
        <h3 className="text-lg font-semibold tracking-tight">
          Processed Videos
        </h3>
      </div>
      {ProcessedVideoCards}
    </div>
  );
}
