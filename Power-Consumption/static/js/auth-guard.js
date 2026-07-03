// Include on any page that requires login: redirects to landing if signed
// out, and fills in the user pill + wires up logout buttons if signed in.
import { watchAuth, logOut } from "/static/js/auth.js";

// Avoid a flash of protected content before auth state resolves.
document.documentElement.style.visibility = "hidden";

watchAuth((user) => {
  if (!user) {
    window.location.href = "/";
    return;
  }

  document.documentElement.style.visibility = "visible";

  const label = user.email || "User";
  document.querySelectorAll(".user-name").forEach(el => { el.textContent = label; });
  document.querySelectorAll(".user-avatar").forEach(el => { el.textContent = label.charAt(0).toUpperCase(); });

  document.querySelectorAll("[data-logout]").forEach(btn => {
    btn.addEventListener("click", () => {
      logOut().then(() => { window.location.href = "/"; });
    });
  });
});
