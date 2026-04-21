# Milestone 4 Grading Rubric

**QM 2023 Capstone: Final Investment Memo (M4)**  
**Total Points: 50** (25% of capstone grade)

---

## Component Breakdown

### 1. Reproducibility & Technical Rigor (10 points)

**Objective:** Verify that findings in the memo are reproducible from the team repository code, and that all models and diagnostics are sound.

| Points | Criteria |
|--------|----------|
| **10** | Excellent — Code runs end-to-end without errors. Regression coefficients, standard errors, and diagnostic plots in memo match code outputs exactly. Models are well-specified (correct FE, clustering, lag structure). No methodological mistakes. |
| **8–9** | Good — Code runs; outputs match memo. Minor inconsistencies (e.g., rounding differences, p-values off by 0.001) resolved easily. Models sound. |
| **6–7** | Satisfactory — Code runs but may require minor fixes (install packages, adjust paths). Outputs substantially match memo. Models mostly sound but may have minor issues (e.g., wrong clustering). |
| **4–5** | Weak — Code has errors or produces conflicting numbers. Figures/tables don't match memo outputs. Substantial model specification issues. |
| **0–3** | Poor — Code doesn't run or outputs are unreconcilable with memo. Major methodological flaws (e.g., no fixed effects, wrong sample). Analysis is not reproducible. |

**Grading Notes:**
- Reproducibility is non-negotiable. The memo PDFs are not graded in isolation; graders will inspect `/code/capstone_models.py` or equivalent to verify results.
- If a coefficient in the memo is 0.0061 and code produces 0.0063, that's a rounding acceptable. If code produces 0.0050, that's a reconciliation problem.
- Diagnostic plots (residuals, Q-Q plot, heteroskedasticity test) must be present in code and figures must be exported to `/results/figures/`.

---

### 2. Structure & Professional Clarity (10 points)

**Objective:** Memo is well-organized, written for a business audience (not economists), and formatted professionally.

| Points | Criteria |
|--------|----------|
| **10** | Excellent — All required sections present (Exec Summary, Methodology, Results, Conclusions, References, AI Audit). Jargon-free language; accessible to portfolio managers. Professional formatting (headers, clear typography, readable tables). No grammar/spelling errors. |
| **8–9** | Good — All sections present. Mostly jargon-free; 1–2 technical terms not explained. Professional formatting. Minor spelling/grammar. |
| **6–7** | Satisfactory — All sections present but may be thin in places (e.g., Methodology is vague on sample construction). Some unexplained jargon ("TWFE," "VIF" without definition). Formatting acceptable but tables could be cleaner. Few grammar errors. |
| **4–5** | Weak — Missing a section (e.g., no Methodology) or sections are out of order. Language is technical; assumes econometrics background. Formatting is sloppy (tables hard to read, inconsistent fonts). Grammar/spelling issues distract. |
| **0–3** | Poor — Major sections missing. Reads like econometrics textbook, not a business memo. Formatting is unprofessional (looks like copy-pasted Python output). Grammar/spelling errors throughout. |

**Grading Notes:**
- **Jargon check:** A portfolio manager with an MBA (no econometrics) should understand the memo. Avoid "two-way FE," "VIF," "treatment effect" without plain-English explanation.
- **Length requirement:** 5–7 pages. If memo is 3 pages, it's too thin (−2 pts). If it's 10 pages, it's verbose (−2 pts).
- **Tables:** Should be publication-ready (not raw Python output). Use the formatted tables you created in M3.

---

### 3. Results & Economic Interpretation (12 points)

**Objective:** Regression tables and figures are clear, interpreted correctly, and findings are translated to business impact.

