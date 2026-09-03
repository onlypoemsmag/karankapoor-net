#!/usr/bin/env python3
"""Build the static pages for karankapoor.net.

Emits index.html, poems/index.html, photographs/index.html, 404.html,
home/index.html (redirect), sitemap.xml and robots.txt at the repo root.
All asset URLs are relative so the site works both at a GitHub Pages
project URL and at the custom domain. Canonical URLs point at the
eventual home, https://www.karankapoor.net/.
"""
import html, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANON = "https://www.karankapoor.net"

# ---------------------------------------------------------------- shared

def head(p, title, desc, canon_path, extra=""):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{CANON}{canon_path}">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{CANON}{canon_path}">
<meta property="og:image" content="{CANON}/assets/img/og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{CANON}/assets/img/og.jpg">
<link rel="icon" href="{p}assets/img/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{p}assets/css/site.css">
<link rel="preload" href="{p}assets/fonts/Fraunces-900.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{p}assets/fonts/Literata-400.woff2" as="font" type="font/woff2" crossorigin>
{extra}</head>
<body>
'''

def nav(p, current, mark_link=True):
    def a(href, label, key):
        cur = ' aria-current="page"' if key == current else ""
        return f'<li><a href="{href}"{cur}>{label}</a></li>'
    mark = (f'<a class="mark" href="{p if p else "./"}">Karan Kapoor</a>' if mark_link
            else '<span class="mark">Karan Kapoor</span>')
    return f'''  <header class="wrap site-head">
    {mark}
    <nav aria-label="Primary">
      <ul>
        {a(p if p else "./", "Home", "home")}
        {a(p + "poems/", "Poems", "poems")}
        {a(p + "photographs/", "Photographs", "photographs")}
      </ul>
    </nav>
  </header>'''

def footer(p):
    return f'''<footer class="site-foot on-dark">
  <div class="wrap row">
    <p class="place">Toronto, Canada</p>
    <div class="links">
      <a class="icon-link mail-link" href="mailto:karan@onlypoems.com" aria-label="Email Karan" title="Email Karan">
        <svg viewBox="0 0 34 26" width="28" height="21" aria-hidden="true"><rect class="m-body" x="1" y="1" width="32" height="24" rx="5"></rect><path class="m-flap" d="M3 4l14 11L31 4"></path></svg>
      </a>
      <a class="icon-link" href="https://onlypoems.com/" aria-label="ONLY POEMS" title="ONLY POEMS"><span class="logo-mask logo-op" style="--mask:url('{p}assets/img/op-logo.png')"></span></a>
      <a class="icon-link" href="https://www.strangepilgrims.com/" aria-label="Strange Pilgrims" title="Strange Pilgrims"><span class="logo-mask logo-sp" style="--mask:url('{p}assets/img/sp-logo.png')"></span></a>
      <a class="icon-link" href="https://www.instagram.com/whyareyounotreading/" aria-label="Instagram" title="Instagram">
        <svg viewBox="0 0 24 24" width="21" height="21" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><rect x="2.5" y="2.5" width="19" height="19" rx="5.5"/><circle cx="12" cy="12" r="4.4"/><circle cx="17.6" cy="6.4" r="1.15" fill="currentColor" stroke="none"/></svg>
      </a>
      <a class="icon-link" href="https://substack.com/@poetkarankapoor" aria-label="Substack" title="Substack">
        <svg viewBox="0 0 24 24" width="19" height="21" fill="currentColor" aria-hidden="true"><path d="M3 3.5h18v2.4H3zM3 8.2h18v2.4H3zM3 12.9h18V21l-9-4.6L3 21z"/></svg>
      </a>
    </div>
  </div>
</footer>

