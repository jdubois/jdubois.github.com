import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { test } from 'node:test';
import { runInNewContext } from 'node:vm';

const source = readFileSync(new URL('../js/analytics.js', import.meta.url), 'utf8');
const key = 'jdubois-analytics-consent';
const gaId = 'G-92TRR0HJMQ';

function init({
    consent = null, storageBlocked = false, loading = false, deck = false,
    reveal = false, ready = true, initialSlide = 0, hidden = false
} = {}) {
    let stored = consent;
    const scripts = [];
    const events = {};
    const revealEvents = {};
    let now = 0;
    let slideIndex = initialSlide;
    const slides = [' Welcome\n to the deck ', 'Architecture', null].map(title => ({
        querySelector: () => title === null ? null : { textContent: title }
    }));
    let focused = null;
    function element() {
        return {
            hidden: true,
            events: {},
            addEventListener(name, handler) { this.events[name] = handler; },
            focus() { focused = this; }
        };
    }
    const banner = element();
    const accept = element();
    const decline = element();
    const manage = element();
    manage.hidden = false;
    manage.classList = { contains: name => deck && name === 'consent-manage-deck' };
    const window = {
        location: {
            hostname: 'www.julien-dubois.com',
            pathname: '/conferences/example/index-en.html'
        },
        performance: { now: () => now },
        localStorage: {
            getItem(name) {
                assert.equal(name, key);
                if (storageBlocked) throw new Error('Storage blocked');
                return stored;
            },
            setItem(name, value) {
                assert.equal(name, key);
                if (storageBlocked) throw new Error('Storage blocked');
                stored = value;
            }
        },
        addEventListener(name, handler) { events[name] = handler; }
    };
    if (reveal) {
        window.Reveal = {
            isReady: () => ready,
            getCurrentSlide: () => slides[slideIndex],
            getSlidePastCount: slide => slides.indexOf(slide),
            on(name, handler) { revealEvents[name] = handler; }
        };
    }
    const document = {
        readyState: loading ? 'loading' : 'complete',
        hidden,
        documentElement: { lang: 'en' },
        cookie: '',
        head: { appendChild(script) { scripts.push(script); } },
        createElement() { return {}; },
        getElementById(id) {
            return { 'consent-banner': banner, 'consent-accept': accept, 'consent-decline': decline }[id];
        },
        querySelectorAll() { return [manage]; },
        addEventListener(name, handler) { events[name] = handler; }
    };
    runInNewContext(source, { window, document });
    return {
        window, document, banner, accept, decline, manage, scripts, events,
        revealEvents,
        advance(ms) { now += ms; },
        navigate(index) {
            slideIndex = index;
            revealEvents.slidechanged?.();
        },
        ready() {
            ready = true;
            revealEvents.ready?.();
        },
        analyticsEvents: () => Array.from(window.dataLayer || [])
            .filter(args => args[0] === 'event')
            .map(args => ({ name: args[1], params: args[2] })),
        stored: () => stored,
        focused: () => focused
    };
}

test('no prior consent shows the banner without contacting Google', () => {
    const page = init();
    assert.equal(page.banner.hidden, false);
    assert.equal(page.scripts.length, 0);
    assert.equal(page.window.dataLayer, undefined);
});

test('acceptance loads the existing GA property exactly once', () => {
    const page = init();
    page.accept.events.click();
    assert.equal(page.stored(), 'granted');
    assert.equal(page.banner.hidden, true);
    assert.equal(page.focused(), page.manage);
    assert.equal(page.scripts[0].src, `https://www.googletagmanager.com/gtag/js?id=${gaId}`);
    assert.equal(page.window.dataLayer[1][0], 'config');
    assert.equal(page.window.dataLayer[1][1], gaId);
    page.manage.events.click();
    page.accept.events.click();
    assert.equal(page.scripts.length, 1);
});

test('consent granted on another page loads GA without showing a second banner', () => {
    const page = init({ consent: 'granted' });
    assert.equal(page.banner.hidden, true);
    assert.equal(page.scripts.length, 1);
});

test('declining and persisted denial never load GA', () => {
    const page = init();
    page.decline.events.click();
    assert.equal(page.stored(), 'denied');
    assert.equal(page.window[`ga-disable-${gaId}`], true);
    assert.equal(page.scripts.length, 0);
    const nextPage = init({ consent: 'denied' });
    assert.equal(nextPage.banner.hidden, true);
    assert.equal(nextPage.window[`ga-disable-${gaId}`], true);
    assert.equal(nextPage.scripts.length, 0);
});

