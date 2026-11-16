"""Builds every page of rayyankhan.dev from the data below and tools/projects.json.

Run from the repo root:  python tools/build_pages.py
Writes index.html, projects.html, work/<slug>.html, <service-slug>.html and
sitemap.xml. Vercel's cleanUrls serves them without the .html extension.
Edit facts here (or in tools/projects.json), never in the generated HTML.

Every claim must be true: facts come from the original project cards,
Rayyan's LinkedIn posts and his project notes. Films with sample data say so.
"""
from __future__ import annotations

import html
import json
from pathlib import Path

SITE = "https://rayyankhan.dev"
NAME = "Agha Muhammad Rayyan Khan"
EMAIL = "agharayyan@gmail.com"
WHATSAPP = "https://wa.me/923218234852"
ROOT = Path(__file__).resolve().parent.parent
# Publish date of these pages and their films (VideoObject uploadDate, sitemap lastmod).
FILM_DATE = "2026-11-16"
# Pages written by hand (not by this script) that still belong in sitemap.xml: (path, lastmod).
HAND_PAGES = [("/seo-ray", "2026-11-16"), ("/privacy", "2026-11-16")]
SAMPLE = "Walkthrough film · names and numbers are sample data"
# Films with light (white UI) posters get a dimmed, blue-tinted hero treatment so they sit in the dark layout.
LIGHT_FILMS = {"almunir", "booking", "flowstate"}

e = html.escape

# ---------------------------------------------------------------- case studies
CASES = [
    {
        "slug": "call-stream",
        "kind": "Voice AI · built with Shahwaiz",
        "name": "Call Stream",
        "title": "Call Stream: Urdu AI Call Agent on a Normal SIM",
        "description": "An Android phone and a normal Pakistani SIM become an AI call agent that answers in Urdu. No SIP trunk, no PTA paperwork, no new number.",
        "h1": ["An Urdu AI agent", "on the number", '<span class="grad">you already have.</span>'],
        "lede": "Call Stream turns an Android phone and a normal Pakistani SIM into an AI call agent that answers in Urdu. No SIP trunk, no PTA paperwork, no new number on your shop board. A property dealer runs it on his own line today. Built together with Shahwaiz.",
        "chips": ["Android + Pakistani SIM", "Asterisk", "SIP over TLS", "Urdu voice AI"],
        "film": "callstream", "tall": True, "note": "Example call for illustration · AI voices",
        "problem": 'Every AI voice vendor in Pakistan opens with the same sentence: <em>“first, get a SIP trunk.”</em>',
        "problem_p": "That means PTA paperwork, weeks of procurement and a brand new number nobody has ever called. For a business whose only line is printed on its shop board, that's a dead end.",
        "steps": [
            ("The customer calls your normal number", "The call lands on a live mobile SIM in an Android phone, exactly like it does today."),
            ("The phone hands the call to a bridge", "Over Bluetooth into an Asterisk bridge, then out to the AI agent over SIP, encrypted with TLS."),
            ("The agent knows who's calling", "The caller's real number travels with the call, so the agent knows who it is before it says a word."),
            ("It talks in Urdu, both ways", "Callers are answered in Urdu, and the same setup phones new leads back. Bresco Properties uses it to call every lead."),
        ],
        "decisions": [
            ("The phone number was the hard part", "Most AI voice talk here is about which model sounds better in Urdu. The real blocker was getting a call off a normal SIM and into an agent without a carrier deal."),
            ("TLS on port 5061", "The week that nearly killed it went to the ISP swallowing SIP on port 5060: every INVITE out, nothing back, not even a 100 Trying. Moving to TLS on 5061 fixed it."),
            ("A demo film for every industry", "I made eight vertical demo films, one per industry: Umrah travel, real estate, healthcare, education, study abroad, BPO, AI agencies and car showrooms."),
        ],
        "facts": [("0", "new numbers, trunks or carrier deals"), ("8", "industry demo films"), ("1", "call at a time per SIM")],
        "limits": "One SIM handles one call at a time. That's fine for a business doing 20 calls a day, not 200.",
        "related": ["bresco", "al-munir"], "service": "ai-voice-agents",
    },
    {
        "slug": "jennifer",
        "kind": "Flagship build · real estate",
        "name": "Jennifer",
        "title": "Jennifer: An AI Employee for Real Estate Agencies",
        "description": "Jennifer manages leads, scores intent, tracks follow-ups, searches live market data and briefs the owner daily, all through a normal chat.",
        "h1": ["An AI employee", "for the real estate", '<span class="grad">lead desk.</span>'],
        "lede": "Jennifer manages leads, scores intent, tracks follow-ups, searches live market data, keeps property inventory current and delivers a daily business briefing, all through a normal chat. Built end to end in Next.js and Supabase.",
        "chips": ["Next.js 14", "Supabase + RLS", "Groq", "OpenRouter", "Gemini", "Tavily", "RAG", "Vercel"],
        "film": "jennifer", "tall": False, "note": SAMPLE,
        "problem": 'Real estate teams bleed leads when follow-ups, property matching and CRM updates all depend on <em>someone remembering</em> to do them.',
        "problem_p": "Agents juggle WhatsApp chats, spreadsheets and site visits. The follow-up that gets forgotten is the deal that gets lost.",
        "steps": [
            ("Tell it what happened, in plain words", "An agent says what happened with a lead. Jennifer decides the action from the conversation itself."),
            ("It updates the CRM itself", "Lead status, intent score, tasks and follow-ups are written to the database. Nobody updates a CRM by hand."),
            ("It answers from your own data", "RAG over the agency's knowledge plus live database context, and live market search when the question needs it."),
            ("It briefs the owner every day", "A daily business briefing: new leads, follow-ups due and inventory changes."),
        ],
        "decisions": [
            ("A four-step fallback chain", "Requests fall back through a four-step chain across Groq, OpenRouter and Gemini, so a single provider having a bad day doesn't stop the lead desk."),
            ("Permissions by role", "Supabase row-level security keeps each person to the data their role allows: Super Admin, Admin or Agent."),
            ("Built for agents on the move", "It installs on a phone as an app (PWA), because agents spend the day at site visits, not at a desk."),
        ],
        "facts": [("4", "steps in the provider fallback chain"), ("0", "manual CRM updates"), ("24/7", "availability")],
        "limits": None,
        "related": ["call-stream", "al-munir"], "service": "ai-agents-automation",
    },
    {
        "slug": "al-munir",
        "kind": "Client build · manufacturing",
        "name": "Al Munir UPVC",
        "title": "Al Munir UPVC: A Sales Pipeline That Runs After Hours",
        "description": "A UPVC manufacturer's pipeline finds buyers in Facebook groups, calls them with a voice agent and sends a priced PDF quote on WhatsApp.",
        "h1": ["A sales pipeline", "that stays open", '<span class="grad">after the lights go off.</span>'],
        "lede": "Al Munir makes UPVC windows in Lahore. Their office closes at 6pm, their customers don't. This pipeline finds buyers in Facebook groups, calls them with a voice agent and sends a priced PDF quote on WhatsApp. Nobody touches a calculator.",
        "chips": ["n8n", "Apify", "Retell AI", "UltraMsg", "WhatsApp Cloud API", "PDF.co", "Google Sheets", "Claude", "Vercel"],
        "film": "almunir", "tall": False, "note": SAMPLE,
        "problem": 'Someone comments <em>“price?”</em> on a Facebook post at 9pm. The team sees it at 9am. By then that person has bought windows from someone else.',
        "problem_p": "That gap was the whole problem. Not marketing. Not pricing. Office hours.",
        "steps": [
            ("Find buying intent", "Apify scans Facebook groups and Instagram hashtags for people asking about windows. Real leads land in a Google Sheet within minutes."),
            ("First message, straight away", "UltraMsg sends the first WhatsApp message automatically."),
            ("A voice agent calls", "A Retell voice agent calls the lead, asks what they need and logs the outcome."),
            ("A priced quote on WhatsApp", "If the call goes well, a quote is priced and sent as a two-page PDF built from the company's own branded template."),
            ("Visits book themselves", "A measurement visit goes into Google Calendar and the team gets an email, so it never gets forgotten."),
            ("DMs answered in Roman Urdu", "On Instagram, a Claude sales bot collects sizes and location in Roman Urdu, and knows not to quote prices."),
        ],
        "decisions": [
            ("A person takes over when asked", "The moment a customer asks for a human, the conversation hands over to the team."),
            ("Their quote, not a generic one", "Quotes render from Al Munir's own branded template as a two-page PDF, so a midnight quote looks like one from the office."),
            ("Scheduled jobs plus webhooks", "Schedulers run the scraping and calling on-site; anything inbound hits serverless webhooks on Vercel."),
        ],
        "facts": [("2", "page branded PDF quote, priced automatically"), ("0", "calculators involved"), ("After hours", "Instagram DMs answered by the sales bot, even at midnight")],
        "limits": None,
        "related": ["call-stream", "bresco"], "service": "whatsapp-automation",
    },
    {
        "slug": "bresco",
        "kind": "Client build · real estate",
        "name": "Bresco Properties",
        "title": "Bresco Properties: An AI Sales Stack for Real Estate",
        "description": "A Lahore real estate agency's pipeline: AI-drafted posts, five agents' WhatsApp numbers on one dashboard, AI replies in Roman Urdu and Urdu calls.",
        "h1": ["Five agents.", "One inbox.", '<span class="grad">Every lead called.</span>'],
        "lede": "A Lahore real estate agency's sales pipeline, end to end. AI writes the Facebook posts a person approves, five agents' own WhatsApp numbers run campaigns from one dashboard, an AI answers leads in Roman Urdu and English, and a calling agent phones every lead in Urdu.",
        "chips": ["Next.js", "Supabase", "Baileys", "Gemini", "Call Stream"],
        "film": "bresco", "hero_film": "bresco-teaser", "tall": False, "note": "Teaser cut · example data for illustration",
        "problem": 'When a team sells from WhatsApp, five agents means <em>five numbers, five inboxes</em> and a lead list someone splits by hand.',
        "problem_p": "Bresco wanted every lead answered and called, without adding people to the lead desk.",
        "steps": [
            ("AI drafts the post, a person approves", "Facebook posts are written by AI and only go out after someone on the team approves them."),
            ("Every agent's number sends it", "One team post goes out from every agent's own WhatsApp number."),
            ("Leads split themselves", "Leads import from Excel and split automatically across the agents who are online."),
            ("AI answers, people take over", "An AI replies in Roman Urdu and English, with a handoff to the agent, all in one shared inbox."),
            ("Every lead gets a call in Urdu", "A calling agent phones each lead in Urdu. The calls run on Call Stream."),
        ],
        "decisions": [
            ("Agents keep their own numbers", "Each agent links their own WhatsApp number to the dashboard. There's no shared company number to set up."),
            ("One inbox for the whole team", "Every agent's chats land in one unified inbox, so anyone can see which lead has been answered."),
            ("Calls on Call Stream", "The Urdu calling runs on Call Stream, the SIM-based call agent built with Shahwaiz."),
        ],
        "facts": [("5", "agents' WhatsApp numbers on one dashboard"), ("2", "reply languages: Roman Urdu and English"), ("Live", "running for Bresco Properties")],
        "limits": None,
        "related": ["call-stream", "whatsapp-lead-system"], "service": "whatsapp-automation",
    },
    {
        "slug": "whatsapp-lead-system",
        "kind": "Automation build · BGMC",
        "name": "WhatsApp Lead Management System",
        "title": "WhatsApp Lead Management: Instant Replies and Routing",
        "description": "Instagram ad leads get a WhatsApp reply in seconds, their needs captured and routed round-robin to the right associate, in the same chat.",
        "h1": ["Every ad lead", "answered on WhatsApp", '<span class="grad">in seconds.</span>'],
        "lede": "Built at BGMC to stop Instagram ad leads going cold when the team was busy. A WhatsApp chatbot replies the moment a lead clicks the ad, collects what they need and routes them to the right associate, who carries on in the same chat.",
        "chips": ["WhatsApp Cloud API", "n8n", "Claude", "Google Sheets"],
        "film": "walead", "tall": False, "note": SAMPLE,
        "problem": 'Leads click the ad and land on WhatsApp. If the team is busy, <em>the lead goes cold</em> and the ad money is wasted.',
        "problem_p": "BGMC runs Instagram ads for consulting services. The fix had to answer every lead instantly and still put a real associate in the conversation.",
        "steps": [
            ("A lead clicks the ad", "They land on WhatsApp and the chatbot replies straight away."),
            ("It collects the requirements", "A natural conversation, not a form, gathers what the lead needs."),
            ("It picks the right person", "It detects which service the lead wants and assigns them round-robin to an associate who's available."),
            ("The associate gets the summary", "An email lands with the full lead summary, and the associate continues the same WhatsApp chat."),
            ("Everything is logged", "Every lead and follow-up is tracked in Google Sheets."),
        ],
        "decisions": [
            ("Round-robin with availability", "Leads only go to associates who are available, so nobody gets a lead they can't answer."),
            ("Same chat, no app switching", "The associate picks up the conversation where the bot left it. The customer never changes apps."),
            ("Sheets as the log", "A simple shared sheet is the record, so the team didn't need a new CRM to start."),
        ],
        "facts": [("Seconds", "to the first reply after an ad click"), ("0", "leads left waiting when the team is busy"), ("1", "WhatsApp chat from bot to associate")],
        "limits": None,
        "related": ["bresco", "al-munir"], "service": "whatsapp-automation",
    },
]