<script src="{p}assets/js/lenis.min.js"></script>
<script src="{p}assets/js/site.js"></script>'''

# ---------------------------------------------------------------- home

BIO = '''Karan Kapoor is the Co-Founder &amp; Editor-in-Chief of <a class="tlink" href="https://onlypoems.com/"><em>ONLY&nbsp;POEMS</em></a> and <a class="tlink" href="https://www.strangepilgrims.com/"><em>Strange Pilgrims</em></a>. His poems have appeared in <em>Best New Poets</em>, <em>AGNI</em>, <em>Shenandoah</em>, <em>Colorado Review</em>, and elsewhere, fiction in <em>JOYLAND</em> and <em>the other side of hope</em>, and translations in <em>The Offing</em> and <em>The Los Angeles Review</em>. He lives in Toronto, Canada with his wife &amp; daughter.'''

BLURBS = [
 ("""“I like Karan's poems. They have a mix of imagination and substance that's very appealing to me...“the sky must hate us/ as it sees everything we do.” I'd like to have written that...I’m especially drawn to the combination of directness and privacy in his poems, and the creation of a world within a world."""
  + '"', "Bob Hicok"),
 ("“These poems are, no bullshit, the real deal. You are the real deal, Karan. You are a real poet.”", "Kaveh Akbar"),
 ("“This devastating poem explores gendered responses to grief, and vividly evokes the aftermath of a process of cremation in India, seen here from the inside, as it were, from a speaker both embedded in his culture and in some ways estranged from it.”", "Mark Doty"),
]

PRIZES = '''A portion of this collection was a finalist for <em>Diode</em>, <em>Iron Horse Literary Review</em>, and <em>Tusculum Review</em> Chapbook Prizes, as well as shortlisted for the <em>Rattle</em> Chapbook prize. The full-length collection was also a finalist for the Charles B. Wheeler Poetry Prize (<em>The Journal</em>), the Felix Pollack Poetry Prize (University of Wisconsin-Madison Press) and the <em>Barrow Street</em> Book Prize. Poems from this collection have appeared in <em>Best New Poets</em>, <em>AGNI</em>, <em>Rattle</em>, <em>Plume</em>, <em>TAB</em>, <em>Poetry Ireland Review</em>, <em>New Welsh Review</em>, <em>Poetry Online</em>, <em>Frontier Poetry</em>, <em>The Margins</em>, <em>Southword</em> and elsewhere.'''

ABOUT1 = '''Though borrowing heavily from personal experience, this collection is constructed with dream and distance. Rooted in the specific time and place of modern Northern India, the themes I explore radiate outwards, and hopefully, this work is as much a mirror as it is a memoir. I am attempting to forge a space for myself, an Indian poet of a fragmented, autocratic past directly marred by the colonial era, in the American poetry scene.'''
ABOUT2 = '''This collection is composed of over 50 poems profiling my father through hybrid forms (such as the interview, questionnaire, visual fragments, prose poems) and traditional forms (villanelle, ghazal, free verse). The poems attempt an obsessive portrait of another that eventually becomes a self-portrait.'''

def home():
    p = ""
    jsonld = json.dumps({
      "@context": "https://schema.org",
      "@graph": [
        {"@type": "Person", "name": "Karan Kapoor", "url": CANON + "/",
         "jobTitle": "Poet and editor",
         "sameAs": ["https://onlypoems.com/", "https://www.strangepilgrims.com/",
                     "https://www.instagram.com/whyareyounotreading/",
                     "https://substack.com/@poetkarankapoor"]},
        {"@type": "Book", "name": "THIRST",
         "author": {"@type": "Person", "name": "Karan Kapoor"},
         "publisher": {"@type": "Organization", "name": "Alice James Books"},
         "datePublished": "2028-04",
         "url": "https://www.alicejamesbooks.org/bookstore/thirst"}
      ]
    }, indent=1)
    extra = f'<script type="application/ld+json">\n{jsonld}\n</script>\n'
    blurbs = "\n".join(f'''    <blockquote class="blurb rise" data-hidden>
      <span>
      <p>{b}</p>
      <cite>{c}</cite>
      </span>
    </blockquote>''' for b, c in BLURBS)
    return head(p, "Karan Kapoor",
        "Karan Kapoor is a poet and editor — Co-Founder & Editor-in-Chief of ONLY POEMS and Strange Pilgrims. His debut collection THIRST is forthcoming from Alice James Books in April 2028.",
        "/", extra) + f'''
