document.addEventListener('DOMContentLoaded', () => {
    const fileList = document.getElementById('file-list');
    const fileSelector = document.getElementById('file-selector');
    const dashboard = document.getElementById('dashboard');
    const changeFileBtn = document.getElementById('change-file-btn');

    let pollInterval = null;

    // Load files on startup
    loadFiles();

    changeFileBtn.addEventListener('click', () => {
        stopPolling();
        dashboard.classList.add('hidden');
        fileSelector.classList.remove('hidden');
        loadFiles();
    });

    async function loadFiles() {
        fileList.innerHTML = '<div class="loading">Caricamento files...</div>';
        try {
            const response = await fetch('/api/files');
            const files = await response.json();

            fileList.innerHTML = '';

            if (files.length === 0) {
                fileList.innerHTML = '<div class="loading">Nessun file trovato.</div>';
                return;
            }

            files.forEach(file => {
                const el = document.createElement('div');
                el.className = 'file-item';

                // Format date
                let dateStr = 'Sconosciuta';
                if (file.timeLastModified) {
                    // Check if it's a timestamp (number) or ISO string
                    const date = new Date(typeof file.timeLastModified === 'number' ? file.timeLastModified * 1000 : file.timeLastModified);
                    dateStr = date.toLocaleString();
                }

                el.innerHTML = `
                    <span class="file-name">${file.name}</span>
                    <span class="file-date">Modifica: ${dateStr}</span>
                `;

                el.addEventListener('click', () => selectFile(file));
                fileList.appendChild(el);
            });

        } catch (err) {
            console.error(err);
            fileList.innerHTML = '<div class="loading">Errore caricamento files.</div>';
        }
    }

    async function selectFile(file) {
        try {
            const response = await fetch('/api/session', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(file)
            });

            if (response.ok) {
                showDashboard(file);
            } else {
                alert('Errore avvio sessione');
            }
        } catch (err) {
            console.error(err);
            alert('Errore di connessione');
        }
    }

    function showDashboard(file) {
        fileSelector.classList.add('hidden');
        dashboard.classList.remove('hidden');
        document.getElementById('current-file-name').textContent = file.name;

        startPolling();
    }

    function startPolling() {
        updateStats(); // Immediate update
        pollInterval = setInterval(updateStats, 2000);
    }

    function stopPolling() {
        if (pollInterval) {
            clearInterval(pollInterval);
            pollInterval = null;
        }
    }

    async function updateStats() {
        try {
            const response = await fetch('/api/stats');
            const data = await response.json();

            if (data.status === 'active') {
                updateValue('stat-total', data.total);
                updateValue('stat-approvo', data.approvo);
                updateValue('stat-contro', data.contro);
                updateValue('stat-astenuto', data.astenuto);

                // Update bars
                const total = data.total || 1; // Avoid division by zero
                updateBar('bar-approvo', data.approvo, total);
                updateBar('bar-contro', data.contro, total);
                updateBar('bar-astenuto', data.astenuto, total);
            }
        } catch (err) {
            console.error("Polling error", err);
        }
    }

    function updateValue(id, value) {
        const el = document.getElementById(id);
        if (el.textContent != value) {
            el.textContent = value;
            // Simple flash effect
            el.style.color = '#fff';
            setTimeout(() => el.style.color = '', 300);
        }
    }

    function updateBar(id, value, total) {
        const percentage = (value / total) * 100;
        document.getElementById(id).style.width = `${percentage}%`;
    }

    // Shutdown Logic
    document.getElementById('shutdown-btn').addEventListener('click', async () => {
        if (confirm('Sei sicuro di voler spegnere il server?')) {
            try {
                await fetch('/api/shutdown', { method: 'POST' });
                alert('Server in arresto...');
                document.body.innerHTML = '<h1 style="text-align:center; margin-top:20%">Server Spento 👋</h1>';
            } catch (err) {
                console.error(err);
            }
        }
    });

    // Login Logic
    const loginModal = document.getElementById('login-modal');
    const loginBtn = document.getElementById('login-btn');
    const closeLoginBtn = document.getElementById('close-login-btn');
    let loginPollInterval = null;

    loginBtn.addEventListener('click', async () => {
        loginModal.classList.remove('hidden');
        document.getElementById('login-status').textContent = "Inizializzazione...";

        try {
            const response = await fetch('/api/login/sharepoint', { method: 'POST' });
            const data = await response.json();

            if (data.status === 'initiated') {
                document.getElementById('login-url').href = data.verification_uri;
                document.getElementById('login-url').textContent = data.verification_uri;
                document.getElementById('login-code').textContent = data.user_code;
                document.getElementById('login-status').textContent = "In attesa di login...";

                // Poll status
                loginPollInterval = setInterval(checkLoginStatus, 2000);
            }
        } catch (err) {
            document.getElementById('login-status').textContent = "Errore avvio login";
        }
    });

    closeLoginBtn.addEventListener('click', () => {
        loginModal.classList.add('hidden');
        if (loginPollInterval) clearInterval(loginPollInterval);
    });

    async function checkLoginStatus() {
        try {
            const response = await fetch('/api/login/status');
            const data = await response.json();

            if (data.status === 'success') {
                document.getElementById('login-status').textContent = "✅ Login Effettuato!";
                document.getElementById('login-status').style.color = '#22c55e';
                clearInterval(loginPollInterval);
                setTimeout(() => {
                    loginModal.classList.add('hidden');
                    loadFiles(); // Refresh files
                }, 1500);
            } else if (data.status === 'error') {
                document.getElementById('login-status').textContent = "❌ Errore: " + data.message;
                document.getElementById('login-status').style.color = '#ef4444';
                clearInterval(loginPollInterval);
            }
        } catch (err) {
            console.error(err);
        }
    }
});
