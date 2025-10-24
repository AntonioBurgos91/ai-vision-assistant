// API Base URL
const API_BASE = '';

// Estado global
let currentActions = [];
let foundElementLocation = null;

// Utilidades
function showLoading(text = 'Procesando...') {
    const overlay = document.getElementById('loadingOverlay');
    const loadingText = document.getElementById('loadingText');
    loadingText.textContent = text;
    overlay.style.display = 'flex';
}

function hideLoading() {
    document.getElementById('loadingOverlay').style.display = 'none';
}

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

// API Calls
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

// Check Status
async function checkStatus() {
    try {
        const result = await apiCall('/api/status');
        const indicator = document.getElementById('statusIndicator');
        const statusText = indicator.querySelector('.status-text');

        if (result.status.ai_enabled) {
            indicator.className = 'status-indicator connected';
            statusText.textContent = 'IA Conectada';
        } else {
            indicator.className = 'status-indicator error';
            statusText.textContent = 'IA No Configurada';
        }
    } catch (error) {
        const indicator = document.getElementById('statusIndicator');
        indicator.className = 'status-indicator error';
        indicator.querySelector('.status-text').textContent = 'Error de Conexión';
    }
}

// Ejecutar Instrucción
async function executeInstruction() {
    const input = document.getElementById('instructionInput');
    const instruction = input.value.trim();

    if (!instruction) {
        showToast('Por favor ingresa una instrucción', 'warning');
        return;
    }

    showLoading('Analizando instrucción con IA...');

    try {
        const result = await apiCall('/api/ai/execute', 'POST', { instruction });

        currentActions = result.actions || [];

        const resultBox = document.getElementById('instructionResult');
        resultBox.style.display = 'block';

        // Mostrar análisis
        document.getElementById('instructionAnalysis').innerHTML = `
            <h3>Análisis</h3>
            <p>${result.analysis}</p>
        `;

        // Mostrar estrategia
        document.getElementById('instructionStrategy').innerHTML = `
            <h3>Estrategia</h3>
            <p>${result.strategy}</p>
        `;

        // Mostrar acciones
        const actionsHtml = currentActions.map((action, idx) => `
            <li><strong>${idx + 1}.</strong> ${action.description || action.type}</li>
        `).join('');

        document.getElementById('instructionActions').innerHTML = `
            <h3>Acciones (${currentActions.length})</h3>
            <ol style="margin-left: 1.5rem;">${actionsHtml}</ol>
        `;

        // Mostrar advertencias
        if (result.warnings && result.warnings.length > 0) {
            const warningsHtml = result.warnings.map(w => `<li>${w}</li>`).join('');
            document.getElementById('instructionWarnings').innerHTML = `
                <h3>Advertencias</h3>
                <ul style="margin-left: 1.5rem; color: var(--warning-color);">${warningsHtml}</ul>
            `;
        } else {
            document.getElementById('instructionWarnings').innerHTML = '';
        }

        hideLoading();
        showToast('Plan generado exitosamente', 'success');

        // Scroll al resultado
        resultBox.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

    } catch (error) {
        hideLoading();
        showToast('Error: ' + error.message, 'error');
    }
}

// Confirmar y ejecutar acciones
async function confirmExecution() {
    if (currentActions.length === 0) {
        showToast('No hay acciones para ejecutar', 'warning');
        return;
    }

    showLoading('Ejecutando acciones...');

    try {
        await apiCall('/api/automation/execute', 'POST', { actions: currentActions });
        hideLoading();
        showToast('Acciones ejecutadas correctamente', 'success');
        document.getElementById('instructionResult').style.display = 'none';
        document.getElementById('instructionInput').value = '';
        currentActions = [];
    } catch (error) {
        hideLoading();
        showToast('Error al ejecutar: ' + error.message, 'error');
    }
}

// Cancelar ejecución
function cancelExecution() {
    document.getElementById('instructionResult').style.display = 'none';
    currentActions = [];
    showToast('Ejecución cancelada', 'info');
}

// Capturar Pantalla
async function captureScreen() {
    showLoading('Capturando pantalla...');

    try {
        const result = await apiCall('/api/capture/screen');
        const preview = document.getElementById('screenPreview');
        preview.innerHTML = `<img src="${result.image}" alt="Captura de pantalla" />`;
        hideLoading();
        showToast('Pantalla capturada', 'success');
    } catch (error) {
        hideLoading();
        showToast('Error: ' + error.message, 'error');
    }
}

// Analizar Pantalla
async function analyzeScreen() {
    showLoading('Analizando pantalla con IA...');

    try {
        const result = await apiCall('/api/ai/analyze', 'POST', {});
        const analysisBox = document.getElementById('analysisResult');
        analysisBox.innerHTML = `<p>${result.analysis}</p>`;
        analysisBox.style.display = 'block';
        hideLoading();
        showToast('Análisis completado', 'success');
    } catch (error) {
        hideLoading();
        showToast('Error: ' + error.message, 'error');
    }
}

