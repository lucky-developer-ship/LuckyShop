// ===== API State =====
const API = '';
let token = localStorage.getItem('token');
let allProducts = [];
let currentCategory = '';
let displayedCount = 12;

function h(str) {
    if (str == null) return '';
    return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#x27;');
}

// ===== Theme =====
function initTheme() {
    const saved = localStorage.getItem('theme') || 'dark';
    if (saved === 'light') {
        document.body.classList.add('light');
        document.getElementById('themeIcon').textContent = '\u2600';
        const ti = document.getElementById('taskThemeIcon');
        const tl = document.getElementById('taskThemeLabel');
        if (ti) ti.textContent = '\u2600';
        if (tl) tl.textContent = 'Light';
    }
}
function toggleTheme() {
    document.body.classList.toggle('light');
    const isLight = document.body.classList.contains('light');
    localStorage.setItem('theme', isLight ? 'light' : 'dark');
    const icon = isLight ? '\u2600' : '\u263E';
    const label = isLight ? 'Light' : 'Dark';
    document.getElementById('themeIcon').textContent = icon;
    const ti = document.getElementById('taskThemeIcon');
    const tl = document.getElementById('taskThemeLabel');
    if (ti) ti.textContent = icon;
    if (tl) tl.textContent = label;
}
function scrollToTop() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ===== Pull to Refresh (Mobile) =====
let ptrStartY = 0;
let ptrCurrentY = 0;
let ptrActive = false;
let ptrTriggered = false;
const PTR_THRESHOLD = 80;
const PTR_MAX = 130;

function initPullToRefresh() {
    if (window.innerWidth > 768) return;
    const indicator = document.getElementById('ptrIndicator');
    if (!indicator) return;

    const queryStr = window.matchMedia('(max-width: 768px)');

    document.addEventListener('touchstart', (e) => {
        if (window.scrollY > 5) return;
        if (document.querySelector('.modal-overlay.show')) return;
        if (document.getElementById('cartDrawer').classList.contains('open')) return;
        if (document.getElementById('navLinks').classList.contains('open')) return;
        ptrStartY = e.touches[0].clientY;
        ptrActive = true;
        ptrTriggered = false;
    }, { passive: true });

    document.addEventListener('touchmove', (e) => {
        if (!ptrActive || window.scrollY > 5) return;
        ptrCurrentY = e.touches[0].clientY - ptrStartY;
        if (ptrCurrentY < 0) return;
        const progress = Math.min(ptrCurrentY, PTR_MAX);
        const ready = ptrCurrentY >= PTR_THRESHOLD;
        indicator.classList.add('visible');
        if (ready) {
            indicator.classList.add('ready');
            indicator.querySelector('.ptr-text').textContent = 'Release to refresh';
        } else {
            indicator.classList.remove('ready');
            indicator.querySelector('.ptr-text').textContent = 'Pull to refresh';
        }
        indicator.style.opacity = Math.min(progress / 60, 1);
    }, { passive: true });

    document.addEventListener('touchend', () => {
        if (!ptrActive) return;
        ptrActive = false;
        if (ptrCurrentY >= PTR_THRESHOLD && !ptrTriggered) {
            ptrTriggered = true;
            doRefresh();
        } else {
            indicator.classList.remove('visible');
            indicator.classList.remove('ready');
        }
        ptrCurrentY = 0;
    });
}

async function doRefresh() {
    const indicator = document.getElementById('ptrIndicator');
    if (!indicator) return;
    indicator.classList.remove('ready');
    indicator.classList.add('refreshing');
    indicator.querySelector('.ptr-text').textContent = 'Refreshing...';
    try {
        await fetchProducts();
        if (token) await loadCart();
        showToast('Updated!');
    } catch (e) {
        showToast('Refresh failed');
    } finally {
        setTimeout(() => {
            indicator.classList.remove('refreshing');
            indicator.classList.remove('visible');
            indicator.querySelector('.ptr-text').textContent = 'Pull to refresh';
        }, 400);
    }
}

