from flask import render_template, request, jsonify, redirect, url_for, session, flash
from app import app, db
from app.models import Question
import json
import random

app.secret_key = 'fX0kR4dyETk8kVs62PwwOmz4H'  # Substitua por uma chave secreta segura

@app.route('/')
def config():
    return render_template('config.html')

@app.route('/quiz', methods=['POST'])
def quiz():
    num_questions = int(request.form['num_questions'])
    duration = int(request.form['duration'])

    # Validação dos valores
    if num_questions <= 0 or duration <= 0:
        flash("O número de perguntas e a duração devem ser maiores que zero.")
        return redirect(url_for('config'))

    duration *= 60  # Convert minutes to seconds
    questions = Question.query.all()
    random.shuffle(questions)
    questions = questions[:num_questions]
    questions_data = [{'id': q.id, 'question': q.question, 'options': q.options} for q in questions]
    return render_template('quiz.html', questions=questions_data, duration=duration)

@app.route('/submit', methods=['POST'])
def submit():
    responses = request.json['responses']
    correct = 0
    total = len(responses)

    user_responses = []
    for response in responses:
        question = Question.query.get(response['id'])
        user_responses.append({
            'id': response['id'],
            'question': question.question,
            'options': question.options,
            'answer': question.answer,
            'user_answer': response['answer'],
            'explanation': question.explanation
        })
        if question.answer == response['answer']:
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
