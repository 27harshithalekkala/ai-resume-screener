from flask import Flask, request, jsonify, render_template
import os, re, json, PyPDF2, urllib.request, urllib.error

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")

def extract_text_from_pdf(filepath):
    text = ""
    with open(filepath, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()

def ask_ai(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"
    data = json.dumps({
        "model": "openrouter/free",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.1
    }).encode("utf-8")

    req = urllib.request.Request(
        url, data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "HTTP-Referer": "http://localhost:5000",
            "X-Title": "Resume Screener"
        },
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return result["choices"][0]["message"]["content"]
    except urllib.error.HTTPError as e:
        raise Exception(f"API Error {e.code}: {e.read().decode()}")

def analyse_resume(resume_text, job_description):
    prompt = f"""You are an expert HR recruiter. Analyse this resume against the job description.
Respond ONLY with valid JSON, no extra text, no markdown, no code fences.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Return exactly this JSON structure:
{{
  "candidate_name": "Full Name or Unknown",
  "email": "email or Not found",
  "phone": "phone or Not found",
  "skills": ["skill1", "skill2", "skill3"],
  "experience_years": 0,
  "education": "Highest degree and field",
  "match_score": 75,
  "match_reason": "One sentence explaining the score",
  "strengths": ["strength1", "strength2"],
  "gaps": ["gap1", "gap2"]
}}"""

    raw = ask_ai(prompt)
    raw = re.sub(r"^```(?:json)?\s*", "", raw.strip())
    raw = re.sub(r"\s*```$", "", raw)
    return json.loads(raw)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/screen", methods=["POST"])
def screen():
    if not OPENROUTER_API_KEY:
        return jsonify({"error": "OPENROUTER_API_KEY not set! Run: set OPENROUTER_API_KEY=your-key"}), 400

    job_description = request.form.get("job_description", "").strip()
    if not job_description:
        return jsonify({"error": "Please provide a job description."}), 400

    files = request.files.getlist("resumes")
    if not files or all(f.filename == "" for f in files):
        return jsonify({"error": "Please upload at least one PDF resume."}), 400

    results = []
    for file in files:
        if file.filename == "":
            continue
        if not file.filename.lower().endswith(".pdf"):
            results.append({"filename": file.filename, "error": "Only PDF files are supported."})
            continue

        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        try:
            resume_text = extract_text_from_pdf(filepath)
            if not resume_text:
                results.append({"filename": file.filename, "error": "Could not extract text from PDF."})
                continue
            analysis = analyse_resume(resume_text, job_description)
            analysis["filename"] = file.filename
            results.append(analysis)
        except Exception as e:
            results.append({"filename": file.filename, "error": str(e)})
        finally:
            if os.path.exists(filepath):
                os.remove(filepath)

    results.sort(key=lambda x: x.get("match_score", -1), reverse=True)
    return jsonify(results)

if __name__ == "__main__":
    print("\n✅ Resume Screener running with OpenRouter FREE!")
    print("   Open http://127.0.0.1:5000\n")
    app.run(debug=True)
