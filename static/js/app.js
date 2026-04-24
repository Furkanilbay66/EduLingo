/* ═══════════════════════════════════════════
   EduLingo - Main JavaScript
   ═══════════════════════════════════════════ */

// ─── Mobile Nav Toggle ───
document.addEventListener("DOMContentLoaded", function () {
  const navToggle = document.getElementById("navToggle");
  const navLinks = document.getElementById("navLinks");

  if (navToggle && navLinks) {
    navToggle.addEventListener("click", function () {
      navLinks.classList.toggle("active");
      navToggle.classList.toggle("active");
    });

    // Close mobile nav on link click
    navLinks.querySelectorAll(".nav-link").forEach(function (link) {
      link.addEventListener("click", function () {
        navLinks.classList.remove("active");
        navToggle.classList.remove("active");
      });
    });
  }

  // ─── User Dropdown ───
  const userDropdown = document.getElementById("userDropdown");
  const dropdownMenu = document.getElementById("dropdownMenu");

  if (userDropdown && dropdownMenu) {
    userDropdown.addEventListener("click", function (e) {
      e.stopPropagation();
      dropdownMenu.classList.toggle("active");
    });

    document.addEventListener("click", function () {
      dropdownMenu.classList.remove("active");
    });
  }

  // ─── Tabs ───
  document.querySelectorAll(".tabs").forEach(function (tabContainer) {
    tabContainer.querySelectorAll(".tab").forEach(function (tab) {
      tab.addEventListener("click", function () {
        const targetId = this.dataset.tab;

        // Deactivate all tabs in this container
        tabContainer.querySelectorAll(".tab").forEach(function (t) {
          t.classList.remove("active");
        });
        this.classList.add("active");

        // Show/hide tab content
        const parent = tabContainer.parentElement;
        parent.querySelectorAll(".tab-content").forEach(function (content) {
          content.classList.remove("active");
        });
        const target = document.getElementById("tab-" + targetId);
        if (target) target.classList.add("active");
      });
    });
  });

  // ─── Auto-dismiss flash messages ───
  document.querySelectorAll(".flash").forEach(function (flash) {
    setTimeout(function () {
      flash.style.opacity = "0";
      flash.style.transform = "translateY(-10px)";
      setTimeout(function () {
        flash.remove();
      }, 300);
    }, 5000);
  });
});

// ─── Dark Mode Toggle ───
function toggleDarkMode() {
  fetch("/toggle-dark-mode", { method: "POST" })
    .then(function (r) {
      return r.json();
    })
    .then(function (data) {
      document.documentElement.dataset.theme = data.dark_mode
        ? "dark"
        : "light";
    });
}

// ─── XP Popup ───
function showXPPopup(xp) {
  if (!xp || xp <= 0) return;

  const popup = document.createElement("div");
  popup.className = "xp-popup";
  popup.textContent = "+" + xp + " XP";
  document.body.appendChild(popup);

  requestAnimationFrame(function () {
    popup.classList.add("show");
  });

  setTimeout(function () {
    popup.classList.add("hide");
    setTimeout(function () {
      popup.remove();
    }, 400);
  }, 2000);
}
