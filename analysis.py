import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

DATA_DIR = "data"
OUT_DIR = os.path.join(DATA_DIR, "analytics")
os.makedirs(OUT_DIR, exist_ok=True)

# ---------- Load data ----------
def safe_load_csv(name):
    path = os.path.join(DATA_DIR, name)
    if not os.path.exists(path):
        print(f"[WARN] missing {path}")
        return pd.DataFrame()
    return pd.read_csv(path)

recipes = safe_load_csv("recipe.csv")
ingredients = safe_load_csv("ingredients.csv")
steps = safe_load_csv("steps.csv")
interactions = safe_load_csv("interactions_normalized.csv")  # aggregated interactions

# Normalize column names (trim)
def normalize_cols(df):
    if df.empty:
        return df
    df = df.copy()
    df.columns = [c.strip() for c in df.columns]
    return df

recipes = normalize_cols(recipes)
ingredients = normalize_cols(ingredients)
steps = normalize_cols(steps)
interactions = normalize_cols(interactions)

# Merge recipe metadata with interactions (left join)
if not recipes.empty and not interactions.empty:
    # unify recipe_id column names (detect common names)
    recipe_id_col = "recipe_id" if "recipe_id" in recipes.columns else ("recipeId" if "recipeId" in recipes.columns else recipes.columns[0])
    interactions_id_col = "recipe_id" if "recipe_id" in interactions.columns else ("recipeId" if "recipeId" in interactions.columns else interactions.columns[0])
    recipes = recipes.rename(columns={recipe_id_col: "recipe_id"})
    interactions = interactions.rename(columns={interactions_id_col: "recipe_id"})
    df = pd.merge(recipes, interactions, on="recipe_id", how="left", suffixes=("_recipe", "_inter"))
else:
    df = pd.DataFrame()

# Helper safe numeric coercion
def to_int_series(s):
    return pd.to_numeric(s, errors="coerce").astype("float").astype("Int64")

def to_float_series(s):
    return pd.to_numeric(s, errors="coerce").astype(float)

# Ensure numeric columns
if not df.empty:
    for col in ["prepTimeMinutes", "prep_time", "prep_time_minutes", "prepTime"]:
        if col in df.columns:
            df["prep_minutes"] = to_float_series(df[col])
            break
    if "prep_minutes" not in df:
        df["prep_minutes"] = np.nan

    for col in ["likes", "Likes", "like_count"]:
        if col in df.columns:
            df["likes"] = to_int_series(df[col])
            break
    if "likes" not in df:
        df["likes"] = pd.Series([np.nan]*len(df))

    for col in ["views", "Views", "view_count"]:
        if col in df.columns:
            df["views"] = to_int_series(df[col])
            break
    if "views" not in df:
        df["views"] = pd.Series([np.nan]*len(df))

    for col in ["cook_attempts", "cookAttempts", "attempts"]:
        if col in df.columns:
            df["cook_attempts"] = to_int_series(df[col])
            break
    if "cook_attempts" not in df:
        df["cook_attempts"] = pd.Series([np.nan]*len(df))

    for col in ["avg_rating", "avgRating", "average_rating"]:
        if col in df.columns:
            df["avg_rating"] = to_float_series(df[col])
            break
    if "avg_rating" not in df:
        df["avg_rating"] = pd.Series([np.nan]*len(df))

    for col in ["rating_count", "ratingCount", "ratings"]:
        if col in df.columns:
            df["rating_count"] = to_int_series(df[col])
            break
    if "rating_count" not in df:
        df["rating_count"] = pd.Series([np.nan]*len(df))

# ---------- Insight computations (unchanged) ----------
insights = []

# ---------- Charts (expanded to 10 analyses) ----------