# ---------------------------------------------------------------- service pages
PROCESS = [
    ("01", "Audit", "I map your current process and find where automation saves the most hours, not the most impressive demo."),
    ("02", "Blueprint", "I design the workflow, tools, data flow, edge cases and failure handling, before writing anything."),
    ("03", "Build", "I build and test against real scenarios and messy real data, not the happy path that always works in a demo."),
    ("04", "Handoff", "You get documentation, workflow access and a recorded walkthrough. The system is yours, not rented from me."),
]
OWN = ("Who owns the system when it's done?", "You do. You get documentation, workflow access and a recorded walkthrough. The system is yours, not rented from me.")

SERVICES = [
    {
        "slug": "ai-voice-agents",
        "glass": [("2", "languages the agents talk in: Urdu and English"), ("0", "new numbers needed with Call Stream")],
        "nums": [("20+", "systems shipped, each with a walkthrough film"), ("8", "industry demo films for Call Stream"), ("24/7", "answering, with no office hours")],
        "label": "Service · AI voice agents",
        "title": "AI Voice Agent Developer: Urdu and English Call Agents",
        "description": "AI voice agents that answer your phone in Urdu or English, book appointments into your calendar and call leads back, even on your existing number.",
        "h1": ["AI voice agents", "that answer in Urdu", '<span class="grad">and book the slot.</span>'],
        "lede": "I build voice agents that answer your phone, hold a real conversation in Urdu or English, check your calendar and book the appointment. They can run on your existing mobile number, with no SIP trunk and no new number.",
        "film": "callstream", "tall": True, "note": "Example call for illustration · AI voices",
        "offer": [
            ("Answer every inbound call", "The agent picks up, understands what the caller needs and qualifies them, day or night."),
            ("Book into your calendar", "Live Google Calendar availability checks, a confirmed slot, then confirmation emails and reminders."),
            ("Call new leads back", "The same agent phones every new lead. Bresco and Al Munir both have every lead called."),
            ("Keep your own number", "With Call Stream the agent runs on a normal Pakistani SIM, so customers call the number they already know."),
            ("Follow up on no-shows", "WhatsApp and email follow-up when someone misses their appointment."),
            ("Voice on your website", "A voice agent that runs in the browser over WebRTC, with no phone line needed."),
        ],
        "proof": ["call-stream", "al-munir", "bresco"],
        "faq": [
            ("Can the agent speak Urdu?", "Yes. Call Stream's agents talk to callers in Urdu, and the same setups work in English. On WhatsApp, the bots handle Roman Urdu too."),
            ("Do I need a new phone number or a SIP trunk?", "No. Call Stream runs on a normal Pakistani SIM in an Android phone, so there's no PTA paperwork or carrier deal. The limit is one call at a time per SIM, which suits a business doing around 20 calls a day. For more volume, we plan a proper phone line together."),
            ("Can it book appointments into my calendar?", "Yes. The booking agent checks real Google Calendar availability, confirms a slot with the caller, books it and sends a confirmation email automatically."),
            ("What does it do when it can't help a caller?", "You decide that in the blueprint: hand over to a person, take a message, or follow up on WhatsApp. Nothing is left to a guess."),
            OWN,
        ],
    },
    {
        "slug": "whatsapp-automation",
        "glass": [("Seconds", "to the first reply after an ad click"), ("2", "reply languages: Roman Urdu and English")],
        "nums": [("20+", "systems shipped, each with a walkthrough film"), ("5", "agents' WhatsApp numbers on one Bresco dashboard"), ("0", "leads left waiting when the team is busy")],
        "label": "Service · WhatsApp automation",
        "title": "WhatsApp Automation in Pakistan: Bots, Routing, Campaigns",
        "description": "WhatsApp bots that reply to leads in seconds in Roman Urdu or English, route them to the right person and send quotes, built in Lahore.",
        "h1": ["WhatsApp automation", "that replies", '<span class="grad">before the lead goes cold.</span>'],
        "lede": "For most local businesses, leads arrive on WhatsApp. I build the bots, routing and campaigns that reply in seconds, in Roman Urdu or English, and hand the conversation to the right person on your team.",
        "film": "walead", "tall": False, "note": SAMPLE,
        "offer": [
            ("Instant replies to ad leads", "A lead clicks your Instagram or Facebook ad and gets an answer in seconds, not the next morning."),
            ("Requirements, captured", "A natural conversation collects what the customer needs before a person ever reads it."),
            ("Routing to the right person", "Round-robin assignment to whoever is available, with an email summary for the associate."),
            ("Campaigns from your agents' numbers", "One post goes out from every agent's own WhatsApp number, managed from one dashboard."),
            ("Quotes and documents", "Priced PDF quotes built from your own template, sent in the chat automatically."),
            ("Handover in the same chat", "When a customer wants a person, your team carries on in the same conversation."),
        ],
        "proof": ["whatsapp-lead-system", "bresco", "al-munir"],
        "faq": [
            ("Official WhatsApp API or my normal number?", "Both are possible. The WhatsApp Lead System and Al Munir use Meta's official Cloud API. Bresco links each agent's own WhatsApp number to one dashboard. I'll tell you which fits your volume and team, and the trade-offs of each."),
            ("Can the bot reply in Roman Urdu?", "Yes. The bots on Bresco and Al Munir reply in Roman Urdu and English, the way customers actually write."),
            ("What happens when a customer wants a real person?", "A person takes over in the same WhatsApp chat. On Al Munir's pipeline that happens the moment a customer asks for one."),
            ("Can it send quotes or files?", "Yes. Al Munir's pipeline prices the order and sends a two-page PDF quote from the company's own branded template."),
            OWN,
        ],
    },
    {
        "slug": "ai-agents-automation",
        "glass": [("4", "step provider fallback chain in Jennifer"), ("0", "manual CRM updates")],
        "nums": [("20+", "systems shipped, each with a walkthrough film"), ("4", "step provider fallback chain in Jennifer"), ("100+", "emails sent by one n8n follow-up system")],
        "label": "Service · AI agents & automation",
        "title": "Hire an AI Agent Developer: Custom AI Agents & Automation",
        "description": "Custom AI agents that decide and act on your systems, plus n8n and Make automation with retries and alerts. Built by Agha Muhammad Rayyan Khan.",
        "h1": ["AI agents that", "do the work,", '<span class="grad">not just the chat.</span>'],
        "lede": "Anyone can wire a chatbot that answers a question. I build the part underneath: agents that decide what to do and actually do it against your systems, with the retries, edge cases and CRM writes that still work on a Sunday at 3am.",
        "film": "leadforge", "tall": False, "note": SAMPLE,
        "offer": [
            ("Agents that take action", "Tool calling that executes real work: updating your CRM, creating tasks, sending messages."),
            ("Answers from your own knowledge", "RAG over your business documents and live data, so answers are grounded in your facts."),
            ("Lead qualification and scoring", "Every lead scored on intent and routed, before anyone on the team spends time on it."),
            ("Workflow automation", "n8n, Make.com and Zapier pipelines with error handling, retries and failure alerts."),
            ("Overnight lead research", "Agents that scan job boards, social platforms and groups for buying signals and draft the reply."),
            ("Outreach and follow-ups", "Personalised emails with follow-ups threaded into the same conversation, sent on schedule."),
        ],
        "proof": ["jennifer", "whatsapp-lead-system", "al-munir"],
        "faq": [
            ("What's the difference between a chatbot and an AI agent?", "A chatbot answers questions. An agent decides what needs to happen and does it: updates the CRM, books the visit, sends the quote. That's the part I build."),
            ("Which tools do you build with?", "n8n, Make.com and Zapier for workflows; Claude, OpenAI, Gemini and Groq for the AI; Next.js and Supabase when the system needs its own app."),
            ("What happens if the AI provider goes down?", "Critical systems get a fallback chain. Jennifer falls back through a four-step provider chain, so one provider having a bad day doesn't stop the work."),
            ("How do we start?", "Send me the workflow, your tool stack, or just describe the manual thing that eats your week. I'll tell you what can be automated, what shouldn't be, and what the first useful version looks like."),
            OWN,
        ],
    },
]

