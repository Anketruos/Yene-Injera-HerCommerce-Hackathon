// ===== SCROLL ANIMATIONS =====
function initScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                
                // Add staggered animation for cards
                if (entry.target.classList.contains('seller-card') || 
                    entry.target.classList.contains('role-card') ||
                    entry.target.classList.contains('stat-card')) {
                    const delay = Array.from(entry.target.parentElement.children).indexOf(entry.target) * 100;
                    entry.target.style.transitionDelay = `${delay}ms`;
                }
            }
        });
    }, observerOptions);

    // Observe all animated elements
    document.querySelectorAll('.fade-in, .slide-in-left, .slide-in-right, .scale-in, .seller-card, .role-card, .stat-card, .team-member').forEach(el => {
        observer.observe(el);
    });
}

// ===== PARALLAX SCROLL EFFECT =====
function initParallax() {
    window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;
        const parallaxElements = document.querySelectorAll('.screen-header');
        
        parallaxElements.forEach(element => {
            const speed = 0.5;
            element.style.transform = `translateY(${scrolled * speed}px)`;
        });
    });
}

// ===== DASHBOARD FUNCTIONS =====
function toggleDashboard() {
    const overlay = document.getElementById('dashboardOverlay');
    const sidebar = document.getElementById('dashboardSidebar');
    
    if (overlay && sidebar) {
        overlay.classList.toggle('active');
        sidebar.classList.toggle('active');
        
        // Prevent body scroll when dashboard is open
        document.body.style.overflow = overlay.classList.contains('active') ? 'hidden' : '';
    }
}

function closeDashboard() {
    const overlay = document.getElementById('dashboardOverlay');
    const sidebar = document.getElementById('dashboardSidebar');
    
    if (overlay && sidebar) {
        overlay.classList.remove('active');
        sidebar.classList.remove('active');
        document.body.style.overflow = '';
    }
}