function refreshSite() {
    fetchProducts().then(() => {
        if (token) loadCart();
        showToast('Updated!');
    }).catch(() => {
        showToast('Refresh failed');
    });
}
function handleProfileTap() {
    if (!token) {
        showLogin();
    } else {
        openProfileModal();
    }
}
function updateTaskbarCartCount(count) {
    const badge = document.getElementById('taskCartCount');
    if (!badge) return;
    if (count > 0) {
        badge.style.display = 'flex';
        badge.textContent = count;
    } else {
        badge.style.display = 'none';
    }
}

// ===== Mobile Menu =====
function toggleMobileMenu() {
    document.getElementById('navLinks').classList.toggle('open');
    document.getElementById('hamburger').classList.toggle('open');
    document.getElementById('mobileOverlay').classList.toggle('show');
}

// ===== Three.js Background =====
function initThreeBackground() {
    const canvas = document.getElementById('three-canvas');
    const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.z = 3;

    const particleCount = window.innerWidth < 768 ? 150 : 400;
    const positions = new Float32Array(particleCount * 3);
    for (let i = 0; i < particleCount; i++) {
        const theta = Math.random() * Math.PI * 2;
        const phi = Math.acos(2 * Math.random() - 1);
        const r = 1.2 + Math.random() * 0.3;
        positions[i * 3] = r * Math.sin(phi) * Math.cos(theta);
        positions[i * 3 + 1] = r * Math.sin(phi) * Math.sin(theta);
        positions[i * 3 + 2] = r * Math.cos(phi);
    }

    const geometry = new THREE.BufferGeometry();
    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));

    const material = new THREE.PointsMaterial({
        color: 0x8b5cf6,
        size: 0.012,
        transparent: true,
        opacity: 0.35,
        blending: THREE.AdditiveBlending,
        depthWrite: false
    });

    const particles = new THREE.Points(geometry, material);
    scene.add(particles);

    function animate() {
        requestAnimationFrame(animate);
        particles.rotation.y += 0.0003;
        particles.rotation.x += 0.0001;
        renderer.render(scene, camera);
    }
    animate();

    window.addEventListener('resize', () => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    });
}

// ===== Lenis Smooth Scroll =====
let lenis;
function initLenis() {
    if (typeof Lenis === 'undefined') return;
    try {
        lenis = new Lenis({
            duration: 1.2,
            easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
            smoothWheel: true
        });

        lenis.on('scroll', ScrollTrigger.update);

        gsap.ticker.add((time) => {
            lenis.raf(time * 1000);
        });

        gsap.ticker.lagSmoothing(0);
    } catch (e) {
        lenis = null;
    }
}

// ===== GSAP Animations =====
function initAnimations() {
    gsap.registerPlugin(ScrollTrigger);

    // Navbar scroll - use Lenis event instead of native scroll
    const navbar = document.getElementById('navbar');
    if (lenis) {
        lenis.on('scroll', (e) => {
            if (lenis.scroll > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });
    } else {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) navbar.classList.add('scrolled');
            else navbar.classList.remove('scrolled');
        });
    }

    // Hero entrance
    const heroTimeline = gsap.timeline({ delay: 0.3 });
    heroTimeline
        .to('.hero-badge', { opacity: 1, y: 0, duration: 0.7, ease: 'power3.out' })
        .to('.hero h1', { opacity: 1, y: 0, duration: 0.7, ease: 'power3.out' }, '-=0.4')
        .to('.hero-desc', { opacity: 1, y: 0, duration: 0.7, ease: 'power3.out' }, '-=0.4')
        .to('.hero-buttons', { opacity: 1, y: 0, duration: 0.7, ease: 'power3.out' }, '-=0.4')
        .to('.hero-search', { opacity: 1, y: 0, duration: 0.7, ease: 'power3.out' }, '-=0.4');

    // Stats counter animation - fetch real data
    async function loadStats() {
        try {
            const res = await fetch(`${API}/api/products/stats`);
            if (res.ok) {
                const data = await res.json();
                const productStat = document.querySelector('.stat-number[data-target="500"]');
                const customerStat = document.querySelector('.stat-number[data-target="10000"]');
                if (productStat) productStat.setAttribute('data-target', data.products || 35);
                if (customerStat) customerStat.setAttribute('data-target', data.users || 0);
            }
        } catch(e) {}
    }
    loadStats();

    const statNumbers = document.querySelectorAll('.stat-number');
    statNumbers.forEach(num => {
        const target = parseInt(num.getAttribute('data-target'));
        gsap.to(num, {
            textContent: target,
            duration: 2,
            ease: 'power2.out',
            snap: { textContent: 1 },
            scrollTrigger: {
                trigger: num,
                start: 'top 85%',
                once: true
            },
            onUpdate: function() {
                const val = Math.round(parseFloat(num.textContent));
                if (target >= 10000) {
                    num.textContent = (val / 1000).toFixed(0) + 'K+';
                } else if (target >= 500) {
                    num.textContent = val + '+';
                } else {
                    num.textContent = val + '%';
                }
            }
        });
    });
}

