from flask import Flask
from flask import render_template
from flask import request
from flask import send_file
import pickle
import os
from sklearn.metrics.pairwise import cosine_similarity
from resume_utils import (extract_text,clean_resume)
from skills import extract_skills
import pandas as pd

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
print("MODEL PATH:")
print(os.path.abspath("models/clf.pkl"))
tfidf = pickle.load(open("models/tfidf.pkl", "rb"))
clf = pickle.load(open("models/clf.pkl", "rb"))
print("Loaded model steps:")
le = pickle.load(open("models/label_encoder.pkl", "rb"))
import sklearn
print("SKLEARN VERSION:", sklearn.__version__)
print("MODEL TYPE:")
print("MODEL FILE:")
import os
print(os.path.abspath("models/clf.pkl"))

@app.route("/")
def home():
    return render_template("index.html")
  
@app.route("/analyze",methods=["POST"])
def analyze():
    files = request.files.getlist("resumes")
    jd = request.form.get("jobdesc", "")
    results = []
    jd_skills = extract_skills(jd)
    for file in files:
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
        resume_text = extract_text(filepath)
        resume_text = clean_resume(resume_text)
        resume_vector = tfidf.transform([resume_text])
        prediction = clf.predict(resume_vector)
        category = le.inverse_transform(prediction)[0]
        jd_vector = tfidf.transform([jd])
        match_score = cosine_similarity(resume_vector, jd_vector)[0][0]*100
        resume_skills = extract_skills(resume_text)
        missing_skills = list(set(jd_skills) - set(resume_skills))
        skill_score = (len(resume_skills) / max(len(jd_skills), 1))*100
        ranking_score = (match_score*0.7 + skill_score*0.3)
        if ranking_score >= 85:
            status = "Highly Recommended"
        elif ranking_score >= 70:
            status = "Recommended"
        else:
            status = "Rejected"
            
        if match_score >= 80:
            bar_class = "high"
        elif match_score >= 60:
            bar_class = "medium"
        else:
            bar_class = "low"

        results.append({
            "name": file.filename,
            "category": category,
            "match": round(match_score,2),
            "ranking": round(ranking_score,2),
            "skills": ", ".join(resume_skills),
            "missing": ", ".join(missing_skills),
            "status": status,
            "bar_class": bar_class,
            "preview": resume_text[:500]
        })
    results = sorted(results, key=lambda x: x["ranking"], reverse=True)
    results = results[:10]
    df_results = pd.DataFrame(results)
    df_results.to_excel("results/final_report.xlsx", index=False)

    return render_template("result.html", results = results)

@app.route("/download")
def download():
    return send_file(
        "results/final_report.xlsx",
        as_attachment=True
    )
    
if __name__ == "__main__":
    app.run(debug=True)
