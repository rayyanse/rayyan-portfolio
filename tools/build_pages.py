"""Builds the case-study and service pages of rayyankhan.dev from the data below.

Run from the repo root:  python tools/build_pages.py
Writes work/<slug>.html and <service-slug>.html. Vercel's cleanUrls serves them
without the .html extension. Edit facts here, never in the generated HTML.

Every claim must be true: facts come from the project cards on index.html,
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
SAMPLE = "Walkthrough film · names and numbers are sample data"

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
        "label": "Service · AI voice agents",
        "title": "AI Voice Agent Developer: Urdu and English Call Agents",
        "description": "AI voice agents that answer your phone in Urdu or English, book appointments into your calendar and call leads back, even on your existing number.",
        "h1": ["AI voice agents", "that answer in Urdu", '<span class="grad">and book the slot.</span>'],
        "lede": "I build voice agents that answer your phone, hold a real conversation in Urdu or English, check your calendar and book the appointment. They can run on your existing mobile number, with no SIP trunk and no new number.",
        "film": "booking", "tall": False, "note": SAMPLE,
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
        "label": "Service · WhatsApp automation",
        "title": "WhatsApp Automation in Pakistan: Bots, Routing, Campaigns",
        "description": "WhatsApp bots that reply to leads in seconds in Roman Urdu or English, route them to the right person and send quotes, built in Lahore.",
        "h1": ["WhatsApp automation", "that replies", '<span class="grad">before the lead goes cold.</span>'],
        "lede": "For most local businesses, leads arrive on WhatsApp. I build the bots, routing and campaigns that reply in seconds, in Roman Urdu or English, and hand the conversation to the right person on your team.",
        "film": "almunir", "tall": False, "note": SAMPLE,
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


def head(title: str, description: str, path: str, image: str, schema: list[dict]) -> str:
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
<meta property="og:type" content="article" />
<meta property="og:url" content="{url}" />
<meta property="og:site_name" content="{NAME}" />
<meta property="og:image" content="{image}" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="theme-color" content="#05070C" />
<script type="application/ld+json">
{json.dumps({"@context": "https://schema.org", "@graph": schema}, indent=1, ensure_ascii=False)}
</script>
<script>
/* Motion start states only when motion is allowed; cleared if GSAP never arrives. */
(function(){{var d=document.documentElement;if(!matchMedia('(prefers-reduced-motion: reduce)').matches){{d.classList.add('js-motion');setTimeout(function(){{if(!window.__motionOK)d.classList.remove('js-motion')}},2500)}}}})();
</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet" media="print" onload="this.media='all'">
<link rel="stylesheet" href="/assets/site.css" />
</head>
<body>
<div class="field"><div class="orb a"></div><div class="orb b"></div></div>
<div class="grain" aria-hidden="true"></div>
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
        <div class="dd"><a href="/#work" class="dd-t">Work</a><div class="dd-m">{work}<a href="/#work" class="dd-all">All projects</a></div></div>
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
  <h3>Case studies</h3>{work}<a href="/#work">All projects</a>
  <h3>More</h3><a href="/#process">How I work</a><a href="/">Home</a>
  <a href="/#contact" class="mm-cta">Work with me</a>
</div></nav>"""


def film(name: str, tall: bool, note: str, poster: str | None = None) -> str:
    """Hero film. `name` is the video file, `poster` the still (defaults to the same name)."""
    return f"""<div class="film{' tall' if tall else ''}">
        <video src="/films/{name}.mp4" poster="/films/{poster or name}.jpg" muted loop playsinline preload="metadata" aria-label="Walkthrough film"></video>
        <div class="film-bar"><button type="button" class="film-sound" aria-pressed="false">{SOUND}<span>Play with sound</span></button></div>
      </div>
      <p class="film-note" data-hi>{e(note)}</p>"""


def cta(heading: str) -> str:
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


def foot() -> str:
    work = "".join(f'<a href="/work/{c["slug"]}">{e(c["name"])}</a>' for c in CASES)
    serv = "".join(f'<a href="/{s["slug"]}">{e(SERVICE_NAMES[s["slug"]])}</a>' for s in SERVICES)
    return f"""</main>
<footer>
  <div class="container">
    <div class="foot-grid">
      <div><h3>{NAME}</h3><a href="/">AI systems that do real work. 20+ shipped, each with a walkthrough film.</a><a href="mailto:{EMAIL}">{EMAIL}</a><a href="https://www.linkedin.com/in/rayyan45/" rel="me noopener" target="_blank">LinkedIn</a><a href="https://github.com/rayyanse" rel="me noopener" target="_blank">GitHub</a></div>
      <div><h3>Case studies</h3>{work}</div>
      <div><h3>Services</h3>{serv}<a href="/#work">All projects</a></div>
    </div>
    <div class="foot-base"><span>© 2026 {NAME}</span><span>AI SYSTEMS ENGINEER · LAHORE, PK · REMOTE</span></div>
  </div>
</footer>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js" defer></script>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/ScrollTrigger.min.js" defer></script>
<script src="/assets/site.js" defer></script>
</body>
</html>
"""


