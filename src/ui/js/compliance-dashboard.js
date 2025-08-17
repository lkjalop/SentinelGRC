/**
 * Compliance Dashboard JavaScript
 * Handles framework selection, user journey, and API integration
 */

// State management
let selectedFrameworks = new Set();
let selectedRegion = null;
let companyProfile = {};

// Framework metadata for recommendations
const frameworkData = {
    privacy_act: {
        name: "Privacy Act 1988",
        region: "australia",
        category: "legal",
        synergies: ["iso_27001", "soc2"],
        timeline: "3-6 months",
        cost: "$5K-25K"
    },
    apra_cps234: {
        name: "APRA CPS 234",
        region: "australia", 
        category: "financial",
        synergies: ["iso_27001", "essential_eight"],
        timeline: "6-12 months",
        cost: "$25K-100K"
    },
    soci_act: {
        name: "SOCI Act 2018",
        region: "australia",
        category: "infrastructure",
        synergies: ["essential_eight", "iso_27001"],
        timeline: "6-18 months",
        cost: "$50K-200K"
    },
    essential_eight: {
        name: "Essential Eight",
        region: "australia",
        category: "security",
        synergies: ["iso_27001", "nist_csf"],
        timeline: "6-12 months",
        cost: "$10K-50K"
    },
    soc2: {
        name: "SOC 2 Type II",
        region: "us",
        category: "trust",
        synergies: ["iso_27001", "nist_csf"],
        timeline: "6-12 months",
        cost: "$25K-150K"
    },
    nist_800_53: {
        name: "NIST SP 800-53",
        region: "us",
        category: "federal",
        synergies: ["iso_27001", "nist_csf"],
        timeline: "18-36 months",
        cost: "$50K-200K"
    },
    nist_csf: {
        name: "NIST CSF 2.0",
        region: "us",
        category: "risk",
        synergies: ["iso_27001", "soc2", "essential_eight"],
        timeline: "9-15 months",
        cost: "$20K-80K"
    },
    iso_27001: {
        name: "ISO 27001:2022",
        region: "international",
        category: "isms",
        synergies: ["soc2", "nist_csf", "essential_eight"],
        timeline: "12-18 months",
        cost: "$15K-75K"
    }
};

// Industry-specific recommendations
const industryRecommendations = {
    "Technology": ["soc2", "iso_27001", "nist_csf"],
    "Financial Services": ["apra_cps234", "soc2", "iso_27001", "nist_800_53"],
    "Healthcare": ["privacy_act", "iso_27001", "soc2"],
    "Government": ["essential_eight", "soci_act", "iso_27001", "nist_800_53"],
    "Manufacturing": ["iso_27001", "essential_eight", "nist_csf"]
};

/**
 * Initialize dashboard on page load
 */
document.addEventListener('DOMContentLoaded', function() {
    initializeDashboard();
    setupEventListeners();
    checkUrlParameters();
});

function initializeDashboard() {
    console.log('Compliance Dashboard initialized');
    
    // Load any saved state
    loadSavedState();
    
    // Set up theme toggle
    setupThemeToggle();
    
    // Initialize framework visibility based on region
    updateFrameworkVisibility();
}

function setupEventListeners() {
    // Form validation
    const form = document.getElementById('company-form');
    if (form) {
        form.addEventListener('input', validateForm);
    }
    
    // Keyboard navigation
    document.addEventListener('keydown', handleKeyboardNavigation);
}

function checkUrlParameters() {
    const urlParams = new URLSearchParams(window.location.search);
    const preselectedFramework = urlParams.get('framework');
    const preselectedRegion = urlParams.get('region');
    
    if (preselectedRegion) {
        selectRegion(preselectedRegion);
    }
    
    if (preselectedFramework) {
        toggleFramework(preselectedFramework, true);
        document.getElementById(`fw_${preselectedFramework}`)?.click();
    }
}

/**
 * Handle region selection
 */
function selectRegion(region) {
    selectedRegion = region;
    
    // Update UI
    document.querySelectorAll('.region-card').forEach(card => {
        card.classList.remove('selected');
    });
    
    const selectedCard = document.querySelector(`[data-region="${region}"]`);
    if (selectedCard) {
        selectedCard.classList.add('selected');
    }
    
    // Update framework visibility
    updateFrameworkVisibility();
    
    // Show region-specific recommendations
    if (region === 'australia') {
        suggestFrameworks(['privacy_act', 'essential_eight']);
    } else if (region === 'us') {
        suggestFrameworks(['soc2', 'nist_csf']);
    } else if (region === 'international') {
        suggestFrameworks(['iso_27001']);
    }
    
    console.log(`Selected region: ${region}`);
}

