/* =========================================================
   SheLearn – Main Script
   Handles:
   1. Custom region dropdown (signup page)
   2. Mobile sidebar toggle (student dashboard)
   3. Active nav item highlighting
   4. Stat number count-up animation (admin dashboard)
   ========================================================= */

document.addEventListener("DOMContentLoaded", function () {

    /* ---------------------------------------------------------
       1. CUSTOM SELECT DROPDOWN
       Only runs if the custom select elements exist on the page
    --------------------------------------------------------- */
    const customSelects = document.querySelectorAll(".custom-select");

    if (customSelects.length > 0) {
        // Support multiple custom-selects on the same page (e.g., region + course)
        // without duplicating CSS/JS or relying on hard-coded element ids.
        function closeAllDropdowns(exceptItems = null, exceptSelected = null) {
            customSelects.forEach(selectEl => {
                const itemsEl = selectEl.querySelector(".select-items");
                const selectedEl = selectEl.querySelector(".select-selected");
                if (!itemsEl || !selectedEl) return;
                if (itemsEl !== exceptItems) itemsEl.classList.add("select-hide");
                if (selectedEl !== exceptSelected) selectedEl.classList.remove("select-active");
            });
        }

        customSelects.forEach(selectEl => {
            const selected = selectEl.querySelector(".select-selected");
            const items = selectEl.querySelector(".select-items");
            const hiddenInput = (selectEl.closest(".input-group") || selectEl.parentElement)?.querySelector("input[type='hidden']");

            if (!selected || !items) return;

            const options = items.querySelectorAll("div");

            function closeDropdown() {
                items.classList.add("select-hide");
                selected.classList.remove("select-active");
            }

            selected.addEventListener("click", function (e) {
                e.stopPropagation();
                const willOpen = items.classList.contains("select-hide");
                closeAllDropdowns(items, selected);
                if (willOpen) {
                    items.classList.remove("select-hide");
                    selected.classList.add("select-active");
                } else {
                    closeDropdown();
                }
            });

            options.forEach(option => {
                option.addEventListener("click", function (e) {
                    e.stopPropagation();
                    selected.textContent = this.textContent;

                    if (hiddenInput) {
                        hiddenInput.value = this.getAttribute("data-value") || this.textContent;
                    }

                    items.querySelectorAll(".same-as-selected").forEach(el => el.classList.remove("same-as-selected"));
                    this.classList.add("same-as-selected");

                    selected.style.color = "#333";
                    closeDropdown();
                });
            });
        });

        document.addEventListener("click", function () {
            closeAllDropdowns();
        });
    }


    /* ---------------------------------------------------------
       2. MOBILE SIDEBAR TOGGLE
       Injects a hamburger button on small screens for the 
       student dashboard sidebar (dashboard-wrapper layout)
    --------------------------------------------------------- */
    const sidebar = document.querySelector(".sidebar");
    const dashboardWrapper = document.querySelector(".dashboard-wrapper");

    if (sidebar && dashboardWrapper) {
        // Read brand color from CSS variables so the mobile toggle stays in sync
        // when the palette changes (no hard-coded purple here).
        const rootStyles = getComputedStyle(document.documentElement);
        const brand = (rootStyles.getPropertyValue("--brand") || "").trim() || "#D9A6F0";
        // Create a hamburger toggle button
        const toggleBtn = document.createElement("button");
        toggleBtn.id = "sidebar-toggle";
        toggleBtn.setAttribute("aria-label", "Toggle navigation");
        toggleBtn.innerHTML = "&#9776; Menu";
        toggleBtn.style.cssText = `
            display: none;
            position: fixed;
            top: 15px;
            left: 15px;
            z-index: 1000;
            background: ${brand};
            color: white;
            border: none;
            border-radius: 10px;
            padding: 10px 16px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(203,135,230,0.35);
            transition: background 0.2s ease;
        `;
        document.body.appendChild(toggleBtn);

        // Show/hide the toggle button based on screen width
        function handleResize() {
            if (window.innerWidth <= 768) {
                toggleBtn.style.display = "block";
                sidebar.style.display = "none"; // Collapsed by default on mobile
            } else {
                toggleBtn.style.display = "none";
                sidebar.style.display = ""; // Restore desktop sidebar
            }
        }

        toggleBtn.addEventListener("click", function () {
            const isHidden = sidebar.style.display === "none" || sidebar.style.display === "";
            sidebar.style.display = isHidden ? "block" : "none";
        });

        toggleBtn.addEventListener("mouseenter", () => {
            toggleBtn.style.background = "#b56fd1";
        });
        toggleBtn.addEventListener("mouseleave", () => {
            toggleBtn.style.background = brand;
        });

        window.addEventListener("resize", handleResize);
        handleResize(); // Run on load
    }


    /* ---------------------------------------------------------
       3. ACTIVE NAV ITEM HIGHLIGHTING
       Marks the nav-item whose href matches the current page
       as active, so it highlights even after page reload.
    --------------------------------------------------------- */
    const navItems = document.querySelectorAll(".nav-item");

    if (navItems.length > 0) {
        const currentPage = window.location.pathname.split("/").pop() || "index.html";

        navItems.forEach(item => {
            const itemPage = (item.getAttribute("href") || "").split("/").pop();
            if (itemPage && itemPage === currentPage) {
                // Remove active from all first
                navItems.forEach(n => n.classList.remove("active"));
                item.classList.add("active");
            }
        });
    }


    /* ---------------------------------------------------------
       4. STAT COUNT-UP ANIMATION
       Animates stat numbers on the admin dashboard from 0
       up to their target value when the page loads.
    --------------------------------------------------------- */
    const statNumbers = document.querySelectorAll(".stat-number");

    if (statNumbers.length > 0) {
        statNumbers.forEach(el => {
            const rawText = el.textContent.trim();
            const isPercent = rawText.includes("%");
            const target = parseFloat(rawText.replace("%", ""));

            if (isNaN(target)) return;

            let start = 0;
            const duration = 1200; // ms
            const startTime = performance.now();

            function countUp(currentTime) {
                const elapsed = currentTime - startTime;
                const progress = Math.min(elapsed / duration, 1);
                // Ease-out curve
                const eased = 1 - Math.pow(1 - progress, 3);
                const current = Math.round(eased * target);
                el.textContent = current + (isPercent ? "%" : "");
                if (progress < 1) {
                    requestAnimationFrame(countUp);
                }
            }

            requestAnimationFrame(countUp);
        });
    }

    /* ---------------------------------------------------------
       5. PLATFORM ANALYTICS CHART (AREA LINE CHART)
       Initializes the Chart.js area chart on the admin dashboard
    --------------------------------------------------------- */
    const chartCanvas = document.getElementById('userTimeChart');
    if (chartCanvas) {
        const ctx = chartCanvas.getContext('2d');
        
        // Gradient for the area fill
        const gradient = ctx.createLinearGradient(0, 0, 0, 300);
        gradient.addColorStop(0, 'rgba(217, 166, 240, 0.5)'); // var(--brand) with opacity
        gradient.addColorStop(1, 'rgba(217, 166, 240, 0.0)');

        new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                datasets: [{
                    label: 'Avg. User Time (Mins)',
                    data: [45, 52, 38, 65, 59, 80, 72],
                    backgroundColor: gradient,
                    borderColor: '#D9A6F0', // var(--brand)
                    borderWidth: 3,
                    pointBackgroundColor: '#ffffff',
                    pointBorderColor: '#D9A6F0',
                    pointBorderWidth: 2,
                    pointRadius: 4,
                    pointHoverRadius: 6,
                    fill: true,
                    tension: 0.4 // Creates the smooth curve
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false // Hide legend for cleaner look
                    },
                    tooltip: {
                        backgroundColor: '#2D3748',
                        padding: 12,
                        titleFont: { family: 'Inter', size: 13 },
                        bodyFont: { family: 'Inter', size: 14, weight: 'bold' },
                        displayColors: false,
                        callbacks: {
                            label: function(context) {
                                return context.parsed.y + ' Mins';
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        grid: {
                            display: false,
                            drawBorder: false
                        },
                        ticks: {
                            font: { family: 'Inter', size: 12 },
                            color: '#777'
                        }
                    },
                    y: {
                        grid: {
                            color: '#f0f0f0',
                            borderDash: [5, 5],
                            drawBorder: false
                        },
                        ticks: {
                            font: { family: 'Inter', size: 12 },
                            color: '#777',
                            stepSize: 20
                        },
                        beginAtZero: true
                    }
                },
                interaction: {
                    intersect: false,
                    mode: 'index',
                },
            }
        });
    }

});
