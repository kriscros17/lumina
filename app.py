# ╔══════════════════════════════════════════════════════════════════════╗
# ║              LUMINA — WELLNESS & SOUL ORACLE                        ║
# ║              app.py  —  The entire Python backend                   ║
# ╚══════════════════════════════════════════════════════════════════════╝
#
# ──────────────────────────────────────────────────────────────────────
# BEGINNER EXPLANATION
# ──────────────────────────────────────────────────────────────────────
# This file is the "brain" of the application. When you open the app in
# your browser, the browser (frontend) talks to this Python file
# (backend) by sending HTTP requests — like pressing a button on a TV
# remote, and this file is the TV that responds.
#
# We use a library called Flask to make Python able to "speak HTTP".
# Think of Flask as a waiter: it receives orders (requests) from the
# browser, processes them using our Python logic, and returns answers
# (responses) as JSON — which is just structured text data.
# ──────────────────────────────────────────────────────────────────────


# ── IMPORTS ────────────────────────────────────────────────────────────
# "import" means: "go fetch this toolkit and make it available here."

from flask import Flask, render_template, request, jsonify, session
# Flask       → the web framework (the waiter that handles browser requests)
# render_template → tells Flask to send our HTML file to the browser
# request     → lets us read data sent BY the browser (e.g. form values)
# jsonify     → converts Python dictionaries into JSON text for the browser
# session     → a small private storage box for each user's visit

from datetime import datetime, date
# datetime    → gives us the current date and time
# date        → used for calendar date calculations (moon phase)

import math
# math        → gives us mathematical functions like floor(), sin(), cos()
# We need it for the moon phase calculation formula

import uuid
# uuid        → generates unique random IDs (like fingerprints for records)

import os


# ── CREATE THE FLASK APP ────────────────────────────────────────────────
# This one line creates our entire web application object.
# Think of it as: "open the restaurant for business."

app = Flask(__name__)

# __name__ is a special Python variable that holds the name of the current
# file. Flask uses it to find your HTML templates and static files.

app.secret_key = "lumina_vintage_journal_2024"
# Sessions (user storage) are encrypted. This secret_key is the lock.
# In a real production app, this would be a long random string stored
# in an environment variable — never hardcoded like this.


# ══════════════════════════════════════════════════════════════════════
# SECTION 1: DATA — THE KNOWLEDGE BASE
# ══════════════════════════════════════════════════════════════════════
#
# Python dictionaries ({ }) are like filing cabinets.
# Each "key" is a label (like a tab), and each "value" is the content.
# Example: {"name": "Alice", "age": 30}  →  key="name", value="Alice"
#
# We store all our personality profiles and mood data here as big
# nested dictionaries. This is cleaner than putting it in a database
# for a small app like this.

# ── MOOD STATES ────────────────────────────────────────────────────────
# Six emotional states mapped to score ranges 0–100.
# Each state carries: its score range, colours, descriptions, advice.

MOOD_STATES = {
    "Radiant": {
        "range": (85, 100),          # tuple: (min_score, max_score)
        "symbol": "✦",
        "palette": ["#E8B86D", "#D4956A", "#C17B5C", "#8B4513", "#6B3410"],
        "ink": "#8B4513",
        "desc": "You carry a rare, full-spectrum aliveness today. Something in you is alight.",
        "tip": "Channel this into creating something — a letter, a sketch, a conversation.",
        "affirmation": "You are a lamp that lit itself. Let others see it.",
        "activity": "Write a letter to someone you've been meaning to thank.",
        "color_therapy": "Surround yourself with warm amber and gold today.",
        "element": "Fire",
        "breath": {"name": "Solar Breath", "in": 4, "hold": 4, "out": 4}
    },
    "Serene": {
        "range": (70, 84),
        "symbol": "◈",
        "palette": ["#5B8DB8", "#7AAFD4", "#9DC4D8", "#B8D9E8", "#D4ECF5"],
        "ink": "#2E6B9E",
        "desc": "Still water. You move with quiet purpose, unhurried and clear.",
        "tip": "This is your finest hour for deep work, reading, or meaningful conversation.",
        "affirmation": "Calm is not emptiness. It is the fullness of being present.",
        "activity": "Sit with a cup of tea and write three things you are grateful for.",
        "color_therapy": "Blues and soft teals help you hold this peace.",
        "element": "Water",
        "breath": {"name": "Ocean Breath", "in": 5, "hold": 2, "out": 5}
    },
    "Balanced": {
        "range": (55, 69),
        "symbol": "◉",
        "palette": ["#6B8F5E", "#8AAF7A", "#A8C99A", "#C4DEB8", "#DFF0D8"],
        "ink": "#4A6741",
        "desc": "Rooted and steady. Not everything is perfect, but you are holding your ground.",
        "tip": "Small acts of care tip the balance. A walk. A warm meal. A quiet moment.",
        "affirmation": "You are enough, exactly as you stand right now.",
        "activity": "Step outside for ten minutes without your phone.",
        "color_therapy": "Greens and earthy tones ground and restore you.",
        "element": "Earth",
        "breath": {"name": "Tree Breath", "in": 4, "hold": 4, "out": 6}
    },
    "Reflective": {
        "range": (40, 54),
        "symbol": "◐",
        "palette": ["#7B5EA7", "#9B7FC4", "#B8A0D8", "#D4C4EC", "#EDE4F8"],
        "ink": "#5A3E8A",
        "desc": "Inward and quiet. The weight you carry today is asking to be heard.",
        "tip": "Don't push through. Sit with it. Write it down. Let it speak.",
        "affirmation": "Every feeling is a letter. Read it — it was sent for a reason.",
        "activity": "Write three lines about what is weighing on your heart today.",
        "color_therapy": "Soft lavenders and muted purples honour your inner world.",
        "element": "Ether",
        "breath": {"name": "Lantern Breath", "in": 4, "hold": 0, "out": 7}
    },
    "Weathering": {
        "range": (20, 39),
        "symbol": "◑",
        "palette": ["#6B7B8D", "#8A9BAD", "#A8B8C8", "#C4D0DC", "#DDE6EE"],
        "ink": "#4A5C6E",
        "desc": "Heavy weather. Showing up when everything is hard is a kind of courage.",
        "tip": "Reach out to one person today. Not to explain — just to connect.",
        "affirmation": "Every storm you have ever faced — you survived it.",
        "activity": "Drink a glass of water. Step outside. Take three slow breaths.",
        "color_therapy": "Slate blues and stone greys meet you where you are.",
        "element": "Air",
        "breath": {"name": "Anchor Breath", "in": 5, "hold": 3, "out": 7}
    },
    "Depleted": {
        "range": (0, 19),
        "symbol": "◯",
        "palette": ["#B56A5A", "#C98070", "#D99888", "#EDB8A8", "#F8D8CC"],
        "ink": "#8B4035",
        "desc": "Running on empty. Your body and soul are asking — quietly but clearly — for rest.",
        "tip": "Rest is not retreat. It is the ground that makes new growth possible.",
        "affirmation": "Even a wick burned to nothing once held great light.",
        "activity": "Lie down. Close your eyes. Do nothing for ten minutes. That is enough.",
        "color_therapy": "Warm terracottas and rose tones remind you of warmth.",
        "element": "Earth",
        "breath": {"name": "Ember Breath", "in": 4, "hold": 0, "out": 8}
    }
}


