```js
// ============================================
// HBnB - Unified JavaScript File (scripts.js)
// FIXED: Removed demo login, proper API authentication
// ============================================

// ========== API CONFIGURATION ==========
const API_BASE_URL = 'http://127.0.0.1:5000/api/v1';

// ========== MOCK DATA ==========
const MOCK_PLACES = [
    {
        id: 1,
        title: 'Lavender Resort',
        name: 'Lavender Resort',
        price: 1200,
        location: 'North Riyadh',
        city_name: 'Riyadh',
        rating: 4.6,
        image_url: 'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=400',
        description: 'Experience luxury and relaxation at Lavender Resort. Features premium amenities and exceptional service in north Riyadh.',
        amenities: [
            { name: 'wifi' },
            { name: 'pool' },
            { name: 'parking' },
            { name: 'breakfast' }
        ],
        host_name: 'Hessa A.'
    },
    {
        id: 2,
        title: 'Golden Palm Chalets',
        name: 'Golden Palm Chalets',
        price: 900,
        location: 'East Riyadh',
        city_name: 'Riyadh',
        rating: 4.4,
        image_url: 'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=400',
        description: 'Golden Palm Chalets offer the perfect family getaway with spacious accommodations and entertainment facilities.',
        amenities: [
            { name: 'wifi' },
            { name: 'pool' },
            { name: 'bbq' },
            { name: 'parking' }
        ],
        host_name: 'Mohammed A.'
    },
    {
        id: 3,
        title: 'Kingdom View Hotel',
        name: 'Kingdom View Hotel',
        price: 2000,
        location: 'Olaya, Riyadh',
        city_name: 'Riyadh',
        rating: 4.8,
        image_url: 'https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=400',
        description: 'Luxury hotel in the heart of Olaya with panoramic city views and premium business facilities.',
        amenities: [
            { name: 'wifi' },
            { name: 'gym' },
            { name: 'restaurant' },
            { name: 'parking' }
        ],
        host_name: 'Abdullah H.'
    },
    {
        id: 4,
        title: 'Wadi Escape Cabin',
        name: 'Wadi Escape Cabin',
        price: 700,
        location: 'Wadi Hanifah',
        city_name: 'Riyadh',
        rating: 4.3,
        image_url: 'https://images.unsplash.com/photo-1449158743715-0a90ebb6d2d8?w=400',
        description: 'Escape to nature at Wadi Escape Cabin. Nestled in Wadi Hanifah, this cozy cabin offers tranquility and comfort.',
        amenities: [
            { name: 'wifi' },
            { name: 'fireplace' },
            { name: 'coffee' },
            { name: 'parking' }
        ],
        host_name: 'Sultan M.'
    },
    {
        id: 5,
        title: 'Diriyah Heritage Stay',
        name: 'Diriyah Heritage Stay',
        price: 1500,
        location: 'Diriyah',
        city_name: 'Riyadh',
        rating: 4.5,
        image_url: 'https://images.unsplash.com/photo-1568605114967-8130f3a36994?w=400',
        description: 'Experience Saudi heritage at Diriyah Heritage Stay. Located in the historic district, this property combines tradition with modern comfort.',
        amenities: [
            { name: 'wifi' },
            { name: 'breakfast' },
            { name: 'heritage' },
            { name: 'parking' }
        ],
        host_name: 'Nora T.'
    },
    {
        id: 6,
        title: 'Moonlight Apartment',
        name: 'Moonlight Apartment',
        price: 1000,
        location: 'Hittin',
        city_name: 'Riyadh',
        rating: 4.2,
        image_url: 'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=400',
        description: 'Modern luxury apartment in Hittin. Perfect for extended stays with full kitchen and premium amenities.',
        amenities: [
            { name: 'wifi' },
            { name: 'kitchen' },
            { name: 'laundry' },
            { name: 'ac' }
        ],
        host_name: 'Lina K.'
    }
];

const MOCK_REVIEWS = [
    {
        id: 1,
        user_name: 'Hessa A.',
        rating: 5,
        text: 'Clean, calm, and the services were perfect.',
        date: '2025-03-12'
    },
    {
        id: 2,
        user_name: 'Nawaf K.',
        rating: 4.5,
        text: 'Great location and smooth check-in.',
        date: '2025-01-28'
    },
    {
        id: 3,
        user_name: 'Sara M.',
        rating: 4.5,
        text: 'Loved the Wi-Fi and the overall comfort.',
        date: '2024-11-05'
    }
];

// ========== COOKIE HELPERS ==========
function setCookie(name, value, days = 7) {
    const expires = new Date();
    expires.setTime(expires.getTime() + days * 24 * 60 * 60 * 1000);
    document.cookie = `${name}=${value};expires=${expires.toUTCString()};path=/;SameSite=Strict`;
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

function deleteCookie(name) {
    document.cookie = `${name}=;expires=Thu, 01 Jan 1970 00:00:00 UTC;path=/;`;
}

// ========== AUTH HELPERS ==========
function isAuthenticated() {
    return !!getCookie('token');
}

function getAuthToken() {
    return getCookie('token');
}

// ========== STORAGE KEYS ==========
const STORAGE_KEYS = {
    LANG: 'hbnb_lang'
};

// ========== STORAGE HELPERS ==========
function getItem(key) {
    try {
        const item = localStorage.getItem(key);
        return item ? JSON.parse(item) : null;
    } catch (e) {
        return null;
    }
}

function setItem(key, value) {
    try {
        localStorage.setItem(key, JSON.stringify(value));
        return true;
    } catch (e) {
        return false;
    }
}

// ========== GLOBAL VARIABLES ==========
let currentLang = getItem(STORAGE_KEYS.LANG) || 'en';
let currentRating = 0;

// ========== ICONS ==========
const ICONS = {
    star: '<svg class="w-3.5 h-3.5 text-yellow-500" fill="currentColor" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/></svg>',
    starBig: '<svg class="w-8 h-8" fill="currentColor" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/></svg>',
    pin: '<svg class="w-3.5 h-3.5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/></svg>',
    close: '<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>'
};

const AMENITY_ICONS = {
    wifi: '<svg class="w-5 h-5 text-[#9B7BB8]" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.8"><path stroke-linecap="round" stroke-linejoin="round" d="M8.111 16.404a5.5 5.5 0 017.778 0M12 20h.01m-7.08-7.071c3.904-3.905 10.236-3.905 14.14 0M1.394 9.393c5.857-5.857 15.355-5.857 21.213 0"/></svg>',
    pool: '<svg class="w-5 h-5 text-[#9B7BB8]" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.8"><rect x="2" y="6" width="20" height="12" rx="2"/><path d="M2 10h20M2 14h20"/></svg>',
    parking: '<svg class="w-5 h-5 text-[#9B7BB8]" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.8"><path d="M5 13l4 4L19 7"/></svg>',
    breakfast: '<svg class="w-5 h-5 text-[#9B7BB8]" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.8"><path d="M3 11h18v2a9 9 0 01-9 9h0a9 9 0 01-9-9v-2z"/><path d="M7 11V8a5 5 0 0110 0v3"/></svg>',
    gym: '<svg class="w-5 h-5 text-[#9B7BB8]" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.8"><rect x="2" y="6" width="20" height="12" rx="2"/><path d="M2 10h20M2 14h20"/></svg>',
    restaurant: '<svg class="w-5 h-5 text-[#9B7BB8]" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.8"><path d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>',
    bbq: '<svg class="w-5 h-5 text-[#9B7BB8]" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.8"><rect x="4" y="11" width="16" height="4" rx="1"/><path d="M8 11V6a4 4 0 018 0v5"/></svg>',
    fireplace: '<svg class="w-5 h-5 text-[#9B7BB8]" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.8"><path d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"/></svg>',
    coffee: '<svg class="w-5 h-5 text-[#9B7BB8]" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.8"><path d="M8 5H6a2 2 0 00-2 2v6a2 2 0 002 2h2m4-10h2a2 2 0 012 2v6a2 2 0 01-2 2h-2M4 15h16"/></svg>',
    kitchen: '<svg class="w-5 h-5 text-[#9B7BB8]" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.8"><path d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/></svg>',
    laundry: '<svg class="w-5 h-5 text-[#9B7BB8]" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.8"><rect x="2" y="7" width="20" height="12" rx="2"/><path d="M2 11h20"/></svg>',
    ac: '<svg class="w-5 h-5 text-[#9B7BB8]" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.8"><rect x="2" y="7" width="20" height="12" rx="2"/><path d="M9 11l3-3 3 3"/></svg>',
    heritage: '<svg class="w-5 h-5 text-[#9B7BB8]" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.8"><path d="M19 21H5a2 2 0 01-2-2V5a2 2 0 012-2h11l5 5v11a2 2 0 01-2 2z"/><path d="M17 21v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4"/></svg>'
};

// ========== TOAST ==========
function showToast(message, duration = 3000) {
    const toast = document.getElementById('toast');
    if (!toast) return;
    toast.textContent = message;
    toast.classList.add('show');
    setTimeout(() => toast.classList.remove('show'), duration);
}

// ========== LANGUAGE ==========
function toggleLanguage() {
    currentLang = currentLang === 'en' ? 'ar' : 'en';
    setItem(STORAGE_KEYS.LANG, currentLang);
    document.documentElement.dir = currentLang === 'ar' ? 'rtl' : 'ltr';
    
    const langIndicator = document.getElementById('lang-indicator');
    if (langIndicator) {
        langIndicator.textContent = currentLang === 'en' ? 'EN' : 'عربي';
    }
    
    showToast(currentLang === 'en' ? 'Language switched' : 'تم التبديل');
}

// ========== AUTH UI ==========
function updateAuthUI() {
    const authLinks = document.getElementById('auth-links');
    const userMenu = document.getElementById('user-menu-container');
    const dropdownName = document.getElementById('dropdown-name');
    const dropdownEmail = document.getElementById('dropdown-email');
    const avatarInitial = document.getElementById('avatar-initial');
    
    if (isAuthenticated()) {
        if (authLinks) authLinks.innerHTML = '';
        if (userMenu) userMenu.classList.remove('hidden');
        
        const token = getAuthToken();
        try {
            const payload = JSON.parse(atob(token.split('.')[1]));
            if (dropdownName) dropdownName.textContent = payload.name || 'User';
            if (dropdownEmail) dropdownEmail.textContent = payload.email || '';
            if (avatarInitial) avatarInitial.textContent = (payload.name || 'U').charAt(0).toUpperCase();
        } catch (e) {
            if (dropdownName) dropdownName.textContent = 'User';
            if (avatarInitial) avatarInitial.textContent = 'U';
        }
    } else {
        if (authLinks) {
            authLinks.innerHTML = '<a href="login.html" class="login-button nav-link px-2 py-1 text-gray-600" data-nav-link>Login</a>';
        }
        if (userMenu) userMenu.classList.add('hidden');
    }
}

function toggleUserDropdown() {
    const dropdown = document.getElementById('user-dropdown');
    if (dropdown) dropdown.classList.toggle('hidden');
}

function handleLogout() {
    deleteCookie('token');
    updateAuthUI();
    showToast('Logged out successfully');
    
    const dropdown = document.getElementById('user-dropdown');
    if (dropdown) dropdown.classList.add('hidden');
    
    const page = document.body.dataset.page;
    if (page === 'add-review' || page === 'login') {
        window.location.href = 'index.html';
    }
}

// ========== LOGIN API - FIXED: Removed demo login completely ==========
async function handleLogin(event) {
    event.preventDefault();
    
    const email = document.getElementById('login-email')?.value;
    const password = document.getElementById('login-password')?.value;
    const errorContainer = document.getElementById('login-error');
    const errorText = document.getElementById('login-error-text');
    
    if (!email || !password) {
        if (errorContainer && errorText) {
            errorText.textContent = 'Please fill in all fields';
            errorContainer.classList.remove('hidden');
        } else {
            showToast('Please fill in all fields');
        }
        return;
    }
    
    // Disable submit button to prevent double submission
    const submitBtn = event.target.querySelector('button[type="submit"]');
    if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.classList.add('opacity-50', 'cursor-not-allowed');
        submitBtn.textContent = 'Signing in...';
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: email.trim(), password })
        });
        
        const data = await response.json();
        
        if (response.ok && data.access_token) {
            // Store token in cookie
            setCookie('token', data.access_token);
            showToast('Login successful!');
            updateAuthUI();
            
            // Hide error if visible
            if (errorContainer) errorContainer.classList.add('hidden');
            
            // Redirect to index.html
            setTimeout(() => window.location.href = 'index.html', 1000);
        } else {
            // Show error message from API
            const errorMsg = data.message || data.error || 'Invalid email or password';
            if (errorContainer && errorText) {
                errorText.textContent = errorMsg;
                errorContainer.classList.remove('hidden');
            } else {
                showToast(errorMsg);
            }
            
            // Re-enable submit button
            if (submitBtn) {
                submitBtn.disabled = false;
                submitBtn.classList.remove('opacity-50', 'cursor-not-allowed');
                submitBtn.textContent = 'Sign In';
            }
        }
    } catch (error) {
        console.error('Login error:', error);
        
        let errorMsg = 'Network error. Please check your connection.';
        if (error.message.includes('Failed to fetch')) {
            errorMsg = 'Unable to connect to server. Please make sure the backend is running.';
        }
        
        if (errorContainer && errorText) {
            errorText.textContent = errorMsg;
            errorContainer.classList.remove('hidden');
        } else {
            showToast(errorMsg);
        }
        
        // Re-enable submit button
        if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.classList.remove('opacity-50', 'cursor-not-allowed');
            submitBtn.textContent = 'Sign In';
        }
    }
}

// ========== FETCH PLACES ==========
async function fetchPlaces() {
    try {
        const response = await fetch(`${API_BASE_URL}/places/`, {
            headers: isAuthenticated() ? { Authorization: `Bearer ${getAuthToken()}` } : {}
        });
        if (response.ok) return await response.json();
        return MOCK_PLACES;
    } catch (error) {
        console.warn('Using mock places');
        return MOCK_PLACES;
    }
}

// ========== RENDER PLACES FOR INDEX ==========
async function renderPlacesList() {
    const container = document.getElementById('places-list');
    if (!container) return;
    
    container.innerHTML = `<div class="col-span-3 text-center py-12"><div class="inline-block animate-spin rounded-full h-8 w-8 border-4 border-[#9B7BB8] border-t-transparent"></div><p class="mt-4 text-gray-600">Loading places...</p></div>`;
    
    const places = await fetchPlaces();
    
    if (!places || places.length === 0) {
        container.innerHTML = `<div class="col-span-3 text-center py-12"><p class="text-gray-600">No places found.</p></div>`;
        return;
    }
    
    const priceFilter = document.getElementById('price-filter-index')?.value;
    let filteredPlaces = places;
    
    if (priceFilter && priceFilter !== '0' && priceFilter !== '') {
        const maxPrice = parseInt(priceFilter);
        filteredPlaces = places.filter(p => (p.price || 0) <= maxPrice);
    }
    
    container.innerHTML = filteredPlaces.map(place => createPlaceCard(place)).join('');
    
    document.getElementById('places-count')?.textContent = `${filteredPlaces.length} place${filteredPlaces.length !== 1 ? 's' : ''} found`;
    
    container.querySelectorAll('.place-card').forEach(card => {
        card.addEventListener('click', function(e) {
            e.preventDefault();
            const placeId = this.dataset.placeId;
            window.location.href = `place.html?id=${placeId}`;
        });
    });
}

// ========== RENDER ALL PLACES FOR PLACE PAGE ==========
async function renderAllPlacesPage() {
    const container = document.getElementById('all-places-grid');
    if (!container) return;
    
    container.innerHTML = `<div class="col-span-3 text-center py-12"><div class="inline-block animate-spin rounded-full h-8 w-8 border-4 border-[#9B7BB8] border-t-transparent"></div><p class="mt-4 text-gray-600">Loading places...</p></div>`;
    
    const places = await fetchPlaces();
    
    if (!places || places.length === 0) {
        container.innerHTML = `<div class="col-span-3 text-center py-12"><p class="text-gray-600">No places found.</p></div>`;
        return;
    }
    
    const priceFilter = document.getElementById('price-filter')?.value;
    let filteredPlaces = places;
    
    if (priceFilter && priceFilter !== '') {
        const maxPrice = parseInt(priceFilter);
        filteredPlaces = places.filter(p => (p.price || 0) <= maxPrice);
    }
    
    container.innerHTML = filteredPlaces.map(place => createPlaceCard(place)).join('');
    
    document.getElementById('places-count')?.textContent = filteredPlaces.length;
    
    container.querySelectorAll('.place-card').forEach(card => {
        card.addEventListener('click', function(e) {
            e.preventDefault();
            const placeId = this.dataset.placeId;
            window.location.href = `place.html?id=${placeId}`;
        });
    });
}

function createPlaceCard(place) {
    return `
        <div class="place-card" data-place-id="${place.id}">
            <img src="${place.image_url || place.image || 'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=400'}" 
                class="w-full h-48 object-cover" alt="${place.title || place.name}" loading="lazy">
            <div class="p-4">
                <div class="flex justify-between items-start mb-2">
                    <h3 class="font-display font-bold text-gray-900">${place.title || place.name}</h3>
                    <span class="rating-badge text-xs flex items-center">
                        ${ICONS.star} <span class="ml-0.5">${place.rating || '4.5'}</span>
                    </span>
                </div>
                <div class="flex items-center gap-1 text-gray-500 text-xs mb-3">
                    ${ICONS.pin} <span>${place.location || place.city_name || 'Riyadh'}</span>
                </div>
                <div class="flex items-center justify-between">
                    <span class="text-[#9B7BB8] font-bold">${place.price || 0} SAR</span>
                    <span class="text-gray-500 text-xs">/ night</span>
                </div>
            </div>
        </div>
    `;
}

// ========== PLACE DETAILS ==========
async function fetchPlaceById(placeId) {
    try {
        const response = await fetch(`${API_BASE_URL}/places/${placeId}`, {
            headers: isAuthenticated() ? { Authorization: `Bearer ${getAuthToken()}` } : {}
        });
        if (response.ok) return await response.json();
        return MOCK_PLACES.find(p => p.id == placeId) || MOCK_PLACES[0];
    } catch (error) {
        return MOCK_PLACES.find(p => p.id == placeId) || MOCK_PLACES[0];
    }
}

async function renderPlaceDetails() {
    const urlParams = new URLSearchParams(window.location.search);
    const placeId = urlParams.get('id');
    
    const loadingSpinner = document.getElementById('loading-spinner');
    const errorMessage = document.getElementById('error-message');
    const detailsContainer = document.getElementById('place-details-container');
    const addReviewSection = document.getElementById('add-review-section');
    const loginPromptSection = document.getElementById('login-prompt-section');
    const addReviewBtn = document.getElementById('add-review-btn');
    
    if (!placeId) {
        if (loadingSpinner) loadingSpinner.classList.add('hidden');
        if (errorMessage) errorMessage.classList.remove('hidden');
        showToast('No place selected');
        return;
    }
    
    try {
        const place = await fetchPlaceById(placeId);
        
        if (!place) throw new Error('Place not found');
        
        if (loadingSpinner) loadingSpinner.classList.add('hidden');
        if (errorMessage) errorMessage.classList.add('hidden');
        if (detailsContainer) detailsContainer.classList.remove('hidden');
        
        const placeDetailsEl = document.querySelector('.place-details');
        if (placeDetailsEl) {
            placeDetailsEl.innerHTML = renderPlaceDetailsHTML(place);
        }
        
        // ===== AUTHENTICATION LOGIC =====
        if (isAuthenticated()) {
            // User is logged in → Show Add Review button
            if (addReviewSection) {
                addReviewSection.classList.remove('hidden');
                addReviewBtn.href = `add_review.html?place_id=${placeId}`;
            }
            if (loginPromptSection) loginPromptSection.classList.add('hidden');
        } else {
            // User is not logged in → Show Login Prompt
            if (addReviewSection) addReviewSection.classList.add('hidden');
            if (loginPromptSection) loginPromptSection.classList.remove('hidden');
        }
        
        await renderReviews(placeId);
        
    } catch (error) {
        console.error('Error:', error);
        if (loadingSpinner) loadingSpinner.classList.add('hidden');
        if (errorMessage) errorMessage.classList.remove('hidden');
        showToast('Failed to load place details');
    }
}

function renderPlaceDetailsHTML(place) {
    const amenities = place.amenities || [];
    
    return `
        <div class="bg-white rounded-xl shadow-md overflow-hidden border border-gray-200">
            <img src="${place.image_url || place.image || 'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800'}" 
                alt="${place.title || place.name}" class="w-full h-96 object-cover">
            <div class="p-6">
                <div class="flex flex-col md:flex-row md:items-start md:justify-between gap-4 mb-6">
                    <div>
                        <h1 class="font-display text-3xl font-bold text-gray-900 mb-2">${place.title || place.name}</h1>
                        <div class="flex items-center gap-2 text-gray-600">
                            ${ICONS.pin} <span>${place.location || place.city_name || 'Riyadh'}</span>
                        </div>
                    </div>
                    <div class="flex items-baseline gap-1">
                        <span class="text-3xl font-bold text-[#9B7BB8]">${place.price || 0}</span>
                        <span class="text-gray-500">SAR/night</span>
                    </div>
                </div>
                
                <div class="mb-6">
                    <h2 class="font-display text-xl font-bold text-gray-900 mb-3">About this place</h2>
                    <p class="text-gray-600 leading-relaxed">${place.description || 'No description available.'}</p>
                </div>
                
                <div class="mb-6">
                    <h2 class="font-display text-xl font-bold text-gray-900 mb-3">Amenities</h2>
                    <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
                        ${amenities.length > 0 ? amenities.map(a => {
                            const name = a.name || a;
                            return `
                                <div class="flex items-center gap-2 bg-gray-50 px-3 py-2 rounded-lg border border-gray-100">
                                    ${AMENITY_ICONS[name.toLowerCase()] || ''}
                                    <span class="text-sm font-medium text-gray-700 capitalize">${name}</span>
                                </div>
                            `;
                        }).join('') : '<p class="text-gray-500">No amenities listed.</p>'}
                    </div>
                </div>
                
                <div class="border-t border-gray-100 pt-6">
                    <h2 class="font-display text-xl font-bold text-gray-900 mb-3">Host</h2>
                    <div class="flex items-center gap-3">
                        <div class="w-12 h-12 bg-gradient-to-br from-[#9B7BB8] to-[#7A5A9A] rounded-full flex items-center justify-center text-white font-bold text-lg">
                            ${(place.host_name || 'H').charAt(0).toUpperCase()}
                        </div>
                        <div>
                            <p class="font-semibold text-gray-900">${place.host_name || 'Anonymous Host'}</p>
                            <p class="text-sm text-gray-500">Host since 2025</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
}