# 1) Most common ingredients (top 20)
if not ingredients.empty and "ingredient" in ingredients.columns:
    ing_counts = ingredients["ingredient"].astype(str).str.lower().str.strip().value_counts().head(20)
    if not ing_counts.empty:
        plt.figure(figsize=(8,6))
        ing_counts.sort_values().plot(kind="barh")
        plt.title("Top 20 Most Common Ingredients")
        plt.xlabel("Count")
        plt.tight_layout()
        plt.savefig(os.path.join(OUT_DIR,"most_common_ingredients_top20.png"))
        plt.close()
        print("Saved most_common_ingredients_top20.png")

# 2) Average preparation time (histogram, boxplot & summary card)
if not df.empty and "prep_minutes" in df.columns and df["prep_minutes"].notna().sum() > 3:
    prep_series = df["prep_minutes"].dropna()

    # histogram
    plt.figure(figsize=(8,4))
    plt.hist(prep_series, bins=30)
    plt.title("Prep Time Distribution (minutes)")
    plt.xlabel("Prep minutes")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR,"prep_time_histogram.png"))
    plt.close()
    print("Saved prep_time_histogram.png")

    # boxplot
    plt.figure(figsize=(6,3))
    plt.boxplot(prep_series, vert=False)
    plt.title("Prep Time Boxplot")
    plt.xlabel("Prep minutes")
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR,"prep_time_boxplot.png"))
    plt.close()
    print("Saved prep_time_boxplot.png")

    # big-card summary (mean, median, n)
    prep_count = int(prep_series.size)
    mean_prep_val = float(prep_series.mean())
    median_prep_val = float(prep_series.median())
    out_img = os.path.join(OUT_DIR, "avg_prep_time_summary.png")
    plt.figure(figsize=(6,3))
    plt.axis("off")
    plt.text(0.5, 0.65, "Average preparation time", ha="center", va="center", fontsize=14, weight="bold")
    plt.text(0.5, 0.40, f"Mean: {mean_prep_val:.1f} min", ha="center", va="center", fontsize=22)
    plt.text(0.5, 0.15, f"Median: {median_prep_val:.1f} min  (n={prep_count})", ha="center", va="center", fontsize=14)
    plt.tight_layout()
    plt.savefig(out_img, dpi=150, bbox_inches="tight")
    plt.close()
    print("Saved avg_prep_time_summary.png")

# 3) Difficulty distribution chart
if isinstance(recipes, pd.DataFrame) and "difficulty" in recipes.columns:
    diff_counts = recipes["difficulty"].astype(str).str.lower().value_counts()
    if not diff_counts.empty:
        plt.figure(figsize=(6,4))
        diff_counts.plot(kind="bar")
        plt.title("Difficulty distribution")
        plt.ylabel("count")
        plt.tight_layout()
        plt.savefig(os.path.join(OUT_DIR,"difficulty_distribution.png"))
        plt.close()
        print("Saved difficulty_distribution.png")

# 4) Prep time vs likes scatter
if not df.empty and df["prep_minutes"].notna().sum()>3 and df["likes"].notna().sum()>3:
    plt.figure(figsize=(6,4))
    plt.scatter(df["prep_minutes"], df["likes"], alpha=0.6)
    plt.xlabel("Prep minutes")
    plt.ylabel("Likes")
    plt.title("Prep time vs Likes")
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR,"prep_vs_likes.png"))
    plt.close()
    print("Saved prep_vs_likes.png")

# 5) Most frequently viewed recipes (bar - top 10)
if not df.empty and df["views"].notna().sum()>0:
    topv = df[["title","views"]].dropna().sort_values("views", ascending=False).head(10)
    if not topv.empty:
        plt.figure(figsize=(8,4))
        plt.barh(topv["title"].astype(str).str[:60][::-1], topv["views"][::-1])
        plt.title("Top 10 Recipes by Views")
        plt.tight_layout()
        plt.savefig(os.path.join(OUT_DIR,"top10_views.png"))
        plt.close()
        print("Saved top10_views.png")

