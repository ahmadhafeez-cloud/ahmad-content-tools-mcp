# Ahmad Content Tools — Custom MCP for Composio

Ek working remote MCP server, test ho chuka hai (initialize, tools/list, tools/call — teeno pass).
Is me 6 tools hain, koi private data ya login nahi chahiye:

1. `get_current_time` — kisi timezone ka current time
2. `script_timing` — script ke words se voiceover duration
3. `youtube_title_ideas` — topic se practical YouTube titles
4. `instagram_hooks` — reel/carousel ki pehli lines
5. `instagram_caption` — caption + hashtags
6. `fiverr_pricing` — Basic/Standard/Premium price tiers

## Zaroori baat

Composio khud MCP server host **nahi** karta. "Add Custom MCP" ke liye pehle server ko
ek **public HTTPS URL** par deploy karna parta hai, phir woh URL Composio me dalta hai.
Local/localhost URL kaam nahi karega.

## Step 1 — Deploy (Render, free)

1. Is folder ko apne GitHub account par ek repo bana kar upload karein
   (ya Render par "New Web Service" me kisi aur host se bhi deploy ho sakta hai).
2. Render.com → New → Web Service → apna repo select karein.
   Is folder me `render.yaml` pehle se hai, settings auto bhar jayengi:
   Build: `pip install -r requirements.txt` — Start: `python server.py`
3. Deploy khatam ho to URL milega, jaisay `https://ahmad-content-tools-mcp.onrender.com`
4. Check: browser me `https://<aapka-url>/mcp` — Composio isi endpoint ko call karega.

Free Render service sust par sakta hai (pehli request par ~1 minute lag sakta hai jab service so rahi ho).

## Step 2 — Composio me Add Custom MCP

Aap ki screenshot wale dialog me yeh bharein:

- **Display name:** `Ahmad Content Tools`
- **MCP server URL:** `https://<aapka-deploy-url>/mcp`  (akhir me `/mcp` lazmi hai, koi redirect nahi)
- **Authentication:** `DCR OAuth` **mat** chunein — yeh server DCR support nahi karta.
  **`No Auth`** chunein (yeh dropdown me hona chahiye). Phir **Add** dabayein — tools foran sync ho jayenge.

### Agar baad me lock karna ho (optional)

Server me `MCP_API_KEY` naam ka environment variable apni hosting par set kar dein (koi bhi lambhi random value).
Phir Composio me is toolkit ko delete karke dobara add karein aur Authentication me **API Key** chunein, wahi key dein.
Note: Composio me URL aur auth mode baad me change nahi hote — badalna ho to toolkit delete karke dobara banana parta hai.

## Local test (optional)

```
python -m venv .venv
.venv/bin/pip install -r requirements.txt   # Windows: .venv\Scripts\pip
python server.py
# endpoint: http://localhost:8000/mcp
```