CASE_BY = {c["slug"]: c for c in CASES}
SERVICE_BY = {s["slug"]: s for s in SERVICES}
SERVICE_NAMES = {"ai-voice-agents": "AI voice agents", "whatsapp-automation": "WhatsApp automation", "ai-agents-automation": "AI agents & automation"}

ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
ARROW_SM = ARROW.replace('<svg ', '<svg width="14" height="14" ', 1)
SOUND = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 5 6 9H2v6h4l5 4z"/><path d="M15.5 8.5a5 5 0 0 1 0 7M19 5a10 10 0 0 1 0 14"/></svg>'
PLAY = '<svg class="play" viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>'
LENIS = "https://unpkg.com/lenis@1.1.13/dist/lenis.min.js"

# Every shipped project (the full archive on /projects). Order is the display order.
PROJECTS = json.loads((ROOT / "tools" / "projects.json").read_text(encoding="utf-8"))
FILTERS = [("all", "Everything"), ("automation", "Automation"), ("ai", "AI & agents"), ("voice", "Voice"),
           ("platforms", "Platforms"), ("web", "Websites"), ("data", "Data & ML")]
CHAT_WIDGET = (ROOT / "tools" / "chat_widget.html").read_text(encoding="utf-8")

# Homepage "What I build": the original homepage's five, plus WhatsApp automation (now its own service page).
# viz = the project scene (assets/scenes.js) the viewer shows for it.
CAPABILITIES = [
    ("Workflow Automation", "Automated pipelines that connect your tools and move data without a human copy-pasting between tabs.",
     ["n8n, Make.com and Zapier workflows", "Error handling, retries and failure alerts", "Sheets, Notion, CRMs, email and REST APIs"], "/ai-agents-automation", "munirquote"),
    ("AI Agents & Chatbots", "Assistants that understand the request, decide what to do, and actually execute it against your systems.",
     ["RAG over your own business knowledge base", "Lead qualification and intent scoring", "Tool-calling with real action execution"], "/ai-agents-automation", "research"),
    ("Voice & Booking Systems", "Voice agents that answer the phone, hold a real conversation, check the calendar and book the slot.",
     ["Live Google Calendar availability checks", "Confirmation emails and reminder sequences", "WhatsApp and email follow-up on no-shows"], "/ai-voice-agents", "receptionist"),
    ("WhatsApp Automation", "Leads from ads, Facebook groups and Excel sheets get a reply on WhatsApp in seconds, routed to the right person in the same chat.",
     ["Instant replies in English, Urdu and Roman Urdu", "Round-robin routing to online agents", "One inbox for every agent's number"], "/whatsapp-automation", "whatsapp"),
    ("Full-Stack Platforms", "The product around the intelligence: dashboards, directories, portals and real-time apps, built so someone else can maintain them.",
     ["Next.js, React and Node with Postgres, Mongo or Convex", "Auth, roles and row-level permissions", "Real-time sockets, presence and live updates"], None, "bresco"),
    ("Websites & 3D Web", "Brand sites and launch pages, from a single-page site to a 3D product viewer that runs in the browser.",
     ["Brand direction, copy and front-end build", "Three.js, WebGL and GSAP scroll-driven motion", "Fast and responsive on real phones, not just a desktop screen"], None, "aurelle"),
]


# Motion start states only when motion is allowed; cleared after 2.5 s if GSAP never arrives.
MOTION_FLAG = "(function(){var d=document.documentElement;if(!matchMedia('(prefers-reduced-motion: reduce)').matches){d.classList.add('js-motion');setTimeout(function(){if(!window.__motionOK)d.classList.remove('js-motion')},2500)}})();"


def head(title: str, description: str, path: str, image: str, schema: list[dict], frame_left: str,
         og_type: str = "article", preload: str | None = None) -> str:
    """The dark layout's head, top bar and menu (archive, case studies, service pages).
    The light homepage has its own: home_head()."""
    url = f"{SITE}{path}"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{e(title)}</title>
<meta name="description" content="{e(description)}" />
<link rel="canonical" href="{url}" />
<link rel="icon" href="/favicon.ico" sizes="32x32 48x48" />
<link rel="icon" href="/favicon-96.png" type="image/png" sizes="96x96" />
<link rel="apple-touch-icon" href="/apple-touch-icon.png" />
<meta property="og:title" content="{e(title)}" />
<meta property="og:description" content="{e(description)}" />
<meta property="og:type" content="{og_type}" />
<meta property="og:url" content="{url}" />
<meta property="og:site_name" content="{NAME}" />
<meta property="og:image" content="{image}" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="theme-color" content="#05070C" />
<link rel="preload" as="image" href="{preload or image.replace(SITE, '')}" fetchpriority="high" />
<script type="application/ld+json">
{json.dumps({"@context": "https://schema.org", "@graph": schema}, indent=1, ensure_ascii=False)}
</script>
<script>
/* Motion start states only when motion is allowed; cleared if GSAP never arrives. */
{MOTION_FLAG}
</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet" media="print" onload="this.media='all'">
<link rel="stylesheet" href="/assets/site.css" />
<link rel="stylesheet" href="/assets/chat.css" />
</head>
<body>
<div class="grain" aria-hidden="true"></div>
<div class="frame bl" aria-hidden="true">{frame_left}</div>
<div class="frame br" aria-hidden="true"><b id="framePct">00%</b> &nbsp;SCROLLED</div>
<header class="topbar" id="topbar">
  <div class="container">
    <nav>
      <a href="/" class="brand"><span class="brand-mark">MR</span><span>Muhammad Rayyan<small>AI Systems Engineer</small></span></a>
{nav_links()}
    </nav>
  </div>
  <div class="scrollbar" id="scrollbar"></div>
