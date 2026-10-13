/*
 * Consent-gated Google Analytics.
 * gtag.js is injected only after the visitor accepts; nothing touches the network or writes a
 * cookie before that. The choice is kept in localStorage (in memory if storage is unavailable).
 */
(function () {
    'use strict';

    var GA_ID = 'G-92TRR0HJMQ';
    var KEY = 'jdubois-analytics-consent';
    var GRANTED = 'granted';
    var DENIED = 'denied';

    var scriptLoaded = false;
    var sessionConsent = null;

    function readConsent() {
        if (sessionConsent) {
            return sessionConsent;
        }
        try {
            var stored = window.localStorage.getItem(KEY);
            return stored === GRANTED || stored === DENIED ? stored : null;
        } catch (e) {
            return null;
        }
    }

    function loadGA() {
        window['ga-disable-' + GA_ID] = false;
        if (scriptLoaded) {
            return;
        }
        scriptLoaded = true;
        window.dataLayer = window.dataLayer || [];
        window.gtag = function () {
            window.dataLayer.push(arguments);
        };
        window.gtag('js', new Date());
        window.gtag('config', GA_ID);
        var s = document.createElement('script');
        s.async = true;
        s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_ID;
        document.head.appendChild(s);
    }

    function clearCookies() {
        var host = window.location.hostname;
        var labels = host.split('.');
        var domains = ['', host, '.' + host];
        if (labels.length > 2) {
            domains.push('.' + labels.slice(-2).join('.'));
        }
        document.cookie.split(';').forEach(function (c) {
            var name = c.split('=')[0].trim();
            if (name === '_ga' || name === '_gid' || name.indexOf('_ga_') === 0 || name.indexOf('_gat') === 0) {
                domains.forEach(function (d) {
                    document.cookie = name + '=; path=/; expires=Thu, 01 Jan 1970 00:00:01 GMT' + (d ? '; domain=' + d : '');
                });
            }
        });
    }

    function disableGA() {
        window['ga-disable-' + GA_ID] = true;
        clearCookies();
    }

    function apply(consent) {
        if (consent === GRANTED) {
            loadGA();
        } else {
            disableGA();
        }
    }

    function setConsent(consent) {
        sessionConsent = consent;
        try {
            window.localStorage.setItem(KEY, consent);
        } catch (e) {
            // Choice is still honoured for this page session.
        }
        apply(consent);
    }

    function init() {
        var banner = document.getElementById('consent-banner');
        var accept = document.getElementById('consent-accept');
        var decline = document.getElementById('consent-decline');
        var manage = document.querySelectorAll('[data-consent-manage]');
        if (!banner || !accept || !decline) {
            return;
        }

        function show() {
            banner.hidden = false;
            accept.focus();
        }

        function hide() {
            banner.hidden = true;
        }

        function choose(consent, returnFocus) {
            setConsent(consent);
            hide();
            if (returnFocus && manage.length) {
                manage[0].focus();
            }
        }

        var current = readConsent();
        if (current === GRANTED) {
            apply(GRANTED);
        } else if (current === null) {
            banner.hidden = false;
        }

        accept.addEventListener('click', function () { choose(GRANTED, true); });
        decline.addEventListener('click', function () { choose(DENIED, true); });
        banner.addEventListener('keydown', function (e) {
            if (e.key === 'Escape') {
                choose(DENIED, true);
            }
        });
        Array.prototype.forEach.call(manage, function (el) {
            el.addEventListener('click', show);
        });

        window.addEventListener('storage', function (e) {
            if (e.key !== KEY) {
                return;
            }
            var consent = e.newValue === GRANTED ? GRANTED : DENIED;
            sessionConsent = consent;
            apply(consent);
            if (consent !== null) {
                hide();
            }
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
