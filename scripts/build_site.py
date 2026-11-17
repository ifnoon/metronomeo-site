"""Build static guide pages, responsive images, and original timing examples.

Run in a Python environment with scripts/requirements.txt installed.
ffmpeg is needed only when regenerating the original audio examples.
The production container serves the generated files without Python or Node.
"""
from pathlib import Path
import hashlib
import html
import json
import math
import re
import struct
import subprocess
import tempfile
import wave

import markdown
from bs4 import BeautifulSoup
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://metronomeo.com'
DATE = '2026-11-17'
STORE = 'https://apps.apple.com/app/metronomeo/id6814776671'
GUIDES = {
    'anchor-shift': {
        'description': 'Practice with an offbeat metronome: move the click to e, &, a or triplets with Anchor Shift. Includes timing examples and exercises for drums and other instruments.',
        'related': ['count-subdivisions', 'gap-practice', 'polyrhythm-practice'],
        'source': ('Berklee Online: Time and Rhythm 1', 'https://online.berklee.edu/courses/time-and-rhythm-1'),
    },
    'count-subdivisions': {
        'description': 'Learn to count eighth notes, sixteenths and triplets with timing diagrams, audio examples and practical exercises that keep your main beat steady.',
        'related': ['polymeter-vs-polyrhythm', 'polyrhythm-practice', 'anchor-shift'],
    },
    'gap-practice': {
        'description': 'Use silent metronome bars to check your internal timing. Hear a gap exercise, learn to spot rushing and dragging, and progress without losing the pulse.',
        'related': ['anchor-shift', 'tempo-ladder', 'count-subdivisions'],
    },
    'tempo-ladder': {
        'description': 'Build a useful tempo ladder with a comfortable starting BPM, small steps and clear checkpoints. Includes a stepped tempo audio example and practice plan.',
        'related': ['gap-practice', 'count-subdivisions', 'ableton-link-midi'],
    },
    'polyrhythm-practice': {
        'description': 'Learn 3:2 and 4:3 polyrhythms with shared pulse diagrams, audio examples and step by step metronome exercises for hands, feet and instruments.',
        'related': ['polymeter-vs-polyrhythm', 'count-subdivisions', 'anchor-shift'],
    },
    'polymeter-vs-polyrhythm': {
        'description': 'Hear the difference between subdivisions, polyrhythms and polymetric groupings. Compare three against four with triplets and repeating accent patterns.',
        'related': ['polyrhythm-practice', 'count-subdivisions', 'anchor-shift'],
    },
    'ableton-link-midi': {
        'description': 'Connect an iPhone or iPad metronome with Ableton Link and MIDI. Share tempo, learn a foot pedal or CC knob, and troubleshoot timing and controller connections.',
        'related': ['tempo-ladder', 'polyrhythm-practice', 'gap-practice'],
        'source': ('Ableton: Link, tempo and MIDI synchronization', 'https://www.ableton.com/en/manual/synchronizing-with-link-tempo-follower-and-midi/'),
    },
}


def esc(value):
    return html.escape(str(value), quote=True)


def responsive_image(name, sizes, alt, eager=False, css=''):
    source = ROOT / 'assets' / f'{name}.png'
    digest = hashlib.sha256(source.read_bytes()).hexdigest()[:8]
    with Image.open(source) as image:
        width, height = image.size
        for target in (360, 720, 1080):
            path = ROOT / 'assets' / f'{name}-{target}-{digest}.webp'
            if not path.exists():
                image.resize((target, round(height * target / width)), Image.Resampling.LANCZOS).save(path, 'WEBP', quality=90, method=6)
    prefix = '' if eager else '../'
    srcset = ', '.join(f'{prefix}assets/{name}-{w}-{digest}.webp {w}w' for w in (360, 720, 1080))
    loading = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return f'<img class="{esc(css)}" src="{prefix}assets/{name}-720-{digest}.webp" srcset="{srcset}" sizes="{esc(sizes)}" width="{width}" height="{height}" {loading} alt="{esc(alt)}">'


def grid(label, cells, active, color='green'):
    parts = ''.join(f'<span class="pulse-cell {"hit" if i in active else "rest"}">{esc(value)}</span>' for i, value in enumerate(cells))
    return f'<div class="pulse-row {color}"><span class="pulse-name">{esc(label)}</span><div class="pulse-grid" style="--cells:{len(cells)}">{parts}</div></div>'


