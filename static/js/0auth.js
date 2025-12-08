// oauth.js - helper for Google OAuth UI (frontend).
// NOTE: Real OAuth requires server-side handling and a Google OAuth client.
// This helper builds a Google Authorization URL if you set client_id & redirect_uri.
// Use only after you register an OAuth client in Google Cloud Console.

const oauth = (function () {
    const GOOGLE_AUTH_BASE = 'https://accounts.google.com/o/oauth2/v2/auth';

    function startGoogleOAuth(opts = {}) {
        // opts: { client_id, redirect_uri, scope, state }
        const client_id = opts.client_id || ''; // **REPLACE** with your client_id for real flow
        const redirect_uri = opts.redirect_uri || ''; // e.g. https://yourdomain.com/oauth2callback
        const scope = opts.scope || 'openid email profile';
        const state = opts.state || '';

        if (!client_id || !redirect_uri) {
            // fallback: UI-only demo
            alert('Demo: Google OAuth button clicked. For real sign-in, set client_id and redirect_uri in oauth.startGoogleOAuth().');
            return;
        }

        const url = new URL(GOOGLE_AUTH_BASE);
        url.searchParams.set('client_id', client_id);
        url.searchParams.set('redirect_uri', redirect_uri);
        url.searchParams.set('response_type', 'code');
        url.searchParams.set('scope', scope);
        url.searchParams.set('access_type', 'offline');
        if (state) url.searchParams.set('state', state);
        // Open in same tab to allow redirect handling
        window.location.href = url.toString();
    }

    // attach demo handlers to buttons (if present)
    document.addEventListener('DOMContentLoaded', function () {
        const googleLogin = document.getElementById('googleLoginBtn');
        const googleSignUp = document.getElementById('googleSignUpBtn');
        if (googleLogin) googleLogin.addEventListener('click', () => startGoogleOAuth());
        if (googleSignUp) googleSignUp.addEventListener('click', () => startGoogleOAuth());
    });

    return {startGoogleOAuth};
})();
