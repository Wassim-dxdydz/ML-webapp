# Soil Strength Predictor (Django)

**FR** — Application web Django pour prédire la **cohésion (c)** et l’**angle de frottement (φ)** de différentes natures de sol à partir de paramètres géotechniques.  
**EN** — Django web app to predict **cohesion (c)** and **friction angle (φ)** for several soil types from geotechnical inputs.

## ✨ Features
- UU / CU / CD prediction modes.
- Supported soils: **argile (clay)**, **limons (silt)**, **marne (marl)**, **sable (sand)** *(availability depends on the mode)*.
- Embedded, deterministic functions (no runtime training) like:
  - `predict_uu_argile`, `predict_uu_limon_marne`
  - `predict_cu_argile`, `predict_cu_limon_marne`
  - `predict_cd_argile`, `predict_cd_sable`
- Mohr circle + Coulomb envelope plot (tangent line) exported as Base64 PNG.

## 🔢 Inputs → Outputs

**Inputs** (sliders / form):
- `FC`, `WL`, `IP`, `MC`, `SR`, `ROD` (floats)

**Outputs**:
- `COH_Pred` *(kPa)*, `PHI_Pred` *(degrees)*

