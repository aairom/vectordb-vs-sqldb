const API_BASE_URL = 'http://localhost:8080/api';

// DOM Elements
const initBtn = document.getElementById('initBtn');
const clearBtn = document.getElementById('clearBtn');
const statsBtn = document.getElementById('statsBtn');
const searchBtn = document.getElementById('searchBtn');
const searchInput = document.getElementById('searchInput');
const statsPanel = document.getElementById('statsPanel');
const resultsSection = document.getElementById('resultsSection');
const notification = document.getElementById('notification');
const exampleBtns = document.querySelectorAll('.example-btn');

// Event Listeners
initBtn.addEventListener('click', initializeDatabases);
clearBtn.addEventListener('click', clearDatabases);
statsBtn.addEventListener('click', toggleStats);
searchBtn.addEventListener('click', performSearch);
searchInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') performSearch();
});

exampleBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        searchInput.value = btn.dataset.query;
        performSearch();
    });
});

// API Functions
async function initializeDatabases() {
    try {
        showNotification('Initializing databases...', 'info');
        initBtn.disabled = true;
        
        const response = await fetch(`${API_BASE_URL}/initialize`, {
            method: 'POST'
        });
        
        const data = await response.json();
        
        if (data.success) {
            showNotification(data.message, 'success');
            await loadStats();
        } else {
            showNotification('Error: ' + data.error, 'error');
        }
    } catch (error) {
        showNotification('Failed to initialize databases: ' + error.message, 'error');
    } finally {
        initBtn.disabled = false;
    }
}

async function clearDatabases() {
    if (!confirm('Are you sure you want to clear all data?')) return;
    
    try {
        showNotification('Clearing databases...', 'info');
        clearBtn.disabled = true;
        
        const response = await fetch(`${API_BASE_URL}/clear`, {
            method: 'POST'
        });
        
        const data = await response.json();
        
        if (data.success) {
            showNotification(data.message, 'success');
            statsPanel.classList.add('hidden');
            resultsSection.classList.add('hidden');
        } else {
            showNotification('Error: ' + data.error, 'error');
        }
    } catch (error) {
        showNotification('Failed to clear databases: ' + error.message, 'error');
    } finally {
        clearBtn.disabled = false;
    }
}

async function loadStats() {
    try {
        const response = await fetch(`${API_BASE_URL}/stats`);
        const data = await response.json();
        
        displayStats(data);
        statsPanel.classList.remove('hidden');
    } catch (error) {
        showNotification('Failed to load statistics: ' + error.message, 'error');
    }
}

function toggleStats() {
    if (statsPanel.classList.contains('hidden')) {
        loadStats();
    } else {
        statsPanel.classList.add('hidden');
    }
}

async function performSearch() {
    const query = searchInput.value.trim();
    
    if (!query) {
        showNotification('Please enter a search query', 'error');
        return;
    }
    
    try {
        showNotification('Searching...', 'info');
        searchBtn.disabled = true;
        
        const response = await fetch(`${API_BASE_URL}/search/compare`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ query })
        });
        
        const data = await response.json();
        
        if (data.error) {
            showNotification('Error: ' + data.error, 'error');
            return;
        }
        
        displayResults(data);
        resultsSection.classList.remove('hidden');
        showNotification('Search completed!', 'success');
        
        // Scroll to results
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    } catch (error) {
        showNotification('Search failed: ' + error.message, 'error');
    } finally {
        searchBtn.disabled = false;
    }
}

// Display Functions
function displayStats(data) {
    const tradStats = data.traditional;
    const vecStats = data.vector;
    
    document.getElementById('tradStats').innerHTML = `
        <p><strong>Total Products:</strong> ${tradStats.total_products}</p>
        <p><strong>Categories:</strong> ${tradStats.total_categories}</p>
        <p><strong>Average Price:</strong> $${tradStats.avg_price}</p>
        <p><strong>Type:</strong> ${tradStats.db_type}</p>
    `;
    
    document.getElementById('vecStats').innerHTML = `
        <p><strong>Total Products:</strong> ${vecStats.total_products}</p>
        <p><strong>Categories:</strong> ${vecStats.total_categories}</p>
        <p><strong>Average Price:</strong> $${vecStats.avg_price}</p>
        <p><strong>Embeddings:</strong> ${vecStats.total_embeddings}</p>
        <p><strong>Dimensions:</strong> ${vecStats.embedding_dimension}</p>
        <p><strong>Type:</strong> ${vecStats.db_type}</p>
    `;
}

function displayResults(data) {
    const tradResults = data.traditional.results;
    const vecResults = data.vector.results;
    
    // Update execution times
    document.getElementById('tradTime').textContent = 
        `⚡ ${data.traditional.execution_time}ms (${data.traditional.count} results)`;
    document.getElementById('vecTime').textContent = 
        `⚡ ${data.vector.execution_time}ms (${data.vector.count} results)`;
    
    // Display traditional results
    const tradResultsEl = document.getElementById('tradResults');
    if (tradResults.length === 0) {
        tradResultsEl.innerHTML = '<div class="no-results">No results found</div>';
    } else {
        tradResultsEl.innerHTML = tradResults.map(product => createProductCard(product, false)).join('');
    }
    
    // Display vector results
    const vecResultsEl = document.getElementById('vecResults');
    if (vecResults.length === 0) {
        vecResultsEl.innerHTML = '<div class="no-results">No results found</div>';
    } else {
        vecResultsEl.innerHTML = vecResults.map(product => createProductCard(product, true)).join('');
    }
}

function createProductCard(product, showSimilarity) {
    const similarityBadge = showSimilarity && product.similarity 
        ? `<span class="similarity-score">Similarity: ${(product.similarity * 100).toFixed(1)}%</span>`
        : '';
    
    return `
        <div class="product-card">
            <div class="product-name">${escapeHtml(product.name)}</div>
            <div class="product-description">${escapeHtml(product.description)}</div>
            <div class="product-meta">
                <span class="product-category">${escapeHtml(product.category)}</span>
                <div>
                    <span class="product-price">$${product.price.toFixed(2)}</span>
                    ${similarityBadge}
                </div>
            </div>
        </div>
    `;
}

function showNotification(message, type = 'info') {
    notification.textContent = message;
    notification.className = 'notification';
    
    if (type === 'error') {
        notification.classList.add('error');
    }
    
    notification.classList.remove('hidden');
    
    setTimeout(() => {
        notification.classList.add('hidden');
    }, 3000);
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    showNotification('Welcome! Click "Initialize Databases" to get started.', 'info');
});

// Made with Bob
