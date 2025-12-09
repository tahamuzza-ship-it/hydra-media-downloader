import express from "express";
import { exec } from "child_process";
import fs from "fs";

const app = express();
app.use(express.json({limit: "50mb"}));

app.post("/yt", (req, res) => {
  const url = req.body.url;
  const id = "video-" + Date.now();
  const output = `/app/${id}.mp3`;

  const cmd = `
    yt-dlp -x --audio-format mp3 \
    --user-agent "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" \
    --add-header "Accept-Language: en-US,en;q=0.9" \
    --add-header "Connection: keep-alive" \
    -o "${output}" "${url}"
  `;

  exec(cmd, (err) => {
    if (err) return res.status(500).json({ error: err.toString() });

    const file = fs.readFileSync(output);
    fs.unlinkSync(output);

    res.setHeader("Content-Type", "audio/mpeg");
    res.send(file);
  });
});

app.listen(process.env.PORT || 8080);
