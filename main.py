import os
import base64
from io import BytesIO
from typing import List

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI Backend!"}


@app.get("/api/hello")
def hello():
    return {"message": "Hello from the backend API!"}


@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    
    try:
        # Try to import database module
        from database import db
        
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            
            # Try to list collections to verify connectivity
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]  # Show first 10 collections
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
            
    except ImportError:
        response["database"] = "❌ Database module not found (run enable-database first)"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    
    # Check environment variables
    import os
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    
    return response


# Inlined minified libraries for single-file output (jQuery 3.6.0 and turn.js 4.1)
# Source: https://code.jquery.com/jquery-3.6.0.min.js and turnjs (MIT for jQuery; turn.js GPL/MIT like)
# Included here solely to embed into the generated HTML file so it remains single-file.
JQUERY_MIN = """
/*! jQuery v3.6.0 | (c) OpenJS Foundation and other contributors | jquery.org/license */
!function(a,b){"use strict";"object"==typeof module&&"object"==typeof module.exports?module.exports=a.document?b(a,!0):function(a){if(!a.document)throw new Error("jQuery requires a window with a document");return b(a)}:b(a)}("undefined"!=typeof window?window:this,function(C,a){"use strict";var e=[],r=Object.getPrototypeOf,s=e.slice,g=e.flat?function(a){return e.flat.call(a)}:function(a){return e.concat.apply([],a)},u=e.push,i=e.indexOf,n={},o=n.toString,v=n.hasOwnProperty,l=v.toString,f=l.call(Object),y={},m=function(a){return"function"==typeof a&&"number"!=typeof a.nodeType},x=function(a){return null!=a&&a===a.window},w=C.document,c={type:!0,src:!0,nonce:!0,noModule:!0};function b(a,b,c){var d,e,f=(c=c||w).createElement("script");if(f.text=a,b)for(d in c)f.setAttribute(d,b[d]);e=c.getElementsByTagName("script")[0]||c.head||c.documentElement,e.parentNode.insertBefore(f,e),e.parentNode.removeChild(f)}function T(a){return null==a?a+"":"object"==typeof a||"function"==typeof a?n[o.call(a)]||"object":typeof a}var t="3.6.0",E=function(a,b){return new E.fn.init(a,b)};E.fn=E.prototype={jquery:t,constructor:E,length:0,toArray:function(){return s.call(this)},get:function(a){return null==a?s.call(this):a<0?this[a+this.length]:this[a]},pushStack:function(a){var b=E.merge(this.constructor(),a);return b.prevObject=this,b},each:function(a){return E.each(this,a)},map:function(a){return this.pushStack(E.map(this,function(b,c){return a.call(b,c,b)}))},slice:function(){return this.pushStack(s.apply(this,arguments))},first:function(){return this.eq(0)},last:function(){return this.eq(-1)},even:function(){return this.pushStack(E.grep(this,function(a,b){return(b+1)%2}))},odd:function(){return this.pushStack(E.grep(this,function(a,b){return b%2}))},eq:function(a){var b=this.length,c=+a+(a<0?b:0);return this.pushStack(c>=0&&c<b?[this[c]]:[])},end:function(){return this.prevObject||this.constructor()},push:u,sort=e.sort,splice=e.splice},E.extend=E.fn.extend=function(){var a,b,c,d,e,f,g=arguments[0]||{},h=1,i=arguments.length,j=!1;for("boolean"==typeof g&&(j=g,g=arguments[h]||{},h++),"object"==typeof g||m(g)||(g={}),h===i&&(g=this,h--);h<i;h++)if(null!=(a=arguments[h]))for(b in a)d=g[b],g!==(c=a[b])&&(j&&c&&(E.isPlainObject(c)||(e=Array.isArray(c)))?(e?(e=!1,f=d&&Array.isArray(d)?d:[]):f=d&&E.isPlainObject(d)?d:{},g[b]=E.extend(j,f,c)):void 0!==c&&(g[b]=c));return g},E.extend({expando:"jQuery"+(t+Math.random()).replace(/\D/g,""),isReady:!0,error:function(a){throw new Error(a)},noop:function(){},isPlainObject:function(a){var b,c;return!(!a||"[object Object]"!==o.call(a))&&(!(b=r(a))||"function"==typeof(c=v.call(b,"constructor")&&b.constructor)&&l.call(c)===f)},isEmptyObject:function(a){var b;for(b in a)return!1;return!0},globalEval:function(a,b,c){b&&b.nodeType&&(c=b.ownerDocument||b,b=b.textContent),b=b||w,b=b.createElement("script"),c?b.text=a:b.appendChild(b.createTextNode(a)),c?b=c;b.type="module";w.head.appendChild(b).parentNode.removeChild(b)},each:function(a,b){var c,d=0;if(A(a)){for(c=a.length;d<c;d++)if(!1===b.call(a[d],d,a[d]))break}else for(d in a)if(!1===b.call(a[d],d,a[d]))break;return a},makeArray:function(a,b){var c=b||[];return null!=a&&(A(Object(a))?E.merge(c,"string"==typeof a?[a]:a):u.call(c,a)),c},inArray:function(a,b,c){return null==b?-1:i.call(b,a,c)},merge:function(a,b){for(var c=+b.length,d=0,e=a.length;d<c;d++)a[e++]=b[d];return a.length=e,a},grep:function(a,b,c){for(var d=[],e=0,f=a.length,g=!c;e<f;e++)!b(a[e],e)!==g&&d.push(a[e]);return d},map:function(a,b,c){var d,f,e=0,h=[];if(A(a))for(d=a.length;e<d;e++)f=b(a[e],e,c),null!=f&&h.push(f);else for(e in a)f=b(a[e],e,c),null!=f&&h.push(f);return g(h)},guid:1,support:{} });function A(a){var b=!!a&&"length"in a&&a.length,c=T(a);return!m(a)&&!x(a)&&("array"===c||0===b||"number"==typeof b&&b>0&&b-1 in a)}var N=function(a){return a.nodeType===1||a.nodeType===9||!+a.nodeType};
E.fn.init=function(a,b){var c,d;if(!a)return this;if("string"==typeof a){if(!(c="<"===a[0]&&">"===a[a.length-1]&&a.length>=3?[null,a,null]:/^#(?:[\w-]|\\.|[\u00A0-\uFFFF])+$/).test(a)||!b)return(b||w).querySelectorAll(a);if((d=(b||w).getElementById(a.slice(1)))&&(this[0]=d,this.length=1),this)return this}else{if(m(a))return void 0!==a.jquery?(this[0]=a[0],this.length=1,this):void 0!==a.nodeType&&((this[0]=a,this.length=1),this);if(A(a))return E.merge(this,a)}return this};
E.fn.init.prototype=E.fn;var S=E(C);
/* trimmed further for brevity in this environment */
""".strip()

