# Milestone 4: Implementation Checklist & Setup Guide

**QM 2023 Capstone — Final Investment Memo (M4)**  
**Due Date:** Friday, May 1, 2026 by 11:59 PM  
**Status:** [SETUP COMPLETE] Ready for team to begin writing

---

## Files Created & Ready to Use

### Templates & Guides (in `results/reports/`)
- ✅ **memo_template.md** — Full template with all required sections, examples, and guidance
- ✅ **individual_addendum_template.md** — Individual contribution + decision + limitation template
- ✅ **Final_Investment_Memo_DRAFT.md** — Starter memo with partial content (team fills in remaining)
- ✅ **INDIVIDUAL_ADDENDUM_TEMPLATE_StartingPoint.md** — Starter template for each team member

### Rubric & Documentation (in `results/documentation/`)
- ✅ **M4_RUBRIC.md** — Complete grading rubric (50 points) with evaluation criteria

### Supporting Assets (from M3)
- ✅ **Regression tables:** `results/tables/M3_REGRESSION_TABLE_FORMATTED.csv` and `.xlsx` (publication-ready)
- ✅ **Diagnostic plots:** `results/figures/M3_residuals_diagnostics.png` and others
- ✅ **Findings report:** `results/reports/M3_findings_report.md` (source material for memo)

---

## Deliverables Checklist

### Team Memo: Final_Investment_Memo.pdf (40 points)

**Format & Structure:**
- [ ] 5–7 pages (not shorter, not longer)
- [ ] Professional PDF (use Markdown PDF extension or pandoc conversion)
- [ ] All sections present with appropriate length:
  - [ ] Executive Summary (0.5 page)
  - [ ] Methodology (1 page)
  - [ ] Results (1.5–2 pages)
  - [ ] Conclusions & Recommendations (1 page)
  - [ ] References (0.5 page)
  - [ ] Appendix: AI Audit (0.5–1 page)

**Content Requirements:**
- [ ] Executive Summary: Key finding(s) with magnitude and significance (e.g., "61 bps premium per unit beta")
- [ ] Executive Summary: Specific investment recommendation (e.g., "Overweight Industrial by 15%")
- [ ] Methodology: Data sources with citations/URLs
- [ ] Methodology: Sample construction (N, date range, observations after cleaning)
- [ ] Methodology: Model equations with all variable definitions
- [ ] Results: Table 1 (Fixed Effects regression) — publication-ready formatting
- [ ] Results: Table 2 (Alternative spec or DiD model) — publication-ready formatting
- [ ] Results: Figure 1 (Key visualization) — high-resolution (300 DPI), well-captioned
- [ ] Results: Figure 2 (Diagnostic plot) — high-resolution, well-captioned
- [ ] Results: Prose interpretation translating coefficients to economics
- [ ] Conclusions: Sector/factor recommendations with specifics (not vague)
- [ ] Conclusions: Risk assessment and model assumption discussion
- [ ] Conclusions: Honest caveats (limitations, omitted variables, external validity)
- [ ] References: Data sources + academic citations (APA format)
- [ ] AI Audit: Summary of AI use across milestones with verification notes

**Writing Standards:**
- [ ] Jargon-free language; accessible to non-econometricians
- [ ] No unexplained acronyms (define "FE," "VIF," "TWFE" on first use)
- [ ] Professional formatting (headers, consistent fonts, readable tables)
- [ ] No grammar or spelling errors
- [ ] Coefficients translated to business impact (not just p-values)

---

### Individual Addendum: Individual_Addendum_[YourName].pdf (10 points per person)

**Required for each team member:**

**Format & Structure:**
- [ ] Exactly 1 page (not 0.5, not 1.5)
- [ ] PDF format
- [ ] Team member's name and date on document

**Content (must be completed by each individual):**
- [ ] Personal Contribution (2–4 bullets with tasks + hours per milestone)
  - [ ] M1 specific contribution (e.g., "Led data merge logic, 15 hrs")
  - [ ] M2 specific contribution (e.g., "Created lag-correlation heatmaps, 12 hrs")
  - [ ] M3 specific contribution (e.g., "Implemented FE model, 18 hrs")
  - [ ] M4 specific contribution (e.g., "Drafted Executive Summary, 10 hrs")
- [ ] One Defended Decision (2–4 sentences with evidence)
  - [ ] State the decision clearly
  - [ ] Provide evidence from prior milestone analysis (M2 EDA, M3 robustness, etc.)
  - [ ] Explain economic/methodological reasoning
- [ ] One Key Limitation (2–4 sentences explaining impact)
  - [ ] Must be substantive (not trivial)
  - [ ] Explain why it matters for conclusions
  - [ ] Discuss potential bias or external validity concern
- [ ] AI Audit Notes (if applicable)
  - [ ] Task + prompt + output + verification + changes
  - [ ] Leave blank if you didn't use AI

---

## Step-by-Step Team Workflow

### Phase 1: Planning (April 21–22, 2026)

