// Cloudflare Worker - YouTube Transcript Extractor
// Usando API pública gratuita (sin API Key)

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
  // Usar yewtu.be (Invidious) - público, sin API Key
  const response = await fetch(`https://yewtu.be/api/v1/captions/${videoId}`);
  
  if (!response.ok) {
    throw new Error(`Error: ${response.status}`);
  }
  
  const data = await response.json();
  
  if (!data.captions) {
    throw new Error('El video no tiene transcripción disponible');
  }
  
  return data.captions;
}