function animateProductCards() {
    const cards = document.querySelectorAll('.product-card');
    cards.forEach(card => { card.style.opacity = '1'; card.style.transform = 'none'; card.style.pointerEvents = 'auto'; });
    gsap.fromTo(cards,
        { opacity: 0, y: 50 },
        { opacity: 1, y: 0, duration: 0.6, ease: 'power3.out', stagger: 0.08, clearProps: 'all' }
    );
}

// ===== Products =====
async function fetchProducts() {
    const res = await fetch(`${API}/api/products/`);
    allProducts = await res.json();
    renderProducts(allProducts, true);
}

function renderProducts(products, animate = false) {
    const grid = document.getElementById('productsGrid');
    const spinner = document.getElementById('loadingSpinner');
    if (spinner) spinner.remove();
    if (products.length === 0) {
        grid.innerHTML = '<div class="empty-state">No products found</div>';
        document.getElementById('seeMoreWrapper').style.display = 'none';
        return;
    }
    const toShow = products.slice(0, displayedCount);
    grid.innerHTML = toShow.map(p => `
        <div class="product-card">
            <div class="image-wrapper">
                <img src="${h(p.image_url) || 'https://via.placeholder.com/300x200?text=' + encodeURIComponent(h(p.name))}" alt="${h(p.name)}" loading="lazy">
                <div class="image-overlay"></div>
                <div class="category-tag">${h(p.category)}</div>
            </div>
            <div class="info">
                <h3>${h(p.name)}</h3>
                <div class="description">${h(p.description)}</div>
                <div class="price-row">
                    <div class="price">$${p.price.toFixed(2)}</div>
                    <div class="stock ${p.stock === 0 ? 'out' : (p.stock < 10 ? 'low' : '')}">${p.stock > 0 ? h(p.stock) + ' in stock' : 'Out of stock'}</div>
                </div>
                <button class="add-btn" onclick="addToCart(event, ${p.id})" ${p.stock === 0 ? 'disabled' : ''}>${p.stock > 0 ? 'Add to Cart' : 'Out of Stock'}</button>
            </div>
        </div>
    `).join('');

    const wrapper = document.getElementById('seeMoreWrapper');
    if (products.length > displayedCount) {
        wrapper.style.display = 'flex';
    } else {
        wrapper.style.display = 'none';
    }

    if (animate) setTimeout(animateProductCards, 50);
}

function showMoreProducts() {
    displayedCount += 12;
    if (currentCategory || document.getElementById('searchInput').value) {
        const q = document.getElementById('searchInput').value.toLowerCase();
        let filtered = allProducts.filter(p => p.name.toLowerCase().includes(q) || p.description.toLowerCase().includes(q));
        if (currentCategory) filtered = filtered.filter(p => p.category === currentCategory);
        renderProducts(filtered);
    } else {
        renderProducts(allProducts);
    }
}

function filterProducts() {
    const q = document.getElementById('searchInput').value.toLowerCase();
    toggleClearBtn();
    let filtered = allProducts.filter(p => p.name.toLowerCase().includes(q) || p.description.toLowerCase().includes(q));
    if (currentCategory) filtered = filtered.filter(p => p.category === currentCategory);
    displayedCount = 12;
    renderProducts(filtered);
}

let searchTimeout;
function debouncedSearch() {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(filterProducts, 200);
}

function toggleClearBtn() {
    const q = document.getElementById('searchInput').value;
    document.getElementById('clearSearchBtn').style.display = q.length > 0 ? 'flex' : 'none';
}

