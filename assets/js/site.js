/* ===========================================================================
   Raven Steele — the small amount of JavaScript this site needs.
   Three jobs: open the menu, pick a chip, handle the signup form.
   No library, no build step.
   =========================================================================== */
(function () {
  "use strict";

  /* --- The menu ---------------------------------------------------------- */
  var btn = document.querySelector(".menu-btn");
  var nav = document.getElementById("site-nav");

  if (btn && nav) {
    var setOpen = function (open) {
      nav.setAttribute("data-open", open ? "true" : "false");
      btn.setAttribute("aria-expanded", open ? "true" : "false");
    };

    btn.addEventListener("click", function () {
      setOpen(nav.getAttribute("data-open") !== "true");
    });

    // Escape closes it, and so does clicking anywhere else.
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") { setOpen(false); }
    });
    document.addEventListener("click", function (e) {
      if (!nav.contains(e.target) && !btn.contains(e.target)) { setOpen(false); }
    });
  }

  /* --- "What are you here for?" -----------------------------------------
     One answer at a time. The chosen one is written into a hidden field so
     it travels with the email address when the list is connected.          */
  var chips = document.querySelectorAll(".chip");
  var reason = document.getElementById("reason");

  Array.prototype.forEach.call(chips, function (chip) {
    chip.addEventListener("click", function () {
      Array.prototype.forEach.call(chips, function (other) {
        other.setAttribute("aria-pressed", "false");
      });
      chip.setAttribute("aria-pressed", "true");
      if (reason) { reason.value = chip.textContent.trim(); }
    });
  });

  /* --- The signup form ---------------------------------------------------
     THERE IS NO EMAIL LIST CONNECTED YET.

     So this does not pretend to work. It says so plainly rather than
     showing a fake thank-you, because a fake thank-you during a review is
     how a broken signup reaches the public.

     When the list exists, this whole block is replaced by the provider's
     form action. See PLACEHOLDERS.md.                                      */
  var forms = document.querySelectorAll("form[data-rebels]");

  Array.prototype.forEach.call(forms, function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var note = form.querySelector(".form-note");
      if (note) {
        note.textContent =
          "Not connected yet. The email list gets wired up before launch.";
        note.style.color = "#c9a227";
      }
    });
  });
})();
