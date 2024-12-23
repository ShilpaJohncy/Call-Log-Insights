# Call Log Insights

This is a web application that allows users to review their past sales calls, particularly:
1. View a summarised list of their previous calls
2. Get a more detailed view of any specific call
3. Ask questions about any specific call and receive answers based on the call's transcript.

The application uses Anthropic's Claude 3.5 Haiku model API to generate answers to questions about the call transcripts.

## Required Files
`calls.json`: Call transcript file with metadata and transcripts for 5 sample sales calls.
`anthropic-api-key.txt`: API key used for Anthropic's API.

## Installation
1. Clone the repository
2. Run the command `python3 -m venv .venv` to create a virtual environment. 
3. Activate the virtual environment using `. .venv/bin/activate`
4. Install the required packages using `pip install -r requirements.txt`
5. cd into the `main` directory
3. Run the app using `python3 -m flask --app app.py run`
4. Open the app in your browser at `http://127.0.0.1:5000`

## Usage
1. Login to the app using the full name and email. 
2. Once logged in, you are shown the call log list which displays all calls that the logged-in user has access to. 
   To keep this MVP simple, this is considered to just be the calls the user was a participant of. 
3. Click on any call to view a detailed view of the call. 
4. Ask any relevant question using the "Ask AI" button at the bottom of the page for querying the call's transcript.

## Example Scenarios To Test
1. Login with a user `Dan McDermott` and email `dan@elevate-strategies.io` who has access to multiple calls. 
2. Login with a user that has no calls associated with them.
3. Try to access the `detailed_log` page for a call the user has no access to. 
4. Ask question(s) about a call in the `detailed_log` page.

## Future Improvements
When building this application, I tried to strike a balance between a functional application, 
not spending too much time on something that wouldn’t have much use after the test. 
Below I have listed the ideas that I would have spent time on if this was a real project:
1. Add more features to the call log list page, such as filtering, sorting, and searching.
2. Expand the concept of "access" to calls based on user requirements. 
3. Improve the UI/UX of the application:
   The looks of the app are very basic at the moment. I would use a more established framework with customised/standard styling through out. 
   Better error handling and feedback to the user.
   Include more details regarding the participants of the call. Hyperlink to their LinkedIn profiles, render their avatar, etc. 
4. Expand the overall test coverage of the application. Include integration tests.