</header>
{mobile_menu()}
<main>
"""


def nav_links() -> str:
    """Desktop nav with Work and Services dropdowns, plus the mobile menu button. Shared with index.html."""
    work = "".join(f'<a href="/work/{c["slug"]}">{e(c["name"])}</a>' for c in CASES)
    serv = "".join(f'<a href="/{s["slug"]}">{e(SERVICE_NAMES[s["slug"]])}</a>' for s in SERVICES)
    return f"""      <div class="nav-links">
        <div class="dd"><a href="/#work" class="dd-t">Work</a><div class="dd-m">{work}<a href="/projects" class="dd-all">All {len(PROJECTS)} projects</a></div></div>
        <div class="dd"><a href="/#services" class="dd-t">Services</a><div class="dd-m">{serv}<a href="/#services" class="dd-all">Everything I build</a></div></div>
        <a href="/#process">Process</a>
        <a href="/#contact" class="nav-cta">Work with me</a>
      </div>
      <button type="button" class="menu-btn" aria-expanded="false" aria-controls="mmenu" aria-label="Open menu"><i></i></button>"""


def mobile_menu() -> str:
    """Full-screen menu for phones, opened by .menu-btn (assets/site.js). Shared with index.html."""
    work = "".join(f'<a href="/work/{c["slug"]}">{e(c["name"])}</a>' for c in CASES)
    serv = "".join(f'<a href="/{s["slug"]}">{e(SERVICE_NAMES[s["slug"]])}</a>' for s in SERVICES)
    return f"""<nav class="mmenu" id="mmenu" aria-label="Site menu"><div class="container">
  <h3>Services</h3>{serv}
  <h3>Case studies</h3>{work}<a href="/projects">All {len(PROJECTS)} projects</a>
  <h3>More</h3><a href="/#process">How I work</a><a href="/">Home</a>
  <a href="/#contact" class="mm-cta">Work with me</a>
</div></nav>"""


def h1(lines: list[str]) -> str:
    return "<h1>" + " ".join(f'<span class="ln"><span>{l}</span></span>' for l in lines) + "</h1>"


def hero(*, crumbs: str, idx_num: str, label: str, lines: list[str], lede: str, actions: str, chips: str,
         film_name: str, poster: str, tall: bool, note: str, glass: list[tuple[str, str]], watch_src: str) -> str:
    """Film full-bleed behind the copy. The poster <img> is the LCP and is visible from the first paint;
    the background video only loads on desktop after `load` (assets/site.js)."""
    g = "".join(
        f'<div class="glass g{i+1}" data-depth="{0.5 + i * 0.35:.2f}"><span class="mono">{"At a glance" if i == 0 else "And"}</span><b>{e(v)}</b><span>{e(l)}</span></div>'
        for i, (v, l) in enumerate(glass[:2])
    )
    phone = (f'<div class="phone" data-depth="0.9"><img src="/films/{poster}.jpg" alt="" width="720" height="1280" />'
             f'<video data-src="/films/{film_name}.mp4" muted loop playsinline preload="none" aria-hidden="true"></video></div>') if tall else ""
    tall_attr = " data-tall" if tall else ""
    return f"""
<section class="xhero{' tall' if tall else ''}{' light' if poster in LIGHT_FILMS else ''}" aria-labelledby="h1">
  <div class="xhero-bg" data-depth="0.25">
    <img src="/films/{poster}.jpg" alt="Still from the walkthrough film" fetchpriority="high" width="1280" height="720" />
    <video data-src="/films/{film_name}.mp4" muted loop playsinline preload="none" aria-hidden="true"></video>
  </div>
  <div class="xhero-shade" aria-hidden="true"></div>
  <div class="floaters" aria-hidden="true">{g}</div>
  {phone}
  <div class="container xhero-in">
    {crumbs}
    <div class="idx" data-hi><span class="num">{idx_num}</span><span class="label" style="margin:0">{e(label)}</span></div>
    <div id="h1">{h1(lines)}</div>
    <p class="lede" data-hi>{e(lede)}</p>
    <div class="actions" data-hi>{actions}<button type="button" class="btn btn-ghost" data-watch="{watch_src}" data-poster="/films/{poster}.jpg"{tall_attr}>{PLAY}Watch the film</button></div>
    <div class="chips" data-hi>{chips}</div>
    <p class="film-note" data-hi style="margin-top:16px">{e(note)}</p>
  </div>
</section>"""


def nums_band(label: str, heading: str, facts: list[tuple[str, str]]) -> str:
    import re
    cells = []
    for v, l in facts:
        m = re.fullmatch(r"(\d+)(\D*)", v)
        dt = f'<dt data-count="{m.group(1)}" data-suffix="{e(m.group(2))}">{e(v)}</dt>' if m else f'<dt class="word">{e(v)}</dt>'
        cells.append(f'<div data-rv>{dt}<dd>{e(l)}</dd></div>')
    return f"""
<section class="red" aria-labelledby="nums-h">
  <div class="container">
    <div class="label" data-rv>{e(label)}</div>
    <h2 id="nums-h" class="mono" style="font-family:var(--mono);font-size:.7rem;letter-spacing:.16em;color:#ffd5db;margin-bottom:28px" data-rv>{e(heading)}</h2>
    <dl class="nums">{''.join(cells)}</dl>
  </div>
</section>"""


def marquee(items: list[str]) -> str:
    row = "".join(f"<span>{e(x)}</span>" for x in items)
    return f'<div class="marquee"><p class="sr-only">Built with: {e(", ".join(items))}</p><div class="marquee-track" aria-hidden="true">{row}{row}{row}{row}</div></div>'


def next_teaser(kind: str, href: str, title: str, sub: str, poster: str) -> str:
    return f"""
<a class="next" href="{href}" aria-label="{e(kind)}: {e(title)}">
  <img src="/films/{poster}.jpg" alt="" loading="lazy" width="1280" height="720" />
  <div class="container">
    <span class="mono">{e(kind)}</span>
    <span class="title">{e(title)}</span>
    <p class="sub">{e(sub)}</p>
    <span class="go"><i>{ARROW}</i>Open it</span>
  </div>
</a>"""


def cta(heading: str) -> str:
    """Closing call to action on the dark pages."""
    return f"""<section class="cta" aria-labelledby="cta-h">
  <div class="container cta-grid">
    <div data-rv>
      <div class="label">Work with me</div>
      <h2 id="cta-h">{heading}</h2>
      <p class="lede">Send me the workflow, your tool stack, or just describe the manual thing that eats your week. I'll tell you what can be automated, what shouldn't be, and what the first useful version looks like.</p>
    </div>
    <div class="actions" data-rv>
      <a href="mailto:{EMAIL}" class="btn btn-primary">Book a free audit{ARROW}</a>
      <a href="{WHATSAPP}" target="_blank" rel="noopener" class="btn btn-ghost">Message on WhatsApp</a>
    </div>
  </div>
</section>
"""


def foot(scripts: str = "") -> str:
    """Footer, film dialog, chat widget and scripts. `scripts` adds page-specific ones (scenes, the 3D network)."""
    work = "".join(f'<a href="/work/{c["slug"]}">{e(c["name"])}</a>' for c in CASES)
    serv = "".join(f'<a href="/{s["slug"]}">{e(SERVICE_NAMES[s["slug"]])}</a>' for s in SERVICES)
    return f"""</main>
<footer>
  <div class="container">
    <div class="foot-grid">
      <div><h3>{NAME}</h3><a href="/">AI systems that do real work. {len(PROJECTS)} shipped, most with a walkthrough film.</a><a href="mailto:{EMAIL}">{EMAIL}</a><a href="https://www.linkedin.com/in/rayyan45/" rel="me noopener" target="_blank">LinkedIn</a><a href="https://github.com/rayyanse" rel="me noopener" target="_blank">GitHub</a></div>
      <div><h3>Case studies</h3>{work}</div>
      <div><h3>Services</h3>{serv}<a href="/projects">All {len(PROJECTS)} projects</a></div>
    </div>
    <div class="foot-base"><span>© 2026 {NAME}</span><span>AI SYSTEMS ENGINEER · LAHORE, PK · REMOTE</span></div>
  </div>
