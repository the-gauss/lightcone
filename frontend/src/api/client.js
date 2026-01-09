const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api/v1";

export async function submitYoutubeUrl(url) {
  const response = await fetch(`${API_BASE_URL}/youtube/process`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ url })
  });

  if (!response.ok) {
    let detail = "Request failed";
    try {
      const data = await response.json();
      if (data?.detail) {
        detail = data.detail;
      }
    } catch (error) {
      // Ignore parsing failures and fall back to generic message.
    }
    throw new Error(detail);
  }

  return response.json();
}
