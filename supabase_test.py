from collections import defaultdict
from fastapi import HTTPException
from dotenv import load_dotenv
import os
from supabase import create_client, Client

# Load environment variables
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

# Connect to Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

# Example question map (expand with all questions/answers)
question_map = {
    "Q1": {
        "A": [("Trailblazer Entrepreneur", 2), ("Creative Maverick", 2)],
        "B": [("Grounded Architect", 2), ("Strategic Techie", 2)],
        "C": [("Visionary Coach", 2), ("Athletic Visionary", 1)],
        "D": [("Healing Alchemist", 2), ("Empathetic Architect", 1)]
    },
    "Q2": {
        "A": [("Grounded Architect", 2), ("Strategic Techie", 1)],
        "B": [("Trailblazer Entrepreneur", 2), ("Athletic Visionary", 1)],
        "C": [("Creative Maverick", 2), ("Healing Alchemist", 1)],
        "D": [("Visionary Coach", 2), ("Empathetic Architect", 1)]
    },
    "Q3": {
        "A": [("Trailblazer Entrepreneur", 2), ("Athletic Visionary", 2)],
        "B": [("Grounded Architect", 2), ("Strategic Techie", 1)],
        "C": [("Creative Maverick", 2), ("Visionary Coach", 1)],
        "D": [("Healing Alchemist", 2), ("Empathetic Architect", 1)]
    },
    "Q4": {
        "A": [("Trailblazer Entrepreneur", 2), ("Athletic Visionary", 1)],
        "B": [("Grounded Architect", 2), ("Strategic Techie", 1)],
        "C": [("Visionary Coach", 2), ("Creative Maverick", 1)],
        "D": [("Healing Alchemist", 2), ("Empathetic Architect", 2)]
    },
    "Q5": {
        "A": [("Trailblazer Entrepreneur", 2), ("Creative Maverick", 1)],
        "B": [("Grounded Architect", 2), ("Strategic Techie", 2)],
        "C": [("Visionary Coach", 2), ("Athletic Visionary", 1)],
        "D": [("Healing Alchemist", 2), ("Empathetic Architect", 2)]
    },
    "Q6": {
        "A": [("Trailblazer Entrepreneur", 2), ("Strategic Techie", 1)],
        "B": [("Grounded Architect", 2), ("Empathetic Architect", 1)],
        "C": [("Visionary Coach", 2), ("Creative Maverick", 1)],
        "D": [("Healing Alchemist", 2), ("Empathetic Architect", 2)]
    },
    "Q7": {
        "A": [("Trailblazer Entrepreneur", 2), ("Creative Maverick", 1)],
        "B": [("Grounded Architect", 2), ("Strategic Techie", 1)],
        "C": [("Creative Maverick", 2), ("Visionary Coach", 1)],
        "D": [("Healing Alchemist", 2), ("Empathetic Architect", 1)]
    },
    "Q8": {
        "A": [("Trailblazer Entrepreneur", 2), ("Athletic Visionary", 1)],
        "B": [("Grounded Architect", 2), ("Strategic Techie", 2)],
        "C": [("Visionary Coach", 2), ("Creative Maverick", 1)],
        "D": [("Healing Alchemist", 2), ("Empathetic Architect", 2)]
    },
    "Q9": {
        "A": [("Trailblazer Entrepreneur", 2), ("Creative Maverick", 1)],
        "B": [("Grounded Architect", 2), ("Strategic Techie", 1)],
        "C": [("Visionary Coach", 2), ("Athletic Visionary", 1)],
        "D": [("Healing Alchemist", 2), ("Empathetic Architect", 2)]
    },
    "Q10": {
        "A": [("Trailblazer Entrepreneur", 2), ("Creative Maverick", 1)],
        "B": [("Grounded Architect", 2), ("Strategic Techie", 2)],
        "C": [("Visionary Coach", 2), ("Athletic Visionary", 1)],
        "D": [("Healing Alchemist", 2), ("Empathetic Architect", 2)]
    },
    "Q11": {
        "A": [("Trailblazer Entrepreneur", 2), ("Creative Maverick", 1)],
        "B": [("Grounded Architect", 2), ("Strategic Techie", 1)],
        "C": [("Visionary Coach", 2), ("Athletic Visionary", 1)],
        "D": [("Healing Alchemist", 2), ("Empathetic Architect", 2)]
    },
    "Q12": {
        "A": [("Trailblazer Entrepreneur", 2), ("Athletic Visionary", 1)],
        "B": [("Grounded Architect", 2), ("Strategic Techie", 2)],
        "C": [("Visionary Coach", 2), ("Creative Maverick", 1)],
        "D": [("Healing Alchemist", 2), ("Empathetic Architect", 1)]
    },
    "Q13": {
        "A": [("Trailblazer Entrepreneur", 2), ("Athletic Visionary", 2)],
        "B": [("Grounded Architect", 2), ("Strategic Techie", 1)],
        "C": [("Visionary Coach", 2), ("Creative Maverick", 1)],
        "D": [("Healing Alchemist", 2), ("Empathetic Architect", 2)]
    },
    "Q14": {
        "A": [("Trailblazer Entrepreneur", 2), ("Creative Maverick", 1)],
        "B": [("Grounded Architect", 2), ("Strategic Techie", 2)],
        "C": [("Visionary Coach", 2), ("Athletic Visionary", 1)],
        "D": [("Healing Alchemist", 2), ("Empathetic Architect", 2)]
    },
    "Q15": {
        "A": [("Trailblazer Entrepreneur", 2), ("Strategic Techie", 1)],
        "B": [("Grounded Architect", 2), ("Empathetic Architect", 1)],
        "C": [("Creative Maverick", 2), ("Visionary Coach", 1)],
        "D": [("Healing Alchemist", 2), ("Empathetic Architect", 2)]
    },
    # Add more questions here...
}