<div class="cover on-yellow">
{nav(p, "home", mark_link=False)}
  <div class="wrap middle">
    <div class="grid">
      <div>
        <h1><span>Karan</span><span>Kapoor</span></h1>
        <p class="coverline">Poet &amp; editor</p>
      </div>
      <div class="portrait">
        <picture>
          <source type="image/webp" srcset="assets/img/portrait-800.webp 800w, assets/img/portrait-1600.webp 1600w" sizes="(max-width:800px) 19rem, 40vw">
          <img src="assets/img/portrait-1200.jpg" alt="Karan Kapoor reading Milan Kundera's The Festival of Insignificance, a crow flying past" width="900" height="1200">
        </picture>
      </div>
    </div>
  </div>
  <div class="wrap foot">
    <a class="down" href="#bio">Read on ↓</a>
  </div>
</div>

<main>
  <section class="bio wrap" id="bio">
    <p>{BIO}</p>
  </section>

  <section class="thirst on-dark">
    <div class="wrap">
      <p class="kicker rise" data-hidden><span>Debut poetry collection</span></p>
      <h2 class="rise" data-hidden><span>Thirst</span></h2>
      <p class="sub rise" data-hidden><span>Forthcoming from <a class="tlink" href="https://www.alicejamesbooks.org/bookstore/thirst">Alice James Books</a> in April 2028</span></p>
      <div class="cols">
        <div class="about">
          <p class="rise" data-hidden><span>{ABOUT1}</span></p>
          <p class="rise" data-hidden><span>{ABOUT2}</span></p>
          <p class="btnrow rise" data-hidden><a class="btn" href="https://www.alicejamesbooks.org/bookstore/thirst">Pre-order Here</a></p>
        </div>
        <figure class="rise" data-hidden>
          <span>
            <picture>
              <source type="image/webp" srcset="assets/img/chalhoub-700.webp 700w, assets/img/chalhoub-1200.webp 1200w" sizes="(max-width:800px) 92vw, 30vw">
              <img src="assets/img/chalhoub-1200.jpg" alt="A screaming figure in scribbled black ink against a cadmium-yellow room — artwork by Naji Chalhoub" width="845" height="1200" loading="lazy">
            </picture>
            <figcaption>Naji Chalhoub, ink and acrylics on paper (2018)</figcaption>
          </span>
        </figure>
      </div>
      <p class="prizes rise" data-hidden><span>{PRIZES}</span></p>
    </div>
  </section>

  <section class="blurbs wrap">
    <p class="kicker rise" data-hidden><span>Praise</span></p>
{blurbs}
  </section>
</main>

{footer(p)}
</body>
</html>
'''

# ---------------------------------------------------------------- poems

POEMS = [
 ("Circles", "Rattle", "https://rattle.com/circles-by-karan-kapoor/"),
 ("Water Under the Bed", "Margins", "https://aaww.org/water-under-the-bed/"),
 ("Love Letters", "The Good Life Review", "https://thegoodlifereview.com/2024/07/01/love-letters-by-karan-kapoor/"),
 ("How to Quit", "Hoax", "https://hoaxpublication.org/works/karan-kapoor-how-to-quit"),
 ("I Don’t Think It’s Fair", "The Maine Review", "https://www.mainereview.com/i-dont-think-its-fair/"),
 ("Rings of Saturn", "Banshee Press", "https://bansheepress.org/read/rings-of-saturn-by-karan-kapoor"),
 ("Things With Which We Foul the Ganges", "The Cincinnati Review", None),
 ("Dida", "Colorado Review", "https://muse.jhu.edu/pub/220/article/912441/pdf"),
 ("There Is No Time Here", "Bellevue Literary Review", None),
 ("A Braid of Unknowing I Tie Before You", "North American Review", None),
 ("Ghazal for Dida", "Rattle", "https://rattle.com/ghazal-for-dida-by-karan-kapoor/"),
 ("Holding the Fingers of Water", "Commonwealth Foundation", "https://www.addastories.org/holding-fingers-water/"),
 ("There Are 51 Descriptions of You on the Wall So Far", "The Ex-Puritan", "https://ex-puritan.ca/there-are-51-descriptions-of-you-on-the-wall-so-far"),
 ("‘I Am’ Is a Sentence, ‘You Are’ Is Not", "Poetry Online", "https://poetry.onl/read/kar-kap"),
 ("This One’s Barely About Him", "Poetry Ireland", None),
 ("Time Is a Motherfucker", "Strange Horizons", None),
 ("Snot Everywhere", "Shenandoah", None),
]
FICTION = ("A Perfect House Is Where No One Lives", "JOYLAND",
           "https://joylandmagazine.com/fiction/a-perfect-house-is-where-no-one-lives/")

def poem_row(t, v, u):
    inner = f'<span class="ptitle">{t}</span><span class="venue">{v}</span>'
    if u:
        return f'    <li><a class="rowlink" href="{u}">{inner}</a></li>'
    return f'    <li><div class="rowlink">{inner}</div></li>'

def poems():
    p = "../"
    rows = "\n".join(poem_row(*e) for e in POEMS)
    return head(p, "Poems — Karan Kapoor",
        "Selected poems by Karan Kapoor, published in Rattle, Margins, The Maine Review, Colorado Review, The Ex-Puritan and elsewhere — and a short story in JOYLAND.",
        "/poems/") + f'''
