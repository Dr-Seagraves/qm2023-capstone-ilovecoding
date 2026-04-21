# Milestone 4 — Complete Setup & Next Steps

**Status:** ✅ READY FOR TEAM TO BEGIN WRITING  
**Due Date:** Friday, May 1, 2026 by 11:59 PM  
**Format:** PDF (Team Memo + Individual Addenda)  
**Points:** 50 (25% of capstone grade)

---

## What's Ready for You

### 📋 Start Here (READ FIRST)

1. **[M4_IMPLEMENTATION_CHECKLIST.md](results/documentation/M4_IMPLEMENTATION_CHECKLIST.md)** ⭐
   - Complete workflow from planning through submission
   - File checklist, phased timeline (April 21–May 1)
   - Writing tips and common pitfalls to avoid
   - **Read this first; use it to organize your team's work**

2. **[README (2).pdf](README%20(2).pdf)** (Official assignment from Dr. Seagraves)
   - Full M4 requirements and overview
   - Learning objectives, deliverables, grading info

### 📝 Writing Templates (Fill These In)

In `results/reports/`:

1. **[Final_Investment_Memo_DRAFT.md](results/reports/Final_Investment_Memo_DRAFT.md)** ← **START HERE**
   - Partial draft with skeleton and some filled-in content
   - Team fills in remaining sections
   - Convert to PDF when complete

2. **[memo_template.md](results/reports/memo_template.md)** ← Use for detailed guidance
   - Full template showing all required sections
   - Examples and explanations
   - Reference when drafting each section

3. **[individual_addendum_template.md](results/reports/individual_addendum_template.md)** ← Use for guidance
   - Detailed template showing what to include
   - Examples of good vs. weak contributions/decisions/limitations

4. **[INDIVIDUAL_ADDENDUM_TEMPLATE_StartingPoint.md](results/reports/INDIVIDUAL_ADDENDUM_TEMPLATE_StartingPoint.md)** ← Each person fills one in
   - Simple starting template (less detail than full template)
   - Each team member creates: `Individual_Addendum_[YourName].md`

### 📊 Supporting Assets (Already Created)

From Milestones 1–3, use these in your memo:

- **Regression Tables:** [results/tables/M3_REGRESSION_TABLE_FORMATTED.csv](results/tables/M3_REGRESSION_TABLE_FORMATTED.csv) or .xlsx
  - Publication-ready formatting (coefficient, SE, p-value, F-stat, etc.)
  - Copy directly into memo Table 1 & Table 2

- **Diagnostic Plots:** [results/figures/M3_residuals_diagnostics.png](results/figures/M3_residuals_diagnostics.png) and others
  - Use for Figure 2 (diagnostic plot)
  - Choose Figure 1 from other available visualizations

- **Findings Report:** [results/reports/M3_findings_report.md](results/reports/M3_findings_report.md)
  - Source material for memo content
  - Interpretation guidance and robustness discussion

- **Model Code:** [code/capstone_models.py](code/capstone_models.py)
  - For reproducibility verification
  - Graders will verify memo numbers match code outputs

### 📖 Rubric & Grading Criteria

- **[M4_RUBRIC.md](results/documentation/M4_RUBRIC.md)** — Full grading rubric
  - 5 components (Reproducibility 10pt, Structure 10pt, Results 12pt, Recommendations 8pt, Individual 10pt)
  - Detailed criteria for each point level
  - Common deductions (e.g., vague recommendations, unformatted tables)
  - **Read this to understand what graders are looking for**

---

## Workflow: Next Steps

### Phase 1: Planning (April 21–22) — **Do This First**

- [ ] **Team meeting:** Read the checklist together (30 min)
- [ ] **Review requirements:** Skim README (2).pdf and M4_IMPLEMENTATION_CHECKLIST.md
- [ ] **Assign roles:** Decide who writes which memo section + reviews
- [ ] **Verify assets:** Check that regression tables and figures exist and are correct

### Phase 2: Draft (April 23–24)

- [ ] **Open [Final_Investment_Memo_DRAFT.md](results/reports/Final_Investment_Memo_DRAFT.md)** — This is your starting file
- [ ] **Each person writes their assigned section:**
  - **Executive Summary:** Key finding + recommendation (2–3 sentences each)
  - **Methodology:** Data sources, sample construction, model equations
  - **Results:** Interpret tables/figures; translate to business impact
  - **Conclusions:** Specific recommendations + caveats
  - **References & AI Audit:** Complete these
- [ ] **Each person starts their [Individual_Addendum_[Name].md](results/reports/INDIVIDUAL_ADDENDUM_TEMPLATE_StartingPoint.md)**

### Phase 3: Review & Revise (April 25–29)

- [ ] **Spot-check numbers:** Do coefficients in memo match M3 code outputs?
- [ ] **Read for jargon:** Can a portfolio manager (with MBA, no econometrics) understand it?
- [ ] **Check tables:** Are they formatted well? Not raw Python output?
- [ ] **Check figures:** Are they high-resolution and captioned?
- [ ] **Verify recommendations:** Are they specific? Actionable? Not vague?
- [ ] **Peer review:** Each section gets read by a teammate not assigned to it

### Phase 4: Finalize & Convert (April 30)