# 6) Ingredients associated with high engagement (avg likes top 20)
if not ingredients.empty and not interactions.empty and "ingredient" in ingredients.columns:
    ing_with_likes = ingredients.merge(interactions, left_on="recipe_id", right_on="recipe_id", how="left")
    group = ing_with_likes.groupby(ing_with_likes["ingredient"].astype(str).str.lower().str.strip())
    avg_likes = group["likes"].agg(lambda s: pd.to_numeric(s, errors="coerce").mean()).dropna().sort_values(ascending=False).head(20)
    if not avg_likes.empty:
        plt.figure(figsize=(8,6))
        avg_likes.sort_values().plot(kind="barh")
        plt.title("Top 20 Ingredients by Avg Likes (per ingredient)")
        plt.xlabel("Average likes per recipe containing ingredient")
        plt.tight_layout()
        plt.savefig(os.path.join(OUT_DIR,"ingredients_high_engagement_avg_likes_top20.png"))
        plt.close()
        print("Saved ingredients_high_engagement_avg_likes_top20.png")

# 7) Top recipes by likes (bar - top 10)  <-- NEW visual
if not df.empty and df["likes"].notna().sum()>0:
    topl = df[["title","likes"]].dropna().sort_values("likes", ascending=False).head(10)
    if not topl.empty:
        plt.figure(figsize=(8,4))
        plt.barh(topl["title"].astype(str).str[:60][::-1], topl["likes"][::-1])
        plt.title("Top 10 Recipes by Likes")
        plt.tight_layout()
        plt.savefig(os.path.join(OUT_DIR,"top10_likes.png"))
        plt.close()
        print("Saved top10_likes.png")

# 8) Top recipes by cook attempts (bar - top 10)  <-- NEW visual
if not df.empty and "cook_attempts" in df.columns and df["cook_attempts"].notna().sum()>0:
    topa = df[["title","cook_attempts"]].dropna().sort_values("cook_attempts", ascending=False).head(10)
    if not topa.empty:
        plt.figure(figsize=(8,4))
        plt.barh(topa["title"].astype(str).str[:60][::-1], topa["cook_attempts"][::-1])
        plt.title("Top 10 Recipes by Cook Attempts")
        plt.tight_layout()
        plt.savefig(os.path.join(OUT_DIR,"top10_attempts.png"))
        plt.close()
        print("Saved top10_attempts.png")

# 9) Rating distribution (histogram of avg_rating)  <-- NEW visual
if not df.empty and "avg_rating" in df.columns and df["avg_rating"].notna().sum()>0:
    ratings = df["avg_rating"].dropna()
    plt.figure(figsize=(8,4))
    plt.hist(ratings, bins=10)
    plt.title("Rating distribution (avg_rating)")
    plt.xlabel("Average rating")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR,"rating_distribution_hist.png"))
    plt.close()
    print("Saved rating_distribution_hist.png")

# 10) Top attempt-rate (cook_attempts / views)  <-- NEW visual
if not df.empty and "cook_attempts" in df.columns and "views" in df.columns:
    df["attempt_rate"] = df.apply(lambda r: (r["cook_attempts"] / r["views"]) if (pd.notna(r.get("cook_attempts")) and pd.notna(r.get("views")) and r["views"]>0) else np.nan, axis=1)
    tar = df[["title","attempt_rate"]].dropna().sort_values("attempt_rate", ascending=False).head(10)
    if not tar.empty:
        plt.figure(figsize=(8,4))
        plt.barh(tar["title"].astype(str).str[:60][::-1], tar["attempt_rate"][::-1])
        plt.title("Top 10 Recipes by Attempt Rate (cook_attempts / views)")
        plt.xlabel("Attempt rate")
        plt.tight_layout()
        plt.savefig(os.path.join(OUT_DIR,"top10_attempt_rate.png"))
        plt.close()
        print("Saved top10_attempt_rate.png")

print("Charts saved — check the files in", OUT_DIR)
