// ─── Helpers ────────────────────────────────────────────────────────────────

function getVideoId(url) {
    const m = url.match(/(?:youtube\.com.*v=|youtu\.be\/)([^&]+)/);
    return m ? m[1] : "";
}

/** Safe percentage: treats null / undefined / NaN as 0 */
function pct(val) {
    const n = parseFloat(val);
    return isNaN(n) ? 0 : Math.min(100, Math.max(0, Math.round(n)));
}

/** Safe string: always returns a trimmed string */
function str(val) {
    return (val !== null && val !== undefined) ? String(val).trim() : "";
}

// ─── File-label feedback ─────────────────────────────────────────────────────

function attachFileLabel(inputId, labelId) {
    const input = document.getElementById(inputId);
    if (!input) return;
    input.addEventListener("change", function () {
        const label = document.getElementById(labelId);
        if (!label || !this.files[0]) return;
        label.querySelector(".title").textContent = this.files[0].name;
        label.querySelector(".sub").textContent   = (this.files[0].size / 1024).toFixed(1) + " KB";
        label.style.borderColor = "rgba(52,211,153,0.5)";
        label.style.background  = "rgba(52,211,153,0.05)";
        label.querySelector(".icon").textContent  = "✅";
    });
}

attachFileLabel("resume", "resumeLabel");
attachFileLabel("jd",     "jdLabel");

// ─── Animated ring ───────────────────────────────────────────────────────────

function buildRing(score, color, size = 110, stroke = 9) {
    const r    = (size / 2) - stroke;
    const circ = 2 * Math.PI * r;
    const id   = "arc_" + Math.random().toString(36).slice(2);
    return {
        html: `
          <svg width="${size}" height="${size}" viewBox="0 0 ${size} ${size}"
               style="transform:rotate(-90deg);display:block;">
            <circle cx="${size/2}" cy="${size/2}" r="${r}"
                fill="none" stroke="rgba(255,255,255,0.06)" stroke-width="${stroke}"/>
            <circle cx="${size/2}" cy="${size/2}" r="${r}"
                fill="none" stroke="${color}" stroke-width="${stroke}"
                stroke-linecap="round"
                stroke-dasharray="${circ}" stroke-dashoffset="${circ}"
                id="${id}"/>
          </svg>`,
        id, circ, filled: (score / 100) * circ
    };
}

function animateRing(id, circ, filled) {
    const el = document.getElementById(id);
    if (!el) return;
    requestAnimationFrame(() => {
        el.style.transition       = "stroke-dashoffset 1.2s cubic-bezier(0.4,0,0.2,1)";
        el.style.strokeDashoffset = circ - filled;
    });
}

function animateCount(elId, target) {
    const el = document.getElementById(elId);
    if (!el) return;
    let cur = 0, step = target / 60;
    const t = setInterval(() => {
        cur = Math.min(cur + step, target);
        el.textContent = Math.round(cur);
        if (cur >= target) clearInterval(t);
    }, 16);
}

function animateBar(elId, pctVal) {
    const el = document.getElementById(elId);
    if (!el) return;
    setTimeout(() => { el.style.width = pctVal + "%"; }, 120);
}

function scoreColor(v) {
    return v >= 70 ? "#34d399" : v >= 40 ? "#4f8eff" : "#f87171";
}

// ─── Build gap_analysis from mismatched_items fallback ───────────────────────

/**
 * mismatched_items has entries like:
 *   "Skill: C#"  |  "Experience: 0–2 years"  |  "Education: BS or MS"
 * gap_analysis (when present) has entries like:
 *   "C# - Learn through Microsoft Learn"
 *
 * We normalise both into the same { skills:[], experience:[], education:[] }
 * shape so the tab renderer always gets consistent data.
 */
function normaliseGapAnalysis(gapAnalysis, mismatchedItems) {

    // ── If gap_analysis already has content, use it ──────────────────────────
    const hasContent =
        gapAnalysis &&
        typeof gapAnalysis === "object" &&
        !Array.isArray(gapAnalysis) &&
        (
            (gapAnalysis.skills     || []).length > 0 ||
            (gapAnalysis.experience || []).length > 0 ||
            (gapAnalysis.education  || []).length > 0
        );

    if (hasContent) return gapAnalysis;

    // ── Otherwise build from mismatched_items ────────────────────────────────
    const out = { skills: [], experience: [], education: [] };

    (mismatchedItems || []).forEach(item => {
        const s = str(item);
        if      (/^skill:/i.test(s))      out.skills    .push(s.replace(/^skill:\s*/i,      ""));
        else if (/^experience:/i.test(s)) out.experience.push(s.replace(/^experience:\s*/i, ""));
        else if (/^education:/i.test(s))  out.education .push(s.replace(/^education:\s*/i,  ""));
        else                               out.skills    .push(s); // default bucket
    });

    return out;
}

// ─── Gap tabs renderer ───────────────────────────────────────────────────────