// ========== REVIEWS ==========
async function fetchReviews(placeId) {
    try {
        // Backend exposes: GET /api/v1/reviews/  (NOT /places/<id>/reviews)
        const response = await fetch(`${API_BASE_URL}/reviews/`, {
            headers: isAuthenticated() ? { Authorization: `Bearer ${getAuthToken()}` } : {}
        });

        if (!response.ok) return MOCK_REVIEWS;

        const allReviews = await response.json();

        // Filter reviews client-side by place_id
        const filtered = (allReviews || []).filter(r => String(r.place_id) === String(placeId));
        return filtered;
    } catch (error) {
        return MOCK_REVIEWS;
    }
}

async function renderReviews(placeId) {
    const reviewsContainer = document.getElementById('reviews-container');
    if (!reviewsContainer) return;
    
    try {
        const reviews = await fetchReviews(placeId);
        
        if (!reviews || reviews.length === 0) {
            reviewsContainer.innerHTML = `<div class="text-center py-8 bg-gray-50 rounded-lg"><p class="text-gray-500">No reviews yet. Be the first to review this place!</p></div>`;
            return;
        }
        
        reviewsContainer.innerHTML = reviews.map(review => `
            <div class="review-card">
                <div class="flex items-start justify-between mb-2">
                    <div class="flex items-center gap-2">
                        <div class="w-10 h-10 bg-[#9B7BB8] rounded-full flex items-center justify-center text-white font-bold">
                            ${(review.user_name || 'U').charAt(0).toUpperCase()}
                        </div>
                        <div>
                            <h4 class="font-semibold text-gray-900">${review.user_name || 'Anonymous'}</h4>
                            <p class="text-xs text-gray-500">${new Date(review.date || review.created_at || Date.now()).toLocaleDateString()}</p>
                        </div>
                    </div>
                    <span class="flex items-center gap-1 bg-yellow-50 px-2 py-1 rounded-full text-xs font-semibold">
                        ${ICONS.star} ${review.rating}
                    </span>
                </div>
                <p class="text-gray-600 text-sm mt-2">${review.text || review.comment || 'No comment provided.'}</p>
            </div>
        `).join('');
        
    } catch (error) {
        reviewsContainer.innerHTML = `<div class="text-center py-8 bg-red-50 rounded-lg"><p class="text-red-600">Failed to load reviews.</p></div>`;
    }
}