<div class="band on-yellow">
{nav(p, "poems")}
  <div class="wrap titlebox">
    <h1>Selected Poems</h1>
  </div>
</div>

<main class="ledger wrap">
  <ul class="poemlist">
{rows}
  </ul>

  <p class="kicker fiction-head">&amp; a short story</p>
  <ul class="poemlist">
{poem_row(*FICTION)}
  </ul>
</main>

{footer(p)}
</body>
</html>
'''

# ---------------------------------------------------------------- photographs

def photographs():
    p = "../"
    photos = json.load(open(os.path.join(ROOT, "assets", "photos", "manifest.json")))
    figs = []
    for ph in photos:
        t = html.escape(ph["title"])
        f = ph["files"]
        w700, w1200, w2000 = f["700"], f["1200"], f["2000"]
        jpg = f["jpg"]
        srcset = f'{p}assets/photos/{ph["slug"]}-700.webp {w700["w"]}w, {p}assets/photos/{ph["slug"]}-1200.webp {w1200["w"]}w, {p}assets/photos/{ph["slug"]}-2000.webp {w2000["w"]}w'
        figs.append(f'''<figure class="ph">
  <a href="{p}assets/photos/{ph["slug"]}-1200.jpg" class="phlink" data-large="{p}assets/photos/{ph["slug"]}-2000.webp" data-title="{t}">
    <picture>
      <source type="image/webp" srcset="{srcset}" sizes="(max-width:640px) 92vw, (max-width:1000px) 45vw, 30vw">
      <img src="{p}assets/photos/{ph["slug"]}-1200.jpg" alt="{t}" width="{jpg["w"]}" height="{jpg["h"]}" loading="lazy">
    </picture>
  </a>
  <figcaption>{t}</figcaption>
</figure>''')
    figs = "\n".join(figs)

    lightbox_js = '''<script>
