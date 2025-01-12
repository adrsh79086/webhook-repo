from flask import Flask, request, jsonify, render_template
import pymongo
from datetime import datetime

app = Flask(__name__)

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["github_events"]
collection = db["events"]

# Create a webhook endpoint to receive GitHub events
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json

    if 'pusher' in data:
        event_type = "Push"
        author = data['pusher']['name']
        branch = data['ref'].split('/')[-1]
        timestamp = datetime.now().strftime("%d %B %Y - %I:%M %p UTC")
        message = f"{author} pushed to {branch} on {timestamp}"

    elif 'pull_request' in data:
        event_type = "Pull Request"
        author = data['pull_request']['user']['login']
        from_branch = data['pull_request']['head']['ref']
        to_branch = data['pull_request']['base']['ref']
        timestamp = datetime.now().strftime("%d %B %Y - %I:%M %p UTC")
        message = f"{author} submitted a pull request from {from_branch} to {to_branch} on {timestamp}"

    elif 'action' in data and data['action'] == 'closed' and data.get('pull_request', {}).get('merged'):
        event_type = "Merge"
        author = data['pull_request']['user']['login']
        from_branch = data['pull_request']['head']['ref']
        to_branch = data['pull_request']['base']['ref']
        timestamp = datetime.now().strftime("%d %B %Y - %I:%M %p UTC")
        message = f"{author} merged branch {from_branch} to {to_branch} on {timestamp}"

    else:
        return jsonify({"message": "Event type not supported"}), 400

    # Save event to MongoDB
    collection.insert_one({
        "event_type": event_type,
        "message": message,
        "timestamp": timestamp
    })

    return jsonify({"message": "Event received and stored"}), 200


# Route to render the UI
@app.route('/')
def index():
    print("Rendering index page")
    return render_template('index.html')


# API endpoint to fetch events from MongoDB
@app.route('/events', methods=['GET'])
def get_events():
    events = list(collection.find({}, {"_id": 0}).sort("timestamp", -1).limit(20))
    return jsonify(events)


# Run the Flask server
if __name__ == '__main__':
    app.run(port=5000, debug=True)