test('cookie settings allow revocation and clear analytics cookies', () => {
    const page = init({ consent: 'granted' });
    page.document.cookie = '_ga=example';
    page.manage.events.click();
    assert.equal(page.banner.hidden, false);
    assert.equal(page.focused(), page.accept);
    page.decline.events.click();
    assert.equal(page.window[`ga-disable-${gaId}`], true);
    assert.match(page.document.cookie, /_ga=; path=\/; expires=/);
});

test('storage events share acceptance and revocation across tabs', () => {
    const page = init();
    page.events.storage({ key, newValue: 'granted' });
    assert.equal(page.banner.hidden, true);
    assert.equal(page.scripts.length, 1);
    page.events.storage({ key, newValue: 'denied' });
    assert.equal(page.window[`ga-disable-${gaId}`], true);
});

test('blocked storage still honors the choice in memory', () => {
    const page = init({ storageBlocked: true });
    page.accept.events.click();
    assert.equal(page.scripts.length, 1);
    page.manage.events.click();
    page.decline.events.click();
    assert.equal(page.window[`ga-disable-${gaId}`], true);
});

test('consent keyboard interactions do not reach Reveal shortcuts', () => {
    const page = init();
    let stopped = 0;
    const stopPropagation = () => { stopped += 1; };
    page.manage.events.keydown({ key: 'Enter', stopPropagation });
    page.manage.events.keydown({ key: ' ', stopPropagation });
    page.manage.events.keydown({ key: 'ArrowRight', stopPropagation });
    assert.equal(stopped, 2);
    page.banner.events.keydown({ key: ' ', stopPropagation });
    assert.equal(page.scripts.length, 0);
    page.banner.events.keydown({ key: 'Escape', stopPropagation });
    assert.equal(stopped, 4);
    assert.equal(page.stored(), 'denied');
    assert.equal(page.banner.hidden, true);
});

test('deferred initialization waits for the consent markup', () => {
    const page = init({ loading: true });
    assert.equal(page.banner.events.keydown, undefined);
    page.events.DOMContentLoaded();
    assert.equal(page.banner.hidden, false);
    assert.equal(typeof page.accept.events.click, 'function');
});

test('deck cookie settings hide after acceptance without focusing the hidden button', () => {
    const page = init({ deck: true });
    assert.equal(page.manage.hidden, false);
    page.accept.events.click();
    assert.equal(page.manage.hidden, true);
    assert.notEqual(page.focused(), page.manage);
    assert.equal(page.banner.hidden, true);
    assert.equal(page.scripts.length, 1);
});

test('saved acceptance hides deck cookie settings but leaves website settings available', () => {
    assert.equal(init({ deck: true, consent: 'granted' }).manage.hidden, true);
    assert.equal(init({ consent: 'granted' }).manage.hidden, false);
});

test('deck cookie settings remain available after denial', () => {
    const page = init({ deck: true });
    page.decline.events.click();
    assert.equal(page.manage.hidden, false);
    assert.equal(page.focused(), page.manage);
    page.manage.events.click();
    assert.equal(page.banner.hidden, false);
    assert.equal(init({ deck: true, consent: 'denied' }).manage.hidden, false);
});

test('deck cookie settings follow consent changes in other tabs', () => {
    const page = init({ deck: true });
    page.events.storage({ key, newValue: 'granted' });
    assert.equal(page.manage.hidden, true);
    page.events.storage({ key, newValue: 'denied' });
    assert.equal(page.manage.hidden, false);
    page.manage.events.click();
    assert.equal(page.banner.hidden, false);
});

test('deck cookie settings hide after acceptance even when storage is blocked', () => {
    const page = init({ deck: true, storageBlocked: true });
    page.accept.events.click();
    assert.equal(page.manage.hidden, true);
    assert.equal(page.scripts.length, 1);
});

test('slide tracking starts at acceptance with the current slide, not earlier navigation', () => {
    const page = init({ deck: true, reveal: true });
    page.advance(10000);
    page.navigate(1);
    assert.deepEqual(page.analyticsEvents(), []);
    page.accept.events.click();
    const [view] = page.analyticsEvents();
    assert.equal(view.name, 'slide_view');
    assert.equal(view.params.deck_path, '/conferences/example/index-en.html');
    assert.equal(view.params.deck_language, 'en');
    assert.equal(view.params.slide_number, 2);
    assert.equal(view.params.slide_title, 'Architecture');
    assert.equal(view.params.send_to, gaId);
    page.advance(1200);
    page.navigate(2);
    const [, engagement, nextView] = page.analyticsEvents();
    assert.equal(engagement.name, 'slide_engagement');
    assert.equal(engagement.params.slide_number, 2);
    assert.equal(engagement.params.slide_duration_ms, 1200);
    assert.equal(engagement.params.engagement_time_msec, 1200);
    assert.equal(nextView.params.slide_number, 3);
    assert.equal(nextView.params.slide_title, 'Slide 3');
});