</footer>
<dialog class="fmodal" id="filmModal" aria-label="Walkthrough film"><button type="button" class="x" aria-label="Close film">×</button><video controls playsinline></video></dialog>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js" defer></script>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/ScrollTrigger.min.js" defer></script>
<script src="{LENIS}" defer></script>
<script src="/assets/site.js" defer></script>
{scripts}{CHAT_WIDGET}<script src="/assets/chat.js" defer></script>
</body>
</html>
"""


def pcard(slug: str, i: int) -> str:
    c = CASE_BY[slug]
    return f"""<a class="pcard" href="/work/{slug}">
        <span class="num">CASE {case_no(slug)}</span>
        <img src="/films/{c['film']}.jpg" alt="Still from the {e(c['name'])} walkthrough film" loading="lazy" width="1280" height="720" />
        <div class="pc-body"><div class="pc-kind">{e(c['kind'])}</div><h3>{e(c['name'])}</h3><p>{e(c['description'])}</p><span class="more wipe">Read the case study {ARROW_SM}</span></div>
      </a>"""


def person() -> dict:
    return {"@type": "Person", "@id": f"{SITE}/#person", "name": NAME, "url": f"{SITE}/"}


def crumbs_schema(items: list[tuple[str, str]]) -> dict:
    return {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": f"{SITE}{p}"} for i, (n, p) in enumerate(items)]}


def video_schema(name: str, description: str, film_name: str) -> dict:
    return {"@type": "VideoObject", "name": f"{name} walkthrough film", "description": description, "thumbnailUrl": f"{SITE}/films/{film_name}.jpg", "contentUrl": f"{SITE}/films/{film_name}.mp4", "uploadDate": FILM_DATE}


def case_no(slug: str) -> str:
    return f"{[c['slug'] for c in CASES].index(slug) + 1:03d}"


def case_page(c: dict) -> str:
    path = f"/work/{c['slug']}"
    svc = c["service"]
    n = case_no(c["slug"])
    total = f"{len(CASES):03d}"
    nxt = CASES[(CASES.index(c) + 1) % len(CASES)]
    schema = [
        {"@type": "CreativeWork", "@id": f"{SITE}{path}#work", "name": c["name"], "headline": c["title"], "description": c["description"], "url": f"{SITE}{path}", "author": person(), "image": f"{SITE}/films/{c['film']}.jpg", "video": video_schema(c["name"], c["description"], c["film"])},
        crumbs_schema([("Home", "/"), ("Work", "/#work"), (c["name"], path)]),
    ]
    crumbs = f'<nav class="crumbs" aria-label="Breadcrumb" data-hi><a href="/">Home</a><span aria-hidden="true">/</span><a href="/#work">Work</a><span aria-hidden="true">/</span><span>{e(c["name"])}</span></nav>'
    actions = f'<a href="mailto:{EMAIL}?subject={e(c["name"])}%20-%20something%20like%20this" class="btn btn-primary">Build something like this{ARROW}</a>'
    chips = "".join(f'<span class="chip">{e(x)}</span>' for x in c["chips"])
    steps = "".join(f'<li class="step"><span class="n">{i+1:02d}</span><h3>{e(t)}</h3><p>{e(p)}</p></li>' for i, (t, p) in enumerate(c["steps"]))
    decisions = "".join(f'<li data-rv><span class="n">{i+1:02d}</span><h3>{e(t)}</h3><p>{e(p)}</p></li>' for i, (t, p) in enumerate(c["decisions"]))
    limits = f'<div class="limits" data-rv><b>Honest limits</b><p>{e(c["limits"])}</p></div>' if c["limits"] else ""
    hero_film = c.get("hero_film", c["film"])
    tall = c["tall"]
    return head(c["title"], c["description"], path, f"{SITE}/films/{c['film']}.jpg", schema,
                f'CASE <b>{n}</b> / {total} &nbsp;·&nbsp; {e(c["name"])}') + hero(
        crumbs=crumbs, idx_num=n, label=f"Case {n} / {total} · {c['kind']}", lines=c["h1"], lede=c["lede"],
        actions=actions, chips=chips, film_name=hero_film, poster=c["film"], tall=tall, note=c["note"],
        glass=c["facts"], watch_src=f"/films/{c['film']}.mp4") + f"""

<section class="paper" aria-labelledby="problem-h">
  <div class="container">
    <div class="label" id="problem-h" data-rv>The problem</div>
    <p class="quote" data-rv>{c['problem']}</p>
    <div class="after"><p class="stamp" data-rv>Case {n} · {e(c['name'])}</p><p class="lede" data-rv>{e(c['problem_p'])}</p></div>
  </div>
</section>

<section aria-labelledby="how-h">
  <div class="container">
    <div class="label" data-rv>How it works</div>
    <h2 id="how-h" data-rv style="margin-bottom:clamp(36px,5vw,64px);max-width:14ch">Step by step, on real data.</h2>
    <div class="how">
      <div class="how-film{' tall' if tall else ''}">
        <div class="film"><video data-src="/films/{hero_film}.mp4" poster="/films/{c['film']}.jpg" muted loop playsinline preload="none" aria-label="Walkthrough film of {e(c['name'])}"></video></div>
        <p class="film-note">{e(c['note'])}</p>
        <div class="meter" aria-hidden="true"><span>01 / {len(c['steps']):02d}</span><i><b></b></i></div>
      </div>
      <ol class="steps">{steps}</ol>
    </div>
  </div>
</section>
""" + nums_band("At a glance", f"{c['name']} in numbers", c["facts"]) + f"""

<section aria-labelledby="dec-h">
  <div class="container">
    <div class="label" data-rv>Under the hood</div>
    <h2 id="dec-h" data-rv style="margin-bottom:clamp(32px,4vw,52px)">The decisions that mattered</h2>
    <ul class="decisions">{decisions}</ul>
    {limits}
    <p class="lede" data-rv style="margin-top:36px">This is what I build as a service: <a class="wipe" href="/{svc}"><strong>{e(SERVICE_NAMES[svc])}</strong></a>.</p>
  </div>
</section>
{marquee(c['chips'])}
""" + next_teaser(f"Next case · {case_no(nxt['slug'])} / {total}", f"/work/{nxt['slug']}", nxt["name"], nxt["description"], nxt["film"]) + cta("Want one of these for your business?") + foot()


def service_page(s: dict) -> str:
    path = f"/{s['slug']}"
    name = SERVICE_NAMES[s["slug"]]
    order = [x["slug"] for x in SERVICES]
    nxt = SERVICES[(order.index(s["slug"]) + 1) % len(SERVICES)]
    schema = [
        {"@type": "Service", "@id": f"{SITE}{path}#service", "name": name, "description": s["description"], "url": f"{SITE}{path}", "provider": person(), "areaServed": ["Pakistan", "Worldwide"]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in s["faq"]]},
        crumbs_schema([("Home", "/"), (name, path)]),
    ]
    crumbs = f'<nav class="crumbs" aria-label="Breadcrumb" data-hi><a href="/">Home</a><span aria-hidden="true">/</span><span>{e(name)}</span></nav>'
    actions = f'<a href="mailto:{EMAIL}?subject={e(name)}" class="btn btn-primary">Book a free audit{ARROW}</a>'
    offer = "".join(f'<li data-rv><span class="n">{i+1:02d}</span><h3>{e(t)}</h3><p>{e(p)}</p></li>' for i, (t, p) in enumerate(s["offer"]))
    proof = "".join(pcard(x, i) for i, x in enumerate(s["proof"]))
    proc = "".join(f'<li data-rv><b>{n}</b><h3>{e(t)}</h3><p>{e(p)}</p></li>' for n, t, p in PROCESS)
    faq = "".join(f'<details data-rv><summary><h3>{e(q)}</h3><i aria-hidden="true"></i></summary><div class="a"><p>{e(a)}</p></div></details>' for q, a in s["faq"])
    num = f"{order.index(s['slug']) + 1:02d}"
    return head(s["title"], s["description"], path, f"{SITE}/films/{s['film']}.jpg", schema,
                f'SERVICE <b>{num}</b> / {len(SERVICES):02d} &nbsp;·&nbsp; {e(name)}') + hero(
        crumbs=crumbs, idx_num=num, label=s["label"], lines=s["h1"], lede=s["lede"], actions=actions, chips="",
        film_name=s["film"], poster=s["film"], tall=s["tall"], note=s["note"], glass=s["glass"],
        watch_src=f"/films/{s['film']}.mp4") + f"""

<section class="paper" aria-labelledby="offer-h">
  <div class="container">
    <div class="label" data-rv>What I build</div>
    <h2 id="offer-h" data-rv style="max-width:16ch">What you get</h2>
    <ul class="offer">{offer}</ul>
  </div>
</section>

<section class="proof" aria-labelledby="proof-h">
  <div class="container proof-head">
    <div class="label" data-rv>Proof</div>
    <h2 id="proof-h" data-rv>Built and running.</h2>
    <p class="lede" data-rv>Real systems, each with a walkthrough film of it working.</p>
  </div>
  <div class="track-wrap"><div class="track">{proof}</div></div>
</section>
""" + nums_band("Track record", f"{name} by the numbers", s["nums"]) + f"""