# ── MBTI PROFILES ──────────────────────────────────────────────────────
# All 16 Myers-Briggs types, each with full profile data.
# The "group" key groups them by cognitive family (NT, NF, SJ, SP).

MBTI_PROFILES = {
    "INTJ": {
        "name": "The Architect", "group": "NT",
        "tagline": "Strategic, private, relentlessly driven.",
        "desc": "INTJs are rare master strategists. They see the world as a system to be understood and improved. Fiercely independent and intensely private, they hold themselves and everyone around them to exacting standards. Behind the composed exterior lives one of the most passionate inner worlds of any type.",
        "strengths": ["Long-range strategic thinking", "Decisive under ambiguity", "Intellectual rigour", "Independent vision"],
        "growth": "Learning to receive care as easily as they give direction.",
        "partner_types": ["ENFP", "ENTP"],
        "partner_reason": "The ENFP's warmth, emotional fluency, and spontaneous joy thaws the INTJ's reserve in ways that feel like magic rather than effort. The ENTP matches their intellectual sharpness — a worthy equal.",
        "ideal_traits": ["Intellectually independent", "Emotionally self-sufficient", "Direct — no games", "Respects ambition and solitude"],
        "ink_color": "#2C4A7C"
    },
    "INTP": {
        "name": "The Logician", "group": "NT",
        "tagline": "Analytical, inventive, perpetually curious.",
        "desc": "INTPs live inside ideas. They are quiet architects of theories, endlessly pulling threads to see where systems lead. Flexible and open-minded to a fault, they will argue any position if it points toward something true.",
        "strengths": ["Deep analytical reasoning", "Creative problem-solving", "Intellectual flexibility", "Pattern recognition across domains"],
        "growth": "Turning insight into action, and thought into genuine connection.",
        "partner_types": ["ENTJ", "ENFJ"],
        "partner_reason": "The ENTJ provides drive and structure that anchors the INTP's free-floating brilliance. The ENFJ's warmth draws them out of their head and into the felt world.",
        "ideal_traits": ["Highly curious", "Patient with silence", "Honest and direct", "Not threatened by debate"],
        "ink_color": "#2C4A7C"
    },
    "ENTJ": {
        "name": "The Commander", "group": "NT",
        "tagline": "Bold, efficient, born to lead.",
        "desc": "ENTJs are natural executives — visionary, decisive, energised by challenge. They don't wait for opportunity; they manufacture it. Their directness can feel startling, but it comes from a belief that excellence is owed to everyone.",
        "strengths": ["Strategic vision", "Bold decision-making", "Natural leadership", "High-performance drive"],
        "growth": "Slowing down enough to truly hear the people they are leading.",
        "partner_types": ["INFP", "INTP"],
        "partner_reason": "The INFP softens the ENTJ's hard edges with deep empathy and creative imagination. The INTP offers the intellectual equal-match they quietly require.",
        "ideal_traits": ["Confident and self-directed", "Emotionally mature", "Ambitious in their own right", "Able to hold ground in disagreement"],
        "ink_color": "#2C4A7C"
    },
    "ENTP": {
        "name": "The Debater", "group": "NT",
        "tagline": "Quick-witted, innovative, relentlessly exploratory.",
        "desc": "ENTPs are idea generators who grow bored the instant they have understood something. They argue not from ego but from love of intellectual collision. Their charm is magnetic and their mind is never still.",
        "strengths": ["Rapid creative ideation", "Wit and adaptability", "Seeing all angles", "Entrepreneurial instinct"],
        "growth": "Following through once the exciting beginning has passed.",
        "partner_types": ["INTJ", "INFJ"],
        "partner_reason": "The INTJ grounds the ENTP with strategic focus. The INFJ provides depth and moral clarity the ENTP finds quietly magnetic.",
        "ideal_traits": ["Intellectually playful", "Not easily rattled", "Emotionally available", "Has strong opinions of their own"],
        "ink_color": "#2C4A7C"
    },
    "INFJ": {
        "name": "The Advocate", "group": "NF",
        "tagline": "Visionary, empathetic, quietly powerful.",
        "desc": "INFJs are rare: they combine deep intuition about people with a clarity of purpose that borders on prophetic. They carry enormous inner lives and pour themselves into meaningful work. They feel everything — and choose carefully who sees it.",
        "strengths": ["Profound empathy", "Long-range vision", "Deep integrity", "Rare emotional intelligence"],
        "growth": "Letting people in before they have proven themselves worthy.",
        "partner_types": ["ENFP", "ENTP"],
        "partner_reason": "The ENFP's warmth coaxes the INFJ out of their protective shell. The ENTP brings stimulating conversation that keeps their ever-active mind engaged.",
        "ideal_traits": ["Emotionally intelligent", "Curious about ideas", "Consistent and trustworthy", "Values meaningful growth"],
        "ink_color": "#3D6B4A"
    },
    "INFP": {
        "name": "The Mediator", "group": "NF",
        "tagline": "Idealistic, empathetic, quietly revolutionary.",
        "desc": "INFPs hold a rich, complex inner world and are fiercely committed to their values. They are natural healers who lead from the heart. Their gentleness hides moral stubbornness — they will not compromise on what matters.",
        "strengths": ["Deep empathy", "Creative imagination", "Authentic self-expression", "Values-driven integrity"],
        "growth": "Acting on their ideals rather than carrying them silently.",
        "partner_types": ["ENFJ", "ENTJ"],
        "partner_reason": "The ENFJ's warmth and encouragement helps the INFP actualise their gifts. The ENTJ offers a safe structure for the INFP's expansive inner life.",
        "ideal_traits": ["Emotionally present", "Appreciates depth", "Authentic — no performance", "Supportive of creative vision"],
        "ink_color": "#3D6B4A"
    },
    "ENFJ": {
        "name": "The Protagonist", "group": "NF",
        "tagline": "Charismatic, empathetic, born to uplift.",
        "desc": "ENFJs see potential in people before those people see it in themselves. Driven by an almost compulsive desire to help and grow, they lead others effortlessly. They are the most human of all types.",
        "strengths": ["Inspiring leadership", "Emotional intelligence", "Natural connector", "Strategic empathy"],
        "growth": "Remembering to receive, not only give.",
        "partner_types": ["INFP", "ISFP"],
        "partner_reason": "The INFP's depth and sincerity resonates with the ENFJ's need for authentic connection. The ISFP brings present-moment warmth that grounds the future-oriented ENFJ.",
        "ideal_traits": ["Emotionally genuine", "Lets themselves be cared for", "Has inner depth", "Appreciates being truly seen"],
        "ink_color": "#3D6B4A"
    },
    "ENFP": {
        "name": "The Campaigner", "group": "NF",
        "tagline": "Enthusiastic, creative, irrepressibly alive.",
        "desc": "ENFPs see possibility everywhere and in everyone. Their warmth is genuine, their creativity boundless, and their restlessness is the price of their brilliance. They love deeply and freely.",
        "strengths": ["Magnetic enthusiasm", "Creative vision", "Emotional warmth", "Ability to inspire"],
        "growth": "Channelling boundless energy into consistent follow-through.",
        "partner_types": ["INTJ", "INFJ"],
        "partner_reason": "The INTJ's depth and mystery is irresistible to the ENFP. The INFJ meets them in vision and soul — a rare and profound match.",
        "ideal_traits": ["Intellectually deep", "Emotionally grounded", "Appreciates spontaneity", "Offers quiet stability"],
        "ink_color": "#3D6B4A"
    },
    "ISTJ": {
        "name": "The Logistician", "group": "SJ",
        "tagline": "Reliable, thorough, the backbone of everything.",
        "desc": "ISTJs are the quiet guarantors of the world. They do what they say, when they say it, without fanfare. Their loyalty runs bone-deep. They show love by showing up, every time, without exception.",
        "strengths": ["Absolute reliability", "Methodical precision", "Deep loyalty", "Practical mastery"],
        "growth": "Expressing what they feel, not only what they do.",
        "partner_types": ["ESFP", "ESTP"],
        "partner_reason": "The ESFP brings warmth and spontaneity that draws the ISTJ into the present. The ESTP energises their structured world.",
        "ideal_traits": ["Dependable and consistent", "Direct, no drama", "Practical and capable", "Shares values"],
        "ink_color": "#6B3A7A"
    },
    "ISFJ": {
        "name": "The Defender", "group": "SJ",
        "tagline": "Devoted, nurturing, quietly extraordinary.",
        "desc": "ISFJs notice what others miss, remember what others forget, and give more than they take. Their care is immense and often invisible. They are more powerful than they appear.",
        "strengths": ["Exceptional attentiveness", "Deep loyalty", "Practical nurturing", "Quiet perseverance"],
        "growth": "Asking for what they need without waiting to be noticed.",
        "partner_types": ["ESFP", "ESTP"],
        "partner_reason": "The ESFP's liveliness lifts the ISFJ's natural tendency to put others first. The ESTP's directness creates exciting balance.",
        "ideal_traits": ["Expressive and appreciative", "Active and decisive", "Reciprocates care", "Values home and loyalty"],
        "ink_color": "#6B3A7A"
    },
    "ESTJ": {
        "name": "The Executive", "group": "SJ",
        "tagline": "Organised, direct, fiercely dependable.",
        "desc": "ESTJs believe in order, honesty, and doing things right. They take responsibility seriously and will carry a team on their back when required. Their bluntness is respect, not unkindness.",
        "strengths": ["Decisive organisation", "Strong moral code", "Reliable leadership", "Clear communication"],
        "growth": "Allowing room for emotion alongside their clarity.",
        "partner_types": ["ISFP", "ISTP"],
        "partner_reason": "The ISFP's warmth and artistry softens the ESTJ's edges. The ISTP brings quiet competence they deeply respect.",
        "ideal_traits": ["Capable and self-assured", "Honest and direct", "Appreciates structure", "Has their own ambitions"],
        "ink_color": "#6B3A7A"
    },
    "ESFJ": {
        "name": "The Consul", "group": "SJ",
        "tagline": "Warm, connected, the social glue.",
        "desc": "ESFJs make people feel seen, included, and celebrated. Their warmth is not performance — it is genuine. Tireless in their care, they are fiercely protective of those they love.",
        "strengths": ["Natural social warmth", "Practical care", "Community building", "Loyalty"],
        "growth": "Caring for themselves with the same ferocity they care for others.",
        "partner_types": ["ISFP", "ISTP"],
        "partner_reason": "The ISFP's sensitivity resonates with the ESFJ's nurturing warmth. The ISTP's quiet competence provides the grounded balance they need.",
        "ideal_traits": ["Appreciates acts of service", "Loyal and dependable", "Expressive and affectionate", "Socially present"],
        "ink_color": "#6B3A7A"
    },
    "ISTP": {
        "name": "The Virtuoso", "group": "SP",
        "tagline": "Masterful, cool, hands-on problem-solver.",
        "desc": "ISTPs move through the world with quiet, assured competence. They understand how things work — machines, systems, people — through direct observation. Their independence is self-sufficiency, not aloofness.",
        "strengths": ["Practical mastery", "Crisis composure", "Mechanical intelligence", "Adaptability"],
        "growth": "Letting people close enough to matter.",
        "partner_types": ["ESTJ", "ESFJ"],
        "partner_reason": "The ESTJ's clarity gives the ISTP external grounding. The ESFJ's warmth draws them gently into emotional territory they rarely visit alone.",
        "ideal_traits": ["Self-sufficient", "Doesn't over-emotionalise", "Adventurous and spontaneous", "Consistent loyalty"],
        "ink_color": "#8B4513"
    },
    "ISFP": {
        "name": "The Adventurer", "group": "SP",
        "tagline": "Artistic, gentle, deeply feeling.",
        "desc": "ISFPs experience the world through sensation and beauty. They live fully in the present and feel deeply — they just don't broadcast it. Their gentleness hides uncommon fierceness when their values are threatened.",
        "strengths": ["Aesthetic sensitivity", "Emotional depth", "Present-moment awareness", "Genuine warmth"],
        "growth": "Voicing their needs before they quietly disappear.",
        "partner_types": ["ESTJ", "ENFJ"],
        "partner_reason": "The ESTJ's decisive structure gives the ISFP security to fully be themselves. The ENFJ sees and celebrates their quiet gifts.",
        "ideal_traits": ["Appreciates beauty", "Patient and attentive", "Decisive when needed", "Expresses appreciation"],
        "ink_color": "#8B4513"
    },
    "ESTP": {
        "name": "The Entrepreneur", "group": "SP",
        "tagline": "Energetic, daring, magnetic in motion.",
        "desc": "ESTPs live at full speed — pragmatic, bold, electrifying in person. They read rooms instantly and act without hesitation. They are at their best in crisis and most alive when the stakes are high.",
        "strengths": ["Real-time intelligence", "Bold risk-taking", "Magnetic presence", "Practical negotiation"],
        "growth": "Staying when things get slow — love often lives there.",
        "partner_types": ["ISTJ", "ISFJ"],
        "partner_reason": "The ISTJ's loyalty provides the stable home base the ESTP secretly needs. The ISFJ's warmth creates a safe haven behind the bravado.",
        "ideal_traits": ["Adventurous", "Emotionally steady", "Appreciates boldness", "Grounded and loyal"],
        "ink_color": "#8B4513"
    },
    "ESFP": {
        "name": "The Entertainer", "group": "SP",
        "tagline": "Spontaneous, generous, irresistibly alive.",
        "desc": "ESFPs turn ordinary moments into celebrations. Warm, expressive, and impossible not to love. They live fully in the present, give generously, and make you feel that right now is exactly where you should be.",
        "strengths": ["Infectious warmth", "Spontaneous joy", "Emotional presence", "Natural performer"],
        "growth": "Building for the future while embracing the present.",
        "partner_types": ["ISTJ", "ISFJ"],
        "partner_reason": "The ISTJ's reliability creates the secure foundation the ESFP can dance from. The ISFJ's consistency makes the ESFP feel truly held.",
        "ideal_traits": ["Appreciates joy", "Grounded and dependable", "Emotionally available", "Loyal through change"],
        "ink_color": "#8B4513"
    }
}