function updateFrameworkVisibility() {
    const categories = document.querySelectorAll('.framework-category');
    
    categories.forEach(category => {
        const categoryRegion = category.getAttribute('data-region');
        
        if (!selectedRegion || selectedRegion === 'all' || categoryRegion === selectedRegion || categoryRegion === 'international') {
            category.style.display = 'block';
        } else {
            category.style.display = 'none';
        }
    });
}

/**
 * Handle framework selection
 */
function toggleFramework(frameworkId, isSelected) {
    if (isSelected) {
        selectedFrameworks.add(frameworkId);
    } else {
        selectedFrameworks.delete(frameworkId);
    }
    
    console.log(`Framework ${frameworkId} ${isSelected ? 'selected' : 'deselected'}`);
    console.log('Current selection:', Array.from(selectedFrameworks));
    
    // Update UI
    updateFrameworkUI();
    
    // Generate recommendations
    generateSmartRecommendations();
    
    // Show/hide next steps
    updateActionButtons();
}

function updateFrameworkUI() {
    // Update framework cards appearance
    document.querySelectorAll('.framework-card').forEach(card => {
        const frameworkId = card.getAttribute('data-framework');
        if (selectedFrameworks.has(frameworkId)) {
            card.classList.add('selected');
        } else {
            card.classList.remove('selected');
        }
    });
}

/**
 * Generate AI-powered recommendations
 */
function generateSmartRecommendations() {
    const recommendationsSection = document.getElementById('smart-recommendations');
    const recommendationText = document.getElementById('recommendation-text');
    const recommendationBenefits = document.getElementById('recommendation-benefits');
    
    if (selectedFrameworks.size === 0) {
        recommendationsSection.style.display = 'none';
        return;
    }
    
    recommendationsSection.style.display = 'block';
    
    // Generate recommendations based on selected frameworks
    const selectedArray = Array.from(selectedFrameworks);
    let recommendations = [];
    let synergyBenefits = [];
    
    // Find synergies
    selectedArray.forEach(framework => {
        const data = frameworkData[framework];
        if (data && data.synergies) {
            data.synergies.forEach(synergy => {
                if (!selectedFrameworks.has(synergy) && !recommendations.includes(synergy)) {
                    recommendations.push(synergy);
                }
            });
        }
    });
    
    // Calculate synergy benefits
    if (selectedFrameworks.has('iso_27001') && selectedFrameworks.has('soc2')) {
        synergyBenefits.push('40% efficiency gain: ISO 27001 ISMS provides strong foundation for SOC 2 Security criteria');
    }
    
    if (selectedFrameworks.has('essential_eight') && selectedFrameworks.has('iso_27001')) {
        synergyBenefits.push('30% efficiency gain: Essential Eight technical controls complement ISO 27001 Annex A');
    }
    
    if (selectedFrameworks.has('nist_csf') && selectedFrameworks.has('nist_800_53')) {
        synergyBenefits.push('50% efficiency gain: NIST CSF framework aligns with NIST SP 800-53 controls');
    }
    
    // Generate recommendation text
    let text = '';
    if (selectedArray.length === 1) {
        text = `Great start! Based on ${frameworkData[selectedArray[0]].name}, we recommend also considering: `;
        text += recommendations.slice(0, 2).map(r => frameworkData[r].name).join(' and ');
        text += ' for comprehensive coverage.';
    } else if (selectedArray.length > 1) {
        text = `Excellent combination! You'll benefit from framework synergies and shared controls.`;
        if (recommendations.length > 0) {
            text += ` Consider adding ${frameworkData[recommendations[0]].name} to complete your compliance portfolio.`;
        }
    }
    
    recommendationText.textContent = text;
    
    // Show synergy benefits
    recommendationBenefits.innerHTML = '';
    if (synergyBenefits.length > 0) {
        const benefitsHtml = synergyBenefits.map(benefit => 
            `<div class="synergy-benefit">💎 ${benefit}</div>`
        ).join('');
        recommendationBenefits.innerHTML = `<h5>Synergy Benefits:</h5>${benefitsHtml}`;
    }
    
    // Industry-specific recommendations
    const industry = document.getElementById('industry')?.value;
    if (industry && industryRecommendations[industry]) {
        const industryRecs = industryRecommendations[industry].filter(r => !selectedFrameworks.has(r));
        if (industryRecs.length > 0) {
            const industryHtml = `<div class="industry-recommendation">
                <h5>Industry Recommendations for ${industry}:</h5>
                ${industryRecs.map(r => `<span class="framework-suggestion" onclick="suggestFramework('${r}')">${frameworkData[r].name}</span>`).join(', ')}
            </div>`;
            recommendationBenefits.innerHTML += industryHtml;
        }
    }
}