<section aria-labelledby="proc-h">
  <div class="container">
    <div class="label" data-rv>How I work</div>
    <h2 id="proc-h" data-rv style="margin-bottom:clamp(32px,4vw,52px)">Simple process. Clear handoff.</h2>
    <ol class="proc">{proc}</ol>
  </div>
</section>

<section aria-labelledby="faq-h" style="padding-top:0">
  <div class="container faq-grid">
    <div><div class="label" data-rv>Questions</div><h2 id="faq-h" data-rv>What clients ask first</h2></div>
    <div class="faq">{faq}</div>
  </div>
</section>
""" + next_teaser("Next service", f"/{nxt['slug']}", SERVICE_NAMES[nxt["slug"]], nxt["description"], nxt["film"]) + cta("Got a process someone repeats every day?") + foot()




# ------------------------------------------------------------------ homepage (light edition)
# Its own stylesheet (assets/home.css) and script (assets/home.js); the other pages keep site.css.

HOME_TITLE = f"{NAME}, AI Automation Engineer in Lahore"
HOME_DESC = f"{NAME} builds AI agents, voice assistants and automation pipelines that run business operations without manual work."
STACK = ["n8n", "Make.com", "Claude", "Gemini", "Groq", "OpenRouter", "LiveKit", "ElevenLabs", "Tavily", "WhatsApp API",
         "Google Calendar", "Supabase", "Next.js", "Three.js", "Python"]
SCENES_JS = '<script src="/assets/scenes.js" defer></script>\n'
NET_JS = '<script type="module" src="/assets/net.js"></script>\n'
# 400 x 400 for now (LinkedIn size). A bigger original can replace it with no layout change.
PHOTO = "/assets/agha-muhammad-rayyan-khan.webp"
PHOTO_JPG = "/assets/agha-muhammad-rayyan-khan.jpg"
PHOTO_ALT = f"{NAME}, AI systems engineer in Lahore"
# Homepage order of the case studies: the flagship first, as the full-width card.
HOME_CASES = ["jennifer", "call-stream", "al-munir", "bresco", "whatsapp-lead-system"]
TINTS = ["t-a", "t-b", "t-c", "t-d", "t-e"]
# The feed beside the photo starts with these three (home.js rotates more in). Sample events, decorative.
FEED = [("WA", "lead.inbound", "New WhatsApp lead, replied in 9s"),
        ("AI", "ai.qualify", "Intent 87/100, routed to an agent"),
        ("CRM", "crm.sync", "Contact and notes written")]
NAV = [("#work", "Work"), ("#services", "Services"), ("#process", "Process"), ("/projects", "All projects")]


def home_head(schema: list[dict]) -> str:
    url = f"{SITE}/"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{e(HOME_TITLE)}</title>
<meta name="description" content="{e(HOME_DESC)}" />
<link rel="canonical" href="{url}" />
<link rel="icon" href="/favicon.ico" sizes="32x32 48x48" />
<link rel="icon" href="/favicon-96.png" type="image/png" sizes="96x96" />
<link rel="apple-touch-icon" href="/apple-touch-icon.png" />
<meta property="og:title" content="{NAME}, AI Systems &amp; Automation Engineer" />
<meta property="og:description" content="{e(HOME_DESC)}" />
<meta property="og:type" content="website" />
<meta property="og:url" content="{url}" />
<meta property="og:site_name" content="{NAME}" />
<meta property="og:image" content="{SITE}/og.png" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="theme-color" content="#F3F4F6" />
<link rel="preload" as="image" href="{PHOTO}" type="image/webp" fetchpriority="high" />
<script type="application/ld+json">
{json.dumps({"@context": "https://schema.org", "@graph": schema}, indent=1, ensure_ascii=False)}
</script>
<script>
{MOTION_FLAG}
/* Boot screen once per session. home.js runs it and clears the flag; a 4.5 s cap keeps a failed script from hiding the page. */
(function(){{var d=document.documentElement;if(matchMedia('(prefers-reduced-motion: reduce)').matches)return;var b=false;try{{b=!sessionStorage.getItem('booted')}}catch(e){{}}if(b){{d.classList.add('booting');setTimeout(function(){{d.classList.remove('booting')}},4500)}}}})();
</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@500;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet" media="print" onload="this.media='all'">
<link rel="stylesheet" href="/assets/home.css" />
<link rel="stylesheet" href="/assets/chat.css" />
</head>
<body>
<div class="boot" id="boot" data-systems="{len(PROJECTS)}" aria-hidden="true"><div class="boot-in">
  <div class="boot-brand"><img src="{PHOTO}" alt="" width="30" height="30" /><span>RAYYAN / SYSTEMS</span></div>
  <ol class="boot-log" id="bootLog"></ol>
  <div class="boot-bar"><i id="bootBar"></i></div>
  <div class="boot-meta"><span id="bootPct">000</span><span>LAHORE · PK</span></div>
</div></div>
<div class="grain" aria-hidden="true"></div>
<header class="pill" id="pill">
  <a href="/" class="pill-brand" aria-label="{NAME}, home"><img src="{PHOTO}" alt="" width="34" height="34" /><span>Rayyan Khan</span></a>
  <nav class="pill-links" aria-label="Main">{''.join(f'<a href="{h}">{t}</a>' for h, t in NAV)}<span class="pill-ind" aria-hidden="true"></span></nav>
  <a href="#contact" class="pill-cta"><span class="dot" aria-hidden="true"></span><span class="t">Work with me</span></a>
  <button type="button" class="pill-menu" aria-expanded="false" aria-controls="sheet" aria-label="Open menu"><i></i></button>
</header>
<nav class="sheet" id="sheet" aria-label="Site menu">
  {''.join(f'<a href="{h}">{t}</a>' for h, t in NAV)}<a href="#contact">Contact</a>
  <small>Services</small>{''.join(f'<a href="/{s["slug"]}" style="font-size:1.3rem">{e(SERVICE_NAMES[s["slug"]])}</a>' for s in SERVICES)}
</nav>
<main>
"""


def home_hero() -> str:
    films = len({p["film"] for p in PROJECTS if p["film"]})
    stats = [(len(PROJECTS), "Systems shipped"), (films, "Walkthrough films"), (len(CASES), "Full case studies")]
    dl = "".join(f'<div><dt data-count="{v}">{v}</dt><dd>{e(l)}</dd></div>' for v, l in stats)
    notes = "".join(f'<div class="note n{i+1}"><i>{e(a)}</i><div><b>{e(b)}</b><span>{e(c)}</span></div></div>' for i, (a, b, c) in enumerate(FEED))
    return f"""
<section class="hero" aria-labelledby="h1">
  <div class="container">
    <div class="hero-panel">
      <div class="hero-copy">
        <div class="status" data-hi><span class="pulse" aria-hidden="true"></span>Available for AI automation projects</div>
        <h1 id="h1"><span class="ln"><span>AI systems that</span></span> <span class="ln"><span>run the work</span></span> <span class="ln"><span class="dim">while you sleep.</span></span></h1>
        <p class="lede">I'm {NAME}, an AI systems engineer in Lahore. I build <strong>AI agents, voice assistants, WhatsApp bots and automation pipelines</strong> that answer leads, qualify them, update your CRM and hand your team the next action.</p>
        <div class="actions" data-hi><a href="#work" class="btn btn-ink">See the systems{ARROW}</a><a href="#contact" class="btn btn-line">Book a free automation audit</a></div>
        <dl class="stats" data-hi>{dl}</dl>
      </div>
      <div class="hero-vis">
        <span class="tagline t1" aria-hidden="true" data-depth="0.4">n8n · Claude · Gemini</span>
        <span class="tagline t2" aria-hidden="true" data-depth="0.5">Urdu + English</span>
        <figure class="me">
          <img src="{PHOTO}" alt="{e(PHOTO_ALT)}" width="400" height="400" fetchpriority="high" />
          <figcaption><span><b>Rayyan</b> · Lahore, PK</span><span class="live"><span class="pulse red" aria-hidden="true"></span>systems live</span></figcaption>
        </figure>
        <div class="feed" aria-hidden="true" data-depth="1">{notes}</div>
      </div>
    </div>
  </div>
  {marquee(STACK)}
</section>"""


