import random
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore

# ------------ CONFIG ------------
SERVICE_KEY_PATH = r"D:\programs\firebase\Task 2\RecipeAccountKey.json"
random.seed(42)  # reproducible values

# list of recipe ids you want covered
recipe_ids = [f"recipe_{i:03d}" for i in range(1, 21)]

# ------------ FIRESTORE INIT ------------
cred = credentials.Certificate(SERVICE_KEY_PATH)
firebase_admin.initialize_app(cred)
db = firestore.client()
col = db.collection("interactions")

# ------------ GENERATOR ------------
def generate_interaction_metrics(recipe_id):
    # realistic ranges
    views = random.randint(120, 600)
    likes = random.randint(5, min(views // 4, 120))
    cook_attempts = random.randint(0, min(views // 8, 60))
    rating_count = random.randint(0, min(20, max(1, views // 20)))

    # if rating_count is 0, set avg_rating = 0.0
    if rating_count == 0:
        avg_rating = 0.0
    else:
        ratings = [random.randint(1, 5) for _ in range(rating_count)]
        avg_rating = round(sum(ratings) / len(ratings), 2)

    return {
        "recipe_id": recipe_id,
        "views": views,
        "likes": likes,
        "cook_attempts": cook_attempts,
        "rating_count": rating_count,
        "avg_rating": avg_rating
    }

# ------------ MAIN LOGIC ------------
created = 0
skipped = 0

for rid in recipe_ids:
    # Check if an AUTO-GENERATED document for this recipe already exists.
    # We only consider docs created by this script if they have source == "auto_generated_v1".
    q = col.where("recipe_id", "==", rid).where("source", "==", "auto_generated_v1").limit(1).stream()
    already = False
    for _ in q:
        already = True
        break

    if already:
        print(f"SKIP (auto doc exists) → {rid}")
        skipped += 1
        continue

    # Not found: create a new document with AUTO ID and a marker so future runs skip
    metrics = generate_interaction_metrics(rid)
    metrics["source"] = "auto_generated_v1"
    metrics["created_at"] = datetime.utcnow().isoformat() + "Z"

    # add() creates a document with an auto-generated ID
    doc_ref = col.add(metrics)
    # doc_ref is a tuple (DocumentReference, write_result) in firebase-admin, but we don't need it here
    print(f"Created → with metrics: {metrics}")
    created
