"""
Ahmad Content Tools - a remote MCP server for Composio (Add Custom MCP).

Run:  python server.py
Endpoint: http://localhost:8000/mcp   (public HTTPS URL when deployed)

Auth: No-auth by default. If you set the environment variable MCP_API_KEY,
every request must carry that key as `Authorization: Bearer <key>` or
`x-api-key: <key>`. In Composio, pick "No Auth" while MCP_API_KEY is unset,
or "API Key" after you set it.
"""

import os
import math
from datetime import datetime
from zoneinfo import ZoneInfo

from mcp.server.fastmcp import FastMCP

PORT = int(os.environ.get("PORT", "8000"))

mcp = FastMCP(
    "Ahmad Content Tools",
    instructions=(
        "Practical content tools for a creator/freelancer: script timing, "
        "YouTube title ideas, Instagram hooks and captions, and Fiverr "
        "package pricing. No private data, no external accounts."
    ),
    host="0.0.0.0",
    port=PORT,
    streamable_http_path="/mcp",
    stateless_http=True,
    json_response=True,
)


@mcp.tool()
def get_current_time(timezone_name: str = "Asia/Karachi") -> str:
    """Get the current date and time in a timezone, e.g. Asia/Karachi, America/New_York, UTC."""
    try:
        tz = ZoneInfo(timezone_name)
    except Exception:
        return f"Unknown timezone '{timezone_name}'. Use a name like Asia/Karachi, America/New_York or UTC."
    now = datetime.now(tz)
    return now.strftime("%A, %d %B %Y, %I:%M %p (%Z)")


@mcp.tool()
def script_timing(script_text: str, words_per_minute: int = 130) -> str:
    """Estimate voiceover duration for a script. Returns word count and timing at the given speaking speed."""
    words = len(script_text.split())
    if words == 0:
        return "Script is empty - 0 words, 0 seconds."
    seconds = words / max(words_per_minute, 1) * 60
    minutes = int(seconds // 60)
    rest = int(round(seconds % 60))
    return (
        f"Words: {words}\n"
        f"Speaking speed: {words_per_minute} wpm\n"
        f"Estimated duration: {minutes} min {rest} sec ({seconds:.0f} seconds total)\n"
        f"Tip: a 60-second Short needs about {words_per_minute} words at this speed."
    )


@mcp.tool()
def youtube_title_ideas(topic: str, audience: str = "students and small business owners", count: int = 5) -> str:
    """Generate practical, non-clickbait YouTube title ideas for a topic and audience."""
    count = max(1, min(count, 10))
    templates = [
        "I Tested {t} for a Real Task - Honest Result",
        "{t} in 10 Minutes: Step-by-Step for {a}",
        "Stop Doing It Manually: {t} Does It Faster",
        "{t} - What Works, What Fails, What It Costs",
        "Beginner's First Win With {t} (No Hype)",
        "I Replaced My Old Workflow With {t} for 7 Days",
        "{t} Mistakes Beginners Make (and the Fix)",
        "{t} vs Doing It Yourself: Time and Cost Compared",
        "One {t} Workflow That Saves an Hour a Week",
        "{t}: Watch This Before You Pay for It",
    ]
    titles = [templates[i].format(t=topic.strip(), a=audience.strip()) for i in range(count)]
    return "YouTube title ideas:\n" + "\n".join(f"{i+1}. {t}" for i, t in enumerate(titles))


@mcp.tool()
def instagram_hooks(topic: str, count: int = 5) -> str:
    """Generate scroll-stopping first-line hooks for an Instagram reel or carousel about a topic."""
    count = max(1, min(count, 10))
    hooks = [
        f"You don't need more tools. You need this {topic} system.",
        f"Stop wasting an hour on what {topic} does in 10 minutes.",
        f"3 {topic} mistakes costing you time every week.",
        f"I tested {topic} on a real task. Here's the honest result.",
        f"The {topic} workflow nobody shows beginners.",
        f"If you run a business, {topic} is leverage - not a toy.",
        f"Before you pay for {topic}, check this one limit.",
        f"{topic}, explained in 30 seconds - no hype.",
        f"One prompt, one system: {topic} done right.",
        f"Save this: my exact {topic} checklist.",
    ]
    return "Instagram hooks:\n" + "\n".join(f"{i+1}. {h}" for i, h in enumerate(hooks[:count]))


@mcp.tool()
def instagram_caption(topic: str, tone: str = "professional", call_to_action: str = "Save this post and follow for one tested system every day.") -> str:
    """Draft a short Instagram caption with hashtags for a topic, aimed at founders and operators."""
    tags = ["#AISystems", "#Founders", "#Operators", "#SmallBusiness", "#Productivity", "#Freelancer"]
    topic_tag = "#" + "".join(word.capitalize() for word in topic.replace("-", " ").split())
    if topic_tag not in tags:
        tags.insert(0, topic_tag)
    return (
        f"{topic.strip()} - tested on a real task, not a demo.\n\n"
        f"What worked, what failed, and what it actually costs. "
        f"Tone: {tone}. No hype, no fake results.\n\n"
        f"{call_to_action}\n\n" + " ".join(tags)
    )


@mcp.tool()
def fiverr_pricing(base_price_usd: float = 25) -> str:
    """Suggest Basic / Standard / Premium package prices from a Basic price (Standard = 2x, Premium = ~3.8x)."""
    if base_price_usd <= 0:
        return "Base price must be more than 0."
    standard = base_price_usd * 2
    premium = round(base_price_usd * 3.8)
    return (
        f"Basic: ${base_price_usd:g} - 1 tool, 1 task, script + copy-paste prompt, 1 revision, 3 days\n"
        f"Standard: ${standard:g} - script + step-by-step SOP + caption pack, 2 revisions, 3 days (recommended)\n"
        f"Premium: ${premium} - 2 tools compared on the same task, script + SOP + caption pack, 2 revisions, 5 days\n"
        f"Note: starting prices only, not a market guarantee."
    )


# --- Optional API-key check (only active when MCP_API_KEY is set) ---
class ApiKeyMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http" and scope["path"].startswith("/mcp"):
            key = os.environ.get("MCP_API_KEY", "")
            if key:
                headers = {k.decode().lower(): v.decode() for k, v in scope.get("headers", [])}
                supplied = headers.get("x-api-key", "")
                auth = headers.get("authorization", "")
                if auth.lower().startswith("bearer "):
                    supplied = auth[7:].strip()
                if supplied != key:
                    body = b'{"error":"unauthorized - missing or wrong API key"}'
                    await send({
                        "type": "http.response.start",
                        "status": 401,
                        "headers": [(b"content-type", b"application/json"), (b"content-length", str(len(body)).encode())],
                    })
                    await send({"type": "http.response.body", "body": body})
                    return
        await self.app(scope, receive, send)


if __name__ == "__main__":
    import uvicorn

    app = ApiKeyMiddleware(mcp.streamable_http_app())
    uvicorn.run(app, host="0.0.0.0", port=PORT)