def home_work() -> str:
    cards = []
    for i, slug in enumerate(HOME_CASES):
        c = CASE_BY[slug]
        hero_film = c.get("hero_film", c["film"])
        stack = " / ".join(c["chips"][:4])
        cards.append(f"""      <article class="work{' feat' if i == 0 else ''}" data-rv>
        <div class="stage {TINTS[i]}">
          <div class="meta" aria-hidden="true"><span>Case {case_no(slug)}</span><span>{'Flagship' if i == 0 else e(c['kind'].split(' · ')[0])}</span></div>
          <div class="screen{' phone' if c['tall'] else ''}">
            <img src="/films/{c['film']}.jpg" alt="Still from the {e(c['name'])} walkthrough film" loading="lazy" width="{720 if c['tall'] else 1280}" height="{1280 if c['tall'] else 720}" />
            <video data-src="/films/{hero_film}.mp4" muted loop playsinline preload="none" aria-hidden="true"></video>
          </div>
        </div>
        <div class="work-body">
          <span class="kind">{e(c['kind'])}</span>
          <h3>{e(c['name'])}</h3>
          <span class="go" aria-hidden="true">{ARROW}</span>
          <p>{e(c['description'])}</p>
          <span class="stack">{e(stack)}</span>
        </div>
        <a href="/work/{slug}" aria-label="Read the {e(c['name'])} case study"></a>
      </article>""")
    return f"""
<section id="work" class="sec" aria-labelledby="work-h">
  <div class="container">
    <div class="sec-head">
      <div><div class="label" data-rv>Case studies · {len(CASES):02d}</div><h2 id="work-h" data-rv>Selected <span class="dim">work.</span></h2></div>
      <div class="side"><p class="lede" data-rv>Five builds, told start to finish: the problem, how it works, the decisions behind it, and a film of it running.</p></div>
    </div>
    <div class="works">
{chr(10).join(cards)}
    </div>
    <div class="works-foot" data-rv><p>Plus {len(PROJECTS) - len(CASES)} more: agents, voice systems, scrapers, platforms and websites.</p><a href="/projects" class="btn btn-line">See all {len(PROJECTS)} projects{ARROW}</a></div>
  </div>
</section>"""


def home_band() -> str:
    films = len({p["film"] for p in PROJECTS if p["film"]})
    nums = [(len(PROJECTS), "Systems shipped"), (films, "Walkthrough films"), (24, "Hours a day they answer")]
    nums_html = "".join(f'<div><dt data-count="{v}" data-suffix="{"/7" if v == 24 else ""}">{v}{"/7" if v == 24 else ""}</dt><dd>{e(l)}</dd></div>' for v, l in nums)
    return f"""
<section class="band" aria-labelledby="band-h">
  <div class="container band-in">
    <div>
      <div class="label" data-rv>Under the hood</div>
      <h2 id="band-h" data-rv>One network. <span class="dim">Every lead through it.</span></h2>
      <p class="lede" data-rv>A lead comes in, an agent qualifies it, the CRM gets written and someone on your team gets the next step. The same loop sits under every system here, tuned to the business.</p>
      <dl class="band-nums" data-rv>{nums_html}</dl>
    </div>
    <div class="net" id="net" aria-hidden="true">
      <canvas id="netCanvas"></canvas>
      <div class="net-read"><span>sys / network</span><span>rot <b id="nrRot">000.0</b>°</span><span>links <b id="nrLinks">000</b></span><span>events <b id="nrEv">0000</b></span></div>
      <span class="live-tag"><span class="pulse red"></span>live</span>
      <div class="hud">
        <div class="hud-tag"><i></i><b>lead.inbound</b><span>new lead · WhatsApp</span></div>
        <div class="hud-tag"><i></i><b>ai.qualify</b><span>intent 87/100</span></div>
        <div class="hud-tag"><i></i><b>crm.sync</b><span>contact + notes written</span></div>
        <div class="hud-tag"><i></i><b>dispatch</b><span>call booked 14:30</span></div>
      </div>
    </div>
  </div>
</section>"""


def home_build() -> str:
    items = []
    for i, (t, p, pts, href, viz) in enumerate(CAPABILITIES):
        svc = f'<a class="svc" href="{href}">{e(SERVICE_NAMES[href.strip("/")])} {ARROW_SM}</a>' if href else ""
        lis = "".join(f"<li>{e(x)}</li>" for x in pts)
        items.append(f"""<li class="cap" data-viz="{viz}" data-rv>
        <button type="button" aria-expanded="false" aria-controls="cap{i}"><span class="n">{i+1:02d}</span><h3>{e(t)}</h3><p>{e(p)}</p></button>
        <div class="more" id="cap{i}"><div><ul>{lis}</ul>{svc}</div></div>
        <span class="bar" aria-hidden="true"><i></i></span>
      </li>""")
    first = CAPABILITIES[0]
    return f"""
<section id="services" class="sec" aria-labelledby="svc-h">
  <div class="container">
    <div class="sec-head">
      <div><div class="label" data-rv>What I build</div><h2 id="svc-h" data-rv>Systems, <span class="dim">not demos.</span></h2></div>
      <div class="side"><p class="lede" data-rv>Anyone can wire a chatbot that answers a question. I build the boring part underneath: the retries, the edge cases, the CRM writes, the thing that still works on a Sunday at 3am.</p></div>
    </div>
    <div class="build">
      <ul class="caps">{''.join(items)}</ul>
      <div class="viewer" aria-hidden="true">
        <div class="viewer-top"><b id="vName">{e(first[0])}</b><span id="vNum">01 / {len(CAPABILITIES):02d}</span></div>
        <div class="proj-viz" data-viz="{first[4]}"></div>
        <div class="vfoot"><span>A scene drawn from a real build</span><span>Pick one on the left</span></div>
      </div>
    </div>
  </div>
</section>"""


def home_more() -> str:
    case_paths = {f"/work/{c['slug']}" for c in CASES}
    more = [p for p in PROJECTS if p["film"] and p.get("case") not in case_paths and p.get("viz")]
    tiles = "".join(f"""<a class="tile" href="/projects#{p['slug']}">
        <div class="proj-viz" data-viz="{p['viz']}"></div>
        <div class="tile-body"><span class="kind">{e(p['tag'])}</span><h3>{e(p['title'])}</h3><p>{e(p['text'])}</p><span class="more">See it in the archive {ARROW_SM}</span></div>
      </a>""" for p in more)
    end = f"""<a class="tile all" href="/projects"><div class="tile-body"><span class="big">{len(PROJECTS)}</span><h3>Every project, in one place.</h3><p>Filter by what you need built: automation, agents, voice, platforms, websites.</p><span class="more">Open the archive {ARROW_SM}</span></div></a>"""
    return f"""
<section class="sec" style="padding-top:0" aria-labelledby="more-h">
  <div class="container">
    <div class="sec-head">
      <div><div class="label" data-rv>More builds</div><h2 id="more-h" data-rv>{len(more)} more, <span class="dim">each with a film.</span></h2></div>
      <div class="side"><p class="lede" data-rv>Agents, voice systems, scraping pipelines and live sites. Swipe through, or open the archive.</p><div class="track-nav" data-rv><button type="button" class="prev" aria-label="Previous projects">{ARROW}</button><button type="button" aria-label="Next projects">{ARROW}</button></div></div>
    </div>
  </div>
  <div class="track">{tiles}{end}</div>
</section>"""


def home_process() -> str:
    proc = "".join(f'<li data-rv><b>{n}</b><h3>{e(t)}</h3><p>{e(p)}</p></li>' for n, t, p in PROCESS)
    return f"""
<section id="process" class="sec" style="padding-top:0" aria-labelledby="proc-h">
  <div class="container">
    <div class="sec-head">
      <div><div class="label" data-rv>How I work</div><h2 id="proc-h" data-rv>Simple process. <span class="dim">Clear handoff.</span></h2></div>
      <div class="side"><p class="lede" data-rv>The goal isn't just a system that works. It's one you understand well enough to explain to your own team without calling me.</p></div>
    </div>
    <ol class="proc">{proc}</ol>
  </div>
</section>"""


def home_contact() -> str:
    return f"""
<section id="contact" class="contact" aria-labelledby="contact-h">
  <div class="container">
    <div class="contact-panel">
      <div class="label" data-rv>Work with me</div>
      <h2 id="contact-h" data-rv style="margin-top:18px">Got a process someone repeats every day? <span class="dim">That's the one.</span></h2>
      <div class="contact-grid">
        <div data-rv>
          <p class="lede">Send me the workflow, your tool stack, or just describe the manual thing that eats your week. I'll tell you what can be automated, what shouldn't be, and what the first useful version looks like.</p>
          <a class="mail" href="mailto:{EMAIL}">{EMAIL}</a>
          <div class="ways"><a href="{WHATSAPP}" target="_blank" rel="noopener">WhatsApp +92 321 8234852</a><a href="https://www.linkedin.com/in/rayyan45/" target="_blank" rel="me noopener">LinkedIn</a><a href="https://github.com/rayyanse" target="_blank" rel="me noopener">GitHub</a></div>
        </div>
        <div class="contact-acts" data-rv>
          <a href="mailto:{EMAIL}?subject=Free%20automation%20audit" class="btn btn-red">Book a free audit{ARROW}</a>
          <button type="button" class="btn btn-line copy" data-copy="{EMAIL}">Copy email<span class="toast" role="status">Copied. Talk soon.</span></button>
        </div>
      </div>
    </div>
  </div>
</section>"""


