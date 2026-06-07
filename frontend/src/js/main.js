import '../css/main.css'

/* ========================================
   Brauni Frontend Engine
   ======================================== */

document.addEventListener('DOMContentLoaded', function () {

    /* ========================================
       HERO CAROUSEL — AUTO-ROTATING + DOTS
       Dynamic: picks up slides & dots from DOM
    ======================================== */

    const carousel = document.getElementById('heroCarousel');
    const dotsContainer = document.getElementById('heroCarouselDots');
    const overlayTitle = document.querySelector('.hero-overlay-title');
    const overlayText = document.querySelector('.hero-overlay-text');
    const overlayButton = document.querySelector('.hero-overlay-button');

    // Store slide metadata from data attributes (if available)
    let slideData = [];

    if (carousel) {
        const slides = carousel.querySelectorAll('.hero-carousel-slide');
        const totalSlides = slides.length;

        // Collect slide metadata from images or default to current overlay
        slides.forEach(function (slide) {
            const img = slide.querySelector('img');
            const title = img ? (img.getAttribute('data-title') || '') : '';
            const desc = img ? (img.getAttribute('data-description') || '') : '';
            const btnText = img ? (img.getAttribute('data-button-text') || '') : '';
            const btnUrl = img ? (img.getAttribute('data-button-url') || '') : '';
            slideData.push({
                title: title,
                description: desc,
                buttonText: btnText,
                buttonUrl: btnUrl,
            });
        });

        if (totalSlides <= 1) {
            // No need for carousel with 0-1 slides
            if (dotsContainer) dotsContainer.style.display = 'none';
            return;
        }

        const dots = dotsContainer ? dotsContainer.querySelectorAll('.hero-carousel-dot') : [];
        let currentIndex = 0;
        const interval = 4000; // 4 seconds
        let autoTimer;

        function updateOverlay(index) {
            const data = slideData[index];
            if (!data) return;
            if (overlayTitle && data.title) overlayTitle.textContent = data.title;
            if (overlayText && data.description) overlayText.textContent = data.description;
            if (overlayButton) {
                if (data.buttonText) overlayButton.textContent = data.buttonText;
                if (data.buttonUrl) overlayButton.setAttribute('href', data.buttonUrl);
            }
        }

        function goToSlide(index) {
            // Update slides
            slides.forEach(function (slide) {
                slide.classList.remove('is-active');
            });
            if (slides[index]) slides[index].classList.add('is-active');

            // Update dots
            dots.forEach(function (dot) {
                dot.classList.remove('is-active');
            });
            if (dots[index]) dots[index].classList.add('is-active');

            // Update overlay content
            updateOverlay(index);

            currentIndex = index;
        }

        function nextSlide() {
            const next = (currentIndex + 1) % totalSlides;
            goToSlide(next);
        }

        function resetAutoTimer() {
            if (autoTimer) {
                clearInterval(autoTimer);
            }
            autoTimer = setInterval(nextSlide, interval);
        }

        // Dot click handlers
        dots.forEach(function (dot) {
            dot.addEventListener('click', function () {
                const index = parseInt(this.getAttribute('data-index'), 10);
                if (!isNaN(index) && index !== currentIndex && index >= 0 && index < totalSlides) {
                    goToSlide(index);
                    resetAutoTimer();
                }
            });
        });

        // Start auto-rotation
        autoTimer = setInterval(nextSlide, interval);
    }

    /* ========================================
       CATEGORY CAROUSEL — INFINITE LOOP
       Active item always in the middle (pos 1 of 3)
    ======================================== */

    const categoryCarousel = document.getElementById('categoryCarousel');
    const categoryTrack = document.getElementById('categoryTabs');
    const categoryProductsContainer = document.getElementById('categoryProducts');

    if (categoryCarousel && categoryTrack && categoryProductsContainer) {
        const originalItems = Array.from(categoryTrack.querySelectorAll('.featured-products-nav-item'));
        const categoryGrids = categoryProductsContainer.querySelectorAll('.featured-products-grid');
        const totalItems = originalItems.length;
        const visibleCount = 3;

        // --- Build infinite track by cloning ---
        // Clone last (visibleCount) items to the beginning, first (visibleCount) to the end.
        const cloneStartFragment = document.createDocumentFragment();
        const cloneEndFragment = document.createDocumentFragment();
        for (let i = 0; i < visibleCount; i++) {
            cloneStartFragment.appendChild(
                originalItems[totalItems - visibleCount + i].cloneNode(true)
            );
        }
        for (let i = 0; i < visibleCount; i++) {
            cloneEndFragment.appendChild(
                originalItems[i].cloneNode(true)
            );
        }
        categoryTrack.prepend(cloneStartFragment);
        categoryTrack.appendChild(cloneEndFragment);

        // All items in the track now (originals + clones)
        const allItems = categoryTrack.querySelectorAll('.featured-products-nav-item');
        // The real items start at index `visibleCount`
        const realStartIndex = visibleCount;

        // Determine initial active real index
        let activeRealIndex = 0;
        originalItems.forEach(function (item, idx) {
            if (item.classList.contains('is-active')) {
                activeRealIndex = idx;
            }
        });

        // Remove is-active from all, set on the correct one in the track
        allItems.forEach(function (item) {
            item.classList.remove('is-active');
        });

        // Current display index in allItems array
        let currentDisplayIndex = realStartIndex + activeRealIndex;
        allItems[currentDisplayIndex].classList.add('is-active');

        // Position the track so the active item is in the middle
        function positionTrack(displayIndex, animate) {
            const offset = -(displayIndex - 1) * (100 / visibleCount);

            if (!animate) {
                categoryTrack.style.transition = 'none';
            } else {
                categoryTrack.style.transition = 'transform 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94)';
            }
            categoryTrack.style.transform = 'translateX(' + offset + '%)';

            // Force reflow if no animation
            if (!animate) {
                void categoryTrack.offsetHeight;
                categoryTrack.style.transition = 'transform 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94)';
            }
        }

        function goToCategory(realIndex) {
            if (realIndex < 0) realIndex = totalItems - 1;
            if (realIndex >= totalItems) realIndex = 0;

            activeRealIndex = realIndex;

            // Calculate target display index
            const targetDisplayIndex = realStartIndex + activeRealIndex;

            // Update active class
            allItems.forEach(function (item) {
                item.classList.remove('is-active');
            });
            allItems[targetDisplayIndex].classList.add('is-active');

            // Animate to position
            positionTrack(targetDisplayIndex, true);

            // Show matching products grid
            const categoryId = originalItems[activeRealIndex].getAttribute('data-category-id');
            categoryGrids.forEach(function (grid) {
                if (grid.getAttribute('data-category-id') === categoryId) {
                    grid.style.display = '';
                } else {
                    grid.style.display = 'none';
                }
            });

            // After animation, check if we need to jump (if in clone zone)
            const maxRealDisplay = realStartIndex + totalItems - 1;

            if (targetDisplayIndex < realStartIndex + 1) {
                // We're in the left clone zone — jump to the real equivalent on the right
                const jumpIndex = targetDisplayIndex + totalItems;
                setTimeout(function () {
                    positionTrack(jumpIndex, false);
                    // Update active on the jumped-to item
                    allItems.forEach(function (item) {
                        item.classList.remove('is-active');
                    });
                    allItems[jumpIndex].classList.add('is-active');
                    currentDisplayIndex = jumpIndex;
                }, 420); // slightly after transition ends
            } else if (targetDisplayIndex > maxRealDisplay) {
                // We're in the right clone zone — jump to the real equivalent on the left
                const jumpIndex = targetDisplayIndex - totalItems;
                setTimeout(function () {
                    positionTrack(jumpIndex, false);
                    allItems.forEach(function (item) {
                        item.classList.remove('is-active');
                    });
                    allItems[jumpIndex].classList.add('is-active');
                    currentDisplayIndex = jumpIndex;
                }, 420);
            } else {
                currentDisplayIndex = targetDisplayIndex;
            }
        }

        // Click on any category item (use event delegation on the track)
        categoryTrack.addEventListener('click', function (e) {
            let target = e.target;
            // Find the button element
            while (target && target !== categoryTrack) {
                if (target.classList && target.classList.contains('featured-products-nav-item')) {
                    const catId = target.getAttribute('data-category-id');
                    // Find which real index this corresponds to
                    for (let j = 0; j < totalItems; j++) {
                        if (originalItems[j].getAttribute('data-category-id') === catId) {
                            goToCategory(j);
                            break;
                        }
                    }
                    break;
                }
                target = target.parentNode;
            }
        });

        // Initialize
        positionTrack(currentDisplayIndex, false);

        // Recalculate on resize
        let resizeTimer;
        window.addEventListener('resize', function () {
            clearTimeout(resizeTimer);
            resizeTimer = setTimeout(function () {
                const newVisibleCount = 3;
                if (newVisibleCount === visibleCount) {
                    positionTrack(currentDisplayIndex, false);
                }
                // A visible-count change requires a full track rebuild.
                // For now we keep the original behavior and just reposition.
                // Future improvement: dynamically rebuild the track on breakpoint change.
            }, 150);
        });
    }


    /* ========================================
       MOBILE BURGER MENU
       ======================================== */

    const burger = document.getElementById('mobileBurger');
    const overlay = document.getElementById('mobileNavOverlay');
    const panel = document.getElementById('mobileNavPanel');
    const closeBtn = document.getElementById('mobileNavClose');
    const body = document.body;

    if (burger && overlay && panel && closeBtn) {

        function openMenu() {
            overlay.classList.add('is-open');
            panel.classList.add('is-open');
            overlay.setAttribute('aria-hidden', 'false');
            burger.setAttribute('aria-expanded', 'true');
            body.classList.add('no-scroll');
        }

        function closeMenu() {
            overlay.classList.remove('is-open');
            panel.classList.remove('is-open');
            overlay.setAttribute('aria-hidden', 'true');
            burger.setAttribute('aria-expanded', 'false');
            body.classList.remove('no-scroll');
        }

        burger.addEventListener('click', function () {
            if (panel.classList.contains('is-open')) {
                closeMenu();
            } else {
                openMenu();
            }
        });

        closeBtn.addEventListener('click', closeMenu);

        overlay.addEventListener('click', function (e) {
            if (e.target === overlay) {
                closeMenu();
            }
        });

        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape' && panel.classList.contains('is-open')) {
                closeMenu();
                burger.focus();
            }
        });

        // Close menu when resizing above mobile breakpoint
        window.addEventListener('resize', function () {
            if (window.innerWidth > 1100 && panel.classList.contains('is-open')) {
                closeMenu();
            }
        });
    }

});