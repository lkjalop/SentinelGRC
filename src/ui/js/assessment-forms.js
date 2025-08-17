/**
 * Assessment Forms JavaScript
 * Interactive multi-step questionnaire with adaptive logic
 */

let currentStep = 1;
const totalSteps = 4;
let formData = {};

// Initialize form when page loads
document.addEventListener('DOMContentLoaded', function() {
    initializeForm();
    setupFileUpload();
    updateProgress();
});

function initializeForm() {
    // Set up form validation
    const form = document.getElementById('assessment-form');
    form.addEventListener('submit', handleFormSubmit);
    
    // Load any saved progress from localStorage
    loadSavedProgress();
    
    // Update recommendations based on default values
    updateFrameworkRecommendations();
}

function nextStep() {
    if (validateCurrentStep()) {
        saveCurrentStepData();
        
        if (currentStep < totalSteps) {
            // Hide current step
            document.querySelector(`.form-step[data-step="${currentStep}"]`).classList.remove('active');
            
            currentStep++;
            
            // Show next step
            document.querySelector(`.form-step[data-step="${currentStep}"]`).classList.add('active');
            
            updateProgress();
            
            // Update dynamic content for the new step
            if (currentStep === 4) {
                updateFrameworkRecommendations();
                updateAssessmentSummary();
            }
        }
    }
}

function prevStep() {
    if (currentStep > 1) {
        // Hide current step
        document.querySelector(`.form-step[data-step="${currentStep}"]`).classList.remove('active');
        
        currentStep--;
        
        // Show previous step
        document.querySelector(`.form-step[data-step="${currentStep}"]`).classList.add('active');
        
        updateProgress();
    }
}

function updateProgress() {
    const progressFill = document.getElementById('progress-fill');
    const currentStepElement = document.getElementById('current-step');
    const totalStepsElement = document.getElementById('total-steps');
    
    const progressPercent = (currentStep / totalSteps) * 100;
    progressFill.style.width = `${progressPercent}%`;
    
    currentStepElement.textContent = currentStep;
    totalStepsElement.textContent = totalSteps;
}

function validateCurrentStep() {
    const currentStepElement = document.querySelector(`.form-step[data-step="${currentStep}"]`);
    const requiredFields = currentStepElement.querySelectorAll('[required]');
    
    for (let field of requiredFields) {
        if (!field.value.trim()) {
            field.focus();
            showError(`Please fill in the required field: ${field.previousElementSibling.textContent}`);
            return false;
        }
    }
    
    return true;
}

function saveCurrentStepData() {
    const currentStepElement = document.querySelector(`.form-step[data-step="${currentStep}"]`);
    const formElements = currentStepElement.querySelectorAll('input, select, textarea');
    
    formElements.forEach(element => {
        if (element.type === 'checkbox') {
            if (element.name === 'currentControls' || element.name === 'dataSensitivity') {
                if (!formData[element.name]) formData[element.name] = [];
                if (element.checked) {
                    formData[element.name].push(element.value);
                }
            } else {
                formData[element.name] = element.checked;
            }
        } else if (element.type === 'radio') {
            if (element.checked) {
                formData[element.name] = element.value;
            }
        } else {
            formData[element.name] = element.value;
        }
    });
    
    // Save to localStorage for persistence
    localStorage.setItem('sentinelAssessmentProgress', JSON.stringify(formData));
}

function loadSavedProgress() {
    const saved = localStorage.getItem('sentinelAssessmentProgress');
    if (saved) {
        formData = JSON.parse(saved);
        
        // Populate form fields with saved data
        Object.keys(formData).forEach(key => {
            const element = document.querySelector(`[name="${key}"]`);
            if (element) {
                if (element.type === 'checkbox') {
                    if (Array.isArray(formData[key])) {
                        formData[key].forEach(value => {
                            const checkbox = document.querySelector(`[name="${key}"][value="${value}"]`);
                            if (checkbox) checkbox.checked = true;
                        });
                    } else {
                        element.checked = formData[key];
                    }
                } else if (element.type === 'radio') {
                    const radio = document.querySelector(`[name="${key}"][value="${formData[key]}"]`);
                    if (radio) radio.checked = true;
                } else {
                    element.value = formData[key];
                }
            }
        });
    }
}

// Adaptive form logic based on user inputs
function handleIndustryChange(industry) {
    // Hide all industry-specific fields first
    document.querySelectorAll('.industry-fields').forEach(field => {
        field.style.display = 'none';
    });
    
    // Show relevant industry fields
    const industryFields = document.getElementById(`${industry}-fields`);
    if (industryFields) {
        industryFields.style.display = 'block';
    }
    
    // Update framework recommendations
    formData.industry = industry;
    if (currentStep === 4) {
        updateFrameworkRecommendations();
    }
}

function handleEmployeeCountChange(count) {
    formData.employeeCount = parseInt(count);
    
    // Adjust recommendations based on company size
    if (currentStep === 4) {
        updateFrameworkRecommendations();
    }
}

