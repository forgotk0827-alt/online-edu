const AUTH_KEYS = {
  client: {
    token: "online-edu-client-token",
    user: "online-edu-client-user"
  },
  admin: {
    token: "online-edu-admin-token",
    user: "online-edu-admin-user"
  }
};

export function getAuthScopeFromLocation() {
  if (typeof window === "undefined") return "client";
  return window.location.hash.startsWith("#/admin") ? "admin" : "client";
}

function scopeKeys(scope = getAuthScopeFromLocation()) {
  return AUTH_KEYS[scope] || AUTH_KEYS.client;
}

export function getAuthToken(scope) {
  return localStorage.getItem(scopeKeys(scope).token) || "";
}

export function getAuthUser(scope) {
  try {
    return JSON.parse(localStorage.getItem(scopeKeys(scope).user) || "null") || null;
  } catch {
    return null;
  }
}

export function setAuth(scope, token, user) {
  const keys = scopeKeys(scope);
  localStorage.setItem(keys.token, token);
  localStorage.setItem(keys.user, JSON.stringify(user || {}));
}

export function clearAuth(scope) {
  const keys = scopeKeys(scope);
  localStorage.removeItem(keys.token);
  localStorage.removeItem(keys.user);
}

export function hasAuth(scope) {
  return Boolean(getAuthToken(scope));
}

export function emitAuthChange() {
  window.dispatchEvent(new Event("storage"));
}