def home_foot() -> str:
    work = "".join(f'<a href="/work/{c["slug"]}">{e(c["name"])}</a>' for c in CASES)
    serv = "".join(f'<a href="/{s["slug"]}">{e(SERVICE_NAMES[s["slug"]])}</a>' for s in SERVICES)
    return f"""</main>
<footer>
  <div class="container">
    <div class="foot">
      <div><div class="me-line"><img src="{PHOTO}" alt="" width="40" height="40" loading="lazy" />{NAME}</div><p class="lede" style="font-size:.9rem;margin-top:14px">AI systems that do real work. {len(PROJECTS)} shipped, most with a walkthrough film.</p></div>
      <div><h3>Case studies</h3>{work}</div>
      <div><h3>Services</h3>{serv}<a href="/projects">All {len(PROJECTS)} projects</a></div>
      <div><h3>Elsewhere</h3><a href="mailto:{EMAIL}">Email</a><a href="https://www.linkedin.com/in/rayyan45/" rel="me noopener" target="_blank">LinkedIn</a><a href="https://github.com/rayyanse" rel="me noopener" target="_blank">GitHub</a><a href="/seo-ray">SEO-Ray</a></div>
    </div>
    <div class="foot-base"><span>© 2026 {NAME}</span><span>AI systems engineer · Lahore, PK · remote</span></div>
  </div>
</footer>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js" defer></script>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/ScrollTrigger.min.js" defer></script>
<script src="{LENIS}" defer></script>
{SCENES_JS}<script src="/assets/home.js" defer></script>
{NET_JS}{CHAT_WIDGET}<script src="/assets/chat.js" defer></script>
</body>
</html>
"""


def home_page() -> str:
    schema = [
        {"@type": "Person", "@id": f"{SITE}/#person", "name": NAME,
         "alternateName": ["Muhammad Rayyan Khan", "Agha Rayyan", "Muhammad Rayyan", "Rayyan Khan"],
         "url": f"{SITE}/", "image": f"{SITE}{PHOTO_JPG}", "jobTitle": "AI Systems & Automation Engineer",
         "description": "Builds AI agents, voice assistants, automation pipelines and full-stack dashboards for businesses.",
         "address": {"@type": "PostalAddress", "addressLocality": "Lahore", "addressCountry": "PK"},
         "knowsAbout": ["AI agents", "Voice AI", "Workflow automation", "n8n", "WhatsApp automation", "Retrieval-augmented generation"],
         "sameAs": ["https://www.linkedin.com/in/rayyan45/", "https://github.com/rayyanse"]},
        {"@type": "WebSite", "@id": f"{SITE}/#website", "url": f"{SITE}/", "name": NAME, "publisher": {"@id": f"{SITE}/#person"}},
        {"@type": "ItemList", "name": "Case studies", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "url": f"{SITE}/work/{s}", "name": CASE_BY[s]["name"]} for i, s in enumerate(HOME_CASES)]},
    ]
    return (home_head(schema) + home_hero() + home_work() + home_band() + home_build() + home_more()
            + home_process() + home_contact() + home_foot())


# ------------------------------------------------------------------ project archive

def project_card(p: dict, first: bool = False) -> str:
    short = p["title"].split(" — ")[0]
    load = 'fetchpriority="high"' if first else 'loading="lazy"'
    if p.get("viz"):  # the project's animated scene (assets/scenes.js), as on the original homepage
        media = f'<div class="pj-media proj-viz" data-viz="{p["viz"]}" aria-hidden="true"></div>'
    elif p["film"]:
        media = f'<div class="pj-media"><img src="/films/{p["film"]}.jpg" alt="Still from the {e(p["title"])} walkthrough film" {load} width="1280" height="720" /></div>'
    else:
        media = f'<div class="pj-media none" aria-hidden="true"><span>{e(short)}</span></div>'
    pts = ("<ul>" + "".join(f"<li>{e(x)}</li>" for x in p["points"]) + "</ul>") if p["points"] else ""
    metric = f'<div class="pj-metric"><b>{e(p["metric"][0])}</b><span>{e(p["metric"][1])}</span></div>' if p.get("metric") else ""
    stack = "".join(f"<span>{e(x)}</span>" for x in p["stack"])
    acts = []
    if p["case"]:
        acts.append(f'<a class="btn btn-ghost btn-sm" href="{p["case"]}">Read the case study{ARROW}</a>')
    if p["film"]:
        acts.append(f'<button type="button" class="btn btn-ghost btn-sm" data-watch="/films/{p["film"]}.mp4" data-poster="/films/{p["film"]}.jpg">{PLAY}Watch the film</button>')
    if p["site"]:
        acts.append(f'<a class="btn btn-ghost btn-sm" href="{p["site"]}" target="_blank" rel="noopener">{e(p["site_label"])} ↗</a>')
    return f"""<article class="pj" id="{p['slug']}" data-cat="{p['cat']}" data-rv>
      {media}
      <div class="pj-in">
        <span class="pj-tag">{e(p['tag'])}</span>
        <h2>{e(p['title'])}</h2>
        <p>{e(p['text'])}</p>{pts}{metric}
        <div class="pj-stack">{stack}</div>
        <div class="pj-acts">{''.join(acts)}</div>
      </div>
    </article>"""


def projects_page() -> str:
    path = "/projects"
    title = f"All {len(PROJECTS)} projects by {NAME}"
    desc = f"Every AI agent, voice system, automation pipeline, platform and website {NAME} has shipped: {len(PROJECTS)} projects, most with a walkthrough film."
    schema = [
        {"@type": "CollectionPage", "@id": f"{SITE}{path}#page", "name": f"All {len(PROJECTS)} projects", "description": desc, "url": f"{SITE}{path}",
         "author": person(), "mainEntity": {"@type": "ItemList", "itemListElement": [
             {"@type": "ListItem", "position": i + 1, "name": p["title"], "url": SITE + (p["case"] or f"{path}#{p['slug']}")} for i, p in enumerate(PROJECTS)]}},
        crumbs_schema([("Home", "/"), ("All projects", path)]),
    ]
    counts = {k: (len(PROJECTS) if k == "all" else sum(p["cat"] == k for p in PROJECTS)) for k, _ in FILTERS}
    filt = "".join(
        f'<button type="button" class="pj-f{" on" if k == "all" else ""}" data-f="{k}" aria-pressed="{"true" if k == "all" else "false"}">{e(l)} <i>{counts[k]}</i></button>'
        for k, l in FILTERS)
    cards = "\n    ".join(project_card(p, i == 0) for i, p in enumerate(PROJECTS))
    films = len({p["film"] for p in PROJECTS if p["film"]})
    return head(title, desc, path, f"{SITE}/films/jennifer.jpg", schema, f"ARCHIVE &nbsp;·&nbsp; <b>{len(PROJECTS)}</b> PROJECTS",
                og_type="website", preload="/films/jennifer.jpg") + f"""
<section class="pj-hero" aria-labelledby="h1">
  <div class="container">
    <nav class="crumbs" aria-label="Breadcrumb" data-hi><a href="/">Home</a><span aria-hidden="true">/</span><span>All projects</span></nav>
    <div id="h1">{h1([f'{len(PROJECTS)} systems,', '<span class="grad">shipped.</span>'])}</div>
    <p class="lede" data-hi>Agents, voice systems, scraping pipelines, platforms and websites. Each one shows the problem, the stack, and whether you can go use it today. {films} have a walkthrough film; {len(CASES)} have a full case study.</p>
    <div class="pj-filters" role="toolbar" aria-label="Filter projects" data-hi>{filt}</div>
  </div>
</section>
<section class="pj-list" aria-label="Projects">
  <div class="container pj-grid">
    {cards}
  </div>
</section>
""" + cta("Want one of these, built around your business?") + foot(SCENES_JS)


def main() -> None:
    (ROOT / "work").mkdir(exist_ok=True)
    for c in CASES:
        (ROOT / "work" / f"{c['slug']}.html").write_text(case_page(c), encoding="utf-8")
    for s in SERVICES:
        (ROOT / f"{s['slug']}.html").write_text(service_page(s), encoding="utf-8")
    (ROOT / "projects.html").write_text(projects_page(), encoding="utf-8")
    (ROOT / "index.html").write_text(home_page(), encoding="utf-8")
    write_sitemap()
    print(f"built the homepage, the {len(PROJECTS)}-project archive, {len(CASES)} case studies, {len(SERVICES)} service pages and sitemap.xml")


def write_sitemap() -> None:
    """Every generated page, plus the hand-written pages in HAND_PAGES. lastmod is the build date
    (FILM_DATE) for generated pages; bump it when content changes."""
    paths = ["/", "/projects"] + [f"/{s['slug']}" for s in SERVICES] + [f"/work/{c['slug']}" for c in CASES]
    entries = [(p, FILM_DATE) for p in paths] + HAND_PAGES
    urls = "".join(f"  <url>\n    <loc>{SITE}{p}</loc>\n    <lastmod>{d}</lastmod>\n  </url>\n" for p, d in entries)
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "</urlset>\n"
    (ROOT / "sitemap.xml").write_text(xml, encoding="utf-8")


if __name__ == "__main__":
    main()
