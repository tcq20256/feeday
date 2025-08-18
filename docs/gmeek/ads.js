/*! Simple AdSense bootstrapper - /gmeek/ads.js */
(function () {
  'use strict';

  // 可在别处提前设置 window.G_ADSENSE_CLIENT / window.G_DEFAULT_AD_SLOT 覆盖默认值
  var DEFAULT_CLIENT = window.G_ADSENSE_CLIENT || 'ca-pub-1964437526797765';
  var DEFAULT_SLOT   = window.G_DEFAULT_AD_SLOT || '3741031277';

  var SDK_SRC = 'https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client='
                + encodeURIComponent(DEFAULT_CLIENT);

  function ensureSdkOnce() {
    var sel = 'script[src^="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"]';
    if (!document.querySelector(sel)) {
      var s = document.createElement('script');
      s.async = true;
      s.src = SDK_SRC;
      s.crossOrigin = 'anonymous';
      document.head.appendChild(s);
    }
  }

  function push(ins) {
    try {
      (window.adsbygoogle = window.adsbygoogle || []).push({});
    } catch (e) {
      // 某些 SPA 场景可能在 SDK 未就绪时调用，稍后 MutationObserver 会再尝试
      // console.warn('[ads] push failed (will retry on mutations):', e);
    }
  }

  // 渲染页面上尚未渲染过的 <ins class="adsbygoogle">
  function renderInsExisting() {
    var nodes = document.querySelectorAll('ins.adsbygoogle:not([data-adsbygoogle-status])');
    nodes.forEach(function (ins) { push(ins); });
  }

  // 将占位符 <div class="g-ads" ...> 转为 <ins class="adsbygoogle"> 并渲染
  function upgradePlaceholders() {
    var nodes = document.querySelectorAll('.g-ads:not([data-g-bound])');
    nodes.forEach(function (host) {
      host.setAttribute('data-g-bound', '1');

      var client = host.getAttribute('data-g-client') || DEFAULT_CLIENT;
      var slot   = host.getAttribute('data-g-adslot') || host.getAttribute('data-g-slot') || DEFAULT_SLOT;
      var format = host.getAttribute('data-g-format') || 'auto';
      var full   = host.getAttribute('data-g-full'); // 存在即为 true，或字符串 "true"
      var style  = host.getAttribute('data-g-style') || 'display:block';
      var layoutKey = host.getAttribute('data-g-layout-key'); // 可选

      var ins = document.createElement('ins');
      ins.className = 'adsbygoogle';
      ins.style.cssText = style;
      ins.setAttribute('data-ad-client', client);
      ins.setAttribute('data-ad-slot', String(slot));
      ins.setAttribute('data-ad-format', format);
      ins.setAttribute('data-full-width-responsive', (full === null ? 'true' : String(full)));
      if (layoutKey) ins.setAttribute('data-ad-layout-key', layoutKey);

      host.innerHTML = '';
      host.appendChild(ins);
      push(ins);
    });
  }

  // 观察新加入的节点（适配 SPA/懒加载）
  function observe() {
    if (observe._on) return;
    observe._on = true;
    var mo = new MutationObserver(function () {
      renderInsExisting();
      upgradePlaceholders();
    });
    mo.observe(document.documentElement, { childList: true, subtree: true });
  }

  // 提供全局 API：动态挂载广告
  window.mountAdsense = function (container, opts) {
    ensureSdkOnce();
    var o = Object.assign({
      client: DEFAULT_CLIENT,
      slot: DEFAULT_SLOT,
      format: 'auto',
      fullWidthResponsive: true,
      style: 'display:block',
      layoutKey: null,
    }, opts || {});

    var root = (typeof container === 'string')
      ? document.querySelector(container)
      : container;

    if (!root) {
      console.warn('[ads] mountAdsense: container not found:', container);
      return null;
    }

    var ins = document.createElement('ins');
    ins.className = 'adsbygoogle';
    ins.style.cssText = o.style;
    ins.setAttribute('data-ad-client', o.client);
    ins.setAttribute('data-ad-slot', String(o.slot));
    ins.setAttribute('data-ad-format', o.format);
    ins.setAttribute('data-full-width-responsive', String(o.fullWidthResponsive));
    if (o.layoutKey) ins.setAttribute('data-ad-layout-key', o.layoutKey);

    root.appendChild(ins);
    push(ins);
    return ins;
  };

  function boot() {
    ensureSdkOnce();
    renderInsExisting();
    upgradePlaceholders();
    observe();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
