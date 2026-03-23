// Fetch interceptor: auto-refresh with 401
const _originalFetch = window.fetch.bind(window);

window.fetch = async function (input, init = {}) {
  // Makes sure cookies are always send
  const options = { ...init, credentials: init.credentials ?? "include" };
  let response = await _originalFetch(input, options);

  if (response.status === 401) {
    // Avoid loop: no interception in the call /refresh or /login
    const url = typeof input === "string" ? input : input.url;
    if (url.includes("/auth/refresh") || url.includes("/auth/login")) {
      return response;
    }

    // Try to refresh access_token
    const refreshRes = await _originalFetch("/api/auth/refresh", {
      method: "POST",
      credentials: "include",
    });

    if (refreshRes.ok) {
      // Re-try the original request with the new token in cookie
      response = await _originalFetch(input, options);
    } else {
      // When the refresh fails, the sesion is expired
      if (!window.location.pathname.startsWith("/login")) {
        window.location.href = "/login";
      }
    }
  }

  return response;
};

// Fuctions
export async function isAuthenticated() {
  try {
    const res = await _originalFetch("/api/auth/me", { credentials: "include" });
    return res.ok;
  } catch {
    return false;
  }
}

export async function requireAuth() {
  if (!(await isAuthenticated())) {
    window.location.href = "/login";
  }
}

export async function logout() {
  await fetch("/api/auth/logout", { method: "POST", credentials: "include" });
  window.location.href = "/login";
}