function buildGapTabs(gapData) {
    const tabs = [
        { key: "skills",     label: "🧠 Skills",    color: "#f87171" },
        { key: "experience", label: "💼 Experience", color: "#fbbf24" },
        { key: "education",  label: "🎓 Education",  color: "#a78bfa" },
    ];

    const tabBtns = tabs.map((t, i) => `
        <button class="gap-tab-btn ${i === 0 ? "active" : ""}"
                onclick="switchGapTab('${t.key}')"
                id="gaptab_${t.key}">
            ${t.label}
            <span class="gap-tab-count">${(gapData[t.key] || []).length}</span>
        </button>`).join("");

    const panels = tabs.map(t => {
        const items = gapData[t.key] || [];
        const rows  = items.length
            ? items.map(item => {
                const [skill, ...rest] = str(item).split(" - ");
                const resource         = rest.join(" - ");
                return `
                  <div class="gap-row">
                    <span class="gap-pill" style="--pill-color:${t.color}">${skill.trim()}</span>
                    ${resource ? `<span class="gap-resource">→ ${resource.trim()}</span>` : ""}
                  </div>`;
              }).join("")
            : `<p style="color:var(--muted);font-size:13px;">No ${t.key} gaps found.</p>`;

        return `<div class="gap-panel ${t.key === "skills" ? "active" : ""}"
                     id="gappanel_${t.key}">${rows}</div>`;
    }).join("");

    return `<div class="gap-tabs">${tabBtns}</div>
            <div class="gap-panels">${panels}</div>`;
}

window.switchGapTab = function (key) {
    document.querySelectorAll(".gap-tab-btn").forEach(b => b.classList.remove("active"));
    document.querySelectorAll(".gap-panel")  .forEach(p => p.classList.remove("active"));
    document.getElementById("gaptab_"   + key)?.classList.add("active");
    document.getElementById("gappanel_" + key)?.classList.add("active");
};

// ─── Main submit ─────────────────────────────────────────────────────────────

