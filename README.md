<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>Recipe Analytics Pipeline — README</title>
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial; line-height: 1.6; color: #111; padding: 32px; background:#f7f9fb; }
    .container { max-width: 980px; margin: 0 auto; background: #fff; padding: 28px 36px; border-radius: 10px; box-shadow: 0 6px 24px rgba(20,30,40,0.08); }
    h1 { margin-top: 0; font-size: 28px; display:flex; gap:12px; align-items:center; }
    h1 .emoji { font-size:28px; }
    h2 { color: #0b57a4; margin-top: 26px; }
    h3 { margin-top: 18px; }
    pre { background:#0f1720; color:#e6eef8; padding:14px; border-radius:8px; overflow:auto; }
    code { background:#eef3f8; padding:2px 6px; border-radius:4px; font-family:monospace; }
    table { border-collapse: collapse; width:100%; margin:10px 0 18px 0; }
    th, td { padding:10px 12px; border:1px solid #e6eef8; text-align:left; }
    .muted { color:#666; font-size:14px; }
    ul { margin:8px 0 12px 1.2em; }
    .pill { display:inline-block; background:#eef7ff; color:#0b57a4; padding:4px 10px; border-radius:999px; font-weight:600; font-size:13px; margin-right:6px; }
    .section { margin-bottom: 20px; }
    .footer { margin-top:30px; padding-top:16px; border-top:1px solid #eef3f8; color:#444; }
    a.file-link { color:#0b57a4; text-decoration:none; font-weight:600; }
    .note { background:#fff8e6; border:1px solid #ffe2a8; padding:10px 12px; border-radius:8px; }
    .code-block { background:#0b1220; color:#e6eef8; padding:12px; border-radius:8px; overflow:auto;}
  </style>
</head>
<body>
  <div class="container">
    <h1><span class="emoji">🍽️</span> Recipe Analytics Pipeline</h1>
    <p class="muted">A Python-based Data Engineering pipeline to extract, transform, validate, and analyze recipe data stored in Firebase Firestore. This page is a complete HTML conversion of the project's README.</p>

    <div class="section">
      <h2>Project Overview</h2>
      <p>This project was developed for a Data Engineering assessment. It includes:</p>
      <ul>
        <li>Firestore collections: <code>recipes</code>, <code>users</code>, <code>interactions</code></li>
        <li>ETL layer (Firestore → CSV)</li>
        <li>Validation layer (schema and data checks)</li>
        <li>Analytics layer (charts and 10+ insights)</li>
      </ul>

      <p class="note">Original uploaded file: <a class="file-link" href="/mnt/data/🍽.docx" title="Original uploaded document">/mnt/data/🍽.docx</a>. :contentReference[oaicite:1]{index=1}</p>
    </div>

    <div class="section">
      <h2>Architecture Diagram</h2>
      <p>(Insert architecture diagram image here)</p>
    </div>

    <div class="section">
      <h2>ER Diagram</h2>
      <p>(Insert ER diagram image here)</p>
    </div>

    <div class="section">
      <h2>Data Flow Diagram</h2>
      <p>(Insert data flow diagram image here)</p>
    </div>

    <div class="section">
      <h2>Project Structure</h2>
      <pre class="code-block">
project-folder/
|
├── data/
│   ├── analytics/              # Generated charts and insights
│   └── validation/             # Data validation results
|
├── recipe.py                   # Upload recipes to Firestore
├── users.py                    # Upload user profiles
├── interaction.py              # Upload interactions
|
├── etl_export_to_csv.py        # Extract Firestore → CSV
├── validate_csv_data.py        # Schema and data quality checks
├── analysis.py                 # Analytics + visualizations
|
└── RecipeAccountKey.json       # Firebase service account key
      </pre>
    </div>

    <div class="section">
      <h2>Features</h2>
      <ul>
        <li><strong>Structured ingestion:</strong> Seed scripts upload fully formed recipe, user, and interaction data.</li>
        <li><strong>ETL pipeline:</strong> Extracts, normalizes nested arrays, and exports clean CSV files.</li>
        <li><strong>Validation:</strong> Detects missing fields, type mismatches, empty arrays, and invalid relations.</li>
        <li><strong>Analytics:</strong> Generates 10+ business insights and PNG charts.</li>
        <li><strong>BI-ready:</strong> Outputs compatible with Power BI, Tableau, Excel.</li>
      </ul>
    </div>

    <div class="section">
      <h2>Data Model</h2>

      <h3>Users Collection</h3>
      <table>
        <thead>
          <tr><th>Field</th><th>Description</th></tr>
        </thead>
        <tbody>
          <tr><td><code>user_id</code></td><td>Unique identifier</td></tr>
          <tr><td><code>name</code></td><td>User name</td></tr>
          <tr><td><code>email</code></td><td>Email address</td></tr>
          <tr><td><code>location</code></td><td>User location</td></tr>
          <tr><td><code>preferences</code></td><td>Array of preferences</td></tr>
          <tr><td><code>signup_date</code></td><td>Date user joined</td></tr>
        </tbody>
      </table>

      <h3>Recipes Collection</h3>
      <table>
        <thead>
          <tr><th>Field</th><th>Description</th></tr>
        </thead>
        <tbody>
          <tr><td><code>recipe_id</code></td><td>Unique recipe ID</td></tr>
          <tr><td><code>title</code></td><td>Recipe title</td></tr>
          <tr><td><code>difficulty</code></td><td>Easy / Medium / Hard</td></tr>
          <tr><td><code>servings</code></td><td>Number of servings</td></tr>
          <tr><td><code>prep_time_min</code></td><td>Preparation time (minutes)</td></tr>
          <tr><td><code>cook_time_min</code></td><td>Cooking time (minutes)</td></tr>
          <tr><td><code>tags</code></td><td>Array of tags</td></tr>
          <tr><td><code>ingredients[]</code></td><td>Array of objects: { name, quantity, unit }</td></tr>
          <tr><td><code>steps[]</code></td><td>Array of objects: { step_no, instruction }</td></tr>
          <tr><td><code>created_at</code></td><td>Timestamp</td></tr>
          <tr><td><code>updated_at</code></td><td>Timestamp</td></tr>
        </tbody>
      </table>

      <h3>Interactions Collection</h3>
      <table>
        <thead>
          <tr><th>Field</th><th>Description</th></tr>
        </thead>
        <tbody>
          <tr><td><code>recipe_id</code></td><td>Reference to recipe</td></tr>
          <tr><td><code>avg_rating</code></td><td>Average rating (1.0 – 5.0)</td></tr>
          <tr><td><code>rating_count</code></td><td>Number of ratings</td></tr>
          <tr><td><code>likes</code></td><td>Total likes</td></tr>
          <tr><td><code>cook_attempts</code></td><td>Cook attempts</td></tr>
          <tr><td><code>views</code></td><td>Total views</td></tr>
        </tbody>
      </table>
    </div>

    <div class="section">
      <h2>Prerequisites</h2>
      <ul>
        <li>Python <strong>3.11+</strong></li>
        <li>Firebase project with Firestore enabled</li>
      </ul>

      <h3>Install dependencies</h3>
      <pre class="code-block">pip install firebase-admin pandas python-dateutil matplotlib pillow</pre>

      <h3>Firebase Setup</h3>
      <ol>
        <li>Create a Firebase project and enable Firestore.</li>
        <li>Generate a Service Account Key (JSON) from Project Settings → Service accounts.</li>
        <li>Save the JSON file in your project root (e.g., <code>RecipeAccountKey.json</code>).</li>
        <li>Update <code>SERVICE_ACCOUNT_PATH</code> in:
          <ul>
            <li><code>recipe.py</code></li>
            <li><code>users.py</code></li>
            <li><code>interaction.py</code></li>
            <li><code>etl_export_to_csv.py</code></li>
          </ul>
        </li>
        <li><em>Security note:</em> Add the service account JSON to <code>.gitignore</code> to avoid committing secrets.</li>
      </ol>
    </div>

    <div class="section">
      <h2>Execution Steps (Pipeline Workflow)</h2>
      <p>The pipeline runs in four sequential phases. Execute them in order.</p>

      <h3>Phase 1 — Database Seeding</h3>
      <p>Upload seed data to Firestore:</p>
      <pre class="code-block">
python recipe.py
python users.py
python interaction.py
      </pre>

      <h3>Phase 2 — ETL (Extract → Transform → Load)</h3>
      <p>Export normalized CSV files:</p>
      <pre class="code-block">python etl_export_to_csv.py</pre>
      <p>Generated files:</p>
      <pre class="code-block">
data/recipe.csv
data/ingredients.csv
data/steps.csv
data/interactions_normalized.csv
      </pre>

      <h3>Phase 3 — Data Validation</h3>
      <p>Run validation checks:</p>
      <pre class="code-block">python validate_csv_data.py</pre>
      <p>Validation outputs:</p>
      <pre class="code-block">
data/validation/
    invalid_recipes.csv
    invalid_ingredients.csv
    invalid_steps.csv
    invalid_interactions.csv
    validation_report.json
      </pre>

      <h3>Phase 4 — Analytics & Visualization</h3>
      <p>Run analytics to generate charts and insights:</p>
      <pre class="code-block">python analysis.py</pre>
      <p>Outputs saved in:</p>
      <pre class="code-block">data/analytics/</pre>
    </div>

    <div class="section">
      <h2>Insights Generated (10+)</h2>
      <ol>
        <li>Most common ingredients</li>
        <li>Average preparation time</li>
        <li>Difficulty distribution (Easy / Medium / Hard)</li>
        <li>Prep-time vs likes correlation</li>
        <li>Top 10 recipes by views</li>
        <li>Top 10 recipes by likes</li>
        <li>Top 10 recipes by cook attempts</li>
        <li>Ingredients with highest average likes</li>
        <li>Rating distribution histogram</li>
        <li>Attempt-rate leaderboard (cook_attempts ÷ views)</li>
      </ol>
    </div>

    <div class="section">
      <h2>Known Limitations</h2>
      <ul>
        <li>Service account path is currently hardcoded in multiple scripts — consider environment variables or a secret manager for production.</li>
        <li>Pipeline optimized for demo volume (~15–20 recipes). For large-scale data, optimize Firestore export/processing.</li>
        <li>User collection not currently joined in analytics — analysis focuses on recipes & interactions.</li>
        <li>Validation checks schema-level rules but not complex multi-table business logic.</li>
      </ul>
    </div>

    <div class="section">
      <h2>Contact</h2>
      <p><strong>Prasad Bari</strong> — <a href="mailto:prasadbari1515@gmail.com">prasadbari1515@gmail.com</a></p>
    </div>

    <div class="footer">
      <p class="muted">This HTML README was generated from your uploaded document. You can open the original file here: <a class="file-link" href="/mnt/data/🍽.docx">/mnt/data/🍽.docx</a>. :contentReference[oaicite:2]{index=2}</p>
      <p class="muted">If you want auxiliary files generated (e.g., <code>requirements.txt</code>, <code>.gitignore</code>, printable PDF, or diagram images), tell me and I will create them in HTML or plaintext form.</p>
    </div>
  </div>
</body>
</html>
