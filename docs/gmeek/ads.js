// adsense.js
export function mountAdsense(container, {
  client = 'ca-pub-1964437526797765',
  slot = '3741031277',
  format = 'auto',
  fullWidthResponsive = true,
  style = 'display:block',
} = {}) {
  // 1) 只加载一次 AdSense SDK
  const sdkSelector = 'script[src^="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"]';
  if (!document.querySelector(sdkSelector)) {
    const s = document.createElement('script');
    s.async = true;
    s.src = `https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=${encodeURIComponent(client)}`;
    s.crossOrigin = 'anonymous';
    document.head.appendChild(s);
  }

  // 2) 创建广告位 <ins class="adsbygoogle">
  const ins = document.createElement('ins');
  ins.className = 'adsbygoogle';
  ins.style.cssText = style; // 例如 "display:block"
  ins.setAttribute('data-ad-client', client);
  ins.setAttribute('data-ad-slot', String(slot));
  ins.setAttribute('data-ad-format', format);
  ins.setAttribute('data-full-width-responsive', String(fullWidthResponsive));

  // 挂到容器里
  const root = typeof container === 'string' ? document.querySelector(container) : container;
  if (!root) throw new Error('mountAdsense: container not found');
  root.appendChild(ins);

  // 3) 触发渲染
  (window.adsbygoogle = window.adsbygoogle || []).push({});
  return ins;
}
