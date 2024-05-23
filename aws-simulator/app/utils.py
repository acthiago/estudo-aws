import json
from app import db
from app.models import Question

def populate_db():
    # Limpar a tabela antes de popular
    db.session.query(Question).delete()
    db.session.commit()
    
    with open('questions.json') as f:
        questions = json.load(f)
        for q in questions:
            # Verificar se a pergunta já existe no banco de dados
            if not db.session.query(Question).filter_by(question=q['question']).first():
                question = Question(
                    question=q['question'],
                    options=q['options'],
                    answer=q['answer'],
                    explanation=q['explanation']
                )
                db.session.add(question)
        db.session.commit()
