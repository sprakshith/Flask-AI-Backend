import os
from flask_cors import CORS
from dotenv import load_dotenv
from flask_socketio import SocketIO, send
from flask import Flask, request, jsonify, session
from database.utils import ProjectUtils, UserStoryUtils
from agents.system_architect_agent import SystemArchitectAgent

load_dotenv()

app = Flask(__name__)
CORS(app)

app.secret_key = os.getenv('FLASK_SESSION_SECRET_KEY', 'secret')
socketio = SocketIO(app, cors_allowed_origins="*")

saa = SystemArchitectAgent()


@app.route('/create-project', methods=['POST'])
def index():

    data = request.get_json()

    if data is None:
        return jsonify({'status': 'No data provided'}), 400
    else:
        project_name = data.get('project_name')
        all_user_stories = data.get('all_user_stories')

        try:
            project = ProjectUtils.create_project(project_name)
        except Exception as e:
            print(e)
            return jsonify({'status': str(e)}), 409

        session['project_id'] = project.id

        try:
            for index, user_story in enumerate(all_user_stories):
                UserStoryUtils.create_user_story(project_id=project.id, user_story_count=index+1, description=user_story)
        except Exception as e:
            print(e)
            return jsonify({'status': str(e)}), 409

    return jsonify({'message': 'Project created successfully', 'project_id': project.id}), 201


@app.route('/chat-agent-interation', methods=['POST'])
def chat_agent_interaction():

    session['project_id'] = 1

    data = request.get_json()

    if data is None:
        return jsonify({'status': 'No data provided'}), 400
    else:
        message = data.get('message')

        try:
            response = saa.process_message(message, session.get('project_id'))
        except Exception as e:
            print(e)
            return jsonify({'status': str(e)}), 409

    return jsonify({'response': response}), 200


@socketio.on('connect')
def handle_connect():
    send('Hello, welcome to Flask AI!\nI am your System Architect Agent.\nHow can I help you today?')


@socketio.on('message')
def handle_message(message):
    send(saa.process_message(message, "user_12873901274_message_session"))


@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port=5000, debug=True)