def calculate_archetypes(answers: dict):
    if not answers:
        raise HTTPException(status_code=400, detail="No answers provided.")

    scores = defaultdict(int)
    for q_num, selected in answers.items():
        if q_num in question_map and selected in question_map[q_num]:
            for archetype, points in question_map[q_num][selected]:
                scores[archetype] += points

    if not scores:
        raise HTTPException(status_code=400, detail="No valid answers matched the question map.")

    sorted_archetypes = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    primary_score = sorted_archetypes[0][1]

    result = {
        "Primary": [],
        "Secondary": [],
        "Wildcard": []
    }

    for name, score in sorted_archetypes:
        if score == primary_score:
            result["Primary"].append(name)
        elif score >= 0.8 * primary_score:
            result["Secondary"].append(name)
        elif score >= 0.65 * primary_score:
            result["Wildcard"].append(name)

    # Save results to Supabase
    try:
        supabase.table("quiz_results").insert({
            "user_id": "test-user_2",
            "answers": answers,
            "archetypes": result  # Store full object in 'archetypes' column
        }).execute()
    except Exception as e:
        print("❌ Error saving to Supabase:", e)

    return {"archetypes": result}


def fetch_quiz_results(limit=5):
    """Fetch the most recent quiz results from Supabase"""
    try:
        response = supabase.table("quiz_results").select("*").order("created_at", desc=True).limit(limit).execute()
        return response.data
    except Exception as e:
        print("❌ Error fetching from Supabase:", e)
        return []


# ✅ Test section for terminal usage
if __name__ == "__main__":
    # Sample answers for test
    sample_answers = {
        "Q1": "A",
        "Q2": "C",
        "Q3": "D",
        "Q4": "B",
        "Q5": "B",
        "Q6": "C",
        "Q7": "D",
        "Q8": "A",
        "Q9": "A",
        "Q10": "D",
        "Q11": "C",
        "Q12": "C",
        "Q13": "A",
        "Q14": "B",
        "Q15": "C"

    }

    print("🧠 Calculating archetypes and saving to Supabase...\n")
    result = calculate_archetypes(sample_answers)
    print("✅ Archetype Calculation Result:")
    print(result)

    print("\n📦 Fetching saved results from Supabase...")
    saved = fetch_quiz_results()
    for idx, entry in enumerate(saved, 1):
        print(f"\n🔹 Entry #{idx}")
        print(f"📝 Answers     : {entry.get('answers')}")
        archetypes = entry.get('archetypes', {})
        print(f"🌟 Primary     : {archetypes.get('Primary')}")
        print(f"🧩 Secondary   : {archetypes.get('Secondary')}")
        print(f"🎯 Wildcard    : {archetypes.get('Wildcard')}")
        print(f"⏰ Created At  : {entry.get('created_at')}")
