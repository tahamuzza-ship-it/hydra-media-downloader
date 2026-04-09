// Cloudflare Worker - YouTube Transcript Extractor
export default {
  async fetch(request) {
    // Health check
    if (request.method === 'GET' && new URL(request.url).pathname === '/') {
      return new Response(JSON.stringify({
        status: 'OK',
        message: 'Hydra Transcript API en Cloudflare Workers'
      }), {
        headers: { 'Content-Type': 'application/json' }
      });
    }

    // POST /process-link
    if (request.method === 'POST' && new URL(request.url).pathname === '/process-link') {
      try {
        const body = await request.json();
        const url = body.url;

        if (!url) {
          return new Response(JSON.stringify({ error: 'URL no proporcionada' }), {
            status: 400,
            headers: { 'Content-Type': 'application/json' }
          });
        }

        const videoId = extractVideoId(url);
        if (!videoId) {
          return new Response(JSON.stringify({ error: 'No se pudo extraer el video_id' }), {
            status: 400,
            headers: { 'Content-Type': 'application/json' }
          });
        }

        const transcript = await getTranscript(videoId);

        return new Response(JSON.stringify({
          status: 'success',
          video_id: videoId,
          transcript: transcript
        }), {
          headers: { 'Content-Type': 'application/json' }
        });

      } catch (error) {
        return new Response(JSON.stringify({
          error: 'No se pudo obtener transcript',
          details: error.message
        }), {
          status: 500,
          headers: { 'Content-Type': 'application/json' }
        });
      }
    }

    return new Response('Not Found', { status: 404 });
  }
};

function extractVideoId(url) {
  const patterns = [
    /v=([^&]+)/,
    /youtu\.be\/([^?&]+)/
  ];
  for (const pattern of patterns) {
    const match = url.match(pattern);
    if (match) return match[1];
  }
  return null;
}

async function getTranscript(videoId) {
  // Usar API pública alternativa (evita bloqueo de YouTube)
  const response = await fetch(`https://pipedapi.kavin.rocks/transcripts/${videoId}`);
  if (response.ok) {
    const data = await response.json();
    if (data.transcripts && data.transcripts.length > 0) {
      return data.transcripts.map(t => t.text).join(' ');
    }
  }
  throw new Error('No se pudo obtener la transcripción');
}