function clearSearch() {
    document.getElementById('searchInput').value = '';
    document.getElementById('clearSearchBtn').style.display = 'none';
    filterProducts();
}

function filterCategory(btn, cat) {
    document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    currentCategory = cat;
    filterProducts();
}

// ===== Auth =====
function showLogin() { closeModals(); document.getElementById('loginModal').classList.add('show'); }
function showRegister() { closeModals(); document.getElementById('registerModal').classList.add('show'); }
function closeModals() { document.querySelectorAll('.modal-overlay').forEach(m => m.classList.remove('show')); }

async function login() {
    const username = document.getElementById('loginUsername').value;
    const password = document.getElementById('loginPassword').value;
    const errEl = document.getElementById('loginError');
    try {
        const res = await fetch(`${API}/api/users/login`, {
            method: 'POST',
            headers: {'Content-Type': 'application/x-www-form-urlencoded'},
            body: `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`
        });
        if (!res.ok) { errEl.textContent = 'Invalid username or password'; errEl.style.display = 'block'; return; }
        const data = await res.json();
        token = data.access_token;
        localStorage.setItem('token', token);
        closeModals();
        updateAuthUI();
        loadCart();
        showToast('Logged in successfully!');
    } catch(e) { errEl.textContent = 'Connection error'; errEl.style.display = 'block'; }
}

async function register() {
    const username = document.getElementById('regUsername').value;
    const email = document.getElementById('regEmail').value;
    const password = document.getElementById('regPassword').value;
    const errEl = document.getElementById('registerError');
    try {
        const res = await fetch(`${API}/api/users/register`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({username, email, password})
        });
        if (!res.ok) { const d = await res.json(); errEl.textContent = d.detail || 'Registration failed'; errEl.style.display = 'block'; return; }
        showToast('Account created! Please login.');
        showLogin();
    } catch(e) { errEl.textContent = 'Connection error'; errEl.style.display = 'block'; }
}

function logout() {
    token = null;
    localStorage.removeItem('token');
    updateAuthUI();
    document.getElementById('cartCount').textContent = '0';
    showToast('Logged out');
}

function googleLogin() {
    const width = 500, height = 600;
    const left = (screen.width - width) / 2;
    const top = (screen.height - height) / 2;
    const popup = window.open(
        `${API}/api/auth/google/login`,
        'googleAuth',
        `width=${width},height=${height},left=${left},top=${top}`
    );
    window.addEventListener('message', function handler(e) {
        if (e.data && e.data.token) {
            token = e.data.token;
            localStorage.setItem('token', token);
            closeModals();
            updateAuthUI();
            loadCart();
            showToast(`Welcome ${e.data.username}!`);
            window.removeEventListener('message', handler);
        }
    });
}

function updateAuthUI() {
    document.getElementById('authBtn').style.display = token ? 'none' : '';
    document.getElementById('userBtn').style.display = token ? '' : 'none';
    document.getElementById('ordersBtn').style.display = token ? '' : 'none';
    document.getElementById('profileBtn').style.display = token ? '' : 'none';
    const tp = document.getElementById('taskProfileLabel');
    if (tp) tp.textContent = token ? 'Profile' : 'Login';
    checkAdmin();
}

async function checkAdmin() {
    if (!token) return;
    try {
        const res = await fetch(`${API}/api/users/me`, {headers: {'Authorization': `Bearer ${token}`}});
        if (res.ok) {
            const user = await res.json();
            document.getElementById('adminBtn').style.display = user.is_admin ? '' : 'none';
        }
    } catch(e) {}
}

// ===== Admin Dashboard =====
function openAdminModal() {
    closeModals();
    document.getElementById('adminModal').classList.add('show');
    loadAdminData();
}

function closeAdminModal() {
    document.getElementById('adminModal').classList.remove('show');
}

