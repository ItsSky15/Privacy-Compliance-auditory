// Constants
const SCORE_THRESHOLDS = {
    HIGH: 80,
    MEDIUM: 60,
    LOW: 40
};

const PERMISSIONS = {
    camera: { id: 'camera-access', icon: '📷' },
    microphone: { id: 'mic-access', icon: '🎤' },
    notifications: { id: 'notifications-access', icon: '🔔' },
    geolocation: { id: 'geolocation-access', icon: '📍' },
    clipboard: { id: 'clipboard-access', icon: '📋' }
};

// UI State Management
const UIState = {
    setLoading() {
        document.getElementById("loading").classList.remove("hidden");
        document.getElementById("results").classList.add("hidden");
        document.getElementById("score-display").innerHTML = `<div class="spinner"></div>`;
        document.getElementById("safety-recommendation").textContent = "";
        this.resetPermissions();
    },
    clearLoading() {
        document.getElementById("loading").classList.add("hidden");
        document.getElementById("results").classList.remove("hidden");
    },
    resetPermissions() {
        Object.values(PERMISSIONS).forEach(({ id }) => {
            const element = document.getElementById(id);
            if (element) element.textContent = "Not Checked";
        });
    },
    showError(message) {
        const errorBox = document.getElementById("error-notification");
        errorBox.textContent = message;
        errorBox.classList.add("visible");
        setTimeout(() => errorBox.classList.remove("visible"), 5000);
        const scoreBox = document.getElementById("score-display");
        scoreBox.innerHTML = `<span class="score-value score-low">Error</span>`;
        scoreBox.className = "score-box error";
    }
};

// Main analysis function
async function analyzeCurrentPage() {
    UIState.setLoading();
    try {
        const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
        if (!tab?.url) throw new Error("No active tab found");
        const url = tab.url;
        if (!url.startsWith("http")) throw new Error("This extension only works on websites");
        const response = await fetch(`http://localhost:5000/analyze?url=${encodeURIComponent(url)}`);
        if (!response.ok) throw new Error(`Server error: ${response.status}`);
        const data = await response.json();
        if (data.error) throw new Error(data.error);
        updateUI(data);
        await checkPermissions(url);
    } catch (err) {
        UIState.showError(err.message || "An error occurred");
    } finally {
        UIState.clearLoading();
    }
}

// UI Update Functions
function updateUI(data) {
    try {
        updateScore(data.score);
        updateSafetyRecommendation(data.safety_recommendation);
        updatePermissions(data.permissions);
        updateFindings(data);
        updateCompliance(data.compliance);
        updateTips(data.tips);
    } catch (err) {
        UIState.showError('Error updating display');
    }
}

function updateScore(score) {
    const scoreBox = document.getElementById("score-display");
    scoreBox.innerHTML = typeof score === "number" ? `${score}%` : "--";
}

// Safety Recommendation Functions
function updateSafetyRecommendation(recommendation) {
    const element = document.getElementById("safety-recommendation");
    if (!element) return;
    element.textContent = recommendation || "No safety recommendations available";
}

// Permission Management Functions
function updatePermissions(permissions = []) {
    UIState.resetPermissions();
    if (!Array.isArray(permissions)) return;
    permissions.forEach(permission => {
        const permissionKey = Object.keys(PERMISSIONS).find(key =>
            permission.toLowerCase().includes(key)
        );
        if (permissionKey) {
            const { id, icon } = PERMISSIONS[permissionKey];
            const element = document.getElementById(id);
            if (element) {
                element.innerHTML = `${icon} Requested`;
                element.className = 'permission-status requested';
            }
        }
    });
}

async function checkPermissions(url) {
    const permissionChecks = Object.entries(PERMISSIONS).map(async ([type, { id, icon }]) => {
        try {
            const result = await navigator.permissions.query({ name: type });
            const element = document.getElementById(id);
            if (element) {
                const status = result.state;
                const statusIcons = {
                    granted: '✅',
                    denied: '❌',
                    prompt: '⚠️'
                };
                element.innerHTML = `${icon} ${statusIcons[status] || '❓'} ${status.charAt(0).toUpperCase() + status.slice(1)}`;
                element.className = `permission-status ${status}`;
            }
        } catch (err) {
            // Permission type not supported
        }
    });
    await Promise.all(permissionChecks);
}

// Dummy implementations for findings, compliance, tips
function updateFindings(data) {
    document.getElementById("key-findings").innerHTML = "<li>Findings go here</li>";
}
function updateCompliance(data) {
    document.getElementById("gdpr-card").textContent = "GDPR: --";
    document.getElementById("dpdp-card").textContent = "DPDP: --";
}
function updateTips(data) {
    document.getElementById("tips").innerHTML = "<li>Tips go here</li>";
}

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById("scan-btn").addEventListener("click", analyzeCurrentPage);
});
