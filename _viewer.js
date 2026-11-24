/* 上架圖庫共用看圖工具：大圖瀏覽切換＋點圖全螢幕、左右滑換張 */
(function () {
  var grids = document.querySelectorAll('.g');
  if (!grids.length) return;
  var css = document.createElement('style');
  css.textContent =
    '.vbar{position:sticky;top:0;z-index:5;display:flex;gap:8px;align-items:center;padding:10px 0;margin:0 0 10px;background:var(--bg,#f5f5f7)}' +
    '.vbar button{font:inherit;font-size:15px;padding:9px 16px;border-radius:999px;border:1px solid #d2d2d7;background:#fff;color:#1d1d1f;cursor:pointer}' +
    '.vbar button.on{background:#1d1d1f;color:#fff;border-color:#1d1d1f}.vbar small{color:#6e6e73;font-size:13px}' +
    'body.big .g{grid-template-columns:1fr;max-width:760px;margin:0 auto;gap:18px}' +
    'body.big .g img{aspect-ratio:auto;object-fit:contain;background:#fff}' +
    '.lb{position:fixed;inset:0;z-index:99;background:rgba(0,0,0,.92);display:none;flex-direction:column;align-items:center;justify-content:center;touch-action:pan-y}' +
    '.lb.on{display:flex}.lb img{max-width:96vw;max-height:84vh;object-fit:contain;user-select:none;-webkit-user-drag:none}' +
    '.lb .cap{color:#ddd;font-size:13px;margin-top:10px;text-align:center;padding:0 16px;word-break:break-all}' +
    '.lb .cap a{color:#8cc8ff;margin-left:10px}' +
    '.lb button{position:absolute;background:rgba(255,255,255,.14);color:#fff;border:0;font-size:28px;width:52px;height:52px;border-radius:50%;cursor:pointer}' +
    '.lb .x{top:14px;right:14px}.lb .p{left:10px;top:50%;margin-top:-26px}.lb .n{right:10px;top:50%;margin-top:-26px}' +
    '@media (max-width:640px){.lb .p,.lb .n{display:none}}';
  document.head.appendChild(css);

  var links = [];
  grids.forEach(function (g) { g.querySelectorAll('a').forEach(function (a) { if (/\.(jpe?g|png|webp)$/i.test(a.getAttribute('href') || '')) links.push(a); }); });

  // 工具列
  var bar = document.createElement('div'); bar.className = 'vbar';
  var b1 = document.createElement('button'); b1.textContent = '小圖';
  var b2 = document.createElement('button'); b2.textContent = '大圖瀏覽';
  var tip = document.createElement('small'); tip.textContent = '點任一張可全螢幕，左右滑換下一張';
  bar.appendChild(b1); bar.appendChild(b2); bar.appendChild(tip);
  grids[0].parentNode.insertBefore(bar, grids[0].previousElementSibling && grids[0].previousElementSibling.tagName === 'H2' ? grids[0].previousElementSibling : grids[0]);
  function mode(big) {
    document.body.classList.toggle('big', big); b1.classList.toggle('on', !big); b2.classList.toggle('on', big);
    links.forEach(function (a) { var im = a.querySelector('img'); if (im && big) im.loading = 'eager'; });
    try { localStorage.setItem('yaViewBig', big ? '1' : '0'); } catch (e) {}
  }
  var saved = null; try { saved = localStorage.getItem('yaViewBig'); } catch (e) {}
  mode(saved === null ? window.innerWidth < 700 : saved === '1');
  b1.onclick = function () { mode(false); }; b2.onclick = function () { mode(true); };

  // 全螢幕
  var lb = document.createElement('div'); lb.className = 'lb';
  lb.innerHTML = '<img alt=""><div class="cap"></div><button class="x" aria-label="關閉">×</button><button class="p" aria-label="上一張">‹</button><button class="n" aria-label="下一張">›</button>';
  document.body.appendChild(lb);
  var im = lb.querySelector('img'), cap = lb.querySelector('.cap'), cur = 0;
  function show(i) {
    cur = (i + links.length) % links.length;
    var a = links[cur], href = a.getAttribute('href'), name = href.split('/').pop();
    im.src = href;
    cap.innerHTML = (cur + 1) + ' / ' + links.length + '　' + name.replace(/</g, '&lt;') + '<a href="' + href + '" download>下載</a>';
    var nx = links[(cur + 1) % links.length]; if (nx) { var pre = new Image(); pre.src = nx.getAttribute('href'); }
  }
  function open(i) { show(i); lb.classList.add('on'); document.body.style.overflow = 'hidden'; }
  function close() { lb.classList.remove('on'); document.body.style.overflow = ''; }
  links.forEach(function (a, i) { a.addEventListener('click', function (e) { e.preventDefault(); open(i); }); });
  lb.querySelector('.x').onclick = close;
  lb.querySelector('.p').onclick = function (e) { e.stopPropagation(); show(cur - 1); };
  lb.querySelector('.n').onclick = function (e) { e.stopPropagation(); show(cur + 1); };
  lb.addEventListener('click', function (e) { if (e.target === lb) close(); });
  document.addEventListener('keydown', function (e) {
    if (!lb.classList.contains('on')) return;
    if (e.key === 'ArrowRight') show(cur + 1); else if (e.key === 'ArrowLeft') show(cur - 1); else if (e.key === 'Escape') close();
  });
  var sx = null, sy = null;
  lb.addEventListener('touchstart', function (e) { sx = e.touches[0].clientX; sy = e.touches[0].clientY; }, { passive: true });
  lb.addEventListener('touchend', function (e) {
    if (sx === null) return;
    var dx = e.changedTouches[0].clientX - sx, dy = e.changedTouches[0].clientY - sy;
    if (Math.abs(dx) > 40 && Math.abs(dx) > Math.abs(dy)) show(cur + (dx < 0 ? 1 : -1));
    else if (dy > 90) close();
    sx = null;
  });
})();