// ===== SCREEN MANAGEMENT =====
function showScreen(screenId) {
    // Hide all screens
    const screens = document.querySelectorAll('.screen');
    screens.forEach(screen => {
        screen.classList.remove('active');
    });
    
    // Show the requested screen
    const targetScreen = document.getElementById(screenId);
    if (targetScreen) {
        targetScreen.classList.add('active');
        
        // Add entrance animation
        targetScreen.style.animation = 'fadeInUp 0.6s ease';
        
        // Re-initialize scroll animations for the new screen
        setTimeout(() => {
            initScrollAnimations();
        }, 100);
    }
    
    // Update navigation active state
    updateNavigation(screenId);
    
    // Handle notifications screen
    if (screenId === 'notificationsScreen') {
        const noNotifications = document.getElementById('noNotifications');
        if (noNotifications) {
            noNotifications.style.display = 'none';
        }
    }
    
    // Scroll to top when changing screens
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function updateNavigation(screenId) {
    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach(item => {
        item.classList.remove('active');
    });
    
    // Map screens to navigation items
    const navMap = {
        'welcomeScreen': 0,
        'searchScreen': 1,
        'leaderboardScreen': 2,
        'ordersScreen': 3,
        'profileScreen': 4,
        'aboutScreen': 5
    };
    
    if (navMap[screenId] !== undefined && navItems[navMap[screenId]]) {
        navItems[navMap[screenId]].classList.add('active');
    }
}

// ===== ORDER FUNCTIONS =====
function submitOrder() {
    const confirmationMessage = document.getElementById('confirmationMessage');
    const submitBtn = document.querySelector('.order-form .btn');
    
    if (submitBtn) {
        // Show loading state
        const originalText = submitBtn.innerHTML;
        submitBtn.innerHTML = '<div class="loading-spinner"></div> Processing...';
        submitBtn.disabled = true;
        
        setTimeout(() => {
            if (confirmationMessage) {
                confirmationMessage.style.display = 'block';
                confirmationMessage.classList.add('scale-in', 'visible');
            }
            
            // Reset button
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
            
            // Reset form after 3 seconds and go back to search
            setTimeout(() => {
                if (confirmationMessage) {
                    confirmationMessage.style.display = 'none';
                }
                showScreen('searchScreen');
            }, 3000);
        }, 1500);
    }
}

// ===== SEARCH FUNCTIONALITY =====
function performSearch() {
    const searchInput = document.querySelector('.search-bar input');
    const searchButton = document.querySelector('.search-bar button');
    const query = searchInput.value.trim();
    
    if (query) {
        // Add loading animation to search button
        const originalHtml = searchButton.innerHTML;
        searchButton.innerHTML = '<div class="loading-spinner"></div>';
        
        setTimeout(() => {
            searchButton.innerHTML = originalHtml;
            // Simulate search results
            alert(`Searching for: ${query}`);
            // In a real app, you would filter results based on the query
            
            // Add pulse animation to matching cards
            document.querySelectorAll('.seller-card').forEach(card => {
                if (card.textContent.toLowerCase().includes(query.toLowerCase())) {
                    card.classList.add('pulse');
                    setTimeout(() => card.classList.remove('pulse'), 2000);
                }
            });
        }, 1000);
    }
}

// ===== ENHANCED CARD INTERACTIONS =====
function initCardInteractions() {
    // Add click effects to cards
    document.addEventListener('click', function(e) {
        if (e.target.closest('.seller-card') || e.target.closest('.role-card')) {
            const card = e.target.closest('.seller-card') || e.target.closest('.role-card');
            card.style.transform = 'scale(0.95)';
            setTimeout(() => {
                card.style.transform = '';
            }, 150);
        }
    });
}

// ===== INITIALIZATION =====
document.addEventListener('DOMContentLoaded', function() {
    console.log('YeneInjera Enhanced App Initialized');
    
    // Initialize all animations and effects
    initScrollAnimations();
    initParallax();
    initCardInteractions();
    
    // Dashboard Event Listeners
    const overlay = document.getElementById('dashboardOverlay');
    const toggleBtn = document.getElementById('dashboardToggle');
    const closeBtn = document.getElementById('closeDashboard');
    
    // Dashboard toggle button
    if (toggleBtn) {
        toggleBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            toggleDashboard();
        });
    }
    
    // Dashboard close button
    if (closeBtn) {
        closeBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            closeDashboard();
        });
    }
    
    // Close dashboard when clicking on overlay
    if (overlay) {
        overlay.addEventListener('click', function(e) {
            if (e.target === overlay) {
                closeDashboard();
            }
        });
    }
    
    // Close dashboard with Escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            closeDashboard();
        }
    });
    
    // Enhanced search functionality
    const searchInput = document.querySelector('.search-bar input');
    const searchButton = document.querySelector('.search-bar button');
    
    if (searchButton && searchInput) {
        searchButton.addEventListener('click', performSearch);
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                performSearch();
            }
        });
        
        // Real-time search highlight
        searchInput.addEventListener('input', function() {
            const query = this.value.toLowerCase();
            document.querySelectorAll('.seller-card').forEach(card => {
                const text = card.textContent.toLowerCase();
                if (query && text.includes(query)) {
                    card.style.border = '2px solid var(--accent)';
                    card.style.boxShadow = '0 0 20px rgba(205, 133, 63, 0.3)';
                } else {
                    card.style.border = '';
                    card.style.boxShadow = '';
                }
            });
        });
    }
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Initialize the first screen with animation
    setTimeout(() => {
        showScreen('welcomeScreen');
    }, 100);
    
    console.log('Enhanced app initialization complete');
});

// ===== PERFORMANCE OPTIMIZATION =====
let ticking = false;

function onScroll() {
    if (!ticking) {
        requestAnimationFrame(() => {
            // Add any scroll-based effects here
            ticking = false;
        });
        ticking = true;
    }
}

window.addEventListener('scroll', onScroll, { passive: true });