// ========== ADD REVIEW ==========
async function initAddReviewPage() {
    if (!isAuthenticated()) {
        showToast('Please login to write a review');
        setTimeout(() => window.location.href = 'index.html', 1500);
        return;
    }
    
    const placeId = new URLSearchParams(window.location.search).get('place_id');
    
    if (!placeId) {
        showToast('No place selected');
        setTimeout(() => window.location.href = 'place.html', 1500);
        return;
    }
    
    const loadingEl = document.getElementById('review-loading');
    const placePreview = document.getElementById('place-preview');
    const formContainer = document.getElementById('review-form-container');
    
    if (loadingEl) loadingEl.classList.add('hidden');
    if (placePreview) placePreview.classList.remove('hidden');
    if (formContainer) formContainer.classList.remove('hidden');
    
    await loadPlacePreview(placeId);
    initRatingStars();
    setupCharCounter();
}

async function loadPlacePreview(placeId) {
    const preview = document.getElementById('place-preview');
    if (!preview) return;
    
    try {
        const place = await fetchPlaceById(placeId);
        preview.innerHTML = `
            <div class="place-preview-content">
                <img src="${place.image_url || place.image || 'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=400'}" 
                    class="place-preview-image" alt="${place.title || place.name}">
                <div class="place-preview-info">
                    <h3 class="place-preview-name">${place.title || place.name}</h3>
                    <p class="place-preview-location">${place.location || place.city_name || 'Riyadh'}</p>
                    <div class="place-preview-price">
                        <span class="place-price-amount">${place.price} SAR</span>
                        <span class="place-price-unit">/ night</span>
                    </div>
                </div>
            </div>
        `;
    } catch (error) {
        preview.innerHTML = `<div class="bg-red-50 border border-red-200 rounded-lg p-4 text-center"><p class="text-red-600">Failed to load place details.</p></div>`;
    }
}

