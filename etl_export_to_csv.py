import os
from datetime import datetime
import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore

# ------------------------
# CONFIG
# ------------------------
PROJECT_ID = "recipe-2c702"         
SERVICE_ACCOUNT_PATH = r"D:\programs\firebase\Task 2\RecipeAccountKey.json" 
OUTPUT_DIR = "data"

# ------------------------
# FIRESTORE INIT
# ------------------------
def init_firestore():
    if not os.path.exists(SERVICE_ACCOUNT_PATH):
        raise SystemExit(f"Service account JSON not found at: {SERVICE_ACCOUNT_PATH}")
    if not firebase_admin._apps:
        cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
        firebase_admin.initialize_app(cred, {"projectId": PROJECT_ID})
    return firestore.client()

# ------------------------
# UTIL
# ------------------------
def to_iso(val):
    # Convert Firestore timestamp or datetime to ISO string, otherwise return original / empty string
    if val is None:
        return ""
    if isinstance(val, datetime):
        return val.isoformat() + "Z"
    # Firestore server timestamp may appear as google.protobuf...; rely on str fallback
    try:
        return str(val)
    except:
        return ""

def safe_get(d, *keys, default=None):
    for k in keys:
        if k in d and d[k] is not None:
            return d[k]
    return default

# ------------------------
# NORMALIZE RECIPE DOC
# ------------------------
def normalize_recipe_doc(doc):
    data = doc.to_dict() if hasattr(doc, "to_dict") else dict(doc)
    # recipe id preference: explicit fields else doc id
    rid = safe_get(data, "recipe_id", "recipeId", "id", "uid") or getattr(doc, "id", None) or ""
    # ensure string
    rid = str(rid)

    title = safe_get(data, "title", "name") or ""
    description = safe_get(data, "description", "desc") or ""
    difficulty = safe_get(data, "difficulty", "level") or ""
    cuisine = data.get("cuisine") or ""
    category = data.get("category") or ""
    authorId = data.get("authorId") or data.get("author") or ""
    prep = data.get("prepTimeMinutes") or data.get("prep_time") or data.get("prepTime") or data.get("prep_time_minutes")
    cook = data.get("cookTimeMinutes") or data.get("cook_time") or data.get("cookTime")
    total = data.get("totalTimeMinutes") or data.get("total_time")
    servings = data.get("servings")
    tags = data.get("tags") or []
    createdAt = to_iso(data.get("createdAt") or data.get("created_at"))
    updatedAt = to_iso(data.get("updatedAt") or data.get("updated_at"))
    isPublic = data.get("isPublic") if "isPublic" in data else data.get("public", "")

    # Ingredients: support list[str] and list[dict]
    raw_ing = data.get("ingredients") or []
    ing_list = []
    if isinstance(raw_ing, str):
        # comma-separated fallback
        for s in raw_ing.split(","):
            s = s.strip()
            if s:
                ing_list.append(s)
    elif isinstance(raw_ing, list):
        for item in raw_ing:
            if isinstance(item, str):
                if item.strip():
                    ing_list.append(item.strip())
            elif isinstance(item, dict):
                name = safe_get(item, "name", "ingredient", "text", "value") or ""
                if name:
                    ing_list.append(str(name).strip())
            else:
                # fallback
                try:
                    txt = str(item).strip()
                    if txt:
                        ing_list.append(txt)
                except:
                    pass

    # Steps: support list[str] and list[dict]
    raw_steps = data.get("steps") or data.get("instructions") or []
    steps_list = []
    if isinstance(raw_steps, str):
        for line in raw_steps.split("\n"):
            text = line.strip()
            if text:
                steps_list.append(text)
    elif isinstance(raw_steps, list):
        for item in raw_steps:
            if isinstance(item, str):
                if item.strip():
                    steps_list.append(item.strip())
            elif isinstance(item, dict):
                text = safe_get(item, "instruction", "step", "description", "text") or ""
                if text:
                    steps_list.append(str(text).strip())
            else:
                try:
                    txt = str(item).strip()
                    if txt:
                        steps_list.append(txt)
                except:
                    pass

    return {
        "recipe_id": rid,
        "title": title,
        "description": description,
        "difficulty": difficulty,
        "cuisine": cuisine,
        "category": category,
        "authorId": authorId,
        "prepTimeMinutes": prep,
        "cookTimeMinutes": cook,
        "totalTimeMinutes": total,
        "servings": servings,
        "tags": tags,
        "createdAt": createdAt,
        "updatedAt": updatedAt,
        "isPublic": isPublic,
        "ingredients": ing_list,
        "steps": steps_list
    }