// Refrescar Lista de Ventanas
async function refreshWindows() {
    showLoading('Actualizando lista de ventanas...');

    try {
        const result = await apiCall('/api/windows');
        const windowsList = document.getElementById('windowsList');

        if (result.windows.length === 0) {
            windowsList.innerHTML = '<p style="color: var(--text-secondary); padding: 1rem;">No hay ventanas abiertas</p>';
        } else {
            const html = result.windows.map(window => `
                <div class="window-item ${window.is_active ? 'active' : ''}">
                    <div class="window-title">${window.title}</div>
                    <div class="window-actions">
                        <button class="btn btn-sm btn-secondary" onclick="focusWindow(${window.index})">
                            <i class="fas fa-expand"></i> Enfocar
                        </button>
                        <button class="btn btn-sm btn-primary" onclick="captureWindow(${window.index})">
                            <i class="fas fa-camera"></i> Capturar
                        </button>
                    </div>
                </div>
            `).join('');

            windowsList.innerHTML = html;
        }

        hideLoading();
        showToast(`${result.count} ventanas encontradas`, 'success');
    } catch (error) {
        hideLoading();
        showToast('Error: ' + error.message, 'error');
    }
}

// Enfocar Ventana
async function focusWindow(index) {
    showLoading('Enfocando ventana...');

    try {
        await apiCall(`/api/windows/focus/${index}`, 'POST');
        hideLoading();
        showToast('Ventana enfocada', 'success');
        setTimeout(refreshWindows, 500);
    } catch (error) {
        hideLoading();
        showToast('Error: ' + error.message, 'error');
    }
}

// Capturar Ventana
async function captureWindow(index) {
    showLoading('Capturando ventana...');

    try {
        const result = await apiCall(`/api/capture/window/${index}`);
        const preview = document.getElementById('screenPreview');
        preview.innerHTML = `
            <img src="${result.image}" alt="Captura de ventana" />
            <p style="text-align: center; margin-top: 0.5rem; color: var(--text-secondary);">${result.window_title}</p>
        `;
        hideLoading();
        showToast('Ventana capturada', 'success');
    } catch (error) {
        hideLoading();
        showToast('Error: ' + error.message, 'error');
    }
}

// Buscar Elemento
async function findElement() {
    const input = document.getElementById('elementDescription');
    const description = input.value.trim();

    if (!description) {
        showToast('Por favor describe el elemento a buscar', 'warning');
        return;
    }

    showLoading('Buscando elemento...');

    try {
        const result = await apiCall('/api/ai/find-element', 'POST', { description });
        const resultBox = document.getElementById('findElementResult');
        const clickBtn = document.getElementById('clickElementBtn');

        if (result.found) {
            foundElementLocation = { x: result.x, y: result.y };
            resultBox.innerHTML = `
                <p><i class="fas fa-check-circle" style="color: var(--success-color);"></i>
                Elemento encontrado en posición: <strong>(${result.x}, ${result.y})</strong></p>
            `;
            resultBox.style.display = 'block';
            clickBtn.style.display = 'inline-flex';
            showToast('Elemento encontrado', 'success');
        } else {
            foundElementLocation = null;
            resultBox.innerHTML = `
                <p><i class="fas fa-times-circle" style="color: var(--danger-color);"></i>
                Elemento no encontrado</p>
            `;
            resultBox.style.display = 'block';
            clickBtn.style.display = 'none';
            showToast('Elemento no encontrado', 'warning');
        }

        hideLoading();
    } catch (error) {
        hideLoading();
        showToast('Error: ' + error.message, 'error');
    }
}

// Hacer clic en elemento encontrado
async function clickElement() {
    if (!foundElementLocation) {
        showToast('No hay elemento para hacer clic', 'warning');
        return;
    }

    showLoading('Haciendo clic...');

    try {
        await apiCall('/api/automation/click', 'POST', {
            x: foundElementLocation.x,
            y: foundElementLocation.y
        });
        hideLoading();
        showToast('Clic ejecutado', 'success');
    } catch (error) {
        hideLoading();
        showToast('Error: ' + error.message, 'error');
    }
}

// Escritura rápida
async function quickType() {
    const input = document.getElementById('quickTypeText');
    const text = input.value.trim();

    if (!text) {
        showToast('Por favor ingresa texto para escribir', 'warning');
        return;
    }

    showLoading('Escribiendo texto...');

    try {
        await apiCall('/api/automation/type', 'POST', { text });
        hideLoading();
        showToast('Texto escrito', 'success');
        input.value = '';
    } catch (error) {
        hideLoading();
        showToast('Error: ' + error.message, 'error');
    }
}

// Actualizar posición del mouse
function updateMousePosition() {
    // Esta funcionalidad requeriría WebSocket o polling
    // Por ahora solo mostramos un placeholder
    const mousePos = document.getElementById('mousePosition');
    mousePos.textContent = 'Mueve el mouse sobre la aplicación';
}

// Event Listeners
document.addEventListener('DOMContentLoaded', function() {
    // Check status on load
    checkStatus();

    // Instrucciones
    document.getElementById('executeInstructionBtn').addEventListener('click', executeInstruction);
    document.getElementById('confirmExecutionBtn').addEventListener('click', confirmExecution);
    document.getElementById('cancelExecutionBtn').addEventListener('click', cancelExecution);

    // Enter en textarea
    document.getElementById('instructionInput').addEventListener('keydown', function(e) {
        if (e.ctrlKey && e.key === 'Enter') {
            executeInstruction();
        }
    });

    // Captura de pantalla
    document.getElementById('captureScreenBtn').addEventListener('click', captureScreen);
    document.getElementById('analyzeScreenBtn').addEventListener('click', analyzeScreen);

    // Ventanas
    document.getElementById('refreshWindowsBtn').addEventListener('click', refreshWindows);

    // Buscar elemento
    document.getElementById('findElementBtn').addEventListener('click', findElement);
    document.getElementById('clickElementBtn').addEventListener('click', clickElement);

    // Acciones rápidas
    document.getElementById('quickTypeBtn').addEventListener('click', quickType);

    // Auto-refresh windows on load
    refreshWindows();
});
