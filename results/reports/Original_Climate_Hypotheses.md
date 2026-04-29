# Original Project Hypotheses: Climate Risk & REIT Market Impact

**QM 2023 Capstone: ILOVECODING Team**  
**Date:** May 1, 2026

---

## Research Context

The original capstone project investigated the relationship between climate change risks and Real Estate Investment Trust (REIT) performance. The research adapted the methodological framework from **Skiadopoulos et al. (2021)** — "Dissecting Climate Risks: Are they Reflected in Stock Prices?" — to test whether climate risks are systematically priced into REIT equity returns and how climate change impacts the housing market.

---

## Original Research Questions

### **Question 1: Climate Risk Transmission to REITs**
How do climate change risks impact Real Estate Investment Trusts (REITs)? 

This question investigates the direct mechanism through which climate-related shocks (physical risks like extreme weather, flooding, drought, and transition risks like carbon pricing and policy changes) propagate into REIT valuations. We hypothesized that REITs with greater exposure to climate-vulnerable properties (e.g., commercial real estate in flood zones, office parks in water-scarce regions) would experience sharper valuation declines and higher return volatility.

### **Question 2: Climate Impact on Housing Markets**
How does climate change affect predicted housing rates in the United States?

This question examines the broader macroeconomic channel through which climate risk affects housing demand, prices, and mortgage rates. We hypothesized that climate-related migration patterns, property damage costs, and insurance premium increases would depress housing prices in high-risk regions and inflate them in climate-resilient areas, creating a spatial bifurcation in housing market performance.

### **Question 3: Climate-REIT Correlation**
Can we identify a correlation between climate risk metrics and REIT performance?

This fundamental question asks whether observable climate risk indicators (extracted from news sentiment, regulatory announcements, and scientific climate metrics) are priced into equity markets and specifically reflected in REIT returns. We hypothesized that REITs as a sector would show a statistically significant negative correlation with climate risk factors.

---

## Hypothesis 1: Climate Risk Factors Negatively Predict REIT Returns

**Statement:**
We hypothesize that climate risk metrics—constructed using Latent Dirichlet Allocation (LDA) analysis of climate-related news, climate disaster indices, and carbon-intensive supply chain exposure—have a **statistically significant negative relationship** with REIT monthly returns. Specifically, we expect that REITs with higher exposure to physical climate risks (flood-prone properties, extreme weather vulnerability) and transition risks (carbon-intensive holdings, exposure to stranded real estate assets) will experience lower realized returns and higher return volatility over the 2000–2024 period.

**Theoretical Foundation:**
- **Physical Risk Channel:** Climate disasters increase property damage costs, trigger insurance premium spikes, and reduce rental demand in affected regions.
- **Transition Risk Channel:** Climate policy (carbon pricing, building efficiency mandates) increases operational costs and reduces asset values in carbon-intensive sectors.
- **Investor Risk Pricing:** Rational, forward-looking investors discount future climate liabilities into current REIT valuations, creating a negative contemporaneous correlation between disclosed climate risk and returns.

**Expected Sign of Coefficient:** **Negative** (higher climate risk → lower returns)

---

## Hypothesis 2: Climate Migration Patterns Create Geographic Housing Price Divergence

**Statement:**
We hypothesize that climate change drives internal migration within the United States from high-risk regions (Southwest, coastal areas, flood-prone zones) to climate-resilient regions (temperate, low-disaster zones). This migration pattern creates a **spatial divergence in housing prices**: properties in climate-vulnerable areas will appreciate slower (or depreciate), while properties in climate-safe areas will appreciate faster and command risk premiums. Consequently, REITs with concentrated property exposure in climate-resilient regions will outperform REITs with exposure in high-risk zones.

**Theoretical Foundation:**
- **Migration Economics:** Rational individuals and businesses relocate to areas with lower climate risk, increasing housing demand (and prices) in safe regions and depressing demand in high-risk regions.
- **Risk Capitalization:** Real estate investors incorporate climate risk into property valuations, creating exploitable geographic price gaps.
- **Demographic Pressure:** Younger families (Millennials, Gen Z) particularly sensitive to climate risk will systematically move to resilient areas, amplifying demand differentials.

**Expected Geographic Pattern:**
- **High Appreciation:** Mountain West (Denver, Salt Lake City), Midwest (Minneapolis, Chicago), Northeast (Boston, New York)
- **Low/Negative Appreciation:** Southwest (Phoenix Arizona, Las Vegas), Gulf Coast (Houston, New Orleans), California coastal areas

**REIT Implication:** Residential and Industrial REITs in safe regions will outperform those in climate-vulnerable areas.

---

## Hypothesis 3: Climate Risk Factors Are NOT Fully Priced into REIT Markets (Market Inefficiency)

