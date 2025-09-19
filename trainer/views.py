from django.shortcuts import render
from .utils.soil_predictor_origin import (
    predict_uu_argile,
    predict_uu_limon_marne,
    predict_cu_argile,
    predict_cu_limon_marne,
    predict_cd_argile,
    predict_cd_sable,
)

# --- NEW: plotting helper ---
import io, base64
import numpy as np
import matplotlib
matplotlib.use("Agg")  # headless backend for servers
import matplotlib.pyplot as plt


def make_mohr_base64(coh_kpa: float, phi_deg: float,
                     sigma1: float = 150.0, sigma3: float = 50.0) -> str:
    """Return a base64 PNG of Mohr circle"""
    phi = np.radians(phi_deg)
    centre = (sigma1 + sigma3) / 2.0
    rayon  = (sigma1 - sigma3) / 2.0

    # Demi-cercle de Mohr
    theta = np.linspace(0, np.pi, 300)
    sigma = centre + rayon * np.cos(theta)
    tau   = rayon * np.sin(theta)

    # Slope (tan φ) and the unique tangent intercept c_tan
    m = np.tan(phi)
    c_tan = rayon * np.sqrt(1 + m**2) - m * centre  # = R secφ - σm tanφ

    # Courbe de la droite tangente
    sigma_line = np.linspace(0, sigma1 * 1.2, 300)
    tau_line   = c_tan + m * sigma_line

    fig = plt.figure(figsize=(5, 3))
    ax = plt.gca()
    ax.plot(sigma, tau, label="Cercle de Mohr")
    ax.plot(sigma_line, tau_line, "--", color="#ff6f00",
            label=f"τ = c + σ·tan(φ)\n(c_tan={c_tan:.2f} kPa, φ={phi_deg:.1f}°)")

    ax.axhline(0, linewidth=0.8, color="black")
    ax.axvline(0, linewidth=0.8, color="black")
    ax.set_xlabel("Contrainte normale σ (kPa)")
    ax.set_ylabel("Contrainte tangentielle τ (kPa)")
    ax.set_title("Demi-cercle de Mohr et enveloppe de Coulomb")
    ax.legend()
    ax.grid(True)
    fig.tight_layout()

    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=160)
    plt.close(fig)
    return base64.b64encode(buf.getvalue()).decode("ascii")


def index(request):
    results = None
    mohr_plot = None
    prev = None  # <-- remember last inputs

    if request.method == 'POST':
        soil   = request.POST.get("soil_type") or ''
        target = request.POST.get("target_type") or ''
        try:
            FC  = float(request.POST.get("FC"))
            WL  = float(request.POST.get("WL"))
            IP  = float(request.POST.get("Ip"))   # keep "Ip" (name in the form)
            MC  = float(request.POST.get("MC"))
            SRv = request.POST.get("SR")
            SR  = float(SRv) if SRv else 0.0
            ROD = float(request.POST.get("ROD"))

            # save what the user entered (so sliders/selects don’t reset)
            prev = {
                "soil": soil, "target": target,
                "FC": FC, "WL": WL, "IP": IP, "MC": MC, "SR": SR, "ROD": ROD,
            }

            # Optional: custom sigmas for the Mohr circle
            try:
                sigma1 = float(request.POST.get("sigma1")) if request.POST.get("sigma1") else 150.0
                sigma3 = float(request.POST.get("sigma3")) if request.POST.get("sigma3") else 50.0
            except Exception:
                sigma1, sigma3 = 150.0, 50.0

            # --- prediction dispatch ---
            if target == "uu":
                if soil == "argile":
                    coh, phi = predict_uu_argile(FC, WL, IP, MC, SR, ROD)
                else:
                    coh, phi = predict_uu_limon_marne(FC, WL, IP, MC, SR, ROD)

            elif target == "cu":
                if soil == "argile":
                    coh, phi = predict_cu_argile(FC, WL, IP, MC, SR, ROD)
                else:
                    coh, phi = predict_cu_limon_marne(FC, WL, IP, MC, SR, ROD)

            elif target == "cd":
                if soil == "argile":
                    coh, phi = predict_cd_argile(FC, WL, IP, MC, SR, ROD)
                elif soil == "sable":
                    coh, phi = predict_cd_sable(FC, WL, IP, MC, SR, ROD)
                else:
                    coh = phi = None
            else:
                coh = phi = None

            if coh is not None and phi is not None:
                results = {
                    'coh': coh,
                    'phi': phi,
                    'soil': soil,
                    'target': target,
                    'vector': {'FC': FC, 'WL': WL, 'IP': IP, 'MC': MC, 'SR': SR, 'ROD': ROD},
                }
                mohr_plot = make_mohr_base64(coh, phi, sigma1=sigma1, sigma3=sigma3)

        except Exception as e:
            print("Erreur de traitement :", e)
            # even on error, keep raw posted values so UI doesn’t reset
            prev = {
                "soil": soil, "target": target,
                "FC": request.POST.get("FC"),
                "WL": request.POST.get("WL"),
                "IP": request.POST.get("Ip"),
                "MC": request.POST.get("MC"),
                "SR": request.POST.get("SR"),
                "ROD": request.POST.get("ROD"),
            }

    return render(request, 'trainer/index.html', {
        'results': results,
        'mohr_plot': mohr_plot,
        'prev': prev,          # <-- pass to template
    })