def audio(name, label, description):
    return f'<div class="audio-example"><h3>{esc(label)}</h3><audio controls preload="none" aria-label="{esc(label)}"><source src="../assets/audio/{name}.mp3" type="audio/mpeg"><a href="../assets/audio/{name}.mp3">Download this audio example</a></audio><p>{esc(description)}</p></div>'


def demos(slug):
    heading = '<section class="timing-example" aria-labelledby="hear-it"><h2 id="hear-it">Hear the relationship</h2>'
    disclaimer = '<p class="example-note">Original timing illustrations made for this guide. These are synthesized clicks, not app recordings. Audio plays only when you press Play.</p></section>'
    if slug == 'anchor-shift':
        body = grid('Beat grid', ['1', 'e', '&', 'a', '2', 'e', '&', 'a'], [0, 4]) + grid('Click on &', ['·', '·', '&', '·', '·', '·', '&', '·'], [2, 6], 'blue')
        body += audio('offbeat-and', 'The click on & at 60 BPM', 'The lower reference marks the numbered beats for four beats, then fades away. The higher click stays halfway between beats for the whole example. Keep your own beat in place.')
    elif slug == 'count-subdivisions':
        body = grid('Eighths', ['1', '&'], [0, 1]) + grid('Triplets', ['1', 'trip', 'let'], [0, 1, 2], 'blue') + grid('Sixteenths', ['1', 'e', '&', 'a'], [0, 1, 2, 3])
        for count, name in [(2, 'Eighth notes'), (3, 'Triplets'), (4, 'Sixteenth notes')]:
            body += audio(f'division-{count}', f'{name} at 60 BPM', 'The lower sound marks each main beat. Higher sounds fill the equal spaces between beats. Every example lasts four beats, so the main pulse stays the same.')
    elif slug == 'polyrhythm-practice':
        body = grid('Two beats', ['1', '·', '·', '2', '·', '·'], [0, 3]) + grid('Three pulses', ['1', '·', '2', '·', '3', '·'], [0, 2, 4], 'blue')
        body += audio('ratio-3-2', 'Three against two', 'The lower sound repeats two beats and the higher sound fits three pulses over the same two second cycle. Listen through four complete cycles.')
        body += grid('Three beats', ['1', '·', '·', '·', '2', '·', '·', '·', '3', '·', '·', '·'], [0, 4, 8]) + grid('Four pulses', ['1', '·', '·', '2', '·', '·', '3', '·', '·', '4', '·', '·'], [0, 3, 6, 9], 'blue')
        body += audio('ratio-4-3', 'Four against three', 'Three lower reference beats and four higher pulses share a three second cycle. The numbered reference beats remain at 60 BPM.')
    elif slug == 'polymeter-vs-polyrhythm':
        body = grid('Group of three', ['1', '2', '3'] * 4, [0, 3, 6, 9]) + grid('Group of four', ['1', '2', '3', '4'] * 3, [0, 4, 8], 'blue')
        body += audio('grouping-3-4', 'Three pulse and four pulse accent groups', 'Both parts share the same 60 BPM pulse. Lower accents repeat every three clicks; higher accents repeat every four. Their accents meet again on the thirteenth click, twelve pulses after the first.')
        body += '<p>Compare that with the <a href="polyrhythm-practice.html">3:2 and 4:3 examples</a>, where the two parts divide one shared cycle at different rates.</p>'
    elif slug == 'gap-practice':
        body = grid('Three bars', ['Sound', 'Silence', 'Return'], [0, 2])
        body += audio('silent-bar', 'One audible bar, one silent bar, then the return', 'At 60 BPM, hear four beats, keep four beats yourself during silence, then check your pulse against four returning beats. Each bar still lasts four seconds.')
    elif slug == 'tempo-ladder':
        body = grid('Three steps', ['60 BPM', '70 BPM', '80 BPM'], [0, 1, 2])
        body += audio('tempo-steps', 'A short stepped tempo example', 'Four beats at 60 BPM, four at 70, then four at 80. These large steps make the change easy to hear; use smaller steps and longer repetitions for your own practice.')
    else:
        return ''
    return heading + body + disclaimer