1. **Read the requirements:** Team members read `README (2).pdf` and this checklist
2. **Review templates:** Familiarize with `memo_template.md` and `individual_addendum_template.md`
3. **Check existing assets:** Verify M3 regression tables, diagnostic plots, and findings report are correct and match memo needs
4. **Assign sections:** Each team member claims responsibility for one memo section + their individual addendum
5. **Decide on figures:** Choose Figure 1 (key visualization) and verify Figure 2 (diagnostics) from M3

**Example task assignment:**
- Ashley: Executive Summary + Methodology + Final review
- Aniya: Results (Tables) + Economic interpretation
- Yuri: Results (Figures) + Conclusions & Recommendations
- Olivia: References + AI Audit appendix + PDF conversion
- All: Individual Addendum (each person writes their own)

### Phase 2: First Draft (April 23–24, 2026)

1. **Start with `Final_Investment_Memo_DRAFT.md`** (already has structure and partial content)
2. **Each person writes their assigned section** using `memo_template.md` as a guide
3. **Insert actual tables and figures** from `/results/tables/` and `/results/figures/`
4. **Write for business audience:** No jargon; translate econometric results to dollars/percentages/actions
5. **Draft individual addendums:** Each team member completes `INDIVIDUAL_ADDENDUM_TEMPLATE_StartingPoint.md`

**Drafting Checklist:**
- [ ] Define all variables in plain English (not "driver_lag1" but "Lagged leverage")
- [ ] Translate coefficients (not just "p<0.001" but "61 basis points, or 7.3% annualized")
- [ ] Cap recommendations at sector level or portfolio allocation level (specific, not vague)
- [ ] List assumptions transparently (parallel trends, no reverse causality, etc.)

### Phase 3: Review & Revision (April 25–29, 2026)

1. **Team review round 1:** Ashley (lead) reviews full memo for:
   - Length (is it 5–7 pages?)
   - Consistency (do sections tell coherent story?)
   - Jargon (can a non-economist understand it?)
   - Technical accuracy (do numbers match M3 code outputs?)

2. **Technical verification:**
   - Spot-check 3–4 regression coefficients against M3 output (results/tables/)
   - Verify figure resolution (open PDF, print-test if available)
   - Confirm all references and citations are present

3. **Peer review:** Each section author gets feedback from teammate not assigned to that section

4. **Individual addenda review:** Each person proofreads and gets peer feedback

5. **Revise:** Address feedback; finalize memo content

### Phase 4: Finalization (April 30, 2026)

1. **Convert memo Markdown to PDF:**
   - **Option A (VS Code):** Install "Markdown PDF" extension → right-click .md → "Export (pdf)"
   - **Option B (Pandoc):** `pandoc Final_Investment_Memo_DRAFT.md -o Final_Investment_Memo.pdf`
   - **Option C (Browser):** Open rendered .md in GitHub → Print → Save as PDF
   - **Option D (Google Docs):** Copy .md → open in Google Docs → File → Download as PDF

2. **Finalize file names:**
   - Team memo: `Final_Investment_Memo.pdf` (exact name required)
   - Individual addenda: `Individual_Addendum_[YourName].pdf` for each member (e.g., `Individual_Addendum_Ashley.pdf`)

3. **Final quality check:**
   - [ ] All sections present and appropriate length
   - [ ] Tables and figures properly formatted
   - [ ] No typos or grammar errors
   - [ ] Team names on both memo and addenda
   - [ ] AI Audit appendix included in memo
   - [ ] All files are PDFs (not Word, not markdown)

4. **Git commit & push to main:**
   ```bash
   git add Final_Investment_Memo.pdf Individual_Addendum_*.pdf
   git commit -m "M4: Submit Final Investment Memo and Individual Addenda"
   git push origin main
   ```

### Phase 5: Submission (April 30 End-of-Day or May 1 by 11:59 PM)