function handleCountryChange(country) {
    formData.country = country;
    
    // Update framework recommendations based on geographic requirements
    if (currentStep === 4) {
        updateFrameworkRecommendations();
    }
}

function updateFrameworkRecommendations() {
    const recommendationsContainer = document.getElementById('recommended-frameworks');
    const frameworks = getRecommendedFrameworks();
    
    recommendationsContainer.innerHTML = frameworks.map(framework => 
        `<span class="framework-badge">${framework}</span>`
    ).join('');
}

function getRecommendedFrameworks() {
    const frameworks = [];
    const industry = formData.industry || document.getElementById('industry').value;
    const country = formData.country || document.getElementById('country').value;
    const employeeCount = formData.employeeCount || parseInt(document.getElementById('employee-count').value);
    
    // Geographic framework recommendations
    switch (country) {
        case 'australia':
            frameworks.push('Essential 8', 'Privacy Act 1988');
            if (industry === 'finance' || industry === 'banking') {
                frameworks.push('APRA CPS 234');
            }
            break;
        case 'united_states':
            frameworks.push('NIST CSF');
            if (industry === 'healthcare') {
                frameworks.push('HIPAA');
            }
            if (industry === 'finance' || industry === 'banking') {
                frameworks.push('SOX');
            }
            // Add NIST SP 800-53 for government contracts or large enterprises
            if (industry === 'government' || employeeCount > 1000) {
                frameworks.push('NIST SP 800-53');
            }
            break;
        case 'european_union':
            frameworks.push('GDPR', 'NIS2');
            break;
    }
    
    // Industry-specific recommendations
    switch (industry) {
        case 'healthcare':
            if (!frameworks.includes('HIPAA')) frameworks.push('HIPAA');
            frameworks.push('HITECH');
            break;
        case 'finance':
        case 'banking':
            frameworks.push('PCI DSS');
            if (employeeCount > 500) {
                frameworks.push('SOX');
            }
            break;
        case 'government':
            frameworks.push('NIST SP 800-53');
            break;
    }
    
    // Size-based recommendations
    if (employeeCount > 250) {
        frameworks.push('ISO 27001');
    }
    
    // Always recommend SOC 2 for technology companies
    if (industry === 'technology') {
        frameworks.push('SOC 2');
    }
    
    return [...new Set(frameworks)]; // Remove duplicates
}

function updateAssessmentSummary() {
    const summary = document.getElementById('assessment-summary');
    const companyName = formData.companyName || document.getElementById('company-name').value;
    const industry = formData.industry || document.getElementById('industry').value;
    const employeeCount = formData.employeeCount || document.getElementById('employee-count').value;
    const frameworks = getRecommendedFrameworks();
    const currentControls = formData.currentControls || [];
    
    const summaryHTML = `
        <div class="summary-item">
            <strong>Company:</strong> ${companyName} (${industry}, ${employeeCount} employees)
        </div>
        <div class="summary-item">
            <strong>Recommended Frameworks:</strong> ${frameworks.join(', ')}
        </div>
        <div class="summary-item">
            <strong>Current Controls:</strong> ${currentControls.length} selected
        </div>
        <div class="summary-item">
            <strong>Assessment Type:</strong> Comprehensive multi-framework analysis
        </div>
        <div class="summary-item">
            <strong>Estimated Duration:</strong> 5-10 minutes
        </div>
    `;
    
    summary.innerHTML = summaryHTML;
}

// File upload functionality
function setupFileUpload() {
    const uploadArea = document.getElementById('file-upload-area');
    const fileInput = document.getElementById('document-upload');
    const uploadedFilesContainer = document.getElementById('uploaded-files');
    
    // Handle drag and drop
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = 'var(--sentinel-primary)';
        uploadArea.style.backgroundColor = 'rgba(var(--sentinel-primary-rgb), 0.1)';
    });
    
    uploadArea.addEventListener('dragleave', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = 'var(--sentinel-gray-300)';
        uploadArea.style.backgroundColor = 'var(--sentinel-gray-50)';
    });
    
    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = 'var(--sentinel-gray-300)';
        uploadArea.style.backgroundColor = 'var(--sentinel-gray-50)';
        
        const files = Array.from(e.dataTransfer.files);
        handleFiles(files);
    });
    
    fileInput.addEventListener('change', (e) => {
        const files = Array.from(e.target.files);
        handleFiles(files);
    });
    
    function handleFiles(files) {
        files.forEach(file => {
            if (file.size > 10 * 1024 * 1024) { // 10MB limit
                showError(`File ${file.name} is too large. Maximum size is 10MB.`);
                return;
            }
            
            const fileElement = document.createElement('div');
            fileElement.className = 'uploaded-file';
            fileElement.innerHTML = `
                <div class="file-info">
                    <span>📄</span>
                    <span>${file.name}</span>
                    <span class="file-size">(${formatFileSize(file.size)})</span>
                </div>
                <span class="file-remove" onclick="removeFile(this)">✕</span>
            `;
            
            uploadedFilesContainer.appendChild(fileElement);
            
            // Store file for later upload
            if (!formData.uploadedFiles) formData.uploadedFiles = [];
            formData.uploadedFiles.push(file);
        });
    }
}

