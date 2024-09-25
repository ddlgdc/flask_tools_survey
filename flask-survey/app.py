from flask import Flask, redirect, render_template, request, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = 'password'
app.config['DEBUG'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

responces_to_survey_questions = []

# home / default page
@app.route('/')
def home():
    # Displays start of survye page with base.html
    return render_template('base.html')

# route for questions
@app.route('/questions/<int:question_id>', methods=['POST', 'GET'])
def question(question_id):
    # check if question_id is valid
    if question_id < 1 or question_id > len(satisfaction_survey.questions):
        flash('You are trying to access an invalid question or skip ahead!')
        return redirect('/')
    
    # if the user has answered questions, check their progress
    if len(responces_to_survey_questions) != question_id - 1:
        # redirect to next quest
        return redirect(f'/questions{len(responces_to_survey_questions) + 1}')
    
    # handle the post req to store the answer
    if request.method == 'POST':
        if question_id == 3: # handle the special case for question 3 (money amount)
            money_amount = request.form.get('money')
            if not money_amount:
                return render_template('question_three.html', question = satisfaction_survey.questions[2], error = 'Please enter an amount.')
            responces_to_survey_questions.append(f'${money_amount}')
        else:
            answer = request.form.get('answer')
            if not answer:
                return render_template(f'question_{question_id}.html', question = satisfaction_survey.questions[question_id - 1], error = 'Please select an answer.')
            responces_to_survey_questions.append(answer)
        
        # redirect to the nest quewtions or to thank you page
        if question_id == len(satisfaction_survey.questions):
            return redirect('/thank_you')
        return redirect(f'/questions/{question_id + 1}')
    
    question = satisfaction_survey.questions[question_id - 1]
    return render_template(f'question_{question_id}.html', question = question)

# thank you page with responces
@app.route('/thank_you', methods=['GET', 'POST'])
def thank_you():
    return render_template('thank_you.html', responses = responces_to_survey_questions)

if __name__ == '__main__':
    app.run(debug = True, port = 5001)