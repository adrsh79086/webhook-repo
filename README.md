# action-repo
This will simulate GitHub actions like Push, Pull Requests, and Merge

# Webhook Receiver Application

This is a Flask application to receive GitHub webhooks and store them in MongoDB.

## How to Run

1. Clone the repository:
2. Install dependencies:
3. Run the Flask app:

## Webhook Events Supported
- Push
- Pull Request
- Merge

The UI automatically fetches the latest events from MongoDB every 15 seconds
 How to Test Before Submission
Run the Flask app locally using:

********
How To run

python app.py

Use LocalTunnel to expose your app to the internet:

lt --port 5000