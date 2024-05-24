from flask import render_template, request, jsonify, redirect, url_for, session, flash
from app import app, db
from bson import ObjectId
import json
import random

app.secret_key = 'f87N9gS65bJPMKzd4nXov'  # Substitua por uma chave secreta segura

@app.route('/')
def config():
    return render_template('config.html')

@app.route('/quiz', methods=['POST'])
def quiz():
    simulation_type = request.form['simulation_type']
    num_questions = int(request.form['num_questions'])
    duration = int(request.form['duration'])

    # Validação dos valores
    if num_questions <= 0 or duration <= 0:
        flash("O número de perguntas e a duração devem ser maiores que zero.")
        return redirect(url_for('config'))

    duration *= 60  # Converter minutos para segundos

    # Selecionar a coleção baseada no tipo de simulado
    questions_collection = db[f'questions_{simulation_type}']
    questions = list(questions_collection.find())
    random.shuffle(questions)
    questions = questions[:num_questions]
    questions_data = [{'id': str(q['_id']), 'question': q['question'], 'options': q['options']} for q in questions]
    return render_template('quiz.html', questions=questions_data, duration=duration)

@app.route('/submit', methods=['POST'])
def submit():
    responses = request.json['responses']
    correct = 0
    total = len(responses)

    # Assumir que a primeira resposta contém o tipo de simulado
    question_id = ObjectId(responses[0]['id'])
    collections = db.list_collection_names()
    collection_name = next(name for name in collections if db[name].find_one({"_id": question_id}))

    questions_collection = db[collection_name]
    user_responses = []
    for response in responses:
        question = questions_collection.find_one({"_id": ObjectId(response['id'])})
        user_responses.append({
            'id': response['id'],
            'question': question['question'],
            'options': question['options'],
            'answer': question['answer'],
            'user_answer': response['answer'],
            'explanation': question['explanation']
        })
        if question['answer'] == response['answer']:
            correct += 1

    percentage = (correct / total) * 100
    session['result'] = {
        'correct': correct,
        'total': total,
        'percentage': percentage,
        'responses': user_responses
    }
    return jsonify({
        'correct': correct,
        'total': total,
        'percentage': percentage
    })

@app.route('/result')
def result():
    result = session.get('result')
    if result is None:
        return redirect(url_for('config'))

    return render_template('result.html', result={
        'correct': result['correct'],
        'total': result['total'],
        'percentage': result['percentage']
    }, questions=result['responses'], responses=result['responses'], zip=zip)
