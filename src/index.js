// Cloudflare Worker - YouTube Transcript Extractor
// Usando YouTube Data API v3 con variable de entorno

export default {
  async fetch(request) {
    const corsHeaders = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    };

    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: corsHeaders });
    }

    // Health check
    if (request.method === 'GET' && new URL(request.url).pathname === '/') {
      return new Response(JSON.stringify({
        status: 'OK',
        message: 'Hydra Transcript API en Cloudflare Workers'
      }), {
        headers: { 'Content-Type': 'application/json', ...corsHeaders }
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
            headers: { 'Content-Type': 'application/json', ...corsHeaders }
          });
        }

        const videoId = extractVideoId(url);
        if (!videoId) {
          return new Response(JSON.stringify({ error: 'No se pudo extraer el video_id' }), {
            status: 400,
            headers: { 'Content-Type': 'application/json', ...corsHeaders }
          });
        }

        const transcript = await getTranscript(videoId);

        return new Response(JSON.stringify({
          status: 'success',
          video_id: videoId,
          transcript: transcript
        }), {
          headers: { 'Content-Type': 'application/json', ...corsHeaders }
        });

      } catch (error) {
        return new Response(JSON.stringify({
          error: 'No se pudo obtener transcript',
          details: error.message
        }), {
          status: 500,
          headers: { 'Content-Type': 'application/json', ...corsHeaders }
        });
      }
    }

    return new Response('Not Found', { status: 404, headers: corsHeaders });
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
  const API_KEY = YOUTUBE_API_KEY;
  
  if (!API_KEY) {
    throw new Error('YOUTUBE_API_KEY no configurada');
  }
  
  const listUrl = `https://youtube.googleapis.com/youtube/v3/captions?part=snippet&videoId=${videoId}&key=${API_KEY}`;
  const listResponse = await fetch(listUrl);
  
  if (!listResponse.ok) {
    throw new Error(`Error al obtener lista: ${listResponse.status}`);
  }
  
  const listData = await listResponse.json();
  
  if (!listData.items || listData.items.length === 0) {
    throw new Error('El video no tiene transcripción disponible');
  }
  
  let captionId = listData.items[0].id;
  
  const transcriptUrl = `https://youtube.googleapis.com/youtube/v3/captions/${captionId}?key=${API_KEY}&tfmt=srt`;
  const transcriptResponse = await fetch(transcriptUrl);
  
  if (!transcriptResponse.ok) {
    throw new Error('No se pudo descargar la transcripción');
  }
  
  return await transcriptResponse.text();
}
