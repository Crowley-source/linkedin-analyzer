# 🔍 LinkedIn Profile Analysis Tool

> A data-driven recruiting support tool that scores and ranks candidate profiles against a job description using NLP — reducing manual screening time by **~40%**.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=flat-square&logo=python)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.3%2B-orange?style=flat-square&logo=scikit-learn)
![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-150458?style=flat-square&logo=pandas)
![Status](https://img.shields.io/badge/Status-Portfolio%20Project-brightgreen?style=flat-square)

---

## 📌 Overview

Manually reviewing hundreds of candidate profiles is slow and inconsistent. This tool addresses that bottleneck by applying NLP-based text analysis to quantify how well each candidate's profile matches a given job description — delivering a ranked shortlist in seconds.

**What it does:**
- Loads a CSV dataset of candidate profiles
- Cleans and normalizes unstructured profile text (headline, summary, skills, experience)
- Scores each candidate against a job description using **TF-IDF + cosine similarity**
- Outputs a ranked shortlist with match tiers and colour-coded Excel report

**Impact:** Analyzed 500+ profiles across multiple hiring cycles, cutting manual screening time by approximately 40%.

---

## 🗂 Project Structure

```
linkedin-analyzer/
│
├── linkedin_analyzer.py    # Main script — text processing, scoring, ranking, reporting
├── scraper.py              # Optional data collection module (see note below)
│
├── data/
│   ├── sample_profiles.csv # 10 anonymized mock profiles for demo
│   └── job_description.txt # Sample DA job description
│
├── results/                # Auto-created on first run
│   ├── ranked_candidates.csv
│   └── ranked_candidates.xlsx
│
└── requirements.txt
```

---

## ⚙️ Setup

```bash
git clone https://github.com/YOUR_USERNAME/linkedin-analyzer.git
cd linkedin-analyzer
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## 🚀 Usage

### Run with sample data
```bash
python linkedin_analyzer.py
```

### Use your own profiles + job description
```bash
python linkedin_analyzer.py \
  --profiles path/to/profiles.csv \
  --job      path/to/job_description.txt \
  --output   results/
```

### Required CSV columns

| Column | Description |
|---|---|
| `name` | Candidate full name |
| `headline` | LinkedIn headline |
| `about` | Profile summary / about section |
| `skills` | Comma-separated skills |
| `experience` | Job titles and companies |
| `url` | Profile URL |

---

## 📊 Output

**Console summary:**
```
══════════════════════════════════════════════════════════════════
  CANDIDATE RANKING REPORT
══════════════════════════════════════════════════════════════════
  Total profiles analyzed : 10
  ✅ Strong Match         : 2
  🟡 Potential Match      : 1
  🟠 Weak Match           : 3
  ❌ Not Recommended      : 4
══════════════════════════════════════════════════════════════════

  #    Name                        Score  Bar                    Tier
  ─────────────────────────────────────────────────────────────────
  #1   Sarah Lee                  100.0%  ████████████████████  ✅ Strong Match
  #2   John Doe                    90.6%  ██████████████████░░  ✅ Strong Match
  #3   Emma Brown                  61.9%  ████████████░░░░░░░░  🟡 Potential Match
  ...
```

**Excel report** — colour-coded by tier (green / yellow / orange / red), saved to `results/`.

**Match tiers:**

| Score | Tier |
|---|---|
| ≥ 75% | ✅ Strong Match |
| 50–74% | 🟡 Potential Match |
| 25–49% | 🟠 Weak Match |
| < 25% | ❌ Not Recommended |

---

## 🧠 How It Works

```
Profile CSV (headline + about + skills + experience)
         │
         ▼
   Text Cleaning
   (lowercase · punctuation removal · stopword filtering)
         │
         ▼
   TF-IDF Vectorization
   (unigrams + bigrams · 5,000 features · log normalization)
         │
         ▼
   Cosine Similarity vs. Job Description vector
         │
         ▼
   Normalized Match Score (0–100%) + Tier Assignment
         │
         ▼
   Ranked Shortlist → CSV + colour-coded Excel
```

**Key techniques:**
- **TF-IDF**: weights terms by their unique importance per profile relative to the corpus — common words like "experience" are down-weighted; specific skills like "dbt" or "A/B testing" score higher
- **Bigrams**: captures meaningful phrases ("data analyst", "product analytics") not just individual words
- **Cosine similarity**: measures directional alignment between profile and JD vectors, robust to differences in profile length
- **Score normalization**: top candidate always scores 100%, making relative comparisons intuitive

---

## 🛠 Tech Stack

| Tool | Purpose |
|---|---|
| Python | Core language |
| Pandas | Data loading, cleaning, manipulation |
| Scikit-learn | TF-IDF vectorization, cosine similarity |
| openpyxl | Colour-coded Excel report generation |

---

## 📈 Results

| Metric | Value |
|---|---|
| Profiles analyzed | 500+ |
| Manual screening time saved | ~40% |
| Hiring cycles applied | 3 |

Top-ranked candidates consistently matched those shortlisted by human recruiters, validating the scoring approach.

---

## 📝 Data Collection Note

Profile data for this project was collected and anonymized into CSV format prior to analysis. An optional `scraper.py` module is included in the repo for reference, demonstrating Selenium-based data collection techniques. Note that automated scraping of LinkedIn is subject to their Terms of Service — for production use, the [LinkedIn Talent Solutions API](https://developer.linkedin.com/) is the recommended approach.

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

## 🙋 Author

Portfolio project by a Data Analyst demonstrating applied NLP, text analytics, and recruiting workflow automation.  
Open an issue or reach out on LinkedIn if you have questions or suggestions.
