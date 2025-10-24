// API Base URL
const API_BASE = '';

// Utilidades
function showToast(message, type = 'info') {
    const container = document.getElementById('toastContainer');
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;

    const icon = {
        success: 'fa-check-circle',
        error: 'fa-exclamation-circle',
        info: 'fa-info-circle',
        warning: 'fa-exclamation-triangle'
    }[type];

    toast.innerHTML = `
        <i class="fas ${icon}"></i>
        <span>${message}</span>
    `;

    container.appendChild(toast);

    setTimeout(() => {
        toast.remove();
    }, 5000);
}

// API Call
async function apiCall(endpoint, method = 'GET', data = null) {
    const options = {
        method,
        headers: {
            'Content-Type': 'application/json'
        }
    };

    if (data) {
        options.body = JSON.stringify(data);
    }

    try {
        const response = await fetch(API_BASE + endpoint, options);
        const result = await response.json();

        if (!result.success) {
            throw new Error(result.error || 'Error desconocido');
        }

        return result;
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// Cargar Estado del Sistema
async function loadStatus() {
    try {
        const result = await apiCall('/api/status');
        const status = result.status;

        // API Key Status
        const apiKeyStatus = document.getElementById('apiKeyStatus');
        if (status.api_key_configured) {
            apiKeyStatus.innerHTML = '<span class="badge badge-success">Configurado</span>';
        } else {
            apiKeyStatus.innerHTML = '<span class="badge badge-warning">No configurado</span>';
        }

        // AI Status
        const aiStatus = document.getElementById('aiStatus');
        if (status.ai_enabled) {
            aiStatus.innerHTML = '<span class="badge badge-success">Habilitada</span>';
        } else {
            aiStatus.innerHTML = '<span class="badge badge-danger">Deshabilitada</span>';
        }

        // Model
        document.getElementById('modelStatus').textContent = status.model || 'N/A';

        // Screen Resolution
        const screenSize = status.screen_size;
        document.getElementById('screenResolution').textContent =
            `${screenSize[0]} x ${screenSize[1]}`;

    } catch (error) {
        showToast('Error al cargar estado: ' + error.message, 'error');
    }
}

// Guardar API Key
async function saveApiKey() {
    const input = document.getElementById('apiKeyInput');
    const apiKey = input.value.trim();

    if (!apiKey) {
        showToast('Por favor ingresa una API key', 'warning');
        return;
    }

    const resultBox = document.getElementById('apiKeyResult');
    resultBox.innerHTML = '<p style="color: var(--text-secondary);">Validando API key...</p>';
    resultBox.style.display = 'block';

    try {
        const result = await apiCall('/api/config/api-key', 'POST', { api_key: apiKey });

        resultBox.innerHTML = `
            <p style="color: var(--success-color);">
                <i class="fas fa-check-circle"></i>
                ${result.message}
            </p>
            <p style="margin-top: 0.5rem;">
                <strong>Modelo:</strong> ${result.model}
            </p>
        `;

        showToast('API key configurada correctamente', 'success');

        // Recargar estado
        setTimeout(() => {
            loadStatus();
        }, 1000);

    } catch (error) {
        resultBox.innerHTML = `
            <p style="color: var(--danger-color);">
                <i class="fas fa-exclamation-circle"></i>
                Error: ${error.message}
            </p>
        `;
        showToast('Error al guardar API key: ' + error.message, 'error');
    }
}

// Toggle API Key Visibility
function toggleApiKeyVisibility() {
    const input = document.getElementById('apiKeyInput');
    const btn = document.getElementById('toggleApiKeyBtn');
    const icon = btn.querySelector('i');

    if (input.type === 'password') {
        input.type = 'text';
        icon.className = 'fas fa-eye-slash';
    } else {
        input.type = 'password';
        icon.className = 'fas fa-eye';
    }
}

// Test Connection
async function testConnection() {
    showToast('Probando conexión...', 'info');

    try {
        const result = await apiCall('/api/status');

        if (result.status.ai_enabled) {
            showToast('Conexión exitosa. IA funcionando correctamente.', 'success');
        } else {
            showToast('Servidor conectado pero IA no configurada.', 'warning');
        }
    } catch (error) {
        showToast('Error de conexión: ' + error.message, 'error');
    }
}

// Event Listeners
document.addEventListener('DOMContentLoaded', function() {
    // Cargar estado inicial
    loadStatus();

    // API Key
    document.getElementById('saveApiKeyBtn').addEventListener('click', saveApiKey);
    document.getElementById('toggleApiKeyBtn').addEventListener('click', toggleApiKeyVisibility);

    // Enter en input de API key
    document.getElementById('apiKeyInput').addEventListener('keydown', function(e) {
        if (e.key === 'Enter') {
            saveApiKey();
        }
    });

    // System Actions
    document.getElementById('testConnectionBtn').addEventListener('click', testConnection);
    document.getElementById('refreshStatusBtn').addEventListener('click', loadStatus);
});