(function(){
  var links=[].slice.call(document.querySelectorAll('.phlink'));
  var lb=document.getElementById('lb'), img=lb.querySelector('img'), cap=lb.querySelector('figcaption');
  var fig=lb.querySelector('figure'), btitle=lb.querySelector('.btitle');
  var flipwrap=lb.querySelector('.flipwrap'), cardtilt=lb.querySelector('.cardtilt'),
      flipper=lb.querySelector('.flipper'), gloss=lb.querySelector('.gloss');
  var reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;
  var idx=-1, lastFocus=null;

  /* the turn: yaw eased per-frame, direction from where you push (after op-poets.js) */
  var yaw=0, spinning=false, tFrom=0, tTo=0, tStart=0, faceBack=false;
  var TURN_MS = reduced ? 1 : 620;
  function easeInOut(k){ return k<.5 ? 4*k*k*k : 1-Math.pow(-2*k+2,3)/2; }
  function paint(){
    flipper.style.transform='rotateY('+yaw.toFixed(2)+'deg)';
    var a=((yaw%360)+360)%360;
    gloss.style.backgroundPosition=(125-(a/180)*170)+'% 0';
  }
  function land(){
    flipper.classList.toggle('landed',faceBack);
    fig.classList.toggle('showing-back',faceBack);
    flipwrap.setAttribute('aria-pressed',faceBack);
  }
  function spin(now){
    var k=Math.min(1,(now-tStart)/TURN_MS);
    yaw=tFrom+(tTo-tFrom)*easeInOut(k);
    paint();
    if(k>=1){ spinning=false; land(); return; }
    flipper.classList.remove('landed');
    requestAnimationFrame(spin);
  }
  function side(e){
    if(!e||e.clientX==null) return 1;
    var r=flipwrap.getBoundingClientRect();
    return e.clientX < r.left+r.width/2 ? -1 : 1;
  }
  function turn(dir){
    if(spinning) return;
    tFrom=yaw; tTo=yaw+180*(dir<0?-1:1);
    faceBack=!faceBack;
    fig.classList.toggle('showing-back',faceBack);
    tStart=performance.now(); spinning=true;
    requestAnimationFrame(spin);
  }
  function faceFront(){ spinning=false; yaw=tFrom=tTo=0; faceBack=false; flipper.classList.remove('landed'); fig.classList.remove('showing-back'); flipwrap.setAttribute('aria-pressed','false'); paint(); }
  flipwrap.addEventListener('click',function(e){ turn(side(e)); });
  flipwrap.addEventListener('keydown',function(e){ if(e.key==='Enter'||e.key===' '){e.preventDefault();turn(1);} });

  /* the lean (mouse only; letting go puts the card back flat) */
  function untilt(){ cardtilt.style.transform='none'; }
  flipwrap.addEventListener('pointermove',function(e){
    if(e.pointerType!=='mouse'||reduced) return;
    var r=flipwrap.getBoundingClientRect();
    var x=(e.clientX-r.left)/r.width, y=(e.clientY-r.top)/r.height;
    cardtilt.style.transform='rotateX('+(-(y-.5)*13.6).toFixed(2)+'deg) rotateY('+((x-.5)*16).toFixed(2)+'deg)';
  });
  flipwrap.addEventListener('pointerleave',untilt);
  flipwrap.addEventListener('pointerup',untilt);
  flipwrap.addEventListener('pointercancel',untilt);

  /* open: the card grows out of the tile you clicked */
  var EASE='cubic-bezier(.19,.86,.24,1)';
  function playOpen(fromEl){
    if(reduced||!fig.animate||!fromEl) return;
    var D=520;
    var to=fig.getBoundingClientRect();
    var r=fromEl.getBoundingClientRect();
    var sc=Math.max(0.08,r.width/to.width);
    var dx=(r.left+r.width/2)-(to.left+to.width/2);
    var dy=(r.top+r.height/2)-(to.top+to.height/2);
    fig.animate([
      {transform:'translate('+dx+'px,'+dy+'px) scale('+sc+')',opacity:.45},
      {transform:'none',opacity:1}
    ],{duration:D,easing:EASE});
    lb.animate([{opacity:0},{opacity:1}],{duration:Math.round(D*.75),easing:'ease-out'});
  }
  function show(i, originEl){
    idx=(i+links.length)%links.length;
    img.src=links[idx].dataset.large; img.alt=links[idx].dataset.title;
    cap.textContent=links[idx].dataset.title; btitle.textContent=links[idx].dataset.title;
    faceFront();
    if(lb.hidden){
      lastFocus=document.activeElement; lb.hidden=false; document.body.style.overflow='hidden';
      playOpen(originEl);
      lb.querySelector('.lb-close').focus();
    }
  }
  function hide(){ lb.hidden=true; document.body.style.overflow=''; faceFront(); untilt(); if(lastFocus)lastFocus.focus(); }
  links.forEach(function(a,i){a.addEventListener('click',function(e){e.preventDefault();show(i,a);});});
  lb.querySelector('.lb-close').addEventListener('click',hide);
  lb.querySelector('.lb-prev').addEventListener('click',function(){show(idx-1);});
  lb.querySelector('.lb-next').addEventListener('click',function(){show(idx+1);});
  lb.addEventListener('click',function(e){if(e.target===lb)hide();});
  document.addEventListener('keydown',function(e){
    if(lb.hidden)return;
    if(e.key==='Escape')hide();
    if(e.key==='ArrowLeft')show(idx-1);
    if(e.key==='ArrowRight')show(idx+1);
  });
  var x0=null;
  lb.addEventListener('touchstart',function(e){x0=e.touches[0].clientX;},{passive:true});
  lb.addEventListener('touchend',function(e){
    if(x0===null)return;
    var dx=e.changedTouches[0].clientX-x0; x0=null;
    if(Math.abs(dx)>40) show(dx<0? idx+1 : idx-1);
  },{passive:true});
})();
</script>'''

    return head(p, "Photographs — Karan Kapoor",
        "Photographs by Karan Kapoor. “A photograph: poetry made image.” —Sivi le poète",
        "/photographs/") + f'''
