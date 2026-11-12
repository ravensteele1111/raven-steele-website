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
    // Where the page was when the menu opened, so a scroll can be measured
    // against it rather than against nothing.
    var openedAt = 0;

    var setOpen = function (open) {
      nav.setAttribute("data-open", open ? "true" : "false");
      btn.setAttribute("aria-expanded", open ? "true" : "false");
      if (open) { openedAt = window.pageYOffset; }
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

    // Starting to scroll means you have moved on. Leaving the menu hanging
    // open over the page is the thing people notice and dislike.
    // The small threshold is so a stray pixel of momentum does not shut it
    // the instant it opens.
    window.addEventListener("scroll", function () {
      if (nav.getAttribute("data-open") !== "true") { return; }
      if (Math.abs(window.pageYOffset - openedAt) > 12) { setOpen(false); }
    }, { passive: true });

    // Tapping a menu item closes it too. Matters for links that jump within
    // the same page, where nothing reloads to close it for us.
    nav.addEventListener("click", function (e) {
      if (e.target.closest("a")) { setOpen(false); }
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

/* ===========================================================================
   Filters, tabs, the guest-list search and the photo lightbox.
   Added as the inner pages were built. Still no library.
   =========================================================================== */
(function () {
  "use strict";

  /* --- Filter chips ------------------------------------------------------
     Any .filters block controls the items inside the element named by its
     data-target. A chip's data-filter of "all" shows everything; otherwise
     it matches an item's data-tag.                                        */
  Array.prototype.forEach.call(document.querySelectorAll(".filters"), function (bar) {
    var target = document.getElementById(bar.getAttribute("data-target"));
    if (!target) { return; }

    var items = target.querySelectorAll("[data-tag]");
    var empty = target.querySelector(".empty");

    bar.addEventListener("click", function (e) {
      var chip = e.target.closest(".chip");
      if (!chip) { return; }

      Array.prototype.forEach.call(bar.querySelectorAll(".chip"), function (c) {
        c.setAttribute("aria-pressed", c === chip ? "true" : "false");
      });

      var want = chip.getAttribute("data-filter");
      var shown = 0;

      Array.prototype.forEach.call(items, function (item) {
        var tags = (item.getAttribute("data-tag") || "").split(" ");
        var show = want === "all" || tags.indexOf(want) !== -1;
        item.setAttribute("data-hidden", show ? "false" : "true");
        if (show) { shown++; }
      });

      if (empty) { empty.setAttribute("data-hidden", shown ? "true" : "false"); }
    });
  });

  /* --- Tabs -------------------------------------------------------------- */
  Array.prototype.forEach.call(document.querySelectorAll(".tabs"), function (bar) {
    bar.addEventListener("click", function (e) {
      var tab = e.target.closest("button");
      if (!tab || tab.disabled) { return; }

      Array.prototype.forEach.call(bar.querySelectorAll("button"), function (b) {
        b.setAttribute("aria-selected", b === tab ? "true" : "false");
      });

      var panelName = tab.getAttribute("data-panel");
      Array.prototype.forEach.call(document.querySelectorAll("[data-panel-name]"), function (p) {
        p.setAttribute("data-hidden", p.getAttribute("data-panel-name") === panelName ? "false" : "true");
      });
    });
  });

  /* --- "Were you there?" -------------------------------------------------
     Searches the guest list. Every guest is a character in the world, so
     this is the universe being searchable, not a record of real people.
     The data lives in the page as data-guests on each event card.          */
  var finder = document.getElementById("guest-search");
  var results = document.getElementById("guest-results");

  if (finder && results) {
    var events = [];
    Array.prototype.forEach.call(document.querySelectorAll("[data-guests]"), function (card) {
      events.push({
        name: (card.getAttribute("data-event") || "").trim(),
        href: card.getAttribute("href") || "#",
        guests: card.getAttribute("data-guests").split(",").map(function (g) { return g.trim(); })
      });
    });

    finder.addEventListener("input", function () {
      var q = finder.value.trim().toLowerCase();
      results.innerHTML = "";

      if (q.length < 2) { return; }

      var hits = [];
      events.forEach(function (ev) {
        ev.guests.forEach(function (g) {
          if (g.toLowerCase().indexOf(q) !== -1) {
            hits.push({ guest: g, event: ev });
          }
        });
      });

      if (!hits.length) {
        var none = document.createElement("li");
        none.innerHTML = "No one by that name on a guest list yet. " +
          "<span class='where'>Join the Rebels for an invite to the next one.</span>";
        results.appendChild(none);
        return;
      }

      hits.slice(0, 8).forEach(function (hit) {
        var li = document.createElement("li");
        var a = document.createElement("a");
        a.href = hit.event.href;
        a.textContent = hit.guest;
        li.appendChild(a);
        var where = document.createElement("span");
        where.className = "where";
        where.textContent = "  " + hit.event.name;
        li.appendChild(where);
        results.appendChild(li);
      });
    });
  }

  /* --- The photo lightbox ------------------------------------------------
     "Tap any photo to see it big and share it." While the photos are
     placeholders it opens the placeholder, which is honest and proves the
     behaviour.                                                             */
  var box = document.getElementById("lightbox");

  if (box) {
    var caption = box.querySelector(".label");

    var open = function (text) {
      if (caption) { caption.textContent = text; }
      box.setAttribute("data-open", "true");
      document.body.style.overflow = "hidden";
    };
    var close = function () {
      box.setAttribute("data-open", "false");
      document.body.style.overflow = "";
    };

    Array.prototype.forEach.call(document.querySelectorAll(".photo-grid button"), function (b) {
      b.addEventListener("click", function () {
        open(b.getAttribute("data-caption") || "Photo");
      });
    });

    box.addEventListener("click", function (e) {
      if (e.target === box || e.target.closest(".close")) { close(); }
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") { close(); }
    });
  }
})();