| Points | Criteria |
|--------|----------|
| **12** | Excellent — Table 1 & 2 are publication-ready (clean formatting, sig stars, clear labels). Figures are high-resolution and well-captioned. Interpretations translate coefficients to economics: "A 1-unit increase in beta raises expected returns by 61 bps/month, or 7.3%/year—equivalent to a risk premium of X%." Robustness and limitations are discussed. |
| **10–11** | Good — Tables and figures present and mostly clean. Interpretations generally correct, though some coefficients lack economic translation (e.g., "0.0061 is significant" without 61 bps/year). Mentions limitations. |
| **8–9** | Satisfactory — Tables/figures present but formatting is rough (small text, unclear labels). Interpretations are present but shallow ("Beta is positive and sig"). Limited discussion of robustness. |
| **6–7** | Weak — Tables/figures present but hard to read (raw Python output, no captions). Interpretations are minimal or incorrect (e.g., "p=0.001 means high beta causes high returns" without discussing causality assumptions). No discussion of robustness. |
| **0–5** | Poor — Tables/figures missing or unintelligible. Interpretations are wrong or absent. No economic translation. |

**Grading Notes:**
- **Economic Translation:** Don't just report "β = 0.0061." Explain: "This means a REIT with 1-unit higher beta expects 61 basis points higher *monthly* return, or about 7.3% annualized—a substantial risk premium."
- **Robustness:** Memo should acknowledge (e.g., "beta is robust to outlier removal and alternative lag specifications") or caveat (e.g., "leverage effect is sensitive to sample composition and is not reliable").
- **Figures:** minimum 300 DPI; should be readable when printed in black-and-white.

---

### 4. Recommendations & Caveats (8 points)

**Objective:** Memo provides specific, actionable recommendations grounded in findings, with honest discussion of limitations.

| Points | Criteria |
|--------|----------|
| **8** | Excellent — Recommendations are specific (e.g., "Overweight Industrial REITs by 15%; underweight Retail by 10%"), directly tied to findings, and actionable (investment committee could implement them). Caveats are substantive (discusses parallel trends assumption, omitted variables, external validity) and honest about effect sizes and robustness. |
| **6–7** | Good — Recommendations are mostly specific (e.g., "Favor high-beta REITs in declining-rate environments") and tied to findings, though some may be vague. Caveats present; could be more thorough. |
| **4–5** | Satisfactory — Recommendations present but generic (e.g., "REITs are a good investment"). Caveats mentioned but superficial (e.g., "We assume the model is correct"). |
| **2–3** | Weak — Recommendations are vague ("Maybe buy REITs") or missing. Caveats are minimal or evasive (e.g., "Our analysis has limitations" with no specifics). |
| **0–1** | Poor — No recommendations or caveats. Reads like an inconclusive research report. |

**Grading Notes:**
- **Specificity:** "Overweight REITs" is vague. "Overweight Industrial REITs by 15% relative to market-cap weighting" is specific.
- **Caveats are required.** Do not gloss over limitations. Discuss:
  - Model assumptions (parallel trends, no reverse causality, etc.)
  - Omitted variables (real estate fundamentals, off-balance-sheet leverage)
  - Sample limitations (survivorship bias, monthly frequency, REIT-specific sample)
  - External validity (does this generalize? what could change?)
- **Honesty matters.** If leverage effects are fragile, *say so.* This is a strength, not weakness—it shows you understand your own limitations.

---

### 5. Individual Addendum (10 points)

**Objective:** Each team member submits a 1-page PDF with personal contribution, a defended methodological decision, and a key limitation.

| Points | Criteria |
|--------|----------|
| **10** | Excellent — Personal contribution is specific (tasks + hours per milestone, e.g., "Led M1 merge logic, 15 hrs"). Defended decision includes evidence from prior milestones (e.g., "M2 EDA showed lag-2 strongest correlation"). Key limitation is substantive (discusses a real methodological concern with why it matters). Honest tone. Exactly 1 page. |
| **8–9** | Good — Contribution is mostly specific; decision and limitation are present and mostly well-reasoned, though may lack detail. Approximately 1 page. |
| **6–7** | Satisfactory — Contribution is somewhat vague ("Helped with data analysis"). Decision/limitation present but may be trivial (e.g., "We didn't use quarterly data" without explaining why this matters). May be 0.75–1.5 pages. |
| **4–5** | Weak — Contribution is vague ("Helped with coding"). Decision/limitation poorly explained or missing. Length is off (0.5 or 2+ pages). |
| **0–3** | Poor — No specific contribution. Decision/limitation missing or insubstantial. Significantly over/under 1 page. Evasive tone (no honesty about limitations). |