# ── DISC PROFILES ──────────────────────────────────────────────────────

DISC_PROFILES = {
    "D": {
        "name": "Dominant", "label": "The Driver",
        "tagline": "Decisive. Bold. Results-first.",
        "desc": "D-styles are outcome-oriented powerhouses who move fast, decide faster, and don't ask permission. They communicate with blunt efficiency. Their directness is clarity, not aggression.",
        "strengths": ["Decisive under pressure", "Results-oriented", "Bold risk-taker", "Natural initiative"],
        "shadow": "Can trample feelings in pursuit of outcomes.",
        "partner_style": "S", "partner_name": "Steady (S-Style)",
        "partner_reason": "The S-style's patience, loyalty, and calm presence provides the emotional anchor the D-type rarely seeks but deeply needs.",
        "color": "#8B3A35"
    },
    "I": {
        "name": "Influential", "label": "The Inspirer",
        "tagline": "Warm. Expressive. Magnetically social.",
        "desc": "I-styles light up every room they enter. They build relationships effortlessly, communicate with infectious enthusiasm, and lead through inspiration rather than authority.",
        "strengths": ["Natural communicator", "Relationship builder", "Enthusiastic motivator", "Creative energy"],
        "shadow": "Can overpromise and underprioritise detail.",
        "partner_style": "C", "partner_name": "Conscientious (C-Style)",
        "partner_reason": "The C-style's depth, precision, and quiet reliability grounds the I-type's warmth, giving their enthusiasm real roots.",
        "color": "#8B6A1A"
    },
    "S": {
        "name": "Steady", "label": "The Supporter",
        "tagline": "Loyal. Patient. The one who always shows up.",
        "desc": "S-styles are the quiet foundation that everything else rests on. Consistent, deeply loyal, genuinely invested in the wellbeing of those around them. They don't make noise — they make things work.",
        "strengths": ["Exceptional loyalty", "Calm under pressure", "Active listening", "Reliable consistency"],
        "shadow": "Can avoid conflict until the cost is too high.",
        "partner_style": "D", "partner_name": "Dominant (D-Style)",
        "partner_reason": "The D-style's energy, direction, and decisiveness gives the S-type momentum and the sense of being truly protected.",
        "color": "#3A6B45"
    },
    "C": {
        "name": "Conscientious", "label": "The Analyser",
        "tagline": "Precise. Deep. Relentlessly thorough.",
        "desc": "C-styles are quiet experts who hold themselves to the highest standards. They think before speaking, research before deciding, and care deeply about accuracy. Their inner world is rich and complex.",
        "strengths": ["Analytical depth", "High standards", "Systematic thinking", "Thoughtful precision"],
        "shadow": "Can become paralysed by perfectionism.",
        "partner_style": "I", "partner_name": "Influential (I-Style)",
        "partner_reason": "The I-style's warmth, spontaneity, and social ease draws the C-type out of their head and into the warmth of the world.",
        "color": "#2C4A7C"
    }
}


