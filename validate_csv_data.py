import os
import json
import pandas as pd
from datetime import datetime
from collections import defaultdict

DATA_DIR = "data"
OUT_DIR = os.path.join(DATA_DIR, "validation")
VALID_DIFFICULTIES = {"easy", "medium", "hard"}

os.makedirs(OUT_DIR, exist_ok=True)

def read_csv_safe(path):
    if not os.path.exists(path):
        return pd.DataFrame()
    return pd.read_csv(path).fillna("")

def is_valid_timestamp(val):
    if not val or str(val).strip() == "":
        return False
    try:
        s = str(val)
        if s.endswith("Z"):
            s = s[:-1]
        datetime.fromisoformat(s)
        return True
    except:
        return False

def to_int(val):
    try:
        if val in ("", None):
            return None
        return int(float(val))
    except:
        return None

def to_float(val):
    try:
        if val in ("", None):
            return None
        return float(val)
    except:
        return None

def fail(row, msg):
    r = row.copy()
    r["validation_errors"] = msg
    return r


# ---------------- LOAD CSV FILES ----------------
recipes = read_csv_safe(os.path.join(DATA_DIR, "recipe.csv"))
ingredients = read_csv_safe(os.path.join(DATA_DIR, "ingredients.csv"))
steps = read_csv_safe(os.path.join(DATA_DIR, "steps.csv"))

interactions_path1 = os.path.join(DATA_DIR, "interactions_normalized.csv")
interactions_path2 = os.path.join(DATA_DIR, "interactions.csv")

if os.path.exists(interactions_path1):
    interactions = read_csv_safe(interactions_path1)
elif os.path.exists(interactions_path2):
    interactions = read_csv_safe(interactions_path2)
else:
    interactions = pd.DataFrame()

known_recipe_ids = set(recipes["recipe_id"].astype(str).tolist()) if "recipe_id" in recipes else set()

invalid_recipes = []
invalid_ingredients = []
invalid_steps = []
invalid_interactions = []


# ---------------- VALIDATE RECIPES ----------------
for _, row in recipes.iterrows():
    r = row.to_dict()
    errs = []

    rid = str(r.get("recipe_id", "")).strip()
    title = str(r.get("title", "")).strip()

    if not rid:
        errs.append("missing recipe_id")
    if not title:
        errs.append("missing title")

    diff = str(r.get("difficulty", "")).lower().strip()
    if diff and diff not in VALID_DIFFICULTIES:
        errs.append(f"invalid difficulty '{diff}'")

    prep = to_int(r.get("prepTimeMinutes", ""))
    if prep is not None and prep < 0:
        errs.append("prepTimeMinutes negative")

    ing_count = to_int(r.get("ingredients_count", ""))
    if ing_count is not None and ing_count < 0:
        errs.append("ingredients_count negative")

    step_count = to_int(r.get("steps_count", ""))
    if step_count is not None and step_count < 0:
        errs.append("steps_count negative")

    if errs:
        invalid_recipes.append(fail(r, "; ".join(errs)))


# ---------------- VALIDATE INGREDIENTS ----------------
for _, row in ingredients.iterrows():
    r = row.to_dict()
    errs = []

    rid = str(r.get("recipe_id", "")).strip()
    ing = str(r.get("ingredient", "")).strip()

    if not rid:
        errs.append("missing recipe_id")
    elif rid not in known_recipe_ids:
        errs.append(f"unknown recipe_id '{rid}'")

    if not ing:
        errs.append("empty ingredient")

    if errs:
        invalid_ingredients.append(fail(r, "; ".join(errs)))


# ---------------- VALIDATE STEPS ----------------
for _, row in steps.iterrows():
    r = row.to_dict()
    errs = []

    rid = str(r.get("recipe_id", "")).strip()
    step_text = str(r.get("step_text", "")).strip()
    step_num = to_int(r.get("step_number", ""))

    if not rid:
        errs.append("missing recipe_id")
    elif rid not in known_recipe_ids:
        errs.append(f"unknown recipe_id '{rid}'")

    if not step_text:
        errs.append("empty step_text")

    if step_num is not None and step_num <= 0:
        errs.append("invalid step_number")

    if errs:
        invalid_steps.append(fail(r, "; ".join(errs)))


# ---------------- VALIDATE INTERACTIONS ----------------
for _, row in interactions.iterrows():
    r = row.to_dict()
    errs = []

    rid = str(r.get("recipe_id", "")).strip()
    if not rid:
        errs.append("missing recipe_id")
    elif rid not in known_recipe_ids:
        errs.append(f"unknown recipe_id '{rid}'")

    avg = to_float(r.get("avg_rating", ""))
    if avg is not None and (avg < 0 or avg > 5):
        errs.append("avg_rating out of range")

    for f in ["views", "likes", "cook_attempts", "rating_count"]:
        v = to_int(r.get(f, ""))
        if v is not None and v < 0:
            errs.append(f"{f} negative")

    if errs:
        invalid_interactions.append(fail(r, "; ".join(errs)))


# ---------------- SAVE INVALID OUTPUT ----------------
pd.DataFrame(invalid_recipes).to_csv(os.path.join(OUT_DIR, "invalid_recipes.csv"), index=False)
pd.DataFrame(invalid_ingredients).to_csv(os.path.join(OUT_DIR, "invalid_ingredients.csv"), index=False)
pd.DataFrame(invalid_steps).to_csv(os.path.join(OUT_DIR, "invalid_steps.csv"), index=False)
pd.DataFrame(invalid_interactions).to_csv(os.path.join(OUT_DIR, "invalid_interactions.csv"), index=False)

report = {
    "invalid_counts": {
        "recipes": len(invalid_recipes),
        "ingredients": len(invalid_ingredients),
        "steps": len(invalid_steps),
        "interactions": len(invalid_interactions),
    }
}

with open(os.path.join(OUT_DIR, "validation_report.json"), "w") as f:
    json.dump(report, f, indent=2)

print("\nValidation complete.")
print("Invalid rows saved in:", OUT_DIR)