<div class="band on-yellow">
{nav(p, "photographs")}
  <div class="wrap titlebox">
    <h1>Photographs</h1>
  </div>
</div>

<main class="wrap">
  <div class="epigraph">
    <p>“A photograph: poetry made image.”</p>
    <cite>―Sivi le poète</cite>
  </div>
  <div class="grid">
{figs}
  </div>
</main>

{footer(p)}

<div class="lb" id="lb" hidden role="dialog" aria-modal="true" aria-label="Photograph viewer">
  <button class="lb-btn lb-close" aria-label="Close"><svg viewBox="0 0 16 16" width="13" height="13" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><path d="M2.5 2.5l11 11M13.5 2.5l-11 11"/></svg></button>
  <button class="lb-btn lb-prev" aria-label="Previous photograph"><svg viewBox="0 0 10 18" width="9" height="16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M8.5 1.5L1.5 9l7 7.5"/></svg></button>
  <figure>
    <div class="flipwrap" role="button" tabindex="0" aria-pressed="false" aria-label="Turn the photograph over to read the poem behind it">
      <div class="cardtilt">
        <div class="flipper">
          <div class="face front"><img alt=""><div class="gloss"></div></div>
          <div class="face back">
            <p class="btitle"></p>
            <p class="bpoem"><span>This is placeholder text — the real</span><span>pairing of poem to photograph</span><span>comes later. For now, imagine</span><span>a stanza living behind this image,</span><span>waiting to be turned over</span><span>like a card, like a leaf, like a page.</span></p>
            <p class="bnote">placeholder poem</p>
          </div>
        </div>
      </div>
    </div>
    <figcaption></figcaption>
  </figure>
  <button class="lb-btn lb-next" aria-label="Next photograph"><svg viewBox="0 0 10 18" width="9" height="16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M1.5 1.5L8.5 9l-7 7.5"/></svg></button>
</div>

{lightbox_js}
</body>
</html>
'''

# ---------------------------------------------------------------- small pages

def page_404():
    p = "/"  # 404 is served from anywhere; use root-absolute for the custom domain,
             # but Pages project URLs need relative — use plain links that work at root.
    p = ""
    return head(p, "Page not found — Karan Kapoor",
        "This page doesn't exist.", "/404.html") + f'''
<div class="cover on-yellow" style="min-height:100svh">
{nav(p, "")}
  <div class="wrap middle">
    <div>
      <h1 style="font-size:clamp(2.6rem,8vw,6rem)"><span>There is</span><span>no page here.</span></h1>
      <p class="coverline">Perhaps it became a poem. Try the <a href="./" style="color:inherit">home page</a>, the <a href="poems/" style="color:inherit">poems</a>, or the <a href="photographs/" style="color:inherit">photographs</a>.</p>
    </div>
  </div>
  <div class="wrap foot"></div>
</div>
</body>
</html>
'''

def home_redirect():
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Karan Kapoor</title>
<meta http-equiv="refresh" content="0; url=../">
<link rel="canonical" href="{CANON}/">
</head>
<body>
<p>This page has moved — <a href="../">continue to karankapoor.net</a>.</p>
</body>
</html>
'''

def sitemap():
    urls = "".join(f"  <url><loc>{CANON}{u}</loc></url>\n" for u in ["/", "/poems/", "/photographs/"])
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n'

def robots():
    return f"User-agent: *\nAllow: /\nDisallow: /archive/\nDisallow: /mocks/\n\nSitemap: {CANON}/sitemap.xml\n"

def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True) if os.path.dirname(path) else None
    open(full, "w").write(content)
    print(path)

if __name__ == "__main__":
    write("index.html", home())
    write("poems/index.html", poems())
    write("photographs/index.html", photographs())
    write("404.html", page_404())
    write("home/index.html", home_redirect())
    write("sitemap.xml", sitemap())
    write("robots.txt", robots())