# ── TEMPERAMENT PROFILES ───────────────────────────────────────────────

TEMPERAMENT_PROFILES = {
    "Choleric": {
        "symbol": "🜂",  "element": "Fire", "season": "Summer",
        "tagline": "Fire. Drive. Unapologetic ambition.",
        "desc": "Choleric types are natural leaders — forceful, decisive, and oriented entirely toward results. They carry burning urgency and lead from the front. Their passion is inspiring; their impatience is their tuition fee.",
        "strengths": ["Natural leadership", "Decisive momentum", "High drive", "Goal mastery"],
        "shadow": "Anger, impatience, and tendency to dominate.",
        "partner_temp": "Phlegmatic",
        "partner_reason": "The Phlegmatic's calm steadiness extinguishes the Choleric's fire without dousing their spark. Their loyalty runs deeper than the Choleric initially expects.",
        "color": "#8B3A35"
    },
    "Sanguine": {
        "symbol": "🜁", "element": "Air", "season": "Spring",
        "tagline": "Air. Warmth. Joy as a way of being.",
        "desc": "Sanguine types are the light in the room — warm, expressive, and irresistibly alive. They live in the present, love freely, and make ordinary moments feel like celebrations. Their joy is not shallow; it is their deepest truth.",
        "strengths": ["Infectious enthusiasm", "Natural warmth", "Social ease", "Present-moment joy"],
        "shadow": "Impulsivity, inconsistency, avoiding hard emotions.",
        "partner_temp": "Melancholic",
        "partner_reason": "The Melancholic's depth and thoughtfulness grounds the Sanguine's lightness into something meaningful. They offer the quiet depth that gives Sanguine roots.",
        "color": "#8B6A1A"
    },
    "Phlegmatic": {
        "symbol": "🜄", "element": "Water", "season": "Autumn",
        "tagline": "Water. Peace. The strength of still things.",
        "desc": "Phlegmatic types are the quiet power of the temperaments — steady, patient, deeply loyal. They do not seek the spotlight but are the person everyone turns to when the storm arrives. Their peace is not passivity — it is mastery.",
        "strengths": ["Unshakeable calm", "Deep loyalty", "Diplomatic ease", "Consistent reliability"],
        "shadow": "Avoidance, inertia, and suppressed needs.",
        "partner_temp": "Choleric",
        "partner_reason": "The Choleric's direction and decisiveness gives the Phlegmatic momentum and purpose. Fire and water, together, move mountains.",
        "color": "#2C5A7A"
    },
    "Melancholic": {
        "symbol": "🜃", "element": "Earth", "season": "Winter",
        "tagline": "Earth. Depth. The pursuit of perfection.",
        "desc": "Melancholic types carry the richest inner world of any temperament. Analytical, idealistic, and deeply feeling, they hold themselves and the world to standards most cannot see. Their sensitivity is their greatest gift.",
        "strengths": ["Profound analytical depth", "Idealistic integrity", "Emotional attunement", "Perfectionist quality"],
        "shadow": "Over-analysis, melancholy, and harsh self-criticism.",
        "partner_temp": "Sanguine",
        "partner_reason": "The Sanguine's warmth and spontaneity lifts the Melancholic out of their depths and into the world. Their joy is the antidote to Melancholic rumination.",
        "color": "#4A3A6B"
    }
}


