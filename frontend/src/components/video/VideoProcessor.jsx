import VideoUploadCard from "@/components/video/VideoUploadCard";
import ProcessedVideoCard from "@/components/video/ProcessedVideoCard";

export default function VideoProcessor({ processedVideos, setProcessedVideos }) {

  function handleUploadStart(file) {
    const processingVideo = {
      name: file.name,
      status: "processing",
      profanitiesDetected: 0,
      wordsReplaced: 0,
      uploadedAt: new Date(),
      progress: 0,
      id: Date.now(),
    };

    setProcessedVideos((prevVideos) => [processingVideo, ...prevVideos]);
    return processingVideo.id;
  }

  function handleUploadComplete(result, videoId) {
    setProcessedVideos((prevVideos) =>
      prevVideos.map((video) =>
        video.id === videoId
          ? {
              ...video,
              status: "completed",
              profanitiesDetected: result.profanity?.total_flagged || 0,
              wordsReplaced: result.profanity?.words_replaced || 0,
              progress: 100,
              downloadUrl: result.download_url,
              fullResult: result,
            }
          : video
      )
    );
  }

  function handleUploadProgress(progress, videoId) {
    setProcessedVideos((prevVideos) =>
      prevVideos.map((video) =>
        video.id === videoId ? { ...video, progress } : video
      )
    );
  }

  function handleUploadError(errorMessage, videoId) {
    setProcessedVideos((prevVideos) =>
      prevVideos.map((video) =>
        video.id === videoId
          ? { ...video, status: "failed", progress: 0 }
          : video
      )
    );
  }

  const ProcessedVideoCards = processedVideos.map((video, videoIndex) => {
    return <ProcessedVideoCard key={video.id || videoIndex} video={video} />;
  });

  return (
    <div className="space-y-4">
      <VideoUploadCard
        onUploadStart={handleUploadStart}
        onUploadComplete={handleUploadComplete}
        onUploadProgress={handleUploadProgress}
        onUploadError={handleUploadError}
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