- [ ] **Resolve all review comments**
- [ ] **Convert Markdown to PDF:**
  - VS Code: Markdown PDF extension
  - Command line: `pandoc Final_Investment_Memo_DRAFT.md -o Final_Investment_Memo.pdf`
  - Google Docs or Word: Copy content → Download as PDF
- [ ] **Rename files to exact requirements:**
  - `Final_Investment_Memo.pdf` (team memo)
  - `Individual_Addendum_Ashley.pdf`, `Individual_Addendum_Aniya.pdf`, etc.

### Phase 5: Submit (May 1 by 11:59 PM)

- [ ] **Git commit:**
  ```bash
  git add Final_Investment_Memo.pdf Individual_Addendum_*.pdf
  git commit -m "M4: Submit Final Investment Memo and Individual Addenda"
  git push origin main
  ```
- [ ] **Verify on GitHub:** Files visible on main branch? No errors in push?

---

## File Organization Reference

```
qm2023-capstone-ilovecoding/
├── README (2).pdf                          ← Official M4 assignment
├── code/
│   └── capstone_models.py                  ← M3 model (for reproducibility)
├── results/
│   ├── figures/
│   │   └── M3_residuals_diagnostics.png   ← Use for Figure 2
│   ├── tables/
│   │   └── M3_REGRESSION_TABLE_FORMATTED.{csv,xlsx}  ← Use for Tables 1 & 2
│   ├── reports/
│   │   ├── M3_findings_report.md          ← Source for interpretations
│   │   ├── memo_template.md               ← Full template (reference)
│   │   ├── Final_Investment_Memo_DRAFT.md ← FILL THIS IN & convert to PDF
│   │   ├── individual_addendum_template.md ← Full template (reference)
│   │   └── INDIVIDUAL_ADDENDUM_TEMPLATE_StartingPoint.md ← Each person fills one
│   └── documentation/
│       ├── README.md                       ← This file (navigation)
│       ├── M4_IMPLEMENTATION_CHECKLIST.md ← Detailed workflow guide ⭐
│       └── M4_RUBRIC.md                    ← Grading rubric
└── [To be created]
    ├── Final_Investment_Memo.pdf          ← Team deliverable
    ├── Individual_Addendum_Ashley.pdf     ← Individual deliverables
    ├── Individual_Addendum_Aniya.pdf
    ├── Individual_Addendum_Olivia.pdf
    └── Individual_Addendum_Yuri.pdf
```

---

## Key Deadlines

| Date | Task | Status |
|------|------|--------|
| April 21 | Setup complete; templates ready | ✅ DONE |
| April 21–22 | Team planning meeting | → **DO THIS NOW** |
| April 23–24 | Write first drafts | → Next |
| April 25–29 | Review and revise | → Next |
| April 30 | Convert to PDF; final check | → Next |
| **May 1, 11:59 PM** | **DEADLINE** | → Final |

---

## Quick Links to Key Documents

| Document | Purpose | Location |
|----------|---------|----------|
| **M4_IMPLEMENTATION_CHECKLIST** | Step-by-step workflow & timeline | results/documentation/ |
| **M4_RUBRIC** | Grading criteria (read to know what you'll be evaluated on) | results/documentation/ |
| **Final_Investment_Memo_DRAFT** | FILL THIS IN and convert to PDF | results/reports/ |
| **memo_template** | Reference for writing quality memo sections | results/reports/ |
| **M3_REGRESSION_TABLE_FORMATTED** | Copy into memo as Tables 1 & 2 | results/tables/ |
| **M3_findings_report** | Source material for interpretations | results/reports/ |

---

## Success Criteria Summary

✅ **Team Memo (Final_Investment_Memo.pdf)**
- 5–7 pages, professional PDF
- All 6 sections present (Exec Summary, Methodology, Results, Conclusions, References, AI Audit)
- Tables/figures publication-ready
- No jargon or well-explained
- Specific, actionable investment recommendations
- Honest discussion of limitations
- Reproducible from M1–M3 code outputs

✅ **Individual Addendum (per person, PDF)**
- 1 page per person
- Specific personal contribution (tasks + hours per milestone)
- One defended methodological decision (with evidence)
- One substantive key limitation
- Optional: AI audit notes if applicable

✅ **Submission**
- Both files committed to main branch by 11:59 PM May 1
- Exact filenames: `Final_Investment_Memo.pdf` + `Individual_Addendum_[Name].pdf`

---

## Need Help?

- **Workflow questions?** → Read M4_IMPLEMENTATION_CHECKLIST.md
- **Writing questions?** → Reference memo_template.md
- **Structure questions?** → Check M4_RUBRIC.md for what's graded
- **Office hours:** Dr. Seagraves, Monday & Wednesday, 3:00–5:00 PM

---

**Ready to get started?**

👉 **Step 1:** Open [M4_IMPLEMENTATION_CHECKLIST.md](results/documentation/M4_IMPLEMENTATION_CHECKLIST.md) and read "Phase 1: Planning"

👉 **Step 2:** Schedule your team's planning meeting for April 21–22

👉 **Step 3:** Assign roles and start your draft using [Final_Investment_Memo_DRAFT.md](results/reports/Final_Investment_Memo_DRAFT.md)

Good luck! 🎯

---

*Last Updated: April 21, 2026*  
*Prepared for: Team ILOVECODING*