**Grading Notes:**
- **Specificity is key.** "I worked on M3" → deducts points. "I implemented the FE model, ran VIF diagnostics, and tested robustness to outlier removal (18 hrs)" → full credit.
- **Evidence matters.** "I chose to use 2-month lags" is weak. "Based on M2 EDA showing r=−0.38 at lag-2 and economic reasoning about financing timelines, I advocated for including lags 1–3" is strong.
- **1-page limit is strict.** More than 1 page = difficult to read and shows lack of concision. Fewer than 0.5 pages = insufficient detail.

---

## Overall Grade Calculation

**Total: 50 points**

- Reproducibility & Rigor: **10 pts**
- Structure & Clarity: **10 pts**
- Results & Interpretation: **12 pts**
- Recommendations & Caveats: **8 pts**
- Individual Addendum: **10 pts**

**Grading Scale:**
- 45–50: A (excellent; publication-ready)
- 40–44: B (good; minor revisions needed)
- 35–39: C (satisfactory; significant revisions needed)
- 30–34: D (weak; major flaws)
- <30: F (poor; incomplete or unpublishable)

---

## Common Deductions

| Issue | Deduction |
|-------|-----------|
| Memo is <5 pages or >7 pages | −2 pts (Structure) |
| Regression tables are unformatted (raw Python output) | −3 pts (Results) |
| Figures are low-resolution (<150 DPI) or missing | −2 pts (Results) |
| No discussion of model limitations | −3 pts (Caveats) |
| Recommendations are vague ("REITs are good") | −2 pts (Recommendations) |
| Individual addendum >1 page | −2 pts (Addendum) |
| Individual contribution is non-specific | −3 pts (Addendum) |
| Code doesn't run or outputs don't match memo | −5 pts (Reproducibility) |
| Jargon not explained to business audience | −2 pts (Clarity) |
| AI Audit appendix is missing from memo | Treated as incomplete capstone documentation (per syllabus) |

---

## Submission Checklist (Final Quality Check)

Before submitting, verify:

- [ ] Team Memo (`Final_Investment_Memo.pdf`) is 5–7 pages
- [ ] All sections present: Exec Summary, Methodology, Results, Conclusions, References, AI Audit
- [ ] Tables are publication-ready (not raw Python output)
- [ ] Figures are high-resolution (300 DPI) and well-captioned
- [ ] No unexplained jargon; readable by portfolio managers without econometrics background
- [ ] Investment recommendations are specific and actionable
- [ ] Limitations and caveats are discussed honestly
- [ ] Code runs end-to-end; outputs match memo numbers
- [ ] Individual Addendum PDFs submitted for each team member (1 page each)
- [ ] Each addendum includes: contribution, defended decision, key limitation
- [ ] AI Audit appendix present in team memo
- [ ] All files submitted as PDF (not Word or Google Docs)
- [ ] Team member names on all documents
- [ ] Committed and pushed to main branch by May 1, 11:59 PM

---

## Grader Notes & Questions

**Reproducibility Check:**
- Do `capstone_models.py` or equivalent scripts run without errors?
- Do reported coefficients (to 4 decimal places) match code outputs?
- Are figures present in `/results/figures/`?

**Interpretation Check:**
- Is 61 bps translated to economic magnitude (7.3%/year)?
- Are assumptions (parallel trends, no reverse causality) stated?
- Is fragility of leverage effects acknowledged?

**Recommendation Check:**
- Are recommendations sector-specific, portfolio-specific, or scenario-specific?
- Could an investment committee act on these recommendations?
- Are trade-offs discussed (e.g., "Overweight Industrial but accept higher sector concentration")?

---

**Document Prepared by:** Dr. Cayman Seagraves  
**Date:** April 2026  
**Contact:** cayman-seagraves@utulsa.edu