# ── COLOR THERAPY DATA ─────────────────────────────────────────────────
# Added feature: each colour carries psychological meaning.
# Users can explore why their mood palette contains those particular shades.

COLOR_MEANINGS = {
    "warm": {
        "title": "Warm Spectrum",
        "meaning": "Reds, oranges, and golds stimulate the nervous system, encourage action, and awaken appetite for life. They speak of fire, vitality, and the courage to be seen.",
        "good_for": "Low energy, creative blocks, social withdrawal",
        "avoid_if": "Already anxious or overstimulated"
    },
    "cool": {
        "title": "Cool Spectrum",
        "meaning": "Blues and teals slow the breath, lower the heart rate, and invite reflection. They carry the quality of deep water — clarity beneath the surface.",
        "good_for": "Stress, overactivity, racing thoughts",
        "avoid_if": "Feeling already cold, distant, or depressed"
    },
    "green": {
        "title": "Earth Greens",
        "meaning": "Greens are the great balancers — the colour of nature in equilibrium. They restore after overstimulation and ground during anxiety.",
        "good_for": "Recovery, balance-seeking, renewal",
        "avoid_if": "Feeling stuck in routine or stagnant"
    },
    "violet": {
        "title": "Violet & Purple",
        "meaning": "Violets and purples have historically been associated with introspection, spiritual depth, and the liminal space between ordinary reality and something more.",
        "good_for": "Meditation, inner work, creative ideation",
        "avoid_if": "Feeling already detached from reality"
    },
    "neutral": {
        "title": "Earth Neutrals",
        "meaning": "Browns, stones, and slate tones are the colours of the ground beneath your feet. They ask nothing of you. They simply hold you.",
        "good_for": "Overwhelm, grief, exhaustion",
        "avoid_if": "Wanting creative stimulation or joy"
    }
}


# ══════════════════════════════════════════════════════════════════════
# SECTION 2: CALCULATION FUNCTIONS
# ══════════════════════════════════════════════════════════════════════
#
# Functions in Python are reusable blocks of code you "define" once
# and "call" (use) many times.
# Syntax:  def function_name(parameters):
#              # code that does something
#              return result