function initRatingStars() {
    const starsContainer = document.getElementById('rating-stars');
    const ratingInput = document.getElementById('rating-value');
    const ratingLabel = document.getElementById('rating-label');
    
    if (!starsContainer) return;
    
    let starsHTML = '';
    for (let i = 1; i <= 5; i++) {
        starsHTML += `<div class="rating-star star-inactive" data-rating="${i}">${ICONS.starBig}</div>`;
    }
    starsContainer.innerHTML = starsHTML;
    
    document.querySelectorAll('.rating-star').forEach(star => {
        star.addEventListener('mouseover', function() {
            const rating = parseInt(this.dataset.rating);
            document.querySelectorAll('.rating-star').forEach((s, i) => {
                if (i < rating) {
                    s.classList.add('star-active');
                    s.classList.remove('star-inactive');
                } else {
                    s.classList.remove('star-active');
                    s.classList.add('star-inactive');
                }
            });
        });
        
        star.addEventListener('mouseout', () => highlightStars(currentRating));
        
        star.addEventListener('click', function() {
            currentRating = parseInt(this.dataset.rating);
            if (ratingInput) ratingInput.value = currentRating;
            
            if (ratingLabel) {
                const labels = ['', 'Poor', 'Fair', 'Good', 'Very Good', 'Excellent'];
                ratingLabel.textContent = labels[currentRating];
                ratingLabel.classList.add('active');
            }
            
            highlightStars(currentRating);
        });
    });
}

