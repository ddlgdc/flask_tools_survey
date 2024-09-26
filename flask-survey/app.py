from flask import Flask, redirect, render_template, request, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = 'some_password'
app.config['DEBUG'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

# home / default page
@app.route('/')
def home():
    # Displays start of survye page with base.html
    return render_template('base.html')

# new route to handle start of survey 
@app.route('/start-survey', methods=['POST'])
def start_survey():
    # intialize the session responses list to store the usrs answers
    session['responses'] = [] # new list made each user session
    return redirect('/questions/1') # redirect to question 1

# route for questions
@app.route('/questions/<int:question_id>', methods=['POST', 'GET'])
def question(question_id):
    # retreive the session responses
    responses = session.get('responses', [])

    # check if question_id is valid
    if question_id < 1 or question_id > len(satisfaction_survey.questions):
        flash('You are trying to access an invalid question or skip ahead!')
        return redirect('/')
    
    # check is user is trying to access a question out of order 
    if len(responses) != question_id - 1:
        flash('You are trying to skip a question.')
        return redirect(f'/questions/{len(responses) + 1}')
    
    # handle the post req to store the answer
    if request.method == 'POST':
        if question_id == 3:
            money = request.form.get('money')
            if not money:
                question = satisfaction_survey.questions[question_id - 1]
                return render_template(f'question_{question_id}.html',question = question, error='Please enter a value.')
            responses.append(money)
        else:
            answer = request.form.get('answer')
            if not answer:
                question = satisfaction_survey.questions[question_id - 1]
                return render_template(f'question_{question_id}.html', question = question, error = 'Please select an answer')
        
        # append the anser to session list 
            responses.append(answer)
        session['responses'] = responses

        # redirect to next question or thank you page
        if question_id == len(satisfaction_survey.questions):
            return redirect('/thank_you')
        return redirect(f'/questions/{question_id + 1}')
    
    # if its a get req, render question template
    question = satisfaction_survey.questions[question_id - 1]
    return render_template(f'question_{question_id}.html', question = question)

# thank you page with responces
@app.route('/thank_you', methods=['GET', 'POST'])
def thank_you():
    # retreive responses from session 
    responses = session.get('responses', [])
    return render_template('thank_you.html', responses = responses)

if __name__ == '__main__':
    app.run(debug = True, port = 5001)