function removeFile(element) {
    const fileElement = element.closest('.uploaded-file');
    const fileName = fileElement.querySelector('.file-info span:nth-child(2)').textContent;
    
    // Remove from formData
    if (formData.uploadedFiles) {
        formData.uploadedFiles = formData.uploadedFiles.filter(file => file.name !== fileName);
    }
    
    fileElement.remove();
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Form submission
async function handleFormSubmit(e) {
    e.preventDefault();
    
    if (!validateCurrentStep()) {
        return;
    }
    
    saveCurrentStepData();
    
    // Show loading overlay
    showLoadingOverlay();
    
    try {
        // Prepare form data for submission
        const assessmentData = {
            companyProfile: {
                companyName: formData.companyName,
                industry: formData.industry,
                employeeCount: formData.employeeCount,
                annualRevenue: formData.annualRevenue,
                country: formData.country,
                hasGovernmentContracts: formData.hasGovernmentContracts
            },
            currentControls: formData.currentControls || [],
            riskProfile: {
                previousIncidents: formData.previousIncidents,
                riskTolerance: formData.riskTolerance,
                complianceTimeline: formData.complianceTimeline,
                dataSensitivity: formData.dataSensitivity || []
            },
            assessmentOptions: {
                enableSidecars: formData.enableSidecars,
                enableAI: formData.enableAI,
                enableExpertReview: formData.enableExpertReview,
                generatePDF: formData.generatePDF
            },
            recommendedFrameworks: getRecommendedFrameworks()
        };
        
        // Submit to backend API
        const response = await fetch('/api/assessment/run', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                company_profile: assessmentData.companyProfile,
                frameworks: assessmentData.recommendedFrameworks,
                region: formData.country
            })
        });
        
        if (!response.ok) {
            throw new Error(`Assessment failed: ${response.statusText}`);
        }
        
        const results = await response.json();
        
        // Clear saved progress
        localStorage.removeItem('sentinelAssessmentProgress');
        
        // Redirect to results page
        window.location.href = `/assessment-results.html?id=${results.assessment_id}`;
        
    } catch (error) {
        console.error('Assessment submission failed:', error);
        hideLoadingOverlay();
        showError(`Assessment failed: ${error.message}`);
    }
}

function showLoadingOverlay() {
    const overlay = document.getElementById('assessment-loading');
    overlay.style.display = 'flex';
    
    // Simulate assessment progress
    const steps = overlay.querySelectorAll('.assessment-steps .step');
    let currentStepIndex = 0;
    
    const progressInterval = setInterval(() => {
        if (currentStepIndex < steps.length) {
            // Mark current step as active
            steps[currentStepIndex].classList.add('active');
            
            // Update status text
            const statusMessages = [
                'Creating company profile...',
                'Analyzing applicable frameworks...',
                'Identifying compliance gaps...',
                'Calculating risk scores...',
                'Generating comprehensive report...'
            ];
            
            document.getElementById('loading-status').textContent = statusMessages[currentStepIndex];
            
            // Complete previous steps
            if (currentStepIndex > 0) {
                steps[currentStepIndex - 1].classList.remove('active');
                steps[currentStepIndex - 1].classList.add('completed');
            }
            
            currentStepIndex++;
        } else {
            clearInterval(progressInterval);
        }
    }, 2000);
}

function hideLoadingOverlay() {
    const overlay = document.getElementById('assessment-loading');
    overlay.style.display = 'none';
}

function showError(message) {
    // Create or update error message
    let errorElement = document.querySelector('.error-message');
    if (!errorElement) {
        errorElement = document.createElement('div');
        errorElement.className = 'error-message';
        errorElement.style.cssText = `
            background: var(--sentinel-error);
            color: white;
            padding: 1rem;
            border-radius: 6px;
            margin-bottom: 1rem;
            font-weight: 500;
        `;
        
        const currentStepElement = document.querySelector(`.form-step[data-step="${currentStep}"]`);
        currentStepElement.insertBefore(errorElement, currentStepElement.firstChild);
    }
    
    errorElement.textContent = message;
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (errorElement.parentNode) {
            errorElement.parentNode.removeChild(errorElement);
        }
    }, 5000);
}

// Keyboard navigation
document.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && e.target.tagName !== 'TEXTAREA') {
        e.preventDefault();
        if (currentStep < totalSteps) {
            nextStep();
        } else {
            document.getElementById('submit-assessment').click();
        }
    }
    
    if (e.key === 'Escape') {
        if (currentStep > 1) {
            prevStep();
        }
    }
});

// Auto-save progress every 30 seconds
setInterval(() => {
    if (currentStep > 0) {
        saveCurrentStepData();
    }
}, 30000);