- [ ] Verify files are visible on GitHub (push was successful)
- [ ] Check that commit is on main branch (not Ashley's-Branch)
- [ ] Double-check file names match requirements:
  - `Final_Investment_Memo.pdf` ✓
  - `Individual_Addendum_[Name].pdf` for each person ✓

---

## Key Writing Tips

### For Business Audience (Non-Economists)

**DON'T SAY:**
- "We estimated a two-way FE panel regression with clustered standard errors"
- "The coefficient is 0.0061 and is significant at the 1% level"
- "Leverage has a negative coefficient in the outlier-free sample"

**DO SAY:**
- "We analyzed 34,121 monthly REIT observations to identify return drivers"
- "A REIT with higher systematic risk (beta) generates 61 extra basis points of return per month"
- "Our main findings about leverage don't hold up under closer scrutiny, so we don't recommend trading on it"

### For Specific Recommendations

**DON'T SAY:**
- "REITs are a good investment"
- "Consider increasing REIT exposure"
- "Beta is important"

**DO SAY:**
- "Overweight Industrial REITs by 15% relative to market-cap weighting; underweight Retail by 10%; maintain Residential at benchmark"
- "When the Fed signals rate cuts, tilt 60% to high-beta REITs (beta > 1.2) and 40% to low-beta REITs (beta < 0.8); reverse in rate-hiking cycles"
- "Adjust REIT beta exposure based on interest rate outlook: higher beta in declining-rate environments, lower beta when rates are rising"

### For Honest Caveats

**DO:**
- "Our analysis assumes X, which may be violated if Y happens"
- "We find no evidence that leverage predicts returns, but this could reflect measurement error or hedging we don't observe"
- "These results are specific to REITs 2000–2024; they may not hold in other sectors or time periods"

**DON'T:**
- "Our model has limitations" (too vague)
- "Future results may differ" (not substantive)
- "External validity is a concern" (no specifics)

---

## Common Pitfalls to Avoid

| Pitfall | How to Avoid |
|---------|-------------|
| **Memo is too technical** | Have a non-data person read draft; ask "Can you explain this to your parents?" If answer is no, rewrite. |
| **No investment recommendations** | Memo must end with "We recommend X." Quantify it (%, sector, scenario). |
| **Ignoring limitations** | Dedicate 1/4 of Conclusions to honest caveats. Be specific: "Parallel trends may be violated if..." |
| **Vague individual addendum** | Include hours. Be specific: "I implemented Model A... (18 hrs)" not "I helped with analysis." |
| **Tables are unreadable** | Don't copy-paste Python output. Use results/tables/M3_REGRESSION_TABLE_FORMATTED.csv and format in Excel or Markdown. |
| **Figures are blurry** | Export at 300 DPI. Test by opening PDF and zooming in—text should be readable. |
| **Missing AI Audit** | Appendix is required per syllabus. Omission is treated as incomplete capstone documentation. |
| **Wrong file format** | Submit PDF only, not Word, Google Docs, or markdown. |

---

## Submission Checklist (Final)

Before pushing to GitHub:

**Team Memo:**
- [ ] Filename: `Final_Investment_Memo.pdf` (exact)
- [ ] Format: PDF (not Word, not markdown)
- [ ] Length: 5–7 pages
- [ ] All sections present: Exec Summary, Methodology, Results, Conclusions, References, AI Audit
- [ ] Tables formatted (not raw Python output)
- [ ] Figures high-resolution (300 DPI) and captioned
- [ ] No unexplained jargon
- [ ] Recommendations specific and actionable
- [ ] Caveats honest and substantive
- [ ] Team member names at top

**Individual Addenda (each person):**
- [ ] Filename: `Individual_Addendum_[Name].pdf` (exact)
- [ ] Format: PDF
- [ ] Length: Exactly 1 page
- [ ] Contribution: Specific tasks + hours per milestone
- [ ] Defended decision: With evidence from prior work
- [ ] Key limitation: Substantive, explains impact
- [ ] Name and date on document

**Git & Submission:**
- [ ] All files added: `git add Final_Investment_Memo.pdf Individual_Addendum_*.pdf`
- [ ] Committed with clear message: `git commit -m "M4: Submit Final Investment Memo and Individual Addenda"`
- [ ] Pushed to main: `git push origin main`
- [ ] Visible on GitHub under main branch

---

## Resources & Support

**Templates (in repo):**
- `results/reports/memo_template.md` — Full guidance
- `results/reports/individual_addendum_template.md` — Full individual addendum template
- `results/documentation/M4_RUBRIC.md` — Grading rubric & feedback criteria

**Existing Assets (from M3):**
- `results/tables/M3_REGRESSION_TABLE_FORMATTED.csv` and `.xlsx` — Use directly in memo
- `results/figures/M3_residuals_diagnostics.png` — Use for diagnostic plot
- `results/reports/M3_findings_report.md` — Source material; plagiarize interpretations

**Writing Guides:**
- Strunk & White, *Elements of Style* (concise, clear writing)
- Williams & Colomb, *Style: Lessons in Clarity and Grace* (professional prose)

**Office Hours:**
- Dr. Seagraves: Monday & Wednesday, 3:00–5:00 PM
- Topics: Memo writing, investment recommendations, limitation discussions

---

## Timeline Summary

| Date | Task | Milestone |
|------|------|-----------|
| **April 21–22** | Read requirements; plan assignments | Planning |
| **April 23–24** | Write first drafts of memo sections | First Draft |
| **April 25–29** | Review, revise, finalize content | Revision |
| **April 30** | Convert to PDF; final proofread; commit to main | Finalization |
| **May 1 by 11:59 PM** | Deadline (push to main if not already done) | **Submission** |
| **May 1 or May 4** | Final presentations (see schedule) | Presentation |

---

## Next Steps (What to Do Now)

1. **Team meeting:** Review this checklist as a group (30 min)
2. **Assign sections:** Each person picks memo section + individual addendum (10 min)
3. **Start drafting:** Begin with memo_template.md and Final_Investment_Memo_DRAFT.md (by April 23)
4. **Verify assets:** Check that M3 tables/figures match what you'll use in memo
5. **Questions?** Post in team Slack or attend office hours

---

**Good luck!** Your memo is the capstone of a semester of rigorous analysis. Show your clear thinking, honest limitations, and actionable insights.

---

**Document Prepared:** April 21, 2026  
**Contact:** Dr. Cayman Seagraves (cayman-seagraves@utulsa.edu)  
**Questions or Clarifications?** Reach out during office hours or via email.