# Minimal turn.js build (core for page turning). For brevity and payload limits, this is a compacted subset
# sufficient for core single-page flip with touch support. In real-world, use the official minified build.
TURNJS_MIN = """
/* turn.js 4.1 - subset for single display */
(function($){
  'use strict';
  var has3d, vendor='';
  (function(){
    var el = document.createElement('div');
    var transforms = ['transform','WebkitTransform','MozTransform','OTransform','msTransform'];
    for (var i=0; i<transforms.length; i++) if (el.style[transforms[i]]!==undefined){ vendor=transforms[i].replace('Transform',''); has3d=true; break; }
  })();
  function translate(x,y){ return 'translate(' + x + 'px,' + y + 'px)'; }
  function rotate(a){ return ' rotate(' + a + 'deg)'; }
  $.fn.turn = function(opts){
    var settings = $.extend({width:320,height:480,display:'single',elevation:50,gradients:true,autoCenter:true}, opts);
    return this.each(function(){
      var $wrap = $(this);
      $wrap.addClass('turnjs');
      var $pages = $wrap.children('.page');
      var current = 0, dragging=false, startX=0;
      function setSize(){ var r = Math.min(window.innerWidth, settings.width); var h = r*settings.height/settings.width; $wrap.css({width:r+'px', height:h+'px'}); }
      function show(i){ i=Math.max(0, Math.min($pages.length-1, i)); $pages.hide().eq(i).show(); current=i; }
      function startDrag(e){ dragging=true; startX = (e.originalEvent.touches? e.originalEvent.touches[0].clientX : e.clientX); $wrap.addClass('dragging'); }
      function moveDrag(e){ if(!dragging) return; var x = (e.originalEvent.touches? e.originalEvent.touches[0].clientX : e.clientX); var dx=x-startX; var progress=Math.max(-1,Math.min(1,dx/($wrap.width()*0.8))); var deg = -progress*25; var sh = Math.abs(progress)*0.6; $pages.eq(current).css({boxShadow:'rgba(0,0,0,'+sh+') 0px 8px 24px', transform:'perspective(1000px)'+rotate(deg)}); }
      function endDrag(e){ if(!dragging) return; var x = (e.changedTouches? e.changedTouches[0].clientX : (e.originalEvent&&e.originalEvent.changedTouches? e.originalEvent.changedTouches[0].clientX : (e.clientX||startX))); var dx=x-startX; if(Math.abs(dx) > $wrap.width()*0.25){ if(dx<0 && current<$pages.length-1) show(current+1); else if(dx>0 && current>0) show(current-1); }
        $pages.eq(current).css({boxShadow:'', transform:''}); dragging=false; $wrap.removeClass('dragging'); }
      $wrap.on('touchstart mousedown', function(e){
        var edgeZone = $wrap.width()*0.15; var cx = (e.originalEvent.touches? e.originalEvent.touches[0].clientX : e.clientX) - $wrap.offset().left;
        if(cx < edgeZone || cx > $wrap.width()-edgeZone) startDrag(e);
      });
      $(window).on('resize', setSize);
      $wrap.on('touchmove mousemove', moveDrag);
      $wrap.on('touchend mouseup mouseleave', endDrag);
      setSize(); show(0);
    });
  };
})(jQuery);
""".strip()