def card(slug: str) -> str:
    c = CASE_BY[slug]
    return f"""<a class="rcard" href="/work/{slug}" data-rv>
        <img src="/films/{c['film']}.jpg" alt="Still from the {e(c['name'])} walkthrough film" loading="lazy" width="1280" height="720" />
        <div class="rc-body"><div class="rc-kind">{e(c['kind'])}</div><h3>{e(c['name'])}</h3><p>{e(c['description'])}</p><span class="more">Read the case study {ARROW_SM}</span></div>
      </a>"""


def person() -> dict:
    return {"@type": "Person", "@id": f"{SITE}/#person", "name": NAME, "url": f"{SITE}/"}


def crumbs_schema(items: list[tuple[str, str]]) -> dict:
    return {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": f"{SITE}{p}"} for i, (n, p) in enumerate(items)]}


def video_schema(name: str, description: str, film_name: str) -> dict:
    return {"@type": "VideoObject", "name": f"{name} walkthrough film", "description": description, "thumbnailUrl": f"{SITE}/films/{film_name}.jpg", "contentUrl": f"{SITE}/films/{film_name}.mp4", "uploadDate": FILM_DATE}


def h1(lines: list[str]) -> str:
    return "<h1>" + " ".join(f'<span class="ln"><span>{l}</span></span>' for l in lines) + "</h1>"


def case_page(c: dict) -> str:
    path = f"/work/{c['slug']}"
    svc = c["service"]
    schema = [
        {"@type": "CreativeWork", "@id": f"{SITE}{path}#work", "name": c["name"], "headline": c["title"], "description": c["description"], "url": f"{SITE}{path}", "author": person(), "image": f"{SITE}/films/{c['film']}.jpg", "video": video_schema(c["name"], c["description"], c["film"])},
        crumbs_schema([("Home", "/"), ("Work", "/#work"), (c["name"], path)]),
    ]
    steps = "".join(f'<li class="step" data-n="{i+1:02d}" data-rv><h3>{e(t)}</h3><p>{e(p)}</p></li>' for i, (t, p) in enumerate(c["steps"]))
    decisions = "".join(f'<li data-rv><div><h3>{e(t)}</h3><p>{e(p)}</p></div></li>' for t, p in c["decisions"])
    def fact(v: str, label: str) -> str:
        num = v.isdigit()
        return f'<div><dt{f" data-count={chr(34)}{v}{chr(34)}" if num else ""}>{e(v)}</dt><dd>{e(label)}</dd></div>'
    facts = "".join(fact(v, l) for v, l in c["facts"])
    chips = "".join(f'<span class="chip">{e(x)}</span>' for x in c["chips"])
    limits = f'<p class="limits" data-rv><b>Honest limits</b>{e(c["limits"])}</p>' if c["limits"] else ""
    related = "".join(card(s) for s in c["related"])
    return head(c["title"], c["description"], path, f"{SITE}/films/{c['film']}.jpg", schema) + f"""
<section class="phero{' tall' if c['tall'] else ''}">
  <div class="container phero-grid">
    <div>
      <nav class="crumbs" aria-label="Breadcrumb" data-hi><a href="/">Home</a><span aria-hidden="true">/</span><a href="/#work">Work</a><span aria-hidden="true">/</span><span>{e(c['name'])}</span></nav>
      <div class="label" data-hi>{e(c['kind'])}</div>
      {h1(c['h1'])}
      <p class="lede" data-hi>{e(c['lede'])}</p>
      <div class="actions" data-hi><a href="mailto:{EMAIL}?subject={e(c['name'])}%20-%20something%20like%20this" class="btn btn-primary">Build something like this{ARROW}</a><a href="/{svc}" class="btn btn-ghost">{e(SERVICE_NAMES[svc])}</a></div>
      <div class="chips" data-hi>{chips}</div>
    </div>
    <div>
      {film(c.get('hero_film', c['film']), c['tall'], c['note'], poster=c['film'])}
    </div>
  </div>
</section>

<section class="band" aria-labelledby="problem-h">
  <div class="container split">
    <div data-rv><div class="label" id="problem-h">The problem</div><p class="big">{c['problem']}</p></div>
    <p class="lede" data-rv>{e(c['problem_p'])}</p>
  </div>
</section>

<section aria-labelledby="how-h">
  <div class="container split">
    <div>
      <div class="sec-head" data-rv><div class="label">How it works</div><h2 id="how-h">Step by step</h2></div>
      <ol class="steps"><span class="rail" aria-hidden="true"></span>{steps}</ol>
    </div>
    <aside class="facts" data-rv><h3>At a glance</h3><dl>{facts}</dl></aside>
  </div>
</section>

<section class="band" aria-labelledby="dec-h">
  <div class="container">
    <div class="sec-head" data-rv><div class="label">Under the hood</div><h2 id="dec-h">The decisions that mattered</h2></div>
    <ul class="decisions">{decisions}</ul>
    {limits}
  </div>
</section>

<section aria-labelledby="rel-h">
  <div class="container">
    <div class="sec-head" data-rv><div class="label">More work</div><h2 id="rel-h">Related builds</h2><p class="lede">Or see what I build as a service: <a href="/{svc}"><strong>{e(SERVICE_NAMES[svc])}</strong></a>.</p></div>
    <div class="related">{related}</div>
  </div>
</section>
""" + cta("Want one of these for your business?") + foot()


def service_page(s: dict) -> str:
    path = f"/{s['slug']}"
    schema = [
        {"@type": "Service", "@id": f"{SITE}{path}#service", "name": SERVICE_NAMES[s["slug"]], "description": s["description"], "url": f"{SITE}{path}", "provider": person(), "areaServed": ["Pakistan", "Worldwide"]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in s["faq"]]},
        crumbs_schema([("Home", "/"), (SERVICE_NAMES[s["slug"]], path)]),
    ]
    offer = "".join(f'<li data-rv><h3>{e(t)}</h3><p>{e(p)}</p></li>' for t, p in s["offer"])
    proof = "".join(card(x) for x in s["proof"])
    proc = "".join(f'<li data-rv><b>{n}</b><h3>{e(t)}</h3><p>{e(p)}</p></li>' for n, t, p in PROCESS)
    faq = "".join(f'<details data-rv><summary><h3>{e(q)}</h3><i aria-hidden="true"></i></summary><div class="a"><p>{e(a)}</p></div></details>' for q, a in s["faq"])
    return head(s["title"], s["description"], path, f"{SITE}/films/{s['film']}.jpg", schema) + f"""
<section class="phero">
  <div class="container phero-grid">
    <div>
      <nav class="crumbs" aria-label="Breadcrumb" data-hi><a href="/">Home</a><span aria-hidden="true">/</span><span>{e(SERVICE_NAMES[s['slug']])}</span></nav>
      <div class="label" data-hi>{e(s['label'])}</div>
      {h1(s['h1'])}
      <p class="lede" data-hi>{e(s['lede'])}</p>
      <div class="actions" data-hi><a href="mailto:{EMAIL}?subject={e(SERVICE_NAMES[s['slug']])}" class="btn btn-primary">Book a free audit{ARROW}</a><a href="#proof" class="btn btn-ghost">See the work</a></div>
    </div>
    <div>
      {film(s['film'], s['tall'], s['note'])}
    </div>
  </div>
</section>

<section class="band" aria-labelledby="offer-h">
  <div class="container">
    <div class="sec-head" data-rv><div class="label">What I build</div><h2 id="offer-h">What you get</h2></div>
    <ul class="offer">{offer}</ul>
  </div>
</section>

<section id="proof" aria-labelledby="proof-h">
  <div class="container">
    <div class="sec-head" data-rv><div class="label">Proof</div><h2 id="proof-h">Built and running</h2><p class="lede">Real systems, each with a walkthrough film of it working.</p></div>
    <div class="related">{proof}</div>
  </div>
</section>

<section class="band" aria-labelledby="proc-h">
  <div class="container">
    <div class="sec-head" data-rv><div class="label">How I work</div><h2 id="proc-h">Simple process. Clear handoff.</h2></div>
    <ol class="proc">{proc}</ol>
  </div>
</section>

<section aria-labelledby="faq-h">
  <div class="container">
    <div class="sec-head" data-rv><div class="label">Questions</div><h2 id="faq-h">What clients ask first</h2></div>
    <div class="faq">{faq}</div>
  </div>
</section>
""" + cta("Got a process someone repeats every day?") + foot()


def main() -> None:
    (ROOT / "work").mkdir(exist_ok=True)
    for c in CASES:
        (ROOT / "work" / f"{c['slug']}.html").write_text(case_page(c), encoding="utf-8")
    for s in SERVICES:
        (ROOT / f"{s['slug']}.html").write_text(service_page(s), encoding="utf-8")
    write_sitemap()
    print(f"built {len(CASES)} case studies, {len(SERVICES)} service pages and sitemap.xml")


def write_sitemap() -> None:
    """Homepage plus every generated page. lastmod is the build date (FILM_DATE), bump it when content changes."""
    paths = ["/"] + [f"/{s['slug']}" for s in SERVICES] + [f"/work/{c['slug']}" for c in CASES]
    urls = "".join(f"  <url>\n    <loc>{SITE}{p}</loc>\n    <lastmod>{FILM_DATE}</lastmod>\n  </url>\n" for p in paths)
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "</urlset>\n"
    (ROOT / "sitemap.xml").write_text(xml, encoding="utf-8")


if __name__ == "__main__":
    main()