document.getElementById("uploadForm").addEventListener("submit", async function (e) {
    e.preventDefault();

    document.getElementById("loading").style.display = "block";
    document.getElementById("result").innerHTML      = "";
    document.querySelector(".submit-btn").disabled   = true;

    const formData = new FormData(e.target);

    try {
        const res = await fetch("/upload", { method: "POST", body: formData });

        // ── Parse JSON safely ──────────────────────────────────────────────
        let data;
        const rawText = await res.text();
        try {
            data = JSON.parse(rawText);
        } catch (parseErr) {
            console.error("JSON parse failed. Raw response:", rawText);
            throw new Error("Server returned invalid JSON. Check console for raw response.");
        }

        console.log("✅ BACKEND DATA:", data);

        if (data.error) {
            document.getElementById("result").innerHTML =
                `<div class="error-box">⚠️ ${data.error}</div>`;
            return;
        }

        // ── Extract every field with safe fallbacks ──────────────────────────
        const atsScore      = pct(data.ats_score);
        const skillsPct     = pct(data.skills_match_percentage);
        const expPct        = pct(data.experience_match_percentage);
        const eduPct        = pct(data.education_match_percentage);
        const matchedSkills = Array.isArray(data.matched_skills)  ? data.matched_skills  : [];
        const mismatchItems = Array.isArray(data.mismatched_items) ? data.mismatched_items : [];
        const analysis      = str(data.analysis);
        const ytData        = (data.youtube_recommendations && typeof data.youtube_recommendations === "object")
                                ? data.youtube_recommendations : {};

        // ── Normalise gap analysis (uses mismatched_items as fallback) ────────
        const gapData = normaliseGapAnalysis(data.gap_analysis, mismatchItems);

        console.log("📊 Parsed values →",
            { atsScore, skillsPct, expPct, eduPct, matchedSkills, analysis, gapData });

        // ── Feedback copy ─────────────────────────────────────────────────────
        const atsFeedback = atsScore >= 70
            ? "Strong match — you're well aligned with this role."
            : atsScore >= 40
            ? "Moderate match — a few skill gaps to address."
            : "Low match — significant gaps detected. Focus on the skills below.";

        // ── Score ring ────────────────────────────────────────────────────────
        const mainRing = buildRing(atsScore, scoreColor(atsScore));

        // ── Sub-score bars ────────────────────────────────────────────────────
        const stats = [
            { label: "Skills Match",     val: skillsPct, color: "#4f8eff", id: "bar_skills" },
            { label: "Experience Match", val: expPct,    color: "#fbbf24", id: "bar_exp"    },
            { label: "Education Match",  val: eduPct,    color: "#a78bfa", id: "bar_edu"    },
        ];

        const statsHtml = stats.map(s => `
            <div class="stat-row">
                <div class="stat-meta">
                    <span class="stat-label">${s.label}</span>
                    <span class="stat-value" style="color:${s.color}">${s.val}%</span>
                </div>
                <div class="stat-track">
                    <div class="stat-fill" id="${s.id}"
                         style="--fill-color:${s.color}; width:0%"></div>
                </div>
            </div>`).join("");

        // ── Matched skills ────────────────────────────────────────────────────
        const matchedHtml = matchedSkills.length
            ? matchedSkills.map(s => `<span class="match-tag">✓ ${s}</span>`).join("")
            : `<span style="color:var(--muted);font-size:13px;">No direct skill matches found.</span>`;

        // ── YouTube cards ─────────────────────────────────────────────────────
        let ytCardsHtml = "";
        let hasVideos   = false;

        for (const cat in ytData) {
            const videos = ytData[cat];
            if (Array.isArray(videos) && videos.length) {
                hasVideos = true;
                videos.forEach(v => {
                    const vid   = getVideoId(str(v.url));
                    const title = str(v.title) || "Untitled";
                    ytCardsHtml += `
                        <a href="${v.url}" target="_blank" rel="noopener" class="yt-card">
                            <div class="yt-thumb">
                                <img src="https://img.youtube.com/vi/${vid}/mqdefault.jpg"
                                     alt="${title}" loading="lazy"
                                     onerror="this.src='https://img.youtube.com/vi/${vid}/0.jpg'">
                                <div class="play-overlay"><div class="play-btn">▶</div></div>
                            </div>
                            <div class="yt-info"><p>${title}</p></div>
                        </a>`;
                });
            }
        }

        // ── Total gap count ───────────────────────────────────────────────────
        const totalGaps =
            (gapData.skills     || []).length +
            (gapData.experience || []).length +
            (gapData.education  || []).length;

        // ── Render ────────────────────────────────────────────────────────────
        document.getElementById("result").innerHTML = `

          <!-- ① SCORE + SUB-SCORES -->
          <div class="result-block score-card anim-up" style="--delay:0s">
            <div class="score-ring-wrap">
              ${mainRing.html}
              <div class="score-overlay">
                <span class="score-num" id="mainScoreNum">0</span>
                <span class="score-lbl">/ 100</span>
              </div>
            </div>
            <div class="score-right">
              <h2 class="score-title">ATS Score:
                <strong style="color:${scoreColor(atsScore)}">${atsScore}</strong>
              </h2>
              <p class="score-feedback">${atsFeedback}</p>
              <div class="stats-stack">${statsHtml}</div>
            </div>
          </div>

          <!-- ② AI ANALYSIS -->
          ${analysis
            ? `<div class="result-block analysis-card anim-up" style="--delay:0.08s">
                 <div class="section-title">
                   <span class="dot" style="background:#4f8eff"></span>AI Analysis
                 </div>
                 <p class="analysis-text">${analysis}</p>
               </div>`
            : `<div class="result-block analysis-card anim-up" style="--delay:0.08s">
                 <div class="section-title">
                   <span class="dot" style="background:#4f8eff"></span>AI Analysis
                 </div>
                 <p class="analysis-text" style="color:var(--muted)">
                   No analysis summary was returned by the server.
                 </p>
               </div>`
          }

          <!-- ③ MATCHED SKILLS -->
          <div class="result-block matched-card anim-up" style="--delay:0.14s">
            <div class="section-title">
              <span class="dot" style="background:#34d399"></span>
              Matched Skills
              <span class="pill-count">${matchedSkills.length}</span>
            </div>
            <div class="match-tags">${matchedHtml}</div>
          </div>

          <!-- ④ GAP ANALYSIS -->
          <div class="result-block gap-card anim-up" style="--delay:0.20s">
            <div class="section-title">
              <span class="dot" style="background:#f87171"></span>
              Gap Analysis
              <span class="pill-count" style="background:rgba(248,113,113,.15);color:#f87171">${totalGaps}</span>
            </div>
            ${buildGapTabs(gapData)}
          </div>

          <!-- ⑤ YOUTUBE -->
          <div class="result-block yt-section anim-up" style="--delay:0.26s">
            <div class="section-title">
              <span class="dot" style="background:#ff4e4e"></span>
              Recommended Learning Resources
            </div>
            ${hasVideos
              ? `<div class="yt-grid">${ytCardsHtml}</div>`
              : `<p style="color:var(--muted);font-size:14px;">No video recommendations available.</p>`}
          </div>`;

        // ── Trigger animations after DOM is ready ─────────────────────────────
        requestAnimationFrame(() => {
            animateRing(mainRing.id, mainRing.circ, mainRing.filled);
            animateCount("mainScoreNum", atsScore);
            stats.forEach(s => animateBar(s.id, s.val));
        });

    } catch (err) {
        console.error("❌ Error:", err);
        document.getElementById("result").innerHTML = `
            <div class="error-box">
                ⚠️ ${err.message || "Failed to process request. Please try again."}
            </div>`;
    } finally {
        document.getElementById("loading").style.display = "none";
        document.querySelector(".submit-btn").disabled   = false;
    }
});