function suggestFramework(frameworkId) {
    const checkbox = document.getElementById(`fw_${frameworkId}`);
    if (checkbox) {
        checkbox.checked = true;
        toggleFramework(frameworkId, true);
    }
}

function suggestFrameworks(frameworkIds) {
    frameworkIds.forEach(id => {
        const checkbox = document.getElementById(`fw_${id}`);
        if (checkbox && !checkbox.checked) {
            // Visual suggestion without auto-selecting
            const card = document.querySelector(`[data-framework="${id}"]`);
            if (card) {
                card.classList.add('suggested');
                setTimeout(() => card.classList.remove('suggested'), 3000);
            }
        }
    });
}

/**
 * Form validation and progression
 */
function validateForm() {
    const requiredFields = ['company_name', 'industry', 'employee_count', 'country'];
    const isValid = requiredFields.every(field => {
        const element = document.getElementById(field);
        return element && element.value.trim() !== '';
    });
    
    if (isValid) {
        document.getElementById('company-profile-section').style.display = 'block';
        collectCompanyProfile();
    }
    
    updateActionButtons();
}

function collectCompanyProfile() {
    const formData = new FormData(document.getElementById('company-form'));
    companyProfile = {};
    
    for (let [key, value] of formData.entries()) {
        if (key === 'current_controls') {
            companyProfile[key] = value.split(',').map(s => s.trim()).filter(s => s);
        } else if (key === 'employee_count' || key === 'annual_revenue') {
            companyProfile[key] = parseInt(value) || 0;
        } else {
            companyProfile[key] = value;
        }
    }
    
    console.log('Company profile updated:', companyProfile);
}

function updateActionButtons() {
    const hasFrameworks = selectedFrameworks.size > 0;
    const hasProfile = Object.keys(companyProfile).length > 0;
    
    document.getElementById('start-assessment').style.display = hasFrameworks && hasProfile ? 'inline-block' : 'none';
    document.getElementById('get-roadmap').style.display = hasFrameworks ? 'inline-block' : 'none';
    
    if (hasFrameworks) {
        document.getElementById('company-profile-section').style.display = 'block';
    }
}

/**
 * Main actions
 */
async function startAssessment() {
    if (selectedFrameworks.size === 0) {
        alert('Please select at least one framework');
        return;
    }
    
    if (Object.keys(companyProfile).length === 0) {
        alert('Please complete the company profile');
        return;
    }
    
    showLoading('Running compliance assessment...');
    
    try {
        const response = await fetch('/api/assess', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                company_profile: companyProfile,
                frameworks: Array.from(selectedFrameworks),
                region: selectedRegion || 'australia'
            })
        });
        
        if (!response.ok) {
            throw new Error(`Assessment failed: ${response.statusText}`);
        }
        
        const results = await response.json();
        displayAssessmentResults(results);
        
    } catch (error) {
        console.error('Assessment error:', error);
        alert(`Assessment failed: ${error.message}`);
    } finally {
        hideLoading();
    }
}

async function generateRoadmap() {
    if (selectedFrameworks.size === 0) {
        alert('Please select at least one framework');
        return;
    }
    
    showLoading('Generating certification roadmap...');
    
    try {
        // For now, create a mock roadmap - integrate with roadmap engine later
        const roadmapData = {
            frameworks: Array.from(selectedFrameworks),
            company: companyProfile,
            recommended_sequence: calculateOptimalSequence(),
            total_timeline: calculateTotalTimeline(),
            total_investment: calculateTotalInvestment(),
            synergy_benefits: calculateSynergyBenefits()
        };
        
        displayRoadmapResults(roadmapData);
        
    } catch (error) {
        console.error('Roadmap generation error:', error);
        alert(`Roadmap generation failed: ${error.message}`);
    } finally {
        hideLoading();
    }
}

function calculateOptimalSequence() {
    const frameworks = Array.from(selectedFrameworks);
    
    // Simple prioritization: legal requirements first, then foundational, then specialized
    const priorityOrder = ['privacy_act', 'essential_eight', 'iso_27001', 'soc2', 'nist_csf', 'nist_800_53', 'apra_cps234', 'soci_act'];
    
    return frameworks.sort((a, b) => {
        const aIndex = priorityOrder.indexOf(a);
        const bIndex = priorityOrder.indexOf(b);
        return (aIndex === -1 ? 999 : aIndex) - (bIndex === -1 ? 999 : bIndex);
    });
}

