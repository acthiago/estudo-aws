import json
from app import db

def populate_db():
    file_mapping = {
        "cloud_practitioner": "questions_cloud_practitioner.json",
        "solutions_architect_associate": "questions_solutions_architect_associate.json",
        "solutions_architect_professional": "questions_solutions_architect_professional.json"
    }

    collections = {
        "cloud_practitioner": db.questions_cloud_practitioner,
        "solutions_architect_associate": db.questions_solutions_architect_associate,
        "solutions_architect_professional": db.questions_solutions_architect_professional
    }

    for sim_type, file_name in file_mapping.items():
        collection = collections[sim_type]
        collection.delete_many({})  # Limpar a coleção antes de popular

        with open(file_name) as f:
            questions = json.load(f)
            for q in questions:
                question = {
                    "question": q['question'],
                    "options": q['options'],
                    "answer": q['answer'],
                    "explanation": q['explanation']
                }
                collection.insert_one(question)