def render_audio():
    """Generate sample accurate click onsets and encode compact MP3 illustrations."""
    destination = ROOT / 'assets' / 'audio'
    destination.mkdir(exist_ok=True)
    def save(name, duration, events):
        out = destination / f'{name}.mp3'
        if out.exists():
            return
        rate = 22050
        samples = [0.0] * round(duration * rate)
        for time, frequency, level in events:
            start = round(time * rate)
            for n in range(round(.055 * rate)):
                if start + n >= len(samples):
                    break
                t = n / rate
                envelope = min(1, n / (rate * .002)) * math.exp(-t * 90)
                samples[start+n] += level * envelope * math.sin(2 * math.pi * frequency * t)
        with tempfile.TemporaryDirectory() as tmp:
            wav = Path(tmp) / 'example.wav'
            with wave.open(str(wav), 'wb') as f:
                f.setparams((1, 2, rate, 0, 'NONE', 'not compressed'))
                f.writeframes(b''.join(struct.pack('<h', round(max(-.98, min(.98, s)) * 32767)) for s in samples))
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(wav), '-codec:a', 'libmp3lame', '-b:a', '96k', str(out)], check=True)
    for div in (2, 3, 4):
        save(f'division-{div}', 4, [(i/div, 650 if i % div == 0 else 1400, .65 if i % div == 0 else .45) for i in range(4*div)])
    for a, b in ((3, 2), (4, 3)):
        save(f'ratio-{a}-{b}', b*4, [(i, 650, .6) for i in range(b*4)] + [(c*b+j*b/a, 1400, .45) for c in range(4) for j in range(a)])
    save('offbeat-and', 8, [(i, 650, .6*(1-i/4)) for i in range(4)] + [(i+.5, 1400, .5) for i in range(8)])
    save('silent-bar', 12, [(i, 650 if i % 4 else 900, .65) for i in list(range(4)) + list(range(8, 12))])
    save('grouping-3-4', 13, [(i, 500, .15) for i in range(13)] + [(i, 700, .6) for i in range(0, 13, 3)] + [(i, 1500, .45) for i in range(0, 13, 4)])
    events=[]
    start=0
    for bpm in (60, 70, 80):
        events.extend((start + i*60/bpm, 650, .65) for i in range(4))
        start += 4*60/bpm
    save('tempo-steps', start, events)