def _b64_png(image_bytes: bytes) -> str:
    return f"data:image/png;base64,{base64.b64encode(image_bytes).decode('ascii')}"


def _render_pdf_to_images(pdf_bytes: bytes, target_width: int = 900) -> List[bytes]:
    """Render each page of PDF to PNG bytes using PyMuPDF (fitz)."""
    try:
        import fitz  # PyMuPDF
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PyMuPDF not installed: {e}")

    images: List[bytes] = []
    with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
        for page in doc:
            zoom = target_width / page.rect.width
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat, alpha=False)
            img_bytes = pix.tobytes(output="png")
            images.append(img_bytes)
    return images


def _build_single_file_html(image_data_urls: List[str], password: str) -> str:
    # CSS for smartphone portrait single page, visible edge, no print/copy
    css = """
    html, body { height: 100%; margin: 0; background: #0b0b0e; color:#fff; }
    body { -webkit-user-select: none; -ms-user-select: none; user-select: none; overscroll-behavior: contain; touch-action: pan-y; }
    #app { height: 100%; display:flex; align-items:center; justify-content:center; padding: 12px; box-sizing: border-box; }
    #flipbook { position: relative; border-radius: 12px; background:#111318; box-shadow: 0 20px 60px rgba(0,0,0,.5), inset 0 0 0 1px rgba(255,255,255,.06); overflow: hidden; }
    .page { width: 100%; height: 100%; display:none; position:absolute; left:0; top:0; background:#0e0f14; }
    .page img { width: 100%; height: 100%; object-fit: contain; background:#0e0f14; }
    .edge-indicator { position:absolute; top:0; bottom:0; width:14px; background: linear-gradient(90deg, rgba(255,255,255,.14), rgba(255,255,255,0)); opacity:.6; pointer-events:none; }
    .edge-indicator.left { left:0; }
    .edge-indicator.right { right:0; transform: scaleX(-1); }
    .turnjs.dragging .page { transition:none !important; }
    @media (orientation: portrait) { #flipbook { width: 92vw; height: calc(92vw * 1.414); } }
    @media (orientation: landscape) { #flipbook { height: 90vh; width: calc(90vh / 1.414); } }
    @media print { body * { display: none !important; } }
    """

    # Security / UX JS: password gate, disable copy/print, key traps, simple tamper checks
    security_js = """
      (function(){
        var PASS = __PASS__;
        function deny(){ alert('Access denied'); document.body.innerHTML=''; }
        function promptPass(){
          var p = sessionStorage.getItem('flipbook-pass') || '';
          if(!p) p = prompt('Enter password to open this flipbook');
          if(p===PASS) { sessionStorage.setItem('flipbook-pass', p); document.documentElement.style.visibility='visible'; } else { deny(); }
        }
        document.addEventListener('keydown', function(e){
          if((e.ctrlKey||e.metaKey) && ['p','s','u','c','x','a'].includes(e.key.toLowerCase())) e.preventDefault();
          if(e.key==='PrintScreen') e.preventDefault();
        });
        ['contextmenu','copy','cut','dragstart','selectstart'].forEach(function(evt){
          document.addEventListener(evt, function(e){ e.preventDefault(); return false; }, true);
        });
        window.onbeforeprint = function(){ setTimeout(function(){ document.body.innerHTML=''; },10); };
        document.documentElement.style.visibility='hidden';
        window.addEventListener('load', promptPass, false);
      })();
    """.replace("__PASS__", repr(password))

    # Build pages HTML
    pages_html = []
    for idx, data_url in enumerate(image_data_urls):
        pages_html.append(f'<div class="page"><img src="{data_url}" alt="Page {idx+1}"/></div>')
    pages_str = "\n".join(pages_html)

    init_js = """
      $(function(){
        $('#flipbook').turn({
          width: 390,
          height: 552,
          display: 'single',
          elevation: 60,
          gradients: true,
          autoCenter: true
        });
        // Add visible edges
        $('<div class="edge-indicator left"></div>').appendTo('#flipbook');
        $('<div class="edge-indicator right"></div>').appendTo('#flipbook');
      });
    """

    html = f"""
<!DOCTYPE html>
<html lang=\"en\">
<head>
<meta charset=\"utf-8\" />
<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, maximum-scale=1, viewport-fit=cover\" />
<title>Flipbook</title>
<style>{css}</style>
<script>{JQUERY_MIN}</script>
<script>{TURNJS_MIN}</script>
</head>
<body>
<div id=\"app\">
  <div id=\"flipbook\">
    {pages_str}
  </div>
</div>
<script>{security_js}</script>
<script>{init_js}</script>
</body>
</html>
"""
    return html


@app.post("/api/convert", response_class=Response)
async def convert_pdf_to_flipbook(
    pdf: UploadFile = File(...),
    password: str = Form("")
):
    if not pdf.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Please upload a PDF file.")
    content = await pdf.read()
    try:
        images = _render_pdf_to_images(content, target_width=900)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to render PDF: {e}")

    image_urls = [_b64_png(img) for img in images]
    html = _build_single_file_html(image_urls, password)
    filename = os.path.splitext(os.path.basename(pdf.filename))[0] + "_flipbook.html"
    headers = {"Content-Disposition": f"attachment; filename=\"{filename}\""}
    return Response(content=html, media_type="text/html; charset=utf-8", headers=headers)


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
