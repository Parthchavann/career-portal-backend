from supabase import create_client
from dotenv import load_dotenv
import os
from collections import defaultdict
from fastapi import HTTPException
from datetime import datetime
import uuid
import json


# Load environment
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


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
    "Q16": {
        "A": [("Trailblazer Entrepreneur", 2), ("Athletic Visionary", 1)],
        "B": [("Grounded Architect", 2), ("Strategic Techie", 2)],
        "C": [("Visionary Coach", 2), ("Creative Maverick", 1)],
        "D": [("Healing Alchemist", 2), ("Empathetic Architect", 2)]
    },
    "Q17": {
        "A": [("Trailblazer Entrepreneur", 2), ("Creative Maverick", 1)],
        "B": [("Grounded Architect", 2), ("Strategic Techie", 2)],
        "C": [("Visionary Coach", 2), ("Athletic Visionary", 1)],
        "D": [("Healing Alchemist", 2), ("Empathetic Architect", 2)]
    },
    "Q18": {
        "A": [("Trailblazer Entrepreneur", 2), ("Strategic Techie", 1)],
        "B": [("Grounded Architect", 2), ("Empathetic Architect", 1)],
        "C": [("Visionary Coach", 2), ("Creative Maverick", 1)],
        "D": [("Healing Alchemist", 2), ("Empathetic Architect", 2)]
    },
    "Q19": {
        "A": [("Trailblazer Entrepreneur", 2), ("Athletic Visionary", 1)],
        "B": [("Grounded Architect", 2), ("Strategic Techie", 2)],
        "C": [("Visionary Coach", 2), ("Creative Maverick", 1)],
        "D": [("Healing Alchemist", 2), ("Empathetic Architect", 2)]
    },
    "Q20": {
        "A": [("Trailblazer Entrepreneur", 2), ("Creative Maverick", 1)],
        "B": [("Grounded Architect", 2), ("Strategic Techie", 2)],
        "C": [("Visionary Coach", 2), ("Athletic Visionary", 1)],
        "D": [("Healing Alchemist", 2), ("Empathetic Architect", 2)]
    },
    "Q21": {
        "A": [("Trailblazer Entrepreneur", 2), ("Athletic Visionary", 1)],
        "B": [("Grounded Architect", 2), ("Strategic Techie", 2)],
        "C": [("Visionary Coach", 2), ("Healing Alchemist", 1)],
        "D": [("Empathetic Architect", 2), ("Healing Alchemist", 2)]
    },
    "Q22": {
        "A": [("Trailblazer Entrepreneur", 2), ("Creative Maverick", 1)],
        "B": [("Strategic Techie", 2), ("Grounded Architect", 1)],
        "C": [("Visionary Coach", 2), ("Athletic Visionary", 1)],
        "D": [("Healing Alchemist", 2), ("Empathetic Architect", 2)]
    },
    "Q23": {
        "A": [("Trailblazer Entrepreneur", 2), ("Athletic Visionary", 1)],
        "B": [("Grounded Architect", 2), ("Strategic Techie", 2)],
        "C": [("Visionary Coach", 2), ("Creative Maverick", 1)],
        "D": [("Healing Alchemist", 2), ("Empathetic Architect", 2)]
    },
    "Q24": {
        "A": [("Trailblazer Entrepreneur", 2), ("Creative Maverick", 1)],
        "B": [("Grounded Architect", 2), ("Strategic Techie", 2)],
        "C": [("Visionary Coach", 2), ("Athletic Visionary", 1)],
        "D": [("Healing Alchemist", 2), ("Empathetic Architect", 2)]
    },
    "Q25": {
        "A": [("Trailblazer Entrepreneur", 2), ("Strategic Techie", 1)],
        "B": [("Grounded Architect", 2), ("Empathetic Architect", 1)],
        "C": [("Visionary Coach", 2), ("Creative Maverick", 1)],
        "D": [("Healing Alchemist", 2), ("Empathetic Architect", 2)]
    },
    "Q26": {
        "A": [("Creative Maverick", 2), ("Trailblazer Entrepreneur", 1)],
        "B": [("Grounded Architect", 2), ("Strategic Techie", 2)],
        "C": [("Visionary Coach", 2), ("Athletic Visionary", 1)],
        "D": [("Healing Alchemist", 2), ("Empathetic Architect", 2)]
    },
    "Q27": {
        "A": [("Trailblazer Entrepreneur", 2), ("Creative Maverick", 1)],
        "B": [("Grounded Architect", 2), ("Strategic Techie", 2)],
        "C": [("Visionary Coach", 2), ("Athletic Visionary", 1)],
        "D": [("Healing Alchemist", 2), ("Empathetic Architect", 2)]
    },
    "Q28": {
        "A": [("Trailblazer Entrepreneur", 2), ("Athletic Visionary", 1)],
        "B": [("Grounded Architect", 2), ("Strategic Techie", 2)],
        "C": [("Visionary Coach", 2), ("Creative Maverick", 1)],
        "D": [("Healing Alchemist", 2), ("Empathetic Architect", 2)]
    },
    "Q29": {
        "A": [("Trailblazer Entrepreneur", 2), ("Athletic Visionary", 1)],
        "B": [("Grounded Architect", 2), ("Strategic Techie", 2)],
        "C": [("Visionary Coach", 2), ("Creative Maverick", 1)],
        "D": [("Healing Alchemist", 2), ("Empathetic Architect", 2)]
    },
    "Q30": {
        "A": [("Trailblazer Entrepreneur", 2), ("Athletic Visionary", 1)],
        "B": [("Grounded Architect", 2), ("Strategic Techie", 2)],
        "C": [("Visionary Coach", 2), ("Creative Maverick", 1)],
        "D": [("Healing Alchemist", 2), ("Empathetic Architect", 2)]
    },
    "Q31": {
        "A": [("Trailblazer Entrepreneur", 2), ("Athletic Visionary", 1)],
        "B": [("Strategic Techie", 2), ("Grounded Architect", 1)],
        "C": [("Visionary Coach", 2), ("Creative Maverick", 1)],
        "D": [("Healing Alchemist", 2), ("Empathetic Architect", 2)]
    },
    "Q32": {
        "A": [("Trailblazer Entrepreneur", 2), ("Athletic Visionary", 1)],
        "B": [("Grounded Architect", 2), ("Strategic Techie", 2)],
        "C": [("Visionary Coach", 2), ("Creative Maverick", 1)],
        "D": [("Healing Alchemist", 2), ("Empathetic Architect", 2)]
    },
    "Q33": {
        "A": [("Trailblazer Entrepreneur", 2), ("Athletic Visionary", 1)],
        "B": [("Grounded Architect", 2), ("Strategic Techie", 2)],
        "C": [("Visionary Coach", 2), ("Creative Maverick", 1)],
        "D": [("Healing Alchemist", 2), ("Empathetic Architect", 2)]
    },
    "Q34": {
        "A": [("Trailblazer Entrepreneur", 2), ("Athletic Visionary", 1)],
        "B": [("Strategic Techie", 2), ("Grounded Architect", 1)],
        "C": [("Visionary Coach", 2), ("Creative Maverick", 1)],
        "D": [("Healing Alchemist", 2), ("Empathetic Architect", 2)]
    },
    "Q35": {
        "A": [("Trailblazer Entrepreneur", 2), ("Visionary Coach", 1)],
        "B": [("Grounded Architect", 2), ("Strategic Techie", 2)],
        "C": [("Creative Maverick", 2), ("Visionary Coach", 2)],
        "D": [("Healing Alchemist", 2), ("Empathetic Architect", 2)]
    },
    "Q36": {
        "A": [("Trailblazer Entrepreneur", 2), ("Creative Maverick", 1)],
        "B": [("Grounded Architect", 2), ("Strategic Techie", 2)],
        "C": [("Visionary Coach", 2), ("Athletic Visionary", 1)],
        "D": [("Healing Alchemist", 2), ("Empathetic Architect", 2)]
    },
    "Q37": {
        "A": [("Trailblazer Entrepreneur", 2), ("Athletic Visionary", 1)],
        "B": [("Grounded Architect", 2), ("Strategic Techie", 2)],
        "C": [("Visionary Coach", 2), ("Creative Maverick", 1)],
        "D": [("Healing Alchemist", 2), ("Empathetic Architect", 2)]
    },
    "Q38": {
        "A": [("Trailblazer Entrepreneur", 2), ("Athletic Visionary", 1)],
        "B": [("Strategic Techie", 2), ("Grounded Architect", 1)],
        "C": [("Visionary Coach", 2), ("Creative Maverick", 1)],
        "D": [("Healing Alchemist", 2), ("Empathetic Architect", 2)]
    },
    "Q39": {
        "A": [("Trailblazer Entrepreneur", 2), ("Athletic Visionary", 1)],
        "B": [("Grounded Architect", 2), ("Strategic Techie", 2)],
        "C": [("Visionary Coach", 2), ("Empathetic Architect", 2)],
        "D": [("Healing Alchemist", 2), ("Empathetic Architect", 2)]
    },
    "Q40": {
        "A": [("Trailblazer Entrepreneur", 2), ("Athletic Visionary", 1)],
        "B": [("Grounded Architect", 2), ("Strategic Techie", 2)],
        "C": [("Visionary Coach", 2), ("Creative Maverick", 1)],
        "D": [("Healing Alchemist", 2), ("Empathetic Architect", 2)]
    },
    "Q41": {
        "A": [("Trailblazer Entrepreneur", 2), ("Athletic Visionary", 1)],
        "B": [("Grounded Architect", 2), ("Strategic Techie", 2)],
        "C": [("Visionary Coach", 2), ("Creative Maverick", 1)],
        "D": [("Healing Alchemist", 2), ("Empathetic Architect", 2)]
    },
    "Q42": {
        "A": [("Trailblazer Entrepreneur", 2), ("Athletic Visionary", 1)],
        "B": [("Strategic Techie", 2), ("Grounded Architect", 1)],
        "C": [("Visionary Coach", 2), ("Creative Maverick", 1)],
        "D": [("Healing Alchemist", 2), ("Empathetic Architect", 2)]
    },
    "Q43": {
        "A": [("Trailblazer Entrepreneur", 2), ("Athletic Visionary", 1)],
        "B": [("Grounded Architect", 2), ("Strategic Techie", 2)],
        "C": [("Visionary Coach", 2), ("Creative Maverick", 1)],
        "D": [("Healing Alchemist", 2), ("Empathetic Architect", 2)]
    },
    "Q44": {
        "A": [("Trailblazer Entrepreneur", 2), ("Creative Maverick", 1)],
        "B": [("Strategic Techie", 2), ("Grounded Architect", 2)],
        "C": [("Visionary Coach", 2), ("Athletic Visionary", 1)],
        "D": [("Healing Alchemist", 2), ("Empathetic Architect", 2)]
    },
    "Q45": {
        "A": [("Trailblazer Entrepreneur", 2), ("Visionary Coach", 1)],
        "B": [("Strategic Techie", 2), ("Grounded Architect", 2)],
        "C": [("Visionary Coach", 2), ("Creative Maverick", 1)],
        "D": [("Healing Alchemist", 2), ("Empathetic Architect", 2)]
    },
    "Q46": {
        "A": [("Trailblazer Entrepreneur", 2), ("Athletic Visionary", 1)],
        "B": [("Grounded Architect", 2), ("Strategic Techie", 2)],
        "C": [("Visionary Coach", 2), ("Creative Maverick", 1)],
        "D": [("Healing Alchemist", 2), ("Empathetic Architect", 2)]
    },
    "Q47": {
        "A": [("Trailblazer Entrepreneur", 2), ("Athletic Visionary", 1)],
        "B": [("Strategic Techie", 2), ("Grounded Architect", 2)],
        "C": [("Creative Maverick", 2), ("Visionary Coach", 1)],
        "D": [("Healing Alchemist", 2), ("Empathetic Architect", 2)]
    },
    "Q48": {
        "A": [("Trailblazer Entrepreneur", 2), ("Athletic Visionary", 1)],
        "B": [("Strategic Techie", 2), ("Grounded Architect", 2)],
        "C": [("Visionary Coach", 2), ("Creative Maverick", 1)],
        "D": [("Healing Alchemist", 2), ("Empathetic Architect", 2)]
    },
    "Q49": {
        "A": [("Trailblazer Entrepreneur", 2), ("Athletic Visionary", 1)],
        "B": [("Grounded Architect", 2), ("Strategic Techie", 2)],
        "C": [("Visionary Coach", 2), ("Creative Maverick", 2)],
        "D": [("Healing Alchemist", 2), ("Empathetic Architect", 2)]
    },
    "Q50": {
        "A": [("Trailblazer Entrepreneur", 2), ("Athletic Visionary", 1)],
        "B": [("Strategic Techie", 2), ("Grounded Architect", 2)],
        "C": [("Visionary Coach", 2), ("Creative Maverick", 1)],
        "D": [("Healing Alchemist", 2), ("Empathetic Architect", 2)]
    },
    "Q51": {
        "A": [("Trailblazer Entrepreneur", 2), ("Athletic Visionary", 1)],
        "B": [("Strategic Techie", 2), ("Grounded Architect", 2)],
        "C": [("Creative Maverick", 2), ("Visionary Coach", 2)],
        "D": [("Healing Alchemist", 2), ("Empathetic Architect", 2)]
    },
    "Q52": {
        "A": [("Trailblazer Entrepreneur", 2), ("Athletic Visionary", 1)],
        "B": [("Strategic Techie", 2), ("Grounded Architect", 2)],
        "C": [("Visionary Coach", 2), ("Creative Maverick", 1)],
        "D": [("Healing Alchemist", 2), ("Empathetic Architect", 2)]
    },
    "Q53": {
        "A": [("Trailblazer Entrepreneur", 2), ("Strategic Techie", 2)],
        "B": [("Grounded Architect", 2), ("Creative Maverick", 2)],
        "C": [("Visionary Coach", 2), ("Athletic Visionary", 1)],
        "D": [("Healing Alchemist", 2), ("Empathetic Architect", 2)]
    },
    "Q54": {
        "A": [("Trailblazer Entrepreneur", 2), ("Athletic Visionary", 1)],
        "B": [("Strategic Techie", 2), ("Grounded Architect", 2)],
        "C": [("Visionary Coach", 2), ("Creative Maverick", 2)],
        "D": [("Healing Alchemist", 2), ("Empathetic Architect", 2)]
    },
    "Q55": {
        "A": [("Trailblazer Entrepreneur", 2), ("Athletic Visionary", 1)],
        "B": [("Strategic Techie", 2), ("Grounded Architect", 2)],
        "C": [("Visionary Coach", 2), ("Creative Maverick", 1)],
        "D": [("Healing Alchemist", 2), ("Empathetic Architect", 2)]
    },
    "Q56": {
        "A": [("Trailblazer Entrepreneur", 2), ("Athletic Visionary", 1)],
        "B": [("Strategic Techie", 2), ("Grounded Architect", 2)],
        "C": [("Visionary Coach", 2), ("Creative Maverick", 1)],
        "D": [("Healing Alchemist", 2), ("Empathetic Architect", 2)]
    },
    "Q57": {
        "A": [("Trailblazer Entrepreneur", 2), ("Athletic Visionary", 1)],
        "B": [("Strategic Techie", 2), ("Grounded Architect", 2)],
        "C": [("Visionary Coach", 2), ("Creative Maverick", 1)],
        "D": [("Healing Alchemist", 2), ("Empathetic Architect", 2)]
    }
}

def calculate_archetypes(answers: dict, user_id: str):
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

    # Save to Supabase
    try:
        supabase.table("quiz_results").insert({
            "id": str(uuid.uuid4()),
            "user_id": user_id,
            "answers": answers,
            "archetypes": result,
            "created_at": datetime.utcnow().isoformat()
        }).execute()
    except Exception as e:
        print("Supabase insert error:", e)

    return {"archetypes": result}