async function loadAdminData() {
    const container = document.getElementById('adminContent');
    try {
        const [statsRes, ordersRes, usersRes] = await Promise.all([
            fetch(`${API}/api/admin/stats`, {headers: {'Authorization': `Bearer ${token}`}}),
            fetch(`${API}/api/admin/orders`, {headers: {'Authorization': `Bearer ${token}`}}),
            fetch(`${API}/api/admin/users`, {headers: {'Authorization': `Bearer ${token}`}}),
        ]);

        if (!statsRes.ok) { container.innerHTML = '<p style="text-align:center; color:var(--accent);">Admin access denied</p>'; return; }

        const stats = await statsRes.json();
        const orders = await ordersRes.json();
        const users = await usersRes.json();

        container.innerHTML = `
            <div class="admin-stats">
                <div class="admin-stat-card"><div class="stat-val">${stats.products}</div><div class="stat-lbl">Products</div></div>
                <div class="admin-stat-card"><div class="stat-val">${stats.users}</div><div class="stat-lbl">Users</div></div>
                <div class="admin-stat-card"><div class="stat-val">${stats.orders}</div><div class="stat-lbl">Orders</div></div>
                <div class="admin-stat-card"><div class="stat-val">$${stats.revenue.toFixed(2)}</div><div class="stat-lbl">Revenue</div></div>
            </div>
            <div class="admin-section-title">Recent Orders</div>
            <div id="adminOrdersList">
                ${orders.length === 0 ? '<p style="color:var(--text-muted); font-size:0.85rem;">No orders yet</p>' :
                    orders.slice(0, 10).map(o => `
                        <div class="admin-order-item">
                            <div class="admin-order-info">
                                <div class="admin-order-id">#${o.id}</div>
                                <div class="admin-order-user">${h(o.items.length)} items</div>
                            </div>
                            <div class="admin-order-total">$${o.total_price.toFixed(2)}</div>
                            <div class="admin-order-actions">
                                <select onchange="updateOrderStatus(${o.id}, this.value)">
                                    <option value="pending" ${o.status==='pending'?'selected':''}>${h(o.status)}</option>
                                    <option value="processing" ${o.status==='processing'?'selected':''}>Processing</option>
                                    <option value="shipped" ${o.status==='shipped'?'selected':''}>Shipped</option>
                                    <option value="delivered" ${o.status==='delivered'?'selected':''}>Delivered</option>
                                    <option value="cancelled" ${o.status==='cancelled'?'selected':''}>Cancelled</option>
                                </select>
                            </div>
                        </div>
                    `).join('')}
            </div>
            <div class="admin-section-title" style="margin-top:1rem;">Users (${users.length})</div>
            <div style="max-height:150px; overflow-y:auto;">
                ${users.map(u => `
                    <div style="display:flex; justify-content:space-between; padding:0.4rem 0; border-bottom:1px solid var(--border); font-size:0.82rem;">
                        <span>${h(u.username)}</span>
                        <span style="color:var(--text-muted);">${h(u.email)}</span>
                        <span style="color:${u.is_admin?'var(--accent)':'var(--text-muted)'};">${u.is_admin?'Admin':'User'}</span>
                    </div>
                `).join('')}
            </div>
        `;
    } catch(e) {
        container.innerHTML = '<p style="text-align:center;">Failed to load admin data</p>';
    }
}

async function updateOrderStatus(orderId, status) {
    try {
        await fetch(`${API}/api/admin/orders/${orderId}`, {
            method: 'PATCH',
            headers: {'Content-Type': 'application/json', 'Authorization': `Bearer ${token}`},
            body: JSON.stringify({status})
        });
        showToast('Order status updated', 'success');
    } catch(e) {
        showToast('Failed to update', 'error');
    }
}

// ===== Profile =====
function openProfileModal() {
    closeModals();
    document.getElementById('profileModal').classList.add('show');
    loadProfile();
}

function closeProfileModal() {
    document.getElementById('profileModal').classList.remove('show');
}

