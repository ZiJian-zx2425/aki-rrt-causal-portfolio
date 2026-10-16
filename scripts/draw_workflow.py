"""Draw the public methods schematic from text and shapes only."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

ROOT = Path(__file__).resolve().parents[1]
NAVY, TEAL, AMBER, INK = "#152D45", "#087F8C", "#B56B22", "#23364A"
plt.rcParams.update({"font.family": "DejaVu Sans", "svg.fonttype": "none"})
fig, ax = plt.subplots(figsize=(16, 10))
fig.patch.set_facecolor("#F5F7FB")
ax.set(xlim=(0, 1600), ylim=(1000, 0))
ax.axis("off")


def text(x, y, s, size=13, color=INK, weight="normal", **kwargs):
    ax.text(x, y, s, fontsize=size, color=color, weight=weight, va="top", **kwargs)


def box(x, y, w, h, title, body, color=TEAL):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=12",
                              facecolor="white", edgecolor="#DCE3ED", linewidth=1))
    ax.plot([x + 16, x + 16], [y + 22, y + h - 22], color=color, lw=3)
    text(x + 32, y + 22, title, 13, color, "bold")
    text(x + 32, y + 58, body, 10.5, linespacing=1.65)


def arrow(x1, y1, x2, y2, color="#728296"):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>",
                                mutation_scale=15, color=color, lw=1.5))


text(45, 30, "RRT TIMING IN SEVERE AKI", 11, TEAL, "bold")
text(45, 65, "Target trial design & causal machine learning", 25, NAVY, "bold")
text(45, 115, "A course-project methods portfolio with an independent synthetic implementation", 13)

text(45, 175, "01  CLINICAL DESIGN", 12, NAVY, "bold")
text(450, 175, "Documented intent; full clinical emulation remains unverified", 11, "#63748A")
box(45, 210, 465, 155, "Define the decision", "Incident stage 3 AKI in hospitalized adults\nEligibility and baseline covariates at time zero\nOutcome: 30-day all-cause mortality", NAVY)
box(565, 210, 465, 155, "Specify the strategies", "Initiate within 24 h vs no initiation in 24 h\nComparator allows later or no RRT\n72 h window = alternative protocol", NAVY)
box(1085, 210, 465, 155, "Resolve timing & ascertainment", "Align eligibility, assignment and follow-up\nValidate grace-period and censoring rules\nConfirm post-discharge outcome capture", NAVY)
arrow(514, 287, 560, 287); arrow(1034, 287, 1080, 287)

text(45, 405, "02  PUBLIC EXECUTABLE DEMO", 12, TEAL, "bold")
text(570, 405, "Baseline treatment at t = 0; no clinical treatment window", 11, "#63748A")
box(45, 440, 340, 190, "Generate", "Independent mathematical distributions\nMeasured baseline confounding\nKnown potential-outcome risks\nFixed seed; no clinical data")
box(435, 440, 340, 190, "Estimate", "Cross-fitted propensity + outcome fits\nIPW and explicit AIPW\nWeighted Cox working model\nOptional CausalForestDML")
box(825, 440, 340, 190, "Diagnose", "Overlap and covariate balance\nEffective sample size + weight tails\nClipping / weight-cap sensitivity\nWeighted survival point estimates")
box(1215, 440, 335, 190, "Verify", "Compare with known synthetic truth\nTest double robustness\nReject temporal boundary errors\nRecord seed and environment")
for x in [390, 780, 1170]: arrow(x, 535, x + 40, 535, TEAL)

text(45, 675, "03  RESEARCH EXTENSION", 12, AMBER, "bold")
text(470, 675, "Proposed; not implemented in the public demo", 11, "#63748A")
box(45, 710, 725, 135, "Grace-period-aware strategy comparison", "Specify within-window treatment and rescue rules; consider clone–censor–weight.\nModel longitudinal history, artificial censoring, and observation censoring.", AMBER)
box(825, 710, 725, 135, "Validate before stronger causal claims", "Audit timestamp resolution, indication bias, positivity, and outcome completeness.\nReproduce only inside an authorized research environment.", AMBER)
arrow(775, 778, 820, 778, AMBER)

ax.add_patch(FancyBboxPatch((45, 890), 1505, 73, boxstyle="round,pad=0,rounding_size=12",
                          facecolor=NAVY, edgecolor=NAVY))
text(68, 910, "PUBLIC RELEASE", 12, "#7BE0D6", "bold")
text(310, 910, "New code + methods + synthetic aggregates only  |  No patient data or clinical results", 12, "white")
fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
for ext in ["png", "svg"]:
    fig.savefig(ROOT / "figures" / f"workflow.{ext}", dpi=180, facecolor=fig.get_facecolor())
plt.close(fig)