function highlightStars(rating) {
    document.querySelectorAll('.rating-star').forEach((s, i) => {
        if (i < rating) {
            s.classList.add('star-active');
            s.classList.remove('star-inactive');
        } else {
            s.classList.remove('star-active');
            s.classList.add('star-inactive');
        }
    });
}

function setupCharCounter() {
    const reviewText = document.getElementById('review-text');
    const charCount = document.getElementById('char-count');
    
    if (reviewText && charCount) {
        reviewText.addEventListener('input', function() {
            const count = this.value.length;
            charCount.textContent = `${count}/500`;
            charCount.classList.toggle('warning', count > 500);
        });
    }
}

async function handleSubmitReview(event) {
    event.preventDefault();
    
    if (!isAuthenticated()) {
        showToast('You must be logged in');
        setTimeout(() => window.location.href = 'login.html', 1500);
        return;
    }
    
    const placeId = new URLSearchParams(window.location.search).get('place_id');
    const rating = currentRating;
    const text = document.getElementById('review-text')?.value;
    
    if (rating === 0) { showToast('Please select a rating'); return; }
    if (!text || !text.trim()) { showToast('Please write your review'); return; }
    if (text.length > 500) { showToast('Review must be less than 500 characters'); return; }
    if (!placeId) { showToast('No place selected'); return; }
    
    try {
        const response = await fetch(`${API_BASE_URL}/reviews/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${getAuthToken()}`
            },
            body: JSON.stringify({
                text: text.trim(),
                rating: Number(rating),
                place_id: String(placeId)
            })
        });

        const data = await response.json().catch(() => ({}));

        if (!response.ok) {
            const msg = data.message || data.error || 'Failed to submit review';
            showToast(msg);
            return;
        }

        showToast('Review submitted successfully!');
        setTimeout(() => {
            window.location.href = `place.html?id=${placeId}`;
        }, 1200);

    } catch (error) {
        console.error('Submit review error:', error);
        showToast('Unable to connect to server. Please make sure the backend is running.');
    }
}