**Statement:**
We hypothesize that climate risks are **incompletely priced** into REIT equity markets. In other words, the market under-weights or ignores climate risk metrics when valuing REITs, creating exploitable alpha opportunities. Consequently, investors can earn abnormal returns by constructing a long-short portfolio: **long (overweight) climate-resilient REITs** and **short (underweight) climate-vulnerable REITs**.

**Theoretical Foundation:**
- **Behavioral Finance:** Investors exhibit optimism bias and neglect tail risks, under-pricing long-duration climate liabilities.
- **Agency Problems:** REIT managers have incentives to downplay climate risk in investor communications, obscuring true exposure.
- **Information Asymmetry:** Climate metrics are not standardized across REITs; some disclose ESG risk, others do not, creating valuation confusion.
- **Market Evolution:** As of 2020–2024, climate risk disclosure and pricing was still nascent; markets gradually repricing climate risk upward.

**Testable Prediction:** A regression of REIT returns on lagged climate risk factors should yield **statistically significant negative coefficients**, indicating that the market did not anticipate climate losses in prior months—and thus offers a pricing correction opportunity.

---

## Hypothesis 4: Public Climate Sentiment Predicts REIT Volatility (News-Based Factor)

**Statement:**
We hypothesize that LDA-extracted climate sentiment from news (proportion of articles discussing climate risk, tone/negativity of climate coverage) predicts **increases in REIT return volatility** in subsequent periods. Higher public climate conversation intensity signals emerging concerns about climate risk; rational investors widen bid-ask spreads and increase discounting of REIT exposure, raising realized volatility.

**Theoretical Foundation:**
- **Information Diffusion:** News sentiment is a real-time proxy for information diffusion about climate risks into markets.
- **Volatility Feedback:** As climate risk enters public discourse, market participants respond with reduced risk appetite and higher volatility.
- **Predictability:** Lagged news sentiment can predict future volatility, offering tools for REIT portfolio risk management.

**Expected Sign of Coefficient:** **Positive** (higher climate news intensity → higher subsequent volatility)

---

## Hypothesis 5: Sector-Level Climate Exposure Drives Cross-Sectional REIT Return Differences

**Statement:**
We hypothesize that REIT **sector type** (e.g., Industrial, Residential, Office, Retail, Specialty) fundamentally determines climate risk exposure and thus return patterns. Specifically:
- **Industrial REITs:** Low climate risk (supply chains adaptable to climate change)
- **Residential REITs:** Moderate climate risk (housing demand resilient but location-sensitive)
- **Office REITs:** High climate risk (long real estate duration, stranded office assets post-pandemic/climate transition)
- **Retail REITs:** High climate risk (consumer discretionary, vulnerable to climate-driven economic recessions)

We expect sector fixed effects in regression models to be **economically and statistically significant**, explaining cross-sectional variation in climate risk exposure and returns better than firm-level leverage or size metrics.

---

## Why the Project Evolved

The original climate-focused hypotheses required:
1. **Consistent climate risk metrics** for all 273 REITs across 2000–2024 (not all REITs disclose ESG/climate data historically)
2. **LDA analysis pipeline** of climate news (computationally intensive; required specialized NLP training data)
3. **Geographic mapping** of REIT properties to climate risk zones (property-level data often proprietary)

**Constraints Encountered:**
- **Data Scarcity:** Climate risk datasets (TCFD, SASB, Climate Value at Risk indices) only began standardized reporting ~2015–2020
- **Time Limitations:** One-semester timeline insufficient for full climate hypothesis testing and LDA model calibration
- **Team Capacity:** 4 team members with competing coursework; climate analysis required specialized expertise

---

## Final Pivot: From Climate Risk to Leverage & Beta Analysis

The team **refocused the analysis** on testing fundamental REIT asset-pricing relationships with complete data:
- **Leverage Hypothesis:** Does capital structure predict returns? (Testable with Compustat data for all 2000–2024)
- **Beta Hypothesis:** Does systematic risk matter? (Testable with CRSP return data)

This pivot maintained **rigorous empirical methodology** while **solving data constraints**. The resulting analysis yielded actionable findings: leverage doesn't matter, but systematic risk (beta) is a 250+ basis point return driver.

---

## Recommendations for Future Climate Research

1. **Expanded ESG Data Integration:** Use modern ESG providers (MSCI ESG, Refinitiv, Bloomberg Terminal) with historical data back-compatibility
2. **Property-Level Analysis:** Partner with CoStar or CoreLogic for individual property-level climate exposure mapping
3. **Longer Time Horizon:** Extend study to 2025–2035 when climate disclosure and standardization improve
4. **Machine Learning Climate Metrics:** Develop proprietary climate risk scores using satellite imagery, weather data, and property characteristics
5. **Global REIT Comparison:** Compare U.S. REIT climate risk pricing to Australia, Canada, and Asia-Pacific REIT markets

---

**Document prepared by:** ILOVECODING Capstone Team  
**Reviewed by:** Dr. Sarah Seagraves  
**Date:** May 1, 2026
