import assert from 'node:assert/strict';
import { existsSync, readFileSync, readdirSync } from 'node:fs';
import { test } from 'node:test';
import { runInNewContext } from 'node:vm';

const root = new URL('../', import.meta.url);
const site = new URL('tools/.build/workshop-migration/', root);
const destination = 'https://www.julien-dubois.com/github-copilot-app-java-workshop/';
const chapters = [
    'index', 'setup', 'ticket', 'modes', 'skills', 'generate', 'canvas', 'tools',
    'parallel', 'integrate', 'rubber-duck', 'subagents', 'tokens', 'finish',
    'prompts', 'worksheet', 'facilitator'
];

function renderedRedirect(path, search = '', hash = '') {
    const html = readFileSync(new URL(path, site), 'utf8');
    const script = html.match(/<script>([\s\S]*?)<\/script>/)?.[1];
    assert.ok(script, `Missing redirect script: ${path}`);
    let redirected;
    runInNewContext(script, {
        window: { location: { search, hash, replace(url) { redirected = url; } } }
    });
    return { html, redirected };
}

for (const chapter of chapters) {
    const slug = chapter === 'index' ? '' : `${chapter}/`;
    test(`legacy ${chapter} links preserve their chapter, query and fragment`, () => {
        const source = readFileSync(new URL(`workshops/copilot-app/${chapter}.md`, root), 'utf8');
        assert.match(source, new RegExp(`^permalink: /workshops/copilot-app/${slug}$`, 'm'));
        assert.ok(source.includes(`redirect_to: ${destination}${slug}\n`));
        assert.ok(source.endsWith('---\n'), 'Legacy pages must not duplicate workshop content');
        for (const [search, hash] of [
            ['', ''], ['', '#move-running-shop'],
            ['?utm_source=conference', '#publish-the-reviewed-result']
        ]) {
            const { html, redirected } = renderedRedirect(
                `workshops/copilot-app/${slug}index.html`, search, hash);
            assert.equal(redirected, destination + slug + search + hash);
            assert.ok(html.includes(`rel="canonical" href="${destination}${slug}"`));
            assert.match(html, /<noscript>[\s\S]*http-equiv="refresh"/);
            assert.ok(html.includes(`href="${destination}${slug}"`));
            assert.doesNotMatch(html, /analytics\.js|gtag|consent-banner/);
        }
    });
}

test('the existing conferences redirect keeps its destination', () => {
    const { redirected } = renderedRedirect('current-talks.html', '?source=old', '#talks');
    assert.equal(redirected, 'https://www.julien-dubois.com/conferences');
});

test('conference links point directly to the workshop website and renamed template', () => {
    const html = readFileSync(new URL('conferences.html', site), 'utf8');
    assert.ok(html.includes('href="/github-copilot-app-java-workshop/"'));
    assert.ok(html.includes('href="https://github.com/jdubois/github-copilot-app-java-workshop"'));
    assert.doesNotMatch(html, /\/workshops\/copilot-app\/|copilot-shopping-cart-workshop/);
});

test('the website owns redirects, not a second copy of the workshop', () => {
    const sources = readdirSync(new URL('workshops/copilot-app/', root));
    assert.deepEqual(sources.sort(), chapters.map(chapter => `${chapter}.md`).sort());
    for (const path of [
        '_data/copilot_workshop.yml', '_includes/copilot-workshop-nav.html',
        'tools/copilot-workshop/check-site.py', 'workshops/copilot-app/assets'
    ]) {
        assert.equal(existsSync(new URL(path, root)), false, path);
    }
    const layout = readFileSync(new URL('_layouts/default.html', root), 'utf8');
    assert.doesNotMatch(layout, /copilot-workshop-nav|\/workshops\/copilot-app\//);
});
