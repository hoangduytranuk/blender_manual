"use strict";StackExchange.mathjaxEditing=function(){function e(){m.disabled=!0,g.resetEquationNumbers()}function t(){m.disabled=!1}function n(e,t){var n=c.slice(e,t+1).join("").replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");for(f&&(n=n.replace(/\n    /g,"\n")),k.Browser.isMSIE&&(n=n.replace(/(%[^\n]*)\n/g,"$1<br/>\n"));t>e;)c[t--]="";c[e]="@@"+h.length+"@@",h.push(n),u=l=d=null}function i(e){u=l=d=f=null,h=[],c=w(e.replace(/\r\n?/g,"\n"),x);for(var t=1,i=c.length;i>t;t+=2){var r=c[t];"@"===r.charAt(0)?(c[t]="@@"+h.length+"@@",h.push(r)):u?r===l?p>0?d=t:0===p?n(u,t):u=l=d=null:r.match(/\n.*\n/)||t+2>=i?(d&&(t=d,p>=0&&n(u,t)),u=l=d=null,p=0):"{"===r&&p>=0?p++:"}"===r&&p>0&&p--:r===y||"$$"===r?(u=t,l=r,p=0):"begin"===r.substr(1,5)?(u=t,l="\\end"+r.substr(6),p=0):"`"===r.charAt(0)?(u=d=t,l=r,p=-1):"\n"===r.charAt(0)&&r.match(/    $/)&&(f=!0)}return d&&n(u,d),c.join("")}function r(e){return e=e.replace(/@@(\d+)@@/g,function(e,t){return h[t]}),h=null,e}function o(n,i){b=!1,k.cancelTypeset=!1,k.Queue(e,[i,k,n],t)}function a(e,t){b||(b=e,v&&(k.Cancel(),k.Queue([o,e,t])))}function s(e,t,n){var s=document.getElementById("wmd-preview"+t);y=n[0][0];var c=e.getConverter();c.hooks.chain("preConversion",i),c.hooks.chain("preSafe",r),e.hooks.chain("onPreviewRefresh",function(){a(s,"Typeset")}),k.Queue(function(){s&&s.querySelector(".mjx-noError")&&o(s,"Reprocess")})}var c,u,l,d,p,f,h,g,m,v=!1,b=null,y="$",k=MathJax.Hub;k.Queue(function(){return g=MathJax.InputJax.TeX,m=g.config.noErrors,v=!0,k.processUpdateTime=50,k.processSectionDelay=0,MathJax.Extension["fast-preview"].Disable(),k.Config({"HTML-CSS":{"EqnChunk":10,"EqnChunkFactor":1},"CommonHTML":{"EqnChunk":10,"EqnChunkFactor":1},"SVG":{"EqnChunk":10,"EqnChunkFactor":1}}),b?o(b,"Typeset"):void 0});var w,x=/(\$\$?|\\(?:begin|end)\{[a-z]*\*?\}|\\[\\{}$]|[{}]|(?:\n\s*)+|@@\d+@@|`+)/i;return w=3==="aba".split(/(b)/).length?function(e,t){return e.split(t)}:function(e,t){var n,i=[];if(!t.global){var r=t.toString(),o="";r=r.replace(/^\/(.*)\/([im]*)$/,function(e,t,n){return o=n,t}),t=new RegExp(r,o+"g")}t.lastIndex=0;for(var a=0;n=t.exec(e);)i.push(e.substring(a,n.index)),i.push.apply(i,n.slice(1)),a=n.index+n[0].length;return i.push(e.substring(a)),i},{"prepareWmdForMathJax":s}}(),function(){var e=MathJax.Hub;if(!e.Cancel){e.cancelTypeset=!1;var t="MathJax Canceled";e.Register.StartupHook("HTML-CSS Jax Config",function(){var n=MathJax.OutputJax["HTML-CSS"],i=n.Translate;n.Augment({"Translate":function(r,o){if(e.cancelTypeset||o.cancelled)throw Error(t);return i.call(n,r,o)}})}),e.Register.StartupHook("SVG Jax Config",function(){var n=MathJax.OutputJax.SVG,i=n.Translate;n.Augment({"Translate":function(r,o){if(e.cancelTypeset||o.cancelled)throw Error(t);return i.call(n,r,o)}})}),e.Register.StartupHook("CommonHTML Jax Config",function(){var n=MathJax.OutputJax.CommonHTML,i=n.Translate;n.Augment({"Translate":function(r,o){if(e.cancelTypeset||o.cancelled)throw Error(t);return i.call(n,r,o)}})}),e.Register.StartupHook("PreviewHTML Jax Config",function(){var n=MathJax.OutputJax.PreviewHTML,i=n.Translate;n.Augment({"Translate":function(r,o){if(e.cancelTypeset||o.cancelled)throw Error(t);return i.call(n,r,o)}})}),e.Register.StartupHook("TeX Jax Config",function(){var n=MathJax.InputJax.TeX,i=n.Translate;n.Augment({"Translate":function(r,o){if(e.cancelTypeset||o.cancelled)throw Error(t);return i.call(n,r,o)}})});var n=e.processError;e.processError=function(i,r,o){return i.message!==t?n.call(e,i,r,o):(MathJax.Message.Clear(0,0),r.jaxIDs=[],r.jax={},r.scripts=[],r.i=r.j=0,r.cancelled=!0,null)},e.Cancel=function(){this.cancelTypeset=!0}}}();