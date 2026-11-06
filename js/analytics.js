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
    var syncSlideTracking = null;

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

    function initSlideTracking() {
        var deck = window.Reveal;
        if (!deck) {
            return null;
        }

        var slide = null;
        var details = null;
        var viewed = false;
        var startedAt = null;
        var pageActive = true;

        function send(name, duration) {
            var params = Object.assign({
                send_to: GA_ID,
                transport_type: 'beacon'
            }, details);
            if (duration !== undefined) {
                params.engagement_time_msec = duration;
                params.slide_duration_ms = duration;
            }
            window.gtag('event', name, params);
        }

        function flush() {
            if (startedAt === null) {
                return;
            }
            var duration = Math.round(window.performance.now() - startedAt);
            startedAt = null;
            if (duration > 0) {
                send('slide_engagement', duration);
            }
        }

        function sync() {
            if (readConsent() !== GRANTED) {
                slide = null;
                details = null;
                viewed = false;
                startedAt = null;
                return;
            }
            if (!deck.isReady()) {
                return;
            }
            var current = deck.getCurrentSlide();
            if (current !== slide) {
                flush();
                slide = current;
                viewed = false;
                var number = deck.getSlidePastCount(slide) + 1;
                var heading = slide.querySelector('h1, h2, h3, h4, h5, h6');
                details = {
                    deck_path: window.location.pathname,
                    deck_language: document.documentElement.lang,
                    slide_number: number,
                    slide_title: heading ? heading.textContent.replace(/\s+/g, ' ').trim().slice(0, 100) : 'Slide ' + number
                };
            }
            if (!pageActive || document.hidden) {
                flush();
                return;
            }
            if (!viewed) {
                send('slide_view');
                viewed = true;
            }
            if (startedAt === null) {
                startedAt = window.performance.now();
            }
        }

        deck.on('ready', sync);
        deck.on('slidechanged', sync);
        document.addEventListener('visibilitychange', sync);
        window.addEventListener('pagehide', function () {
            pageActive = false;
            sync();
        });
        window.addEventListener('pageshow', function () {
            pageActive = true;
            sync();
        });
        return sync;
    }

    function apply(consent) {
        if (consent === GRANTED) {
            loadGA();
        } else {
            disableGA();
        }
        if (syncSlideTracking) {
            syncSlideTracking();
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
        if (Array.prototype.some.call(manage, function (el) {
            return el.classList.contains('consent-manage-deck');
        })) {
            syncSlideTracking = initSlideTracking();
        }

        function show() {
            banner.hidden = false;
            accept.focus();
        }

        function hide() {
            banner.hidden = true;
        }

        function updateManage(consent) {
            Array.prototype.forEach.call(manage, function (el) {
                if (el.classList.contains('consent-manage-deck')) {
                    el.hidden = consent === GRANTED;
                }
            });
        }

        function choose(consent, returnFocus) {
            setConsent(consent);
            hide();
            updateManage(consent);
            if (returnFocus && manage.length && !manage[0].hidden) {
                manage[0].focus();
            }
        }

        var current = readConsent();
        updateManage(current);
        if (current !== null) {
            apply(current);
        } else if (current === null) {
            banner.hidden = false;
        }

        accept.addEventListener('click', function () { choose(GRANTED, true); });
        decline.addEventListener('click', function () { choose(DENIED, true); });
        banner.addEventListener('keydown', function (e) {
            // Reveal.js must not interpret consent interactions as slide shortcuts.
            e.stopPropagation();
            if (e.key === 'Escape') {
                choose(DENIED, true);
            }
        });
        Array.prototype.forEach.call(manage, function (el) {
            el.addEventListener('click', show);
            el.addEventListener('keydown', function (e) {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.stopPropagation();
                }
            });
        });

        window.addEventListener('storage', function (e) {
            if (e.key !== KEY) {
                return;
            }
            var consent = e.newValue === GRANTED ? GRANTED : DENIED;
            sessionConsent = consent;
            apply(consent);
            updateManage(consent);
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