// ========== INITIALIZATION ==========
function initApp() {
    document.documentElement.dir = currentLang === 'ar' ? 'rtl' : 'ltr';
    updateAuthUI();
    
    const page = document.body.dataset.page;
    
    if (page === 'index') {
        renderPlacesList();
        document.getElementById('filter-btn')?.addEventListener('click', renderPlacesList);
        document.getElementById('price-filter-index')?.addEventListener('change', renderPlacesList);
    }
    
    if (page === 'place') {
        renderAllPlacesPage();
        
        document.getElementById('price-filter')?.addEventListener('change', renderAllPlacesPage);
        
        // Check if we're on a specific place detail page (has ?id= in URL)
        if (window.location.search.includes('id=')) {
            renderPlaceDetails();
        }
    }
    
    if (page === 'add-review') {
        initAddReviewPage();
        document.getElementById('review-form')?.addEventListener('submit', handleSubmitReview);
    }
    
    if (page === 'login') {
        // إزالة أي مستمعين سابقين وإضافة المستمع الجديد
        const loginForm = document.getElementById('login-form-element');
        if (loginForm) {
            loginForm.removeEventListener('submit', handleLogin);
            loginForm.addEventListener('submit', handleLogin);
        }
    }
    
    // Global listeners
    document.getElementById('lang-indicator')?.addEventListener('click', toggleLanguage);
    document.getElementById('user-avatar')?.addEventListener('click', toggleUserDropdown);
    document.getElementById('logout-btn')?.addEventListener('click', handleLogout);
    
    // Close dropdown
    window.addEventListener('click', function(e) {
        const dropdown = document.getElementById('user-dropdown');
        const avatar = document.getElementById('user-avatar');
        if (dropdown && avatar && !avatar.contains(e.target) && !dropdown.contains(e.target)) {
            dropdown.classList.add('hidden');
        }
    });
    
    // Active nav link
    document.querySelectorAll('[data-nav-link]').forEach(link => {
        const href = link.getAttribute('href');
        const currentPath = window.location.pathname.split('/').pop() || 'index.html';
        if (href === currentPath) link.classList.add('active');
    });
}

document.addEventListener('DOMContentLoaded', initApp);
```