def build():
    render_audio()
    home_path = ROOT / 'index.html'
    home = home_path.read_text()
    for name, sizes, eager, css in [
        ('metronome', '(max-width:800px) 233px, 276px', True, ''),
        ('tempo-plan', '(max-width:800px) 225px, 255px', False, ''),
        ('duo-outer-anchor-shift', '(max-width:430px) calc(100vw - 50px), 380px', False, ''),
        ('duo-outer-playlists', '(max-width:480px) 85vw, 380px', False, 'duo-portrait'),
    ]:
        pattern = r'<img\b[^>]*src="assets/' + re.escape(name) + r'(?:\.png|-\d+-[a-f0-9]+\.webp)"[^>]*>'
        match = re.search(pattern, home)
        if match:
            alt = BeautifulSoup(match[0], 'html.parser').img.get('alt', '')
            tag = responsive_image(name, sizes, alt, eager, css).replace('../assets/', 'assets/')
            home = home[:match.start()] + tag + home[match.end():]
    home_path.write_text(home)
    titles = {slug: (ROOT / 'content' / f'{slug}.md').read_text().splitlines()[0][2:] for slug in GUIDES}
    for slug, meta in GUIDES.items():
        source = (ROOT / 'content' / f'{slug}.md').read_text()
        if re.search('[–—]', source):
            raise ValueError(f'{slug}: prose contains a dash')
        title=titles[slug]
        body=markdown.markdown(source.split('\n', 1)[1], extensions=['tables', 'toc'])
        soup=BeautifulSoup(body, 'html.parser')
        soup.find('p')['class']='summary'
        for table in soup.find_all('table'):
            wrapper=soup.new_tag('div', attrs={'class':'table-wrap'});table.wrap(wrapper)
            for th in table.find_all('th'):
                th['scope']='col'
        toc=[]
        for h in soup.find_all('h2'):
            toc.append(f'<a href="#{esc(h["id"])}">{esc(h.get_text())}</a>')
        examples=demos(slug)
        if examples:
            toc.insert(0, '<a href="#hear-it">Hear the relationship</a>')
        contents='<nav class="toc" aria-label="On this page"><p>In this guide</p>'+''.join(toc)+'</nav>'
        first=str(soup.find('p'));body=str(soup).replace(first,first+contents+examples,1)
        if slug=='anchor-shift':
            body+='<figure>'+responsive_image('duo-outer-anchor-shift', '(max-width:800px) 280px, 358px', 'Anchor Shift settings on iPhone Duo’s outer display')+'<figcaption>Choose the target under Land on and use Guide fade to establish your reference.</figcaption></figure>'
        if meta.get('source'):
            label,url=meta['source'];body+=f'<p class="source">Further reading: <a href="{esc(url)}">{esc(label)}</a>.</p>'
        url=f'{BASE}/guides/{slug}.html'
        schema={'@context':'https://schema.org','@graph':[{'@type':'Article','headline':title,'description':meta['description'],'author':{'@type':'Organization','name':'Metronomeo','url':BASE+'/'},'publisher':{'@type':'Organization','name':'ifnoon','url':BASE+'/'},'datePublished':DATE,'dateModified':DATE,'mainEntityOfPage':url,'inLanguage':'en'},breadcrumb(title,url)]}
        minutes=math.ceil(len(source.split())/220)
        related='<nav class="related" aria-label="Related guides"><h2>Related guides</h2>'+''.join(f'<a href="{s}.html">{esc(titles[s])}</a>' for s in meta['related'])+'</nav>'
        author='<p class="guide-credit">Written by the Metronomeo team at ifnoon. App instructions describe Metronomeo’s current controls. Questions or corrections? <a href="mailto:support@ifnoon.com">Contact us</a>.</p>'
        page=f'<!doctype html><html lang="en"><head>{head(title+" | Metronomeo",meta["description"],url)}<script type="application/ld+json">{json.dumps(schema)}</script></head><body><a class="skip" href="#main">Skip to content</a><main class="article wrap" id="main"><nav class="crumbs" aria-label="Breadcrumb"><a href="../">Metronomeo</a> / <a href="./">Practice guides</a></nav><h1>{esc(title)}</h1><p class="byline">By Metronomeo · <time datetime="{DATE}">17 November 2026</time> · {minutes} min read</p>{body}<aside><p>Explore these exercises in Metronomeo for iPhone and iPad. Advanced practice tools and connectivity are available with Pro.</p><a href="{STORE}">View Metronomeo on the App Store ↗</a></aside>{related}{author}</main>{footer()}</body></html>'
        (ROOT/'guides'/f'{slug}.html').write_text(page)
        print(slug, len(source.split()), 'words')
    listing=''.join(f'<li><a href="{slug}.html"><h2>{esc(titles[slug])}</h2><p>{esc(meta["description"])}</p></a></li>' for slug,meta in GUIDES.items())
    url=BASE+'/guides/'
    schema={'@context':'https://schema.org','@graph':[breadcrumb('Practice guides',url),{'@type':'CollectionPage','name':'Metronome practice guides','url':url,'hasPart':[{'@type':'Article','headline':titles[s],'url':f'{url}{s}.html'} for s in GUIDES]}]}
    (ROOT/'guides/index.html').write_text(f'<!doctype html><html lang="en"><head>{head("Metronome practice guides | Metronomeo","Practical rhythm exercises with diagrams and audio. Learn subdivisions, polyrhythms, offbeat clicks, silent bars, tempo ladders and Ableton Link.",url)}<script type="application/ld+json">{json.dumps(schema)}</script></head><body><main class="article wrap" id="main"><a class="back" href="../">← Metronomeo</a><h1>Practice guides</h1><p>Rhythm concepts and exercises you can hear, understand and use in your next session.</p><ul class="guide-list">{listing}</ul></main>{footer()}</body></html>')
    urls=[BASE+'/',BASE+'/guides/']+[f'{BASE}/guides/{s}.html' for s in GUIDES]+[BASE+'/support.html',BASE+'/privacy.html']
    (ROOT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>{u}</loc><lastmod>{DATE}</lastmod></url>\n' for u in urls)+'</urlset>\n')


def breadcrumb(title,url):
    items=[{'@type':'ListItem','position':1,'name':'Metronomeo','item':BASE+'/'}]
    items.append({'@type':'ListItem','position':2,'name':'Practice guides','item':BASE+'/guides/'})
    if url != BASE+'/guides/':
        items.append({'@type':'ListItem','position':3,'name':title,'item':url})
    return {'@type':'BreadcrumbList','itemListElement':items}


def head(title,description,url):
    return f'<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)}</title><meta name="description" content="{esc(description)}"><link rel="canonical" href="{url}"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(description)}"><meta property="og:type" content="{"website" if url.endswith("/guides/") else "article"}"><meta property="og:url" content="{url}"><meta property="og:site_name" content="Metronomeo"><link rel="icon" href="../assets/icon.png"><link rel="stylesheet" href="../landing.css"><script defer src="../analytics.js"></script>'


def footer():
    return '<footer class="wrap guide-footer"><a href="../">Metronomeo</a><div><a href="./">Practice guides</a><a href="../support.html">Support</a><a href="../privacy.html">Privacy</a></div></footer>'


if __name__=='__main__':
    build()