def calculate_wellness_score(data):
    """
    Calculate a wellness score from 0 to 100.

    Parameters:
        data (dict): A dictionary of 7 slider values sent from the browser.
                     Example: {"sleep": 7.5, "stress": 3.0, ...}

    Returns:
        float: A score between 0.0 and 100.0

    HOW IT WORKS:
    Each of the 7 factors gets a "weight" — how much it contributes to
    the total score. The weights all add up to 1.0 (100%).
    We multiply each factor's value (out of 10) by its weight and
    accumulate the result.

    Stress is special: it's "inverted" because high stress = bad wellness.
    So a stress of 8 becomes (10 - 8) = 2 — a low contribution.
    """

    # A dictionary mapping each input key to its weight in the final score.
    # Notice they sum to 1.0 (0.25 + 0.20 + 0.18 + 0.15 + 0.10 + 0.07 + 0.05)
    weights = {
        "sleep":     0.25,   # Sleep is the #1 predictor of wellness
        "stress":    0.20,   # Stress is weighted high — and inverted
        "energy":    0.18,   # How much fuel you're running on
        "mood":      0.15,   # Your felt emotional state
        "activity":  0.10,   # Physical movement supports everything
        "social":    0.07,   # Connection matters more than we admit
        "hydration": 0.05,   # Small but real
    }

    score = 0.0  # Start at zero; we'll add to this as we loop

    # Loop through every key-value pair in our weights dictionary.
    # "for key, weight in weights.items()" unpacks each pair:
    #   key    → e.g. "sleep"
    #   weight → e.g. 0.25
    for key, weight in weights.items():

        # Get the value the user sent. If a key is missing, default to 5.
        # float() converts the value to a decimal number (e.g. "7" → 7.0)
        value = float(data.get(key, 5))

        # Invert stress: high stress should lower the score, not raise it
        if key == "stress":
            value = 10 - value

        # Add this factor's contribution to the running total.
        # (value / 10) converts 0–10 range → 0.0–1.0 fraction
        # × weight × 100 gives us a contribution out of 100
        score += (value / 10.0) * weight * 100

    # BONUS: If most values are high (≥7), add a small bonus.
    # This rewards consistency — being good at several things matters.
    high_value_count = 0
    for key, weight in weights.items():
        v = float(data.get(key, 5))
        if key == "stress":
            v = 10 - v
        if v >= 7:
            high_value_count += 1

    # The bonus scales from 0 to 5 extra points based on how many
    # values were "high". If all 7 are high → 5 bonus points.
    bonus = (high_value_count / len(weights)) * 5

    # min() ensures we never go above 100 even with the bonus.
    # round() rounds to 1 decimal place for display.
    return round(min(score + bonus, 100), 1)


def get_mood_state(score):
    """
    Match a wellness score to the correct mood state.

    Parameters:
        score (float): A wellness score from 0 to 100.

    Returns:
        tuple: (mood_name: str, mood_data: dict)
               e.g. ("Serene", { ...all the data for Serene... })

    HOW IT WORKS:
    We loop through every mood in MOOD_STATES and check if the score
    falls within that mood's range (lo to hi). The first match wins.
    """

    for mood_name, mood_data in MOOD_STATES.items():
        lo, hi = mood_data["range"]   # Unpack the (min, max) tuple
        if lo <= score <= hi:         # Is our score within this range?
            return mood_name, mood_data

    # Fallback: if nothing matched (shouldn't happen), return Balanced
    return "Balanced", MOOD_STATES["Balanced"]


def calculate_moon_phase():
    """
    Calculate the current moon phase based on today's date.

    Returns:
        dict: Phase name, emoji, illumination %, and description.

    HOW IT WORKS:
    The lunar cycle is ~29.53 days long. We calculate how many days
    have passed since a known New Moon date (Jan 6, 2000), then divide
    by the cycle length to find where we are in the cycle (0.0 → 1.0).
    That fraction maps to one of 8 named phases.

    This is an approximation — precise moon phase requires astronomical
    calculations accounting for Earth's elliptical orbit, but this is
    accurate to within ±1 day for everyday purposes.
    """

    # A known New Moon reference date (verified historical date)
    known_new_moon = date(2000, 1, 6)

    # Today's date
    today = date.today()

    # Calculate number of days since our reference new moon
    # .days extracts the integer number of days from a timedelta object
    days_since = (today - known_new_moon).days

    # The average length of a lunar cycle in days
    lunar_cycle = 29.53058867

    # Where are we in the current cycle? (0.0 = new moon, 1.0 = next new moon)
    # % is the "modulo" operator: gives the remainder after division.
    # e.g. 35 % 29.53 ≈ 5.47 — we're 5.47 days into the current cycle.
    position = (days_since % lunar_cycle) / lunar_cycle

    # Map the 0.0–1.0 position to one of 8 named phases.
    # We divide the cycle into 8 equal segments (each = 0.125 = 1/8).
    if position < 0.0625:
        phase, emoji, illumination = "New Moon", "🌑", 0
    elif position < 0.1875:
        phase, emoji, illumination = "Waxing Crescent", "🌒", 25
    elif position < 0.3125:
        phase, emoji, illumination = "First Quarter", "🌓", 50
    elif position < 0.4375:
        phase, emoji, illumination = "Waxing Gibbous", "🌔", 75
    elif position < 0.5625:
        phase, emoji, illumination = "Full Moon", "🌕", 100
    elif position < 0.6875:
        phase, emoji, illumination = "Waning Gibbous", "🌖", 75
    elif position < 0.8125:
        phase, emoji, illumination = "Last Quarter", "🌗", 50
    else:
        phase, emoji, illumination = "Waning Crescent", "🌘", 25

    # Moon phase descriptions for wellness context
    descriptions = {
        "New Moon": "A time of new beginnings. Plant intentions, not expectations.",
        "Waxing Crescent": "Energy slowly builds. Take small, deliberate steps forward.",
        "First Quarter": "Push through resistance. What began is now asking for effort.",
        "Waxing Gibbous": "Refine and adjust. The fullness is almost here.",
        "Full Moon": "Peak illumination. Emotions run high — honour them all.",
        "Waning Gibbous": "Share what you have learned. Gratitude is the work now.",
        "Last Quarter": "Release what is not serving you. Let things fall away cleanly.",
        "Waning Crescent": "Rest and surrender. The cycle is completing."
    }

    return {
        "phase": phase,
        "emoji": emoji,
        "illumination": illumination,
        "description": descriptions[phase],
        "position_pct": round(position * 100, 1)
    }


