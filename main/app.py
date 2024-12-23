import html
import json

from flask import Flask, request, render_template, session, redirect

from main.utils import format_utc_date, has_access, ask_anthropic

# Load the calls data
with open('resources/calls.json', 'r') as f:
    calls_data = json.load(f)

app = Flask(__name__)
app.secret_key = 'SOME_SECRET_KEY'


# Route to display the home page
@app.route("/")
def home():
    return render_template('home.html')


# Route to handle login
@app.route("/login", methods=["POST"])
def login():
    user_name = request.form.get("fullName")
    email = request.form.get("email")

    # Store the data in session
    session["user_name"] = user_name
    session["email"] = email
    session.permanent = True

    return redirect("/list")


# Route to display the list of calls
@app.route('/list')
def call_logs():
    call_list = []
    for call in calls_data:
        if has_access(call):
            call_list.append({
                'id': call['id'],
                'title': call['call_metadata']['title'],
                'participants': ", ".join({participant['name'] for participant in call['call_metadata']['parties']}),
                'date': format_utc_date(call['call_metadata']['start_time']),
                'summary': call['inference_results']['call_summary'] if 'call_summary' in call['inference_results'] else 'No summary available'
            })
    if call_list:
        return render_template('call_log_list.html', calls=call_list)
    else:
        return "No call logs found accessible to the user: {} ".format(session['user_name']), 404


# Route to display more details of a specific sales call
@app.route('/detailed_log/<string:call_id>', methods=['GET', 'POST'])
def detailed_log(call_id):
    call_entry = next((call for call in calls_data if call['id'] == call_id), None)
    answer = None

    is_authorized = has_access(call_entry)
    call_entry['call_metadata']['start_time'] = format_utc_date(call_entry['call_metadata']['start_time'])

    if call_entry and is_authorized:
        if request.method == 'POST':
            question = request.form.get('question').strip()
            if question:
                unescaped_answer = ask_question(call_id, question)
                unescaped_answer = html.escape(unescaped_answer[0])
                answer = unescaped_answer.replace("\n", "<br>")
        return render_template('call_details.html', call=call_entry, answer=answer)
    elif not is_authorized:
        return ("User {} does not have access to view the details of this call. Please contact your supervisor."
                .format(session['user_name']), 403)
    else:
        return "Call not found", 404


# Function to answer a question about a specific call
def ask_question(call_id, question):
    # Find the call transcript
    call = next((call for call in calls_data if call['id'] == call_id), None)
    if not call:
        return "Call not found", 404

    if not has_access(call):
        return "User does not have access to this call", 403

    transcript = call['transcript']
    if not transcript:
        return "Transcript not available for this call", 400

    return ask_anthropic(question, transcript)


if __name__ == '__main__':
    app.run(debug=True)

