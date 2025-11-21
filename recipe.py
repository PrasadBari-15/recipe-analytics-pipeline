
import os
import datetime
import firebase_admin
from firebase_admin import credentials, firestore

KEY_FILE = r"D:\programs\firebase\Task 2\RecipeAccountKey.json"
if not os.path.exists(KEY_FILE):
    raise SystemExit(f"{KEY_FILE} not found. Put your service account JSON in the script folder.")

cred = credentials.Certificate(KEY_FILE)
firebase_admin.initialize_app(cred)
db = firestore.client()

now = datetime.datetime.utcnow()

recipes = [
    {
        "recipe_id": "recipe_001",
        "title": "Vegetable Pulav",
        "difficulty": "Medium",
        "servings": 4,
        "prep_time_min": 15,
        "cook_time_min": 25,
        "ingredients": [
            {"name": "Basmati rice", "quantity": 1.5, "unit": "cups"},
            {"name": "Ghee", "quantity": 2, "unit": "tbsp"},
            {"name": "Mixed vegetables", "quantity": 1, "unit": "cup"},
            {"name": "Green peas", "quantity": 0.5, "unit": "cup"},
            {"name": "Onion", "quantity": 1, "unit": "medium"},
            {"name": "Green chili", "quantity": 2, "unit": "pieces"},
            {"name": "Water", "quantity": 3, "unit": "cups"},
            {"name": "Salt", "quantity": 1, "unit": "tsp"}
        ],
        "steps": [
            {"step_no": 1, "instruction": "Measure 1.5 cups basmati rice and place in a strainer."},
            {"step_no": 2, "instruction": "Rinse rice under running water until water is mostly clear."},
            {"step_no": 3, "instruction": "Let rice drain for 5 minutes."},
            {"step_no": 4, "instruction": "Chop onion and green chilies into small slices."},
            {"step_no": 5, "instruction": "Heat a pot on medium and add 2 tbsp ghee."},
            {"step_no": 6, "instruction": "Add sliced onion and chilies; sauté for 2 minutes."},
            {"step_no": 7, "instruction": "Add mixed vegetables and peas; cook for 3-4 minutes."},
            {"step_no": 8, "instruction": "Add drained rice and lightly stir for 1 minute."},
            {"step_no": 9, "instruction": "Pour 3 cups water into the pot and stir once."},
            {"step_no": 10, "instruction": "Add 1 tsp salt and combine gently."},
            {"step_no": 11, "instruction": "Bring mixture to a steady boil on high heat."},
            {"step_no": 12, "instruction": "Reduce heat to low, cover, and cook for 12–15 minutes. Then rest 5 minutes and fluff."}
        ],
        "tags": ["rice", "vegetarian", "one-pot"],
        "created_at": now,
        "updated_at": now
    },
    {
        "recipe_id": "recipe_002",
        "title": "Masala Khichdi",
        "difficulty": "Easy",
        "servings": 3,
        "prep_time_min": 12,
        "cook_time_min": 18,
        "ingredients": [
            {"name": "Rice", "quantity": 1, "unit": "cup"},
            {"name": "Moong dal", "quantity": 0.5, "unit": "cup"},
            {"name": "Turmeric", "quantity": 0.5, "unit": "tsp"},
            {"name": "Ghee", "quantity": 1, "unit": "tbsp"},
            {"name": "Cumin seeds", "quantity": 1, "unit": "tsp"},
            {"name": "Salt", "quantity": 1, "unit": "tsp"},
            {"name": "Water", "quantity": 3, "unit": "cups"}
        ],
        "steps": [
            {"step_no": 1, "instruction": "Wash rice and moong dal together until water runs clearer."},
            {"step_no": 2, "instruction": "Soak for 5 minutes then drain."},
            {"step_no": 3, "instruction": "Heat ghee in a pressure cooker on medium heat."},
            {"step_no": 4, "instruction": "Add cumin seeds; let them crackle for a few seconds."},
            {"step_no": 5, "instruction": "Add rice and dal; sauté for 1 minute."},
            {"step_no": 6, "instruction": "Add turmeric, salt and 3 cups water."},
            {"step_no": 7, "instruction": "Stir, close the lid and cook for 3 whistles on medium heat."},
            {"step_no": 8, "instruction": "Turn off heat and allow pressure to release naturally."},
            {"step_no": 9, "instruction": "Open lid, stir gently to combine."},
            {"step_no": 10, "instruction": "Serve hot with a drizzle of ghee and pickle."}
        ],
        "tags": ["comfort", "light-meal"],
        "created_at": now,
        "updated_at": now
    },
    {
        "recipe_id": "recipe_003",
        "title": "Lemon Rice",
        "difficulty": "Easy",
        "servings": 2,
        "prep_time_min": 10,
        "cook_time_min": 8,
        "ingredients": [
            {"name": "Cooked rice", "quantity": 2, "unit": "cups"},
            {"name": "Lemon juice", "quantity": 2, "unit": "tbsp"},
            {"name": "Oil", "quantity": 1, "unit": "tbsp"},
            {"name": "Peanuts", "quantity": 2, "unit": "tbsp"},
            {"name": "Turmeric", "quantity": 0.25, "unit": "tsp"},
            {"name": "Mustard seeds", "quantity": 0.5, "unit": "tsp"},
            {"name": "Salt", "quantity": 1, "unit": "tsp"}
        ],
        "steps": [
            {"step_no": 1, "instruction": "Spread leftover rice on a plate to remove clumps."},
            {"step_no": 2, "instruction": "Heat oil in a pan and add mustard seeds until they pop."},
            {"step_no": 3, "instruction": "Add peanuts and roast until crisp."},
            {"step_no": 4, "instruction": "Add turmeric and mix quickly."},
            {"step_no": 5, "instruction": "Add rice to the pan and stir gently."},
            {"step_no": 6, "instruction": "Add lemon juice and salt, mix evenly."},
            {"step_no": 7, "instruction": "Keep stirring for 1–2 minutes on low heat."},
            {"step_no": 8, "instruction": "Turn off heat and let it rest covered briefly."},
            {"step_no": 9, "instruction": "Garnish with coriander leaves if available."},
            {"step_no": 10, "instruction": "Serve warm or at room temperature."}
        ],
        "tags": ["quick", "rice"],
        "created_at": now,
        "updated_at": now
    },
    {
        "recipe_id": "recipe_004",
        "title": "Aloo Paratha",
        "difficulty": "Medium",
        "servings": 4,
        "prep_time_min": 20,
        "cook_time_min": 15,
        "ingredients": [
            {"name": "Wheat flour", "quantity": 2, "unit": "cups"},
            {"name": "Boiled potatoes", "quantity": 3, "unit": "pieces"},
            {"name": "Salt", "quantity": 1, "unit": "tsp"},
            {"name": "Oil", "quantity": 1, "unit": "tbsp"},
            {"name": "Coriander", "quantity": 2, "unit": "tbsp"}
        ],
        "steps": [
            {"step_no": 1, "instruction": "Make a soft dough with wheat flour and water; rest 10 minutes."},
            {"step_no": 2, "instruction": "Boil and peel potatoes; mash smoothly."},
            {"step_no": 3, "instruction": "Mix mashed potatoes with salt, coriander and mild spices."},
            {"step_no": 4, "instruction": "Divide dough and stuffing into equal portions."},
            {"step_no": 5, "instruction": "Roll a dough ball into a small circle, place stuffing, fold edges."},
            {"step_no": 6, "instruction": "Gently roll the stuffed ball into a paratha shape."},
            {"step_no": 7, "instruction": "Heat a tawa (griddle) and add a few drops of oil."},
            {"step_no": 8, "instruction": "Cook paratha on both sides until golden brown."},
            {"step_no": 9, "instruction": "Apply oil/ghee while cooking for crisp finish."},
            {"step_no": 10, "instruction": "Serve hot with curd or pickle."}
        ],
        "tags": ["stuffed", "breakfast"],
        "created_at": now,
        "updated_at": now
    },
    {
        "recipe_id": "recipe_005",
        "title": "Dal Tadka",
        "difficulty": "Easy",
        "servings": 4,
        "prep_time_min": 10,
        "cook_time_min": 20,
        "ingredients": [
            {"name": "Toor dal", "quantity": 1, "unit": "cup"},
            {"name": "Ghee", "quantity": 1, "unit": "tbsp"},
            {"name": "Garlic", "quantity": 4, "unit": "cloves"},
            {"name": "Cumin", "quantity": 1, "unit": "tsp"},
            {"name": "Tomato", "quantity": 1, "unit": "medium"},
            {"name": "Salt", "quantity": 1, "unit": "tsp"}
        ],
        "steps": [
            {"step_no": 1, "instruction": "Rinse toor dal under cold water."},
            {"step_no": 2, "instruction": "Pressure cook dal with water until soft (3–4 whistles)."},
            {"step_no": 3, "instruction": "Heat ghee in a pan and add cumin seeds."},
            {"step_no": 4, "instruction": "Add chopped garlic and sauté till light brown."},
            {"step_no": 5, "instruction": "Add chopped tomato and cook until soft."},
            {"step_no": 6, "instruction": "Pour cooked dal into the pan; mix well."},
            {"step_no": 7, "instruction": "Add salt and simmer for 5 minutes."},
            {"step_no": 8, "instruction": "Prepare a tadka (ghee, cumin, garlic) and pour over dal."},
            {"step_no": 9, "instruction": "Stir and simmer for another minute."},
            {"step_no": 10, "instruction": "Serve hot with rice or roti."}
        ],
        "tags": ["dal", "comfort"],
        "created_at": now,
        "updated_at": now
    },
    {
        "recipe_id": "recipe_006",
        "title": "Paneer Bhurji",
        "difficulty": "Easy",
        "servings": 3,
        "prep_time_min": 10,
        "cook_time_min": 12,
        "ingredients": [
            {"name": "Paneer", "quantity": 200, "unit": "g"},
            {"name": "Onion", "quantity": 1, "unit": "medium"},
            {"name": "Tomato", "quantity": 1, "unit": "medium"},
            {"name": "Turmeric", "quantity": 0.25, "unit": "tsp"},
            {"name": "Salt", "quantity": 1, "unit": "tsp"},
            {"name": "Oil", "quantity": 1, "unit": "tbsp"}
        ],
        "steps": [
            {"step_no": 1, "instruction": "Crumble paneer and keep aside."},
            {"step_no": 2, "instruction": "Heat oil in a pan and add chopped onions."},
            {"step_no": 3, "instruction": "Sauté onions until translucent."},
            {"step_no": 4, "instruction": "Add chopped tomatoes and cook till soft."},
            {"step_no": 5, "instruction": "Add turmeric and salt; mix."},
            {"step_no": 6, "instruction": "Add crumbled paneer and stir for 2–3 minutes."},
            {"step_no": 7, "instruction": "Adjust seasoning and cook until paneer is warm."},
            {"step_no": 8, "instruction": "Garnish with coriander and serve hot."},
            {"step_no": 9, "instruction": "Serve with roti or bread."},
            {"step_no": 10, "instruction": "Store leftovers in fridge for up to 2 days."}
        ],
        "tags": ["paneer", "quick"],
        "created_at": now,
        "updated_at": now
    },
    {
        "recipe_id": "recipe_007",
        "title": "Egg Curry",
        "difficulty": "Medium",
        "servings": 3,
        "prep_time_min": 12,
        "cook_time_min": 18,
        "ingredients": [
            {"name": "Eggs", "quantity": 4, "unit": "pieces"},
            {"name": "Onion", "quantity": 1, "unit": "medium"},
            {"name": "Tomato", "quantity": 2, "unit": "medium"},
            {"name": "Ginger-garlic paste", "quantity": 1, "unit": "tsp"},
            {"name": "Oil", "quantity": 1, "unit": "tbsp"},
            {"name": "Salt", "quantity": 1, "unit": "tsp"}
        ],
        "steps": [
            {"step_no": 1, "instruction": "Boil eggs, cool, peel and set aside."},
            {"step_no": 2, "instruction": "Heat oil and sauté chopped onions until golden."},
            {"step_no": 3, "instruction": "Add ginger-garlic paste; cook briefly."},
            {"step_no": 4, "instruction": "Add chopped tomatoes and cook until mushy."},
            {"step_no": 5, "instruction": "Season with salt and spices to taste."},
            {"step_no": 6, "instruction": "Add a little water to make gravy and simmer 5 mins."},
            {"step_no": 7, "instruction": "Make shallow slits in eggs and add to gravy."},
            {"step_no": 8, "instruction": "Simmer eggs in gravy for 5–7 minutes."},
            {"step_no": 9, "instruction": "Garnish with coriander and serve hot."},
            {"step_no": 10, "instruction": "Serve with rice or roti."}
        ],
        "tags": ["nonveg", "curry"],
        "created_at": now,
        "updated_at": now
    },
    {
        "recipe_id": "recipe_008",
        "title": "Jeera Rice",
        "difficulty": "Easy",
        "servings": 3,
        "prep_time_min": 5,
        "cook_time_min": 12,
        "ingredients": [
            {"name": "Rice", "quantity": 1, "unit": "cup"},
            {"name": "Cumin seeds", "quantity": 1, "unit": "tsp"},
            {"name": "Ghee", "quantity": 1, "unit": "tbsp"},
            {"name": "Salt", "quantity": 1, "unit": "tsp"},
            {"name": "Water", "quantity": 2, "unit": "cups"}
        ],
        "steps": [
            {"step_no": 1, "instruction": "Rinse rice and soak for 10 minutes."},
            {"step_no": 2, "instruction": "Heat ghee in a pot and add cumin seeds."},
            {"step_no": 3, "instruction": "Sauté cumin seeds until aromatic."},
            {"step_no": 4, "instruction": "Add drained rice and stir for a minute."},
            {"step_no": 5, "instruction": "Add 2 cups water and salt; mix gently."},
            {"step_no": 6, "instruction": "Bring to boil, then reduce heat, cover and cook 12 minutes."},
            {"step_no": 7, "instruction": "Turn off heat and rest covered for 5 minutes."},
            {"step_no": 8, "instruction": "Fluff with fork and serve."},
            {"step_no": 9, "instruction": "Optional: garnish with fried cashews."},
            {"step_no": 10, "instruction": "Serve hot with dal or curry."}
        ],
        "tags": ["rice", "side-dish"],
        "created_at": now,
        "updated_at": now
    },
    {
        "recipe_id": "recipe_009",
        "title": "Tomato Soup",
        "difficulty": "Easy",
        "servings": 2,
        "prep_time_min": 8,
        "cook_time_min": 15,
        "ingredients": [
            {"name": "Tomatoes", "quantity": 4, "unit": "medium"},
            {"name": "Butter", "quantity": 1, "unit": "tbsp"},
            {"name": "Onion", "quantity": 0.5, "unit": "medium"},
            {"name": "Salt", "quantity": 1, "unit": "tsp"},
            {"name": "Water", "quantity": 1.5, "unit": "cups"}
        ],
        "steps": [
            {"step_no": 1, "instruction": "Chop tomatoes and onion roughly."},
            {"step_no": 2, "instruction": "Heat butter in a pan and sauté onion until soft."},
            {"step_no": 3, "instruction": "Add chopped tomatoes and cook until soft."},
            {"step_no": 4, "instruction": "Add water and salt; simmer 8–10 minutes."},
            {"step_no": 5, "instruction": "Blend the mixture until smooth."},
            {"step_no": 6, "instruction": "Strain soup if a smoother texture is desired."},
            {"step_no": 7, "instruction": "Reheat, adjust salt, and add a dash of pepper."},
            {"step_no": 8, "instruction": "Serve hot with croutons or bread."},
            {"step_no": 9, "instruction": "Optional: add cream swirl for richness."},
            {"step_no": 10, "instruction": "Store leftovers in fridge up to 2 days."}
        ],
        "tags": ["soup", "starter"],
        "created_at": now,
        "updated_at": now
    },
    {
        "recipe_id": "recipe_010",
        "title": "Upma",
        "difficulty": "Easy",
        "servings": 3,
        "prep_time_min": 6,
        "cook_time_min": 10,
        "ingredients": [
            {"name": "Sooji (rava)", "quantity": 1, "unit": "cup"},
            {"name": "Water", "quantity": 2.5, "unit": "cups"},
            {"name": "Oil", "quantity": 1, "unit": "tbsp"},
            {"name": "Mustard seeds", "quantity": 0.5, "unit": "tsp"},
            {"name": "Curry leaves", "quantity": 6, "unit": "leaves"},
            {"name": "Salt", "quantity": 1, "unit": "tsp"}
        ],
        "steps": [
            {"step_no": 1, "instruction": "Heat oil in a pan and add mustard seeds."},
            {"step_no": 2, "instruction": "When seeds pop, add curry leaves and sauté."},
            {"step_no": 3, "instruction": "Add 2.5 cups water and bring to a boil."},
            {"step_no": 4, "instruction": "Slowly add sooji while stirring to avoid lumps."},
            {"step_no": 5, "instruction": "Add salt and mix thoroughly."},
            {"step_no": 6, "instruction": "Cook on low heat for 4–5 minutes till water absorbs."},
            {"step_no": 7, "instruction": "Turn off heat and cover for 2 minutes."},
            {"step_no": 8, "instruction": "Fluff with a fork and serve hot."},
            {"step_no": 9, "instruction": "Optional: garnish with lemon and coriander."},
            {"step_no": 10, "instruction": "Serve with chutney or pickle."}
        ],
        "tags": ["breakfast", "quick"],
        "created_at": now,
        "updated_at": now
    },
    {
        "recipe_id": "recipe_011",
        "title": "Poha",
        "difficulty": "Easy",
        "servings": 2,
        "prep_time_min": 6,
        "cook_time_min": 10,
        "ingredients": [
            {"name": "Poha (flattened rice)", "quantity": 2, "unit": "cups"},
            {"name": "Onion", "quantity": 1, "unit": "medium"},
            {"name": "Peanuts", "quantity": 2, "unit": "tbsp"},
            {"name": "Mustard seeds", "quantity": 0.5, "unit": "tsp"},
            {"name": "Turmeric", "quantity": 0.25, "unit": "tsp"},
            {"name": "Lemon juice", "quantity": 1, "unit": "tbsp"},
            {"name": "Salt", "quantity": 1, "unit": "tsp"}
        ],
        "steps": [
            {"step_no": 1, "instruction": "Rinse poha briefly and drain; keep aside."},
            {"step_no": 2, "instruction": "Heat oil and add mustard seeds; let them crackle."},
            {"step_no": 3, "instruction": "Add peanuts and roast until crisp."},
            {"step_no": 4, "instruction": "Add chopped onions and cook until translucent."},
            {"step_no": 5, "instruction": "Add turmeric and mix well."},
            {"step_no": 6, "instruction": "Add drained poha and salt; mix gently."},
            {"step_no": 7, "instruction": "Cook for 1–2 minutes to heat through."},
            {"step_no": 8, "instruction": "Turn off heat and add lemon juice."},
            {"step_no": 9, "instruction": "Garnish with coriander and serve."},
            {"step_no": 10, "instruction": "Serve warm with chai or as a snack."}
        ],
        "tags": ["breakfast", "quick"],
        "created_at": now,
        "updated_at": now
    },
    {
        "recipe_id": "recipe_012",
        "title": "Chole Masala",
        "difficulty": "Medium",
        "servings": 4,
        "prep_time_min": 12,
        "cook_time_min": 25,
        "ingredients": [
            {"name": "Chickpeas (boiled)", "quantity": 1, "unit": "cup"},
            {"name": "Onion", "quantity": 1, "unit": "medium"},
            {"name": "Tomato", "quantity": 2, "unit": "medium"},
            {"name": "Ginger-garlic paste", "quantity": 1, "unit": "tsp"},
            {"name": "Chole masala", "quantity": 1, "unit": "tbsp"},
            {"name": "Oil", "quantity": 1, "unit": "tbsp"},
            {"name": "Salt", "quantity": 1, "unit": "tsp"}
        ],
        "steps": [
            {"step_no": 1, "instruction": "Heat oil and sauté chopped onions till golden."},
            {"step_no": 2, "instruction": "Add ginger-garlic paste and sauté briefly."},
            {"step_no": 3, "instruction": "Add chopped tomatoes and cook until mushy."},
            {"step_no": 4, "instruction": "Add chole masala and mix well."},
            {"step_no": 5, "instruction": "Add boiled chickpeas and 1 cup water; stir."},
            {"step_no": 6, "instruction": "Simmer for 15 minutes on low heat."},
            {"step_no": 7, "instruction": "Adjust salt and spices to taste."},
            {"step_no": 8, "instruction": "Garnish with coriander and serve hot."},
            {"step_no": 9, "instruction": "Serve with bhatura, puri or rice."},
            {"step_no": 10, "instruction": "Store leftovers in fridge up to 3 days."}
        ],
        "tags": ["curry", "protein"],
        "created_at": now,
        "updated_at": now
    },
    {
        "recipe_id": "recipe_013",
        "title": "Fried Rice",
        "difficulty": "Easy",
        "servings": 2,
        "prep_time_min": 10,
        "cook_time_min": 12,
        "ingredients": [
            {"name": "Cooked rice", "quantity": 2, "unit": "cups"},
            {"name": "Mixed vegetables", "quantity": 1, "unit": "cup"},
            {"name": "Soy sauce", "quantity": 1, "unit": "tbsp"},
            {"name": "Oil", "quantity": 1, "unit": "tbsp"},
            {"name": "Green onion", "quantity": 1, "unit": "stalk"}
        ],
        "steps": [
            {"step_no": 1, "instruction": "Heat oil in a wok on high heat."},
            {"step_no": 2, "instruction": "Add mixed vegetables and stir-fry until tender."},
            {"step_no": 3, "instruction": "Add cooked rice and toss well."},
            {"step_no": 4, "instruction": "Add soy sauce and mix thoroughly."},
            {"step_no": 5, "instruction": "Season with salt/pepper as needed."},
            {"step_no": 6, "instruction": "Garnish with chopped green onion."},
            {"step_no": 7, "instruction": "Serve immediately while hot."},
            {"step_no": 8, "instruction": "Optional: add scrambled egg for non-veg version."},
            {"step_no": 9, "instruction": "Adjust seasoning and serve."},
            {"step_no": 10, "instruction": "Store leftovers separately for best texture."}
        ],
        "tags": ["indo-chinese", "quick"],
        "created_at": now,
        "updated_at": now
    },
    {
        "recipe_id": "recipe_014",
        "title": "Rava Sheera",
        "difficulty": "Easy",
        "servings": 2,
        "prep_time_min": 6,
        "cook_time_min": 10,
        "ingredients": [
            {"name": "Rava (semolina)", "quantity": 0.5, "unit": "cup"},
            {"name": "Sugar", "quantity": 0.5, "unit": "cup"},
            {"name": "Ghee", "quantity": 2, "unit": "tbsp"},
            {"name": "Water", "quantity": 1, "unit": "cup"},
            {"name": "Cardamom", "quantity": 2, "unit": "pods"}
        ],
        "steps": [
            {"step_no": 1, "instruction": "Heat ghee in a pan and roast rava until aromatic."},
            {"step_no": 2, "instruction": "Boil water with cardamom pods."},
            {"step_no": 3, "instruction": "Slowly add rava to boiling water while stirring."},
            {"step_no": 4, "instruction": "Add sugar and mix until dissolved."},
            {"step_no": 5, "instruction": "Cook on low heat until sheera thickens."},
            {"step_no": 6, "instruction": "Add a little ghee for shine and flavor."},
            {"step_no": 7, "instruction": "Turn off heat and let it rest for a minute."},
            {"step_no": 8, "instruction": "Serve warm; garnish with nuts if desired."},
            {"step_no": 9, "instruction": "Store leftovers in fridge for a day."},
            {"step_no": 10, "instruction": "Reheat gently before serving."}
        ],
        "tags": ["dessert", "sweet"],
        "created_at": now,
        "updated_at": now
    },
    {
        "recipe_id": "recipe_015",
        "title": "Dal Fry",
        "difficulty": "Easy",
        "servings": 3,
        "prep_time_min": 8,
        "cook_time_min": 15,
        "ingredients": [
            {"name": "Toor dal", "quantity": 1, "unit": "cup"},
            {"name": "Ghee", "quantity": 1, "unit": "tbsp"},
            {"name": "Garlic", "quantity": 4, "unit": "cloves"},
            {"name": "Tomato", "quantity": 1, "unit": "medium"},
            {"name": "Cumin", "quantity": 1, "unit": "tsp"},
            {"name": "Salt", "quantity": 1, "unit": "tsp"}
        ],
        "steps": [
            {"step_no": 1, "instruction": "Rinse dal and cook until soft."},
            {"step_no": 2, "instruction": "Mash dal slightly to desired consistency."},
            {"step_no": 3, "instruction": "Heat ghee and add cumin and garlic."},
            {"step_no": 4, "instruction": "Add chopped tomato and cook into a thick masala."},
            {"step_no": 5, "instruction": "Combine dal with the masala and simmer."},
            {"step_no": 6, "instruction": "Adjust salt and add water if needed."},
            {"step_no": 7, "instruction": "Finish with a tadka (ghee + spices) poured on top."},
            {"step_no": 8, "instruction": "Garnish with coriander and serve hot."},
            {"step_no": 9, "instruction": "Serve with steamed rice or roti."},
            {"step_no": 10, "instruction": "Store leftovers in refrigerator."}
        ],
        "tags": ["dal", "comfort"],
        "created_at": now,
        "updated_at": now
    }
]

# Upload all recipes
for r in recipes:
    doc_ref = db.collection("recipes").document(r["recipe_id"])
    doc_ref.set(r)
    print(f"Uploaded recipe: {r['recipe_id']} - {r['title']}")

print("All 15 recipes uploaded successfully.")      