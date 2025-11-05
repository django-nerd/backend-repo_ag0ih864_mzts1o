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


# Minimal jQuery-compatible shim sufficient for our subset usage
# Supports: $(selector), $(fn) ready, $.extend, $.fn plugin, .children(sel), .hide/.show, .eq, .on,
# .width/.height, .css, .addClass/.removeClass, .offset, $('<div>').appendTo, $(window)
JQUERY_MIN = (
    "!function(global){\n"
    "  function $(arg){\n"
    "    if(typeof arg==='function'){ if(document.readyState!=='loading') arg(); else document.addEventListener('DOMContentLoaded', arg); return $; }\n"
    "    if(arg===global) return new Wrapper([global]);\n"
    "    if(arg instanceof Wrapper) return arg;\n"
    "    if(typeof arg==='string'){ if(arg.trim().startsWith('<')){ var tmp=document.createElement('div'); tmp.innerHTML=arg.trim(); return new Wrapper([tmp.firstElementChild]); } return new Wrapper(Array.from(document.querySelectorAll(arg))); }\n"
    "    if(arg && (arg.nodeType===1||arg===document)) return new Wrapper([arg]);\n"
    "    if(Array.isArray(arg)) return new Wrapper(arg);\n"
    "    return new Wrapper([]);\n"
    "  }\n"
    "  function Wrapper(nodes){ this.nodes = nodes; }\n"
    "  $.fn = Wrapper.prototype;\n"
    "  $.extend = function(target){ for(var i=1;i<arguments.length;i++){ var src=arguments[i]||{}; for(var k in src){ if(Object.prototype.hasOwnProperty.call(src,k)) target[k]=src[k]; } } return target; };\n"
    "  Wrapper.prototype.each = function(cb){ this.nodes.forEach(function(n,i){ cb.call(n,i,n); }); return this; };\n"
    "  Wrapper.prototype.children = function(sel){ var out=[]; this.each(function(){ out = out.concat(Array.from(this.children)); }); if(sel){ out=out.filter(function(n){ return n.matches(sel); }); } return new Wrapper(out); };\n"
    "  Wrapper.prototype.hide = function(){ return this.css({display:'none'}); };\n"
    "  Wrapper.prototype.show = function(){ return this.css({display:''}); };\n"
    "  Wrapper.prototype.eq = function(i){ return new Wrapper([this.nodes[i]].filter(Boolean)); };\n"
    "  Wrapper.prototype.on = function(ev, handler){ var evs=ev.split(/\s+/); return this.each(function(){ evs.forEach(function(e){ this.addEventListener(e, handler, {passive:false}); }, this); }); };\n"
    "  Wrapper.prototype.width = function(){ var n=this.nodes[0]; return n===global ? global.innerWidth : (n.getBoundingClientRect().width); };\n"
    "  Wrapper.prototype.height = function(){ var n=this.nodes[0]; return n===global ? global.innerHeight : (n.getBoundingClientRect().height); };\n"
    "  Wrapper.prototype.css = function(obj){ return this.each(function(){ for(var k in obj){ this.style[k.replace(/-([a-z])/g,function(_,c){return c.toUpperCase();})]=obj[k]; } }); };\n"
    "  Wrapper.prototype.addClass = function(c){ return this.each(function(){ this.classList.add(c); }); };\n"
    "  Wrapper.prototype.removeClass = function(c){ return this.each(function(){ this.classList.remove(c); }); };\n"
    "  Wrapper.prototype.offset = function(){ var n=this.nodes[0]; var r=n.getBoundingClientRect(); return {top:r.top+global.pageYOffset,left:r.left+global.pageXOffset}; };\n"
    "  Wrapper.prototype.appendTo = function(sel){ var parent = (typeof sel==='string')? document.querySelector(sel) : (sel instanceof Wrapper? sel.nodes[0] : sel); return this.each(function(){ parent && parent.appendChild(this); }); };\n"
    "  global.jQuery = global.$ = $;\n"
    "}(window);\n"
)

# Minimal turn.js build (subset) that depends on the shimmed jQuery interface
TURNJS_MIN = """
/* turn.js 4.1 - subset for single display */
(function($){
  'use strict';
  $.fn.turn = function(opts){
    var settings = $.extend({width:320,height:480,display:'single',elevation:50,gradients:true,autoCenter:true}, opts);
    return this.each(function(){
      var $wrap = $(this);
      $wrap.addClass('turnjs');
      var $pages = $wrap.children('.page');
      var current = 0, dragging=false, startX=0;
      function setSize(){ var vw = $(window).width(); var r = Math.min(vw, settings.width); var h = r*settings.height/settings.width; $wrap.css({width:r+'px', height:h+'px'}); }
      function show(i){ i=Math.max(0, Math.min($pages.nodes.length-1, i)); $pages.hide().eq(i).show(); current=i; }
      function startDrag(e){ dragging=true; startX = (e.touches? e.touches[0].clientX : (e.clientX|| (e.changedTouches? e.changedTouches[0].clientX:0))); $wrap.addClass('dragging'); e.preventDefault && e.preventDefault(); }
      function moveDrag(e){ if(!dragging) return; var x = (e.touches? e.touches[0].clientX : (e.clientX|| (e.changedTouches? e.changedTouches[0].clientX:startX))); var dx=x-startX; var progress=Math.max(-1,Math.min(1,dx/($wrap.width()*0.8))); var deg = -progress*25; var sh = Math.abs(progress)*0.6; $pages.eq(current).css({boxShadow:'rgba(0,0,0,'+sh+') 0px 8px 24px', transform:'perspective(1000px) rotate('+deg+'deg)'}); }
      function endDrag(e){ if(!dragging) return; var x = (e.changedTouches? e.changedTouches[0].clientX : (e.clientX||startX)); var dx=x-startX; if(Math.abs(dx) > $wrap.width()*0.25){ if(dx<0 && current<$pages.nodes.length-1) show(current+1); else if(dx>0 && current>0) show(current-1); }
        $pages.eq(current).css({boxShadow:'', transform:''}); dragging=false; $wrap.removeClass('dragging'); }
      $wrap.on('touchstart mousedown', function(e){ var ev = e.touches? e.touches[0] : e; var edgeZone = $wrap.width()*0.15; var cx = ev.clientX - $wrap.offset().left; if(cx < edgeZone || cx > $wrap.width()-edgeZone) startDrag(e); });
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
        $('<div class=\"edge-indicator left\"></div>').appendTo('#flipbook');
        $('<div class=\"edge-indicator right\"></div>').appendTo('#flipbook');
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