def determine_personality(scores):
    """
    Determine the user's MBTI type, DISC style, and Temperament from quiz scores.

    Parameters:
        scores (dict): Raw accumulated scores from all 20 questions.
                       Keys include: E, I_mbti, N, S_mbti, T, F, J, P,
                                     Di, Ii, Si, Ci, Cho, San, Phl, Mel

    Returns:
        dict: Complete personality results for all three systems.

    HOW IT WORKS:
    Each quiz question secretly adds points to relevant trait dimensions.
    At the end, we compare opposing dimensions:
      - MBTI: E vs I, N vs S, T vs F, J vs P (higher score wins each pair)
      - DISC: highest of D, I, S, C
      - Temperament: highest of Choleric, Sanguine, Phlegmatic, Melancholic
    """

    # ── DETERMINE MBTI ─────────────────────────────────────────────
    # For each opposing pair, whichever has the higher score wins.

    e_score = scores.get("E", 0)
    i_score = scores.get("I_mbti", 0)
    n_score = scores.get("N", 0)
    s_score = scores.get("S_mbti", 0)
    t_score = scores.get("T", 0)
    f_score = scores.get("F", 0)
    j_score = scores.get("J", 0)
    p_score = scores.get("P", 0)

    # String concatenation builds the 4-letter type code
    mbti_type = ""
    mbti_type += "E" if e_score >= i_score else "I"
    mbti_type += "N" if n_score >= s_score else "S"
    mbti_type += "T" if t_score >= f_score else "F"
    mbti_type += "J" if j_score >= p_score else "J"

    # ── DETERMINE DISC ─────────────────────────────────────────────
    disc_scores = {
        "D": scores.get("Di", 0),
        "I": scores.get("Ii", 0),
        "S": scores.get("Si", 0),
        "C": scores.get("Ci", 0)
    }
    # max() with key= finds the key with the highest value
    disc_type = max(disc_scores, key=disc_scores.get)

    # ── DETERMINE TEMPERAMENT ──────────────────────────────────────
    temp_scores = {
        "Choleric":   scores.get("Cho", 0),
        "Sanguine":   scores.get("San", 0),
        "Phlegmatic": scores.get("Phl", 0),
        "Melancholic": scores.get("Mel", 0)
    }
    temp_type = max(temp_scores, key=temp_scores.get)

    # ── FETCH PROFILES ─────────────────────────────────────────────
    # .get() safely retrieves from dict; falls back to INFP if unknown
    mbti_profile = MBTI_PROFILES.get(mbti_type, MBTI_PROFILES["INFP"])
    disc_profile  = DISC_PROFILES[disc_type]
    temp_profile  = TEMPERAMENT_PROFILES[temp_type]

    # ── BUILD PARTNER SYNTHESIS ────────────────────────────────────
    synthesis = build_partner_synthesis(mbti_type, disc_type, temp_type,
                                        mbti_profile, disc_profile, temp_profile)

    # ── RETURN COMPLETE RESULTS ────────────────────────────────────
    return {
        "mbti": {
            **mbti_profile,           # ** "unpacks" the dictionary (spreads all keys)
            "type": mbti_type,
        },
        "disc": {
            **disc_profile,
            "style": disc_type,
        },
        "temperament": {
            **temp_profile,
            "type": temp_type,
        },
        "synthesis": synthesis,
        "raw_scores": {
            "mbti": {
                "E": e_score, "I": i_score,
                "N": n_score, "S": s_score,
                "T": t_score, "F": f_score,
                "J": j_score, "P": p_score
            },
            "disc": disc_scores,
            "temp": temp_scores
        }
    }


def build_partner_synthesis(mbti, disc, temp, mp, dp, tp):
    """
    Build a synthesised ideal partner profile combining all three systems.

    Parameters:
        mbti, disc, temp  → the type codes (e.g. "INFJ", "S", "Phlegmatic")
        mp, dp, tp        → the full profile dictionaries for each

    Returns:
        dict: A synthesised partner description.
    """

    # Love language tendencies mapped to MBTI type
    love_languages = {
        "INTJ": "quality time and deep, unhurried conversation",
        "INTP": "intellectual exploration and honest, precise words",
        "ENTJ": "acts of purposeful action and focused presence",
        "ENTP": "playful debate and intellectual respect",
        "INFJ": "being truly known — beneath the surface",
        "INFP": "emotional honesty and space for creative expression",
        "ENFJ": "words of affirmation and reciprocal care",
        "ENFP": "spontaneous adventure and emotional depth",
        "ISTJ": "acts of service and loyal, consistent presence",
        "ISFJ": "attentiveness and quiet, steady devotion",
        "ESTJ": "direct appreciation and shared acts of service",
        "ESFJ": "quality time and verbal affirmation",
        "ISTP": "shared experience and respectful space",
        "ISFP": "beauty, presence, and aesthetic experience together",
        "ESTP": "shared thrills and bold aliveness",
        "ESFP": "physical warmth and joyful shared experience"
    }

    # Relationship style from DISC
    rel_styles = {
        "D": "direct and action-oriented",
        "I": "warm, expressive, and socially alive",
        "S": "steady, loyal, and quietly devoted",
        "C": "thoughtful, precise, and deeply intentional"
    }

    return {
        "headline": f"{mp['name']} × {dp['label']} × {tp['element']} Soul",
        "love_language": love_languages.get(mbti, "authentic presence"),
        "relationship_style": rel_styles.get(disc, "thoughtfully"),
        "intro": (
            f"Across all three lenses, your ideal partner is someone who can meet the full "
            f"complexity of who you are. As a {mbti} with a {disc}-style presence and a "
            f"{temp} temperament, you bring depth, intensity, and a particular way of moving "
            f"through the world that not everyone can hold — but the right person will."
        ),
        "partner_desc": (
            f"They should be {mp['ideal_traits'][0].lower()}, {mp['ideal_traits'][1].lower()}, "
            f"and carry the {dp['partner_name'].split('(')[0].strip()} energy — "
            f"{dp['partner_reason'].split('.')[0].lower()}. "
            f"Temperamentally, a {tp['partner_temp']} counterpart offers the natural balance "
            f"your {temp.lower()} nature quietly needs: {tp['partner_reason'].split('.')[0].lower()}."
        ),
        "red_flags": [
            "Someone who cannot match your emotional depth or intellectual pace",
            "People-pleasers who have no clear identity of their own",
            "Emotional unavailability masquerading as strength or independence",
            "Those who mistake the complexity of your needs for neediness"
        ]
    }


