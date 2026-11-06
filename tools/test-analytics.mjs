import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { test } from 'node:test';
import { runInNewContext } from 'node:vm';

const source = readFileSync(new URL('../js/analytics.js', import.meta.url), 'utf8');
const key = 'jdubois-analytics-consent';
const gaId = 'G-92TRR0HJMQ';

function init({ consent = null, storageBlocked = false, loading = false } = {}) {
    let stored = consent;
    const scripts = [];
    const events = {};
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
    const window = {
        location: { hostname: 'www.julien-dubois.com' },
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
    const document = {
        readyState: loading ? 'loading' : 'complete',
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
