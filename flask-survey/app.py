from flask import Flask, redirect, render_template, request
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

# question 1
@app.route('/questions/1', methods=['POST', 'GET'])
def question_one():
    # will return and display question one

    if request.method == 'POST':
        answer = request.form.get('answer')
        if not answer:
            return render_template('question_one.html', question = satisfaction_survey.questions[0], error = 'Please select an answer')
        
        responces_to_survey_questions.append(answer)
        return redirect('/questions/2')
    
    question = satisfaction_survey.questions[0]
    return render_template('question_one.html', question = question)

# question 2
@app.route('/questions/2', methods=['POST', 'GET'])
def question_two():
    # will return and display question two

    if request.method == 'POST':
        answer = request.form.get('answer')
        if not answer:
            return render_template('question_two.html', question=satisfaction_survey.questions[1], error='Please select an answer')
        
        responces_to_survey_questions.append(answer)
        return redirect('/questions/3')

    question = satisfaction_survey.questions[1]
    return render_template('question_two.html', question = question)

# question 3
@app.route('/questions/3', methods=['POST', 'GET'])
def question_three():
    # will return and display question three

    if request.method == 'POST':
        money_amount = request.form.get('money')

        if not money_amount:
            return render_template('question_three.html', question=satisfaction_survey.questions[2], error='Please select an answer')
        
        responces_to_survey_questions.append(f"${money_amount}")
        return redirect('/questions/4')

    question = satisfaction_survey.questions[2]
    return render_template('question_three.html', question = question)

# question 4
@app.route('/questions/4', methods=['POST', 'GET'])
def question_four():
    if request.method == 'POST':
        answer = request.form.get('answer')  
        
        if not answer:
            return render_template('question_four.html', question=satisfaction_survey.questions[3], error='Please select an answer')

        responces_to_survey_questions.append(answer) 
        return redirect('/thank_you')  

    question = satisfaction_survey.questions[3]  
    return render_template('question_four.html', question=question)

# thank you page with responces
@app.route('/thank_you', methods=['GET', 'POST'])
def thank_you():
    print("Final Responses:", responces_to_survey_questions)
    return render_template('thank_you.html', responses=responces_to_survey_questions)

if __name__ == '__main__':
    app.run(debug = True, port = 5001)