# ------------------------
# EXPORT RECIPES
# ------------------------
def export_recipes(db, output_dir=OUTPUT_DIR):
    col = db.collection("recipes")
    docs = list(col.stream())
    recipe_rows = []
    ingredients_rows = []
    steps_rows = []

    ing_counter = 1
    step_counter = 1

    for doc in docs:
        r = normalize_recipe_doc(doc)
        recipe_rows.append({
            "recipe_id": r["recipe_id"],
            "title": r["title"],
            "description": r["description"],
            "difficulty": r["difficulty"],
            "cuisine": r["cuisine"],
            "category": r["category"],
            "authorId": r["authorId"],
            "prepTimeMinutes": r["prepTimeMinutes"] if r["prepTimeMinutes"] is not None else "",
            "cookTimeMinutes": r["cookTimeMinutes"] if r["cookTimeMinutes"] is not None else "",
            "totalTimeMinutes": r["totalTimeMinutes"] if r["totalTimeMinutes"] is not None else "",
            "servings": r["servings"] if r["servings"] is not None else "",
            "tags": ",".join(r["tags"]) if isinstance(r["tags"], (list, tuple)) else r["tags"],
            "createdAt": r["createdAt"],
            "updatedAt": r["updatedAt"],
            "isPublic": r["isPublic"],
            "ingredients_count": len(r["ingredients"]),
            "steps_count": len(r["steps"])
        })

        for ing in r["ingredients"]:
            ingredients_rows.append({
                "ingredient_id": f"ing_{ing_counter:06d}",
                "recipe_id": r["recipe_id"],
                "ingredient": ing
            })
            ing_counter += 1

        for i, stext in enumerate(r["steps"], start=1):
            steps_rows.append({
                "step_id": f"step_{step_counter:06d}",
                "recipe_id": r["recipe_id"],
                "step_number": i,
                "step_text": stext
            })
            step_counter += 1

    # write CSVs
    os.makedirs(output_dir, exist_ok=True)
    recipes_path = os.path.join(output_dir, "recipe.csv")
    ingredients_path = os.path.join(output_dir, "ingredients.csv")
    steps_path = os.path.join(output_dir, "steps.csv")

    pd.DataFrame(recipe_rows).to_csv(recipes_path, index=False)
    pd.DataFrame(ingredients_rows).to_csv(ingredients_path, index=False)
    pd.DataFrame(steps_rows).to_csv(steps_path, index=False)

    print(f"Exported {len(recipe_rows)} recipes -> {recipes_path}")
    print(f"Exported {len(ingredients_rows)} ingredients -> {ingredients_path}")
    print(f"Exported {len(steps_rows)} steps -> {steps_path}")

# ------------------------
# EXPORT INTERACTIONS
# ------------------------
def export_interactions(db, output_dir=OUTPUT_DIR):
    col = db.collection("interactions")
    docs = list(col.stream())

    rows = []
    for doc in docs:
        data = doc.to_dict()
        # Some interactions may be aggregated per recipe (one doc per recipe_id),
        # other docs may be event-level. We'll prefer aggregated fields if present.
        recipe_id = safe_get(data, "recipe_id", "recipeId", "recipe", default=None) or str(doc.id)
        # Map likely aggregated field names:
        avg_rating = safe_get(data, "avg_rating", "avgRating", "average_rating", default=None)
        rating_count = safe_get(data, "rating_count", "ratingCount", "rating_count", "ratings", default=None)
        likes = safe_get(data, "likes", "like_count", "likeCount", default=None)
        cook_attempts = safe_get(data, "cook_attempts", "cookAttempts", "attempts", default=None)
        views = safe_get(data, "views", "view_count", "viewsCount", default=None)

        # If aggregated doc doesn't exist but there are event-like fields, try to derive:
        # For safety we coerce numeric-looking values to int/float, else set to 0.
        def to_int(v):
            try:
                return int(v)
            except:
                return 0
        def to_float(v):
            try:
                return round(float(v), 2)
            except:
                return 0.0

        row = {
            "recipe_id": str(recipe_id),
            "avg_rating": to_float(avg_rating) if avg_rating is not None else 0.0,
            "rating_count": to_int(rating_count) if rating_count is not None else 0,
            "likes": to_int(likes) if likes is not None else 0,
            "cook_attempts": to_int(cook_attempts) if cook_attempts is not None else 0,
            "views": to_int(views) if views is not None else 0
        }

        rows.append(row)

    # There may be multiple aggregated docs per recipe (unlikely). consolidate by recipe_id: sum counts and compute weighted avg.
    consolidated = {}
    for r in rows:
        rid = r["recipe_id"]
        if rid not in consolidated:
            consolidated[rid] = {
                "views": r["views"],
                "likes": r["likes"],
                "cook_attempts": r["cook_attempts"],
                "rating_count": r["rating_count"],
                "avg_rating_numerator": r["avg_rating"] * r["rating_count"] if r["rating_count"] else 0.0
            }
        else:
            c = consolidated[rid]
            c["views"] += r["views"]
            c["likes"] += r["likes"]
            c["cook_attempts"] += r["cook_attempts"]
            c["avg_rating_numerator"] += r["avg_rating"] * r["rating_count"]
            c["rating_count"] += r["rating_count"]

    out_rows = []
    for rid, c in consolidated.items():
        if c["rating_count"] > 0:
            avg = round(c["avg_rating_numerator"] / c["rating_count"], 2)
        else:
            avg = 0.0
        out_rows.append({
            "recipe_id": rid,
            "avg_rating": avg,
            "rating_count": int(c["rating_count"]),
            "likes": int(c["likes"]),
            "cook_attempts": int(c["cook_attempts"]),
            "views": int(c["views"])
        })

    os.makedirs(output_dir, exist_ok=True)
    interactions_path = os.path.join(output_dir, "interactions_normalized.csv")
    pd.DataFrame(out_rows).to_csv(interactions_path, index=False)
    print(f"Exported {len(out_rows)} aggregated interaction rows -> {interactions_path}")

# ------------------------
# MAIN
# ------------------------
def main():
    db = init_firestore()
    export_recipes(db, OUTPUT_DIR)
    export_interactions(db, OUTPUT_DIR)
    print("ETL export complete.")

if __name__ == "__main__":
    main()