function calculateTotalTimeline() {
    const frameworks = Array.from(selectedFrameworks);
    const maxTimelineMonths = Math.max(...frameworks.map(f => {
        const timeline = frameworkData[f]?.timeline || '12 months';
        const months = parseInt(timeline.match(/\d+/)[0]);
        return months;
    }));
    
    // Account for parallel work and synergies
    const synergyReduction = frameworks.length > 1 ? 0.85 : 1.0;
    const adjustedMonths = Math.ceil(maxTimelineMonths * synergyReduction);
    
    return `${adjustedMonths}-${adjustedMonths + 6} months`;
}

function calculateTotalInvestment() {
    const frameworks = Array.from(selectedFrameworks);
    let totalMin = 0;
    let totalMax = 0;
    
    frameworks.forEach(f => {
        const cost = frameworkData[f]?.cost || '$10K-50K';
        const matches = cost.match(/\$(\d+)K.*\$(\d+)K/);
        if (matches) {
            totalMin += parseInt(matches[1]) * 1000;
            totalMax += parseInt(matches[2]) * 1000;
        }
    });
    
    // Apply synergy discount for multiple frameworks
    if (frameworks.length > 1) {
        totalMin *= 0.85;
        totalMax *= 0.85;
    }
    
    return `$${(totalMin/1000).toFixed(0)}K - $${(totalMax/1000).toFixed(0)}K annually`;
}

function calculateSynergyBenefits() {
    const benefits = [];
    const frameworks = Array.from(selectedFrameworks);
    
    if (frameworks.includes('iso_27001') && frameworks.includes('soc2')) {
        benefits.push('40% efficiency gain from shared ISMS controls');
    }
    
    if (frameworks.includes('essential_eight') && frameworks.includes('iso_27001')) {
        benefits.push('30% efficiency gain from technical control alignment');
    }
    
    if (frameworks.length > 2) {
        benefits.push('Consolidated audit activities reduce assessment costs');
    }
    
    return benefits;
}

/**
 * Results display
 */
function displayAssessmentResults(results) {
    const resultsSection = document.getElementById('results-section');
    const resultsContent = document.getElementById('results-content');
    
    let html = '<div class="results-grid">';
    
    Object.entries(results).forEach(([framework, result]) => {
        const score = result.overall_score || result.compliance_percentage || 0;
        const risk = result.risk_level || 'Unknown';
        
        html += `
            <div class="result-card">
                <h4>${frameworkData[framework]?.name || framework}</h4>
                <div class="score-circle" data-score="${score}">
                    <span class="score-value">${score.toFixed(1)}%</span>
                </div>
                <div class="result-meta">
                    <span class="risk-level risk-${risk.toLowerCase()}">${risk} Risk</span>
                    <span class="recommendations-count">${(result.recommendations || []).length} recommendations</span>
                </div>
            </div>
        `;
    });
    
    html += '</div>';
    
    // Add action buttons for results
    html += `
        <div class="results-actions">
            <button class="btn btn-primary" onclick="downloadPDFReport()">
                📄 Download PDF Report
            </button>
            <button class="btn btn-secondary" onclick="viewDetailedResults()">
                🔍 View Detailed Results
            </button>
        </div>
    `;
    
    resultsContent.innerHTML = html;
    resultsSection.style.display = 'block';
    
    // Animate score circles
    animateScoreCircles();
}

function displayRoadmapResults(roadmapData) {
    const resultsSection = document.getElementById('results-section');
    const resultsContent = document.getElementById('results-content');
    
    let html = `
        <div class="roadmap-summary">
            <h3>Certification Roadmap</h3>
            <div class="roadmap-overview">
                <div class="overview-item">
                    <span class="overview-label">Total Timeline</span>
                    <span class="overview-value">${roadmapData.total_timeline}</span>
                </div>
                <div class="overview-item">
                    <span class="overview-label">Investment</span>
                    <span class="overview-value">${roadmapData.total_investment}</span>
                </div>
                <div class="overview-item">
                    <span class="overview-label">Frameworks</span>
                    <span class="overview-value">${roadmapData.frameworks.length}</span>
                </div>
            </div>
        </div>
        
        <div class="roadmap-sequence">
            <h4>Recommended Certification Sequence</h4>
            <div class="sequence-timeline">
    `;
    
    roadmapData.recommended_sequence.forEach((framework, index) => {
        const data = frameworkData[framework];
        html += `
            <div class="timeline-item">
                <div class="timeline-marker">${index + 1}</div>
                <div class="timeline-content">
                    <h5>${data.name}</h5>
                    <p>Timeline: ${data.timeline} | Cost: ${data.cost}</p>
                </div>
            </div>
        `;
    });
    
    html += `
            </div>
        </div>
        
        <div class="synergy-benefits">
            <h4>Synergy Benefits</h4>
            <ul>
    `;
    
    roadmapData.synergy_benefits.forEach(benefit => {
        html += `<li>💎 ${benefit}</li>`;
    });
    
    html += `
            </ul>
        </div>
        
        <div class="roadmap-actions">
            <button class="btn btn-primary" onclick="downloadRoadmapPDF()">
                📊 Download Roadmap PDF
            </button>
            <button class="btn btn-secondary" onclick="startAssessment()">
                🚀 Start Assessment
            </button>
        </div>
    `;
    
    resultsContent.innerHTML = html;
    resultsSection.style.display = 'block';
}