test('saved consent records a deep-linked initial slide and normalizes titles', () => {
    const page = init({ deck: true, reveal: true, consent: 'granted', initialSlide: 1 });
    assert.equal(page.analyticsEvents()[0].params.slide_number, 2);
    page.navigate(0);
    assert.equal(page.analyticsEvents().at(-1).params.slide_title, 'Welcome to the deck');
});

test('slide tracking waits for Reveal readiness and does not duplicate its first view', () => {
    const page = init({ deck: true, reveal: true, consent: 'granted', ready: false });
    assert.deepEqual(page.analyticsEvents(), []);
    page.advance(5000);
    page.ready();
    page.ready();
    page.navigate(0);
    assert.equal(page.analyticsEvents().length, 1);
    page.advance(900);
    page.navigate(1);
    assert.equal(page.analyticsEvents()[1].params.slide_duration_ms, 900);
});

test('hidden-tab time is excluded and returning does not add another view', () => {
    const page = init({ deck: true, reveal: true, consent: 'granted' });
    page.advance(1000);
    page.document.hidden = true;
    page.events.visibilitychange();
    page.advance(60000);
    page.document.hidden = false;
    page.events.visibilitychange();
    page.advance(500);
    page.navigate(1);
    assert.deepEqual(page.analyticsEvents().map(event => event.name),
        ['slide_view', 'slide_engagement', 'slide_engagement', 'slide_view']);
    assert.deepEqual(page.analyticsEvents().filter(event => event.name === 'slide_engagement')
        .map(event => event.params.slide_duration_ms), [1000, 500]);
});

test('background slides are counted only when visible', () => {
    const page = init({ deck: true, reveal: true, consent: 'granted', hidden: true });
    page.advance(1000);
    page.navigate(1);
    assert.deepEqual(page.analyticsEvents(), []);
    page.document.hidden = false;
    page.events.visibilitychange();
    assert.equal(page.analyticsEvents().length, 1);
    assert.equal(page.analyticsEvents()[0].params.slide_number, 2);
});

test('page exit flushes time once and back-forward restoration resumes timing', () => {
    const page = init({ deck: true, reveal: true, consent: 'granted' });
    page.advance(2000);
    page.events.pagehide();
    page.document.hidden = true;
    page.events.visibilitychange();
    assert.equal(page.analyticsEvents()[1].params.slide_duration_ms, 2000);
    assert.equal(page.analyticsEvents()[1].params.transport_type, 'beacon');
    page.advance(10000);
    page.document.hidden = false;
    page.events.pageshow();
    page.advance(300);
    page.navigate(1);
    assert.equal(page.analyticsEvents()[2].params.slide_duration_ms, 300);
});

test('revocation discards pending slide time and renewed consent starts fresh', () => {
    const page = init({ deck: true, reveal: true, consent: 'granted' });
    page.advance(5000);
    page.events.storage({ key, newValue: 'denied' });
    page.navigate(1);
    page.events.pagehide();
    assert.equal(page.analyticsEvents().length, 1);
    page.events.pageshow();
    page.advance(10000);
    page.events.storage({ key, newValue: 'granted' });
    assert.equal(page.analyticsEvents().at(-1).params.slide_number, 2);
    page.advance(700);
    page.navigate(2);
    assert.equal(page.analyticsEvents().at(-2).params.slide_duration_ms, 700);
});

test('denied consent never sends slide events', () => {
    const page = init({ deck: true, reveal: true, consent: 'denied' });
    page.navigate(1);
    page.advance(1000);
    page.events.pagehide();
    assert.deepEqual(page.analyticsEvents(), []);
    assert.equal(page.scripts.length, 0);
});

test('slide events work with blocked storage and are not installed on website pages', () => {
    const deck = init({ deck: true, reveal: true, storageBlocked: true });
    deck.accept.events.click();
    assert.equal(deck.analyticsEvents()[0].name, 'slide_view');
    const website = init({ reveal: true, consent: 'granted' });
    assert.deepEqual(website.analyticsEvents(), []);
    assert.equal(website.revealEvents.slidechanged, undefined);
});
