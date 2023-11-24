from sentence_transformers import SentenceTransformer, util
from pymongo import MongoClient
from bson import ObjectId
from flask import Flask, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

# Load the pre-trained BERT model
bert_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Connect to MongoDB
client = MongoClient("mongodb://172.17.0.2:27017/")
db = client.notes_db
notes_collection = db.notes

@app.route("/similar_notes", methods=["GET"])
def similar_notes():
    query_string = request.args.get("query_string", "")

    # Get all notes from the database
    all_notes = list(notes_collection.find())

    # Embed the query string using BERT
    query_embedding = bert_model.encode(query_string, convert_to_tensor=True)

    # Embed each note's content using BERT and calculate similarity
    similarity_results = []
    for note in all_notes:
        note_embedding = bert_model.encode(note["content"], convert_to_tensor=True)
        similarity_score = util.pytorch_cos_sim(query_embedding, note_embedding)[0][0].item()

        # Append note details along with similarity score
        similarity_results.append({
            "note_id": str(note["_id"]),
            "title": note["title"],
            "content": note["content"],
            "timestamp": note["timestamp"].isoformat() if "timestamp" in note else None,
            "similarity_score": similarity_score
        })

    # Sort notes by similarity score in descending order
    similarity_results.sort(key=lambda x: x["similarity_score"], reverse=True)

    response = {
        "query_string": query_string,
        "similar_notes": similarity_results
    }

    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")