/**
 * Utility functions
 */
function showLoading(message = 'Loading...') {
    const overlay = document.getElementById('loading-overlay');
    const text = overlay.querySelector('.loading-text');
    if (text) text.textContent = message;
    overlay.style.display = 'flex';
}

function hideLoading() {
    document.getElementById('loading-overlay').style.display = 'none';
}

function animateScoreCircles() {
    document.querySelectorAll('.score-circle').forEach(circle => {
        const score = parseInt(circle.getAttribute('data-score'));
        const circumference = 2 * Math.PI * 45; // radius = 45
        const offset = circumference - (score / 100) * circumference;
        
        // Add SVG circle if not exists
        if (!circle.querySelector('svg')) {
            circle.innerHTML += `
                <svg width="100" height="100" class="score-svg">
                    <circle cx="50" cy="50" r="45" stroke="#e5e7eb" stroke-width="4" fill="none"/>
                    <circle cx="50" cy="50" r="45" stroke="#10b981" stroke-width="4" fill="none"
                            stroke-dasharray="${circumference}" stroke-dashoffset="${offset}"
                            transform="rotate(-90 50 50)" class="score-progress"/>
                </svg>
                ${circle.innerHTML}
            `;
        }
    });
}

function downloadPDFReport() {
    // Integrate with PDF generation API
    const url = `/api/reports/pdf?frameworks=${Array.from(selectedFrameworks).join(',')}&company=${encodeURIComponent(companyProfile.company_name)}`;
    window.open(url, '_blank');
}

function downloadRoadmapPDF() {
    // Integrate with roadmap PDF generation
    const url = `/api/roadmap/pdf?frameworks=${Array.from(selectedFrameworks).join(',')}&company=${encodeURIComponent(companyProfile.company_name)}`;
    window.open(url, '_blank');
}

function viewDetailedResults() {
    // Navigate to detailed results view
    const params = new URLSearchParams({
        frameworks: Array.from(selectedFrameworks).join(','),
        company: companyProfile.company_name
    });
    window.location.href = `/detailed-results.html?${params}`;
}

function setupThemeToggle() {
    // Implement theme toggle functionality
    const themeToggle = document.querySelector('.theme-toggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
            const newTheme = currentTheme === 'light' ? 'dark' : 'light';
            document.documentElement.setAttribute('data-theme', newTheme);
            
            // Save preference
            localStorage.setItem('theme', newTheme);
        });
    }
}

function handleKeyboardNavigation(event) {
    // Implement keyboard shortcuts for accessibility
    if (event.ctrlKey && event.key === 'Enter') {
        if (selectedFrameworks.size > 0 && Object.keys(companyProfile).length > 0) {
            startAssessment();
        }
    }
}

function loadSavedState() {
    // Load any previously saved state from localStorage
    try {
        const saved = localStorage.getItem('compliance-dashboard-state');
        if (saved) {
            const state = JSON.parse(saved);
            if (state.selectedFrameworks) {
                selectedFrameworks = new Set(state.selectedFrameworks);
                // Update checkboxes
                selectedFrameworks.forEach(fw => {
                    const checkbox = document.getElementById(`fw_${fw}`);
                    if (checkbox) checkbox.checked = true;
                });
            }
        }
    } catch (error) {
        console.warn('Failed to load saved state:', error);
    }
}

function saveState() {
    // Save current state to localStorage
    try {
        const state = {
            selectedFrameworks: Array.from(selectedFrameworks),
            selectedRegion: selectedRegion,
            companyProfile: companyProfile
        };
        localStorage.setItem('compliance-dashboard-state', JSON.stringify(state));
    } catch (error) {
        console.warn('Failed to save state:', error);
    }
}

// Save state periodically
setInterval(saveState, 30000); // Every 30 seconds

// Save state before page unload
window.addEventListener('beforeunload', saveState);