# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
client = MongoClient("mongodb://172.17.0.2:27017/")  # "mongo" is the name of the MongoDB container

db = client.notes_db
notes_collection = db.notes


@app.route("/notes", methods=["GET", "POST"])
def notes():
    if request.method == "GET":
        all_notes = list(notes_collection.find())

        # Convert ObjectId and datetime to JSON-serializable types
        serialized_notes = []
        for note in all_notes:
            serialized_note = {
                "_id": str(note["_id"]),  # Convert ObjectId to string
                "title": note["title"],
                "content": note["content"],
                "timestamp": note["timestamp"].isoformat() if "timestamp" in note else None  # Convert datetime to string
            }
            serialized_notes.append(serialized_note)

        return jsonify({"notes": serialized_notes})

    elif request.method == "POST":
        data = request.get_json()
        title = data.get("title")
        content = data.get("content")

        if title and content:
            note = {"title": title, "content": content}
            result = notes_collection.insert_one(note)
            return jsonify({"message": "Note added successfully", "note_id": str(result.inserted_id)})
        else:
            return jsonify({"error": "Title and content are required"}), 400


@app.route("/notes/<note_id>", methods=["GET", "PUT", "DELETE"])
def manage_note(note_id):
    if request.method == "GET":
        note = notes_collection.find_one({"_id": note_id})
        if note:
            return jsonify({"note": note})
        else:
            return jsonify({"error": "Note not found"}), 404

    elif request.method == "PUT":
        data = request.get_json()
        title = data.get("title")
        content = data.get("content")

        if title and content:
            result = notes_collection.update_one({"_id": note_id}, {"$set": {"title": title, "content": content}})
            if result.modified_count > 0:
                return jsonify({"message": "Note updated successfully"})
            else:
                return jsonify({"error": "Note not found"}), 404
        else:
            return jsonify({"error": "Title and content are required"}), 400

    elif request.method == "DELETE":
        result = notes_collection.delete_one({"_id": note_id})
        if result.deleted_count > 0:
            return jsonify({"message": "Note deleted successfully"})
        else:
            return jsonify({"error": "Note not found"}), 404


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")