async function loadProfile() {
    const container = document.getElementById('profileContent');
    if (!token) {
        container.innerHTML = '<div class="orders-empty"><h3>Please login</h3></div>';
        return;
    }
    try {
        const res = await fetch(`${API}/api/users/me`, {headers: {'Authorization': `Bearer ${token}`}});
        if (!res.ok) throw new Error();
        const user = await res.json();
        const initial = user.username.charAt(0).toUpperCase();
        const joinDate = new Date(user.created_at).toLocaleDateString('en-US', {year:'numeric', month:'long', day:'numeric'});
        container.innerHTML = `
            <div class="profile-card">
                <div class="profile-avatar">${h(initial)}</div>
                <div class="profile-name">${h(user.username)}</div>
                <div class="profile-email">${h(user.email)}</div>
                <div class="profile-joined">Joined ${h(joinDate)}</div>
            </div>
            <div style="text-align:center; margin-top: 0.5rem;">
                <button class="btn-primary" onclick="closeProfileModal(); openOrdersModal();">View My Orders</button>
            </div>
        `;
    } catch(e) {
        container.innerHTML = '<div class="orders-empty"><h3>Failed to load profile</h3></div>';
    }
}

// ===== Cart =====
function openCart() {
    document.getElementById('cartDrawer').classList.add('open');
    document.getElementById('cartOverlay').classList.add('show');
}
function closeCart() {
    document.getElementById('cartDrawer').classList.remove('open');
    document.getElementById('cartOverlay').classList.remove('show');
}
function toggleCart() {
    const drawer = document.getElementById('cartDrawer');
    if (drawer.classList.contains('open')) { closeCart(); }
    else { openCart(); }
}

async function addToCart(event, productId) {
    event.stopPropagation();
    if (!token) { showLogin(); return; }
    const btn = event.target;
    btn.disabled = true;
    btn.textContent = 'Adding...';
    try {
        const res = await fetch(`${API}/api/cart/add`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json', 'Authorization': `Bearer ${token}`},
            body: JSON.stringify({product_id: productId, quantity: 1})
        });
        if (res.ok) {
            const data = await res.json();
            renderCart(data);
            openCart();
            showToast('Added to cart!', 'success');
        } else {
            const d = await res.json();
            showToast(d.detail || 'Failed to add to cart', 'error');
        }
    } catch(e) {
        showToast('Connection error', 'error');
    }
    btn.disabled = false;
    btn.textContent = 'Add to Cart';
}

async function loadCart() {
    if (!token) return;
    const res = await fetch(`${API}/api/cart/`, {headers: {'Authorization': `Bearer ${token}`}});
    if (res.ok) renderCart(await res.json());
}

function renderCart(data) {
    document.getElementById('cartCount').textContent = data.items.length;
    if (typeof updateTaskbarCartCount === 'function') updateTaskbarCartCount(data.items.length);
    document.getElementById('cartTotal').textContent = `$${data.total.toFixed(2)}`;
    const container = document.getElementById('cartItems');
    if (data.items.length === 0) {
        container.innerHTML = '<div class="cart-empty"><div style="font-size: 2rem; margin-bottom: 0.5rem; opacity: 0.4;">🛒</div><div>Your cart is empty</div><div style="font-size: 0.8rem; margin-top: 0.3rem; opacity: 0.6;">Add some products to get started</div></div>';
        return;
    }
    container.innerHTML = data.items.map(item => `
        <div class="cart-item">
            <div class="item-info">
                <h4>${h(item.product_name)}</h4>
                <span>$${item.product_price.toFixed(2)} each</span>
                <div class="qty-controls">
                    <button class="qty-btn" onclick="changeQty(${item.id}, ${item.quantity}, -1)">-</button>
                    <input class="qty-input" type="number" min="1" value="${item.quantity}" onchange="setQty(${item.id}, this.value)" onkeydown="if(event.key==='Enter'){setQty(${item.id}, this.value); this.blur();}">
                    <button class="qty-btn" onclick="changeQty(${item.id}, ${item.quantity}, 1)">+</button>
                </div>
            </div>
            <button class="remove-btn" onclick="removeFromCart(${item.id})">Remove</button>
        </div>
    `).join('');
}

async function removeFromCart(itemId) {
    const res = await fetch(`${API}/api/cart/${itemId}`, {
        method: 'DELETE',
        headers: {'Authorization': `Bearer ${token}`}
    });
    if (res.ok) renderCart(await res.json());
}

async function updateCartItem(itemId, newQty) {
    if (newQty < 1) return removeFromCart(itemId);
    const res = await fetch(`${API}/api/cart/${itemId}`, {
        method: 'PATCH',
        headers: {'Content-Type': 'application/json', 'Authorization': `Bearer ${token}`},
        body: JSON.stringify({quantity: newQty})
    });
    if (res.ok) {
        renderCart(await res.json());
    } else {
        const d = await res.json();
        showToast(d.detail || 'Failed to update', 'error');
    }
}