# ══════════════════════════════════════════════════════════════════════
# SECTION 3: ROUTES
# ══════════════════════════════════════════════════════════════════════
#
# A "route" in Flask is a URL path that triggers a specific function.
# @app.route("/path") is a "decorator" — it tells Flask:
# "When someone visits /path, run the function below."
#
# HTTP Methods:
#   GET  → The browser is asking for a page to display (like visiting a URL)
#   POST → The browser is sending data to be processed (like submitting a form)


@app.route("/")
def index():
    """
    Serve the main HTML page.
    Called when a user visits http://127.0.0.1:5000/

    render_template("index.html") finds the file in the /templates folder
    and sends it to the browser as a complete HTML page.
    """
    # Get moon data to pass to the template on initial load
    moon = calculate_moon_phase()
    return render_template("index.html", moon=moon)


@app.route("/wellness", methods=["POST"])
def wellness_route():
    """
    Receive wellness slider data from the browser, calculate results,
    and return JSON.

    The browser sends: { "sleep": 7.5, "stress": 3, ... }
    We return:         { "score": 74.2, "mood": "Serene", "palette": [...], ... }
    """

    # request.json reads the JSON body the browser sent us
    data = request.json

    # Run our calculation functions
    score = calculate_wellness_score(data)
    mood_name, mood = get_mood_state(score)

    # ── SESSION HISTORY ─────────────────────────────────────────────
    # session acts like a small dictionary that persists across requests
    # for this specific user (stored in an encrypted cookie).

    if "history" not in session:
        session["history"] = []    # Initialise if this is first visit

    # Create a record of this check-in
    entry = {
        "id":    str(uuid.uuid4())[:6],           # Short unique ID
        "ts":    datetime.now().strftime("%b %d, %H:%M"),  # e.g. "Apr 08, 14:23"
        "score": score,
        "mood":  mood_name,
        "symbol": mood["symbol"],
        "ink":   mood["ink"]
    }

    # Prepend the new entry and keep only the last 7
    # [entry] creates a list with one item; + session["history"] joins them
    session["history"] = ([entry] + session["history"])[:7]
    session.modified = True    # Tell Flask the session data has changed

    # ── BUILD AND RETURN RESPONSE ───────────────────────────────────
    return jsonify({
        "score":      score,
        "mood":       mood_name,
        "symbol":     mood["symbol"],
        "palette":    mood["palette"],
        "ink":        mood["ink"],
        "desc":       mood["desc"],
        "tip":        mood["tip"],
        "affirmation": mood["affirmation"],
        "activity":   mood["activity"],
        "color_therapy": mood["color_therapy"],
        "element":    mood["element"],
        "breath":     mood["breath"],
        "history":    session["history"],
        "breakdown": {
            "Sleep Quality":    float(data.get("sleep", 5)),
            "Low Stress":       round(10 - float(data.get("stress", 5)), 1),
            "Energy Level":     float(data.get("energy", 5)),
            "Inner Mood":       float(data.get("mood", 5)),
            "Physical Activity": float(data.get("activity", 5)),
            "Social Connection": float(data.get("social", 5)),
            "Hydration":        float(data.get("hydration", 5))
        }
    })


@app.route("/personality", methods=["POST"])
def personality_route():
    """
    Receive accumulated quiz scores, determine personality types,
    and return JSON.
    """
    scores = request.json
    result = determine_personality(scores)
    session["personality"] = result
    session.modified = True
    return jsonify(result)


@app.route("/moon", methods=["GET"])
def moon_route():
    """
    Return the current moon phase data.
    The browser can call this independently to display the moon.
    """
    return jsonify(calculate_moon_phase())


@app.route("/gratitude", methods=["POST"])
def gratitude_route():
    """
    NEW FEATURE: Save a gratitude journal entry.

    The browser sends: { "entries": ["entry1", "entry2", "entry3"] }
    We store them in the session and return them with the timestamp.
    """
    data = request.json
    entries = data.get("entries", [])

    # Filter out empty strings with list comprehension:
    # [x for x in list if condition] creates a new filtered list
    entries = [e.strip() for e in entries if e.strip()]

    if not entries:
        # Return a 400 Bad Request if nothing was submitted
        return jsonify({"error": "No entries provided"}), 400

    if "journal" not in session:
        session["journal"] = []

    record = {
        "date": datetime.now().strftime("%A, %B %d"),    # e.g. "Tuesday, April 08"
        "time": datetime.now().strftime("%I:%M %p"),     # e.g. "02:23 PM"
        "entries": entries
    }

    session["journal"] = ([record] + session["journal"])[:10]  # Keep last 10
    session.modified = True

    return jsonify({
        "saved": True,
        "record": record,
        "total_entries": len(session["journal"])
    })


@app.route("/journal", methods=["GET"])
def journal_route():
    """
    Return all saved gratitude journal entries for this session.
    """
    return jsonify(session.get("journal", []))


# ══════════════════════════════════════════════════════════════════════
# SECTION 4: ENTRY POINT
# ══════════════════════════════════════════════════════════════════════
#
# Python files can be run directly OR imported by other files.
# "if __name__ == '__main__'" means: "only run this block if this file
# was run directly (not imported)."
# This is the standard Python pattern for runnable scripts.

""" if __name__ == "__main__":
    # debug=True → Flask shows detailed error pages and reloads automatically
    #              when you save changes. NEVER use debug=True in production.
    # port=5000   → The URL will be http://127.0.0.1:5000
    app.run(debug=True, port=5000) """
if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))