function changeQty(itemId, currentQty, delta) {
    updateCartItem(itemId, currentQty + delta);
}

function setQty(itemId, value) {
    const qty = parseInt(value);
    if (isNaN(qty) || qty < 1) return removeFromCart(itemId);
    updateCartItem(itemId, qty);
}

async function placeOrder() {
    if (!token) { showLogin(); return; }
    const res = await fetch(`${API}/api/orders/`, {
        method: 'POST',
        headers: {'Authorization': `Bearer ${token}`}
    });
    if (res.ok) {
        showToast('Order placed successfully!', 'success');
        loadCart();
    } else {
        const d = await res.json();
        showToast(d.detail || 'Failed to place order', 'error');
    }
}

function showToast(msg, type = '') {
    const toast = document.getElementById('toast');
    toast.textContent = msg;
    toast.className = 'toast show ' + type;
    setTimeout(() => toast.className = 'toast', 3000);
}

// ===== Add Product =====
function showAddProduct() {
    if (!token) { showLogin(); return; }
    closeModals();
    document.getElementById('addProductModal').classList.add('show');
}

async function addProduct() {
    const name = document.getElementById('prodName').value.trim();
    const description = document.getElementById('prodDesc').value.trim();
    const price = parseFloat(document.getElementById('prodPrice').value);
    const stock = parseInt(document.getElementById('prodStock').value) || 0;
    const category = document.getElementById('prodCategory').value.trim();
    const fileInput = document.getElementById('prodImageFile');
    const imageUrlInput = document.getElementById('prodImage');
    const errEl = document.getElementById('addProductError');

    if (!name || !price) { errEl.textContent = 'Name and price are required'; errEl.style.display = 'block'; return; }

    let image_url = imageUrlInput.value.trim();

    if (fileInput.files.length > 0) {
        const formData = new FormData();
        formData.append('file', fileInput.files[0]);
        try {
            const uploadRes = await fetch(`${API}/api/upload/image`, { method: 'POST', body: formData });
            if (uploadRes.ok) {
                const uploadData = await uploadRes.json();
                image_url = uploadData.url;
            } else {
                errEl.textContent = 'Image upload failed'; errEl.style.display = 'block'; return;
            }
        } catch(e) {
            errEl.textContent = 'Image upload failed'; errEl.style.display = 'block'; return;
        }
    }

    try {
        const res = await fetch(`${API}/api/products/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
            body: JSON.stringify({ name, description, price, stock, category, image_url })
        });
        if (!res.ok) { const d = await res.json(); errEl.textContent = d.detail || 'Failed to add product'; errEl.style.display = 'block'; return; }
        closeModals();
        document.getElementById('prodName').value = '';
        document.getElementById('prodDesc').value = '';
        document.getElementById('prodPrice').value = '';
        document.getElementById('prodStock').value = '';
        document.getElementById('prodCategory').value = '';
        document.getElementById('prodImage').value = '';
        document.getElementById('prodImageFile').value = '';
        fetchProducts();
        showToast('Product added successfully!', 'success');
    } catch(e) { errEl.textContent = 'Connection error'; errEl.style.display = 'block'; }
}

// ===== Support / Customer Service =====
function openSupportModal() {
    closeModals();
    document.getElementById('supportModal').classList.add('show');
}

// ===== Orders =====
function openOrdersModal() {
    closeModals();
    document.getElementById('ordersModal').classList.add('show');
    loadOrders();
}

function closeOrdersModal() {
    document.getElementById('ordersModal').classList.remove('show');
}

async function loadOrders() {
    const container = document.getElementById('ordersContent');
    if (!token) {
        container.innerHTML = '<div class="orders-empty"><div class="orders-empty-icon">&#128100;</div><h3>Login Required</h3><p>Please login to view your order history.</p></div>';
        return;
    }
    try {
        const res = await fetch(`${API}/api/orders/`, {headers: {'Authorization': `Bearer ${token}`}});
        if (!res.ok) throw new Error();
        const orders = await res.json();
        if (orders.length === 0) {
            container.innerHTML = '<div class="orders-empty"><div class="orders-empty-icon">&#128722;</div><h3>No Orders Yet</h3><p>Start shopping to see your orders here!</p></div>';
            return;
        }
        container.innerHTML = orders.map(o => {
            const date = new Date(o.created_at);
            const dateStr = date.toLocaleDateString('en-US', {year:'numeric', month:'short', day:'numeric'});
            const timeStr = date.toLocaleTimeString('en-US', {hour:'2-digit', minute:'2-digit'});
            const totalItems = o.items.reduce((sum, i) => sum + i.quantity, 0);
            const statusClass = o.status === 'delivered' ? 'delivered' : o.status === 'cancelled' ? 'cancelled' : 'pending';
            return `
                <div class="order-card">
                    <div class="order-header">
                        <span class="order-id">Order #${o.id}</span>
                        <span class="order-status ${statusClass}">${h(o.status)}</span>
                    </div>
                    <div class="order-meta">
                        <div class="order-item-row">&#128197; ${h(dateStr)}</div>
                        <div class="order-item-row">&#128337; ${h(timeStr)}</div>
                        <div class="order-item-row">&#128722; ${h(totalItems)} item${totalItems !== 1 ? 's' : ''}</div>
                    </div>
                    <div class="order-items-list">
                        ${o.items.map(i => `
                            <div class="order-item-row">
                                <span class="order-item-name">${h(i.product_name)}</span>
                                <span class="order-item-qty">x${i.quantity}</span>
                                <span class="order-item-price">$${(i.product_price * i.quantity).toFixed(2)}</span>
                            </div>
                        `).join('')}
                    </div>
                    <div class="order-footer">
                        <span class="order-total-label">Total</span>
                        <span class="order-total">$${o.total_price.toFixed(2)}</span>
                    </div>
                </div>
            `;
        }).join('');
    } catch(e) {
        container.innerHTML = '<div class="orders-empty"><div class="orders-empty-icon">&#9888;</div><h3>Failed to Load</h3><p>Something went wrong. Please try again.</p></div>';
    }
}

function closeSupportModal() {
    document.getElementById('supportModal').classList.remove('show');
}

function showSupportTab(event, tab) {
    document.querySelectorAll('.support-tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.support-content').forEach(c => c.style.display = 'none');
    event.target.classList.add('active');
    document.getElementById('support' + tab.charAt(0).toUpperCase() + tab.slice(1)).style.display = 'block';
}

function toggleFaq(el) {
    const item = el.parentElement;
    item.classList.toggle('open');
}

async function submitSupport() {
    const name = document.getElementById('supportName').value.trim();
    const email = document.getElementById('supportEmail').value.trim();
    const subject = document.getElementById('supportSubject').value;
    const message = document.getElementById('supportMessage').value.trim();
    const errEl = document.getElementById('supportError');

    if (!name || !email || !message) {
        errEl.textContent = 'Please fill in all fields';
        errEl.style.display = 'block';
        return;
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        errEl.textContent = 'Please enter a valid email address';
        errEl.style.display = 'block';
        return;
    }

    try {
        const res = await fetch(`${API}/api/support/`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({name, email, subject, message})
        });
        if (res.ok) {
            document.getElementById('supportName').value = '';
            document.getElementById('supportEmail').value = '';
            document.getElementById('supportMessage').value = '';
            errEl.style.display = 'none';
            showToast('Message sent! We\'ll get back to you soon.', 'success');
        } else {
            errEl.textContent = 'Failed to send message. Try again.';
            errEl.style.display = 'block';
        }
    } catch(e) {
        showToast('Message received! We\'ll contact you at ' + email, 'success');
        document.getElementById('supportName').value = '';
        document.getElementById('supportEmail').value = '';
        document.getElementById('supportMessage').value = '';
        errEl.style.display = 'none';
    }
}

// ===== Init =====
document.addEventListener('DOMContentLoaded', () => {
    initTheme();
    initThreeBackground();
    initLenis();
    initAnimations();
    initPullToRefresh();
    updateAuthUI();
    fetchProducts();
    if (token) loadCart();
});
