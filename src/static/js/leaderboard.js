(function() {var g,n=this;function p(){}function aa(a){a.ca=function(){return a.ra?a.ra:a.ra=new a}}
function q(a){var b=typeof a;if("object"==b)if(a){if(a instanceof Array)return"array";if(a instanceof Object)return b;var c=Object.prototype.toString.call(a);if("[object Window]"==c)return"object";if("[object Array]"==c||"number"==typeof a.length&&"undefined"!=typeof a.splice&&"undefined"!=typeof a.propertyIsEnumerable&&!a.propertyIsEnumerable("splice"))return"array";if("[object Function]"==c||"undefined"!=typeof a.call&&"undefined"!=typeof a.propertyIsEnumerable&&!a.propertyIsEnumerable("call"))return"function"}else return"null";
else if("function"==b&&"undefined"==typeof a.call)return"object";return b}function s(a){var b=q(a);return"array"==b||"object"==b&&"number"==typeof a.length}function t(a){return"string"==typeof a}function ba(a){var b=typeof a;return"object"==b&&null!=a||"function"==b}function u(a){return a[ca]||(a[ca]=++da)}var ca="closure_uid_"+(1E9*Math.random()>>>0),da=0;function ea(a,b,c){return a.call.apply(a.bind,arguments)}
function fa(a,b,c){if(!a)throw Error();if(2<arguments.length){var d=Array.prototype.slice.call(arguments,2);return function(){var c=Array.prototype.slice.call(arguments);Array.prototype.unshift.apply(c,d);return a.apply(b,c)}}return function(){return a.apply(b,arguments)}}function v(a,b,c){v=Function.prototype.bind&&-1!=Function.prototype.bind.toString().indexOf("native code")?ea:fa;return v.apply(null,arguments)}
function ga(a,b){var c=Array.prototype.slice.call(arguments,1);return function(){var b=Array.prototype.slice.call(arguments);b.unshift.apply(b,c);return a.apply(this,b)}}function ha(a,b){var c=a.split("."),d=n;c[0]in d||!d.execScript||d.execScript("var "+c[0]);for(var f;c.length&&(f=c.shift());)c.length||void 0===b?d=d[f]?d[f]:d[f]={}:d[f]=b}function w(a,b){function c(){}c.prototype=b.prototype;a.w=b.prototype;a.prototype=new c};function ia(a,b){for(var c=1;c<arguments.length;c++){var d=String(arguments[c]).replace(/\$/g,"$$$$");a=a.replace(/\%s/,d)}return a}function ja(a){if(!ka.test(a))return a;-1!=a.indexOf("&")&&(a=a.replace(la,"&amp;"));-1!=a.indexOf("<")&&(a=a.replace(ma,"&lt;"));-1!=a.indexOf(">")&&(a=a.replace(na,"&gt;"));-1!=a.indexOf('"')&&(a=a.replace(oa,"&quot;"));return a}var la=/&/g,ma=/</g,na=/>/g,oa=/\"/g,ka=/[&<>\"]/;var y,pa,qa,ra;function sa(){return n.navigator?n.navigator.userAgent:null}ra=qa=pa=y=!1;var ta;if(ta=sa()){var ua=n.navigator;y=0==ta.indexOf("Opera");pa=!y&&-1!=ta.indexOf("MSIE");qa=!y&&-1!=ta.indexOf("WebKit");ra=!y&&!qa&&"Gecko"==ua.product}var va=y,A=pa,B=ra,C=qa;function wa(){var a=n.document;return a?a.documentMode:void 0}var xa;
a:{var ya="",D;if(va&&n.opera)var za=n.opera.version,ya="function"==typeof za?za():za;else if(B?D=/rv\:([^\);]+)(\)|;)/:A?D=/MSIE\s+([^\);]+)(\)|;)/:C&&(D=/WebKit\/(\S+)/),D)var Aa=D.exec(sa()),ya=Aa?Aa[1]:"";if(A){var Ba=wa();if(Ba>parseFloat(ya)){xa=String(Ba);break a}}xa=ya}var Ca={};
function E(a){var b;if(!(b=Ca[a])){b=0;for(var c=String(xa).replace(/^[\s\xa0]+|[\s\xa0]+$/g,"").split("."),d=String(a).replace(/^[\s\xa0]+|[\s\xa0]+$/g,"").split("."),f=Math.max(c.length,d.length),e=0;0==b&&e<f;e++){var h=c[e]||"",k=d[e]||"",l=RegExp("(\\d*)(\\D*)","g"),x=RegExp("(\\d*)(\\D*)","g");do{var m=l.exec(h)||["","",""],r=x.exec(k)||["","",""];if(0==m[0].length&&0==r[0].length)break;b=((0==m[1].length?0:parseInt(m[1],10))<(0==r[1].length?0:parseInt(r[1],10))?-1:(0==m[1].length?0:parseInt(m[1],
10))>(0==r[1].length?0:parseInt(r[1],10))?1:0)||((0==m[2].length)<(0==r[2].length)?-1:(0==m[2].length)>(0==r[2].length)?1:0)||(m[2]<r[2]?-1:m[2]>r[2]?1:0)}while(0==b)}b=Ca[a]=0<=b}return b}var Da=n.document,Ea=Da&&A?wa()||("CSS1Compat"==Da.compatMode?parseInt(xa,10):5):void 0;function Fa(a,b){for(var c in a)b.call(void 0,a[c],c,a)}function Ga(a){var b=[],c=0,d;for(d in a)b[c++]=a[d];return b}function Ha(a){var b=[],c=0,d;for(d in a)b[c++]=d;return b}var Ia="constructor hasOwnProperty isPrototypeOf propertyIsEnumerable toLocaleString toString valueOf".split(" ");function Ja(a,b){for(var c,d,f=1;f<arguments.length;f++){d=arguments[f];for(c in d)a[c]=d[c];for(var e=0;e<Ia.length;e++)c=Ia[e],Object.prototype.hasOwnProperty.call(d,c)&&(a[c]=d[c])}};function F(a){Error.captureStackTrace?Error.captureStackTrace(this,F):this.stack=Error().stack||"";a&&(this.message=String(a))}w(F,Error);F.prototype.name="CustomError";function Ka(a,b){b.unshift(a);F.call(this,ia.apply(null,b));b.shift()}w(Ka,F);Ka.prototype.name="AssertionError";function La(a,b){throw new Ka("Failure"+(a?": "+a:""),Array.prototype.slice.call(arguments,1));};var G=Array.prototype,H=G.indexOf?function(a,b,c){return G.indexOf.call(a,b,c)}:function(a,b,c){c=null==c?0:0>c?Math.max(0,a.length+c):c;if(t(a))return t(b)&&1==b.length?a.indexOf(b,c):-1;for(;c<a.length;c++)if(c in a&&a[c]===b)return c;return-1},I=G.forEach?function(a,b,c){G.forEach.call(a,b,c)}:function(a,b,c){for(var d=a.length,f=t(a)?a.split(""):a,e=0;e<d;e++)e in f&&b.call(c,f[e],e,a)},Ma=G.filter?function(a,b,c){return G.filter.call(a,b,c)}:function(a,b,c){for(var d=a.length,f=[],e=0,h=t(a)?
a.split(""):a,k=0;k<d;k++)if(k in h){var l=h[k];b.call(c,l,k,a)&&(f[e++]=l)}return f},Na=G.map?function(a,b,c){return G.map.call(a,b,c)}:function(a,b,c){for(var d=a.length,f=Array(d),e=t(a)?a.split(""):a,h=0;h<d;h++)h in e&&(f[h]=b.call(c,e[h],h,a));return f};function Oa(a,b){var c=H(a,b);0<=c&&G.splice.call(a,c,1)}function Pa(a){return G.concat.apply(G,arguments)}function Qa(a){var b=a.length;if(0<b){for(var c=Array(b),d=0;d<b;d++)c[d]=a[d];return c}return[]}
function Ra(a,b,c){return 2>=arguments.length?G.slice.call(a,b):G.slice.call(a,b,c)};var Sa;function Ta(a){a=a.className;return t(a)&&a.match(/\S+/g)||[]}function Ua(a,b){for(var c=Ta(a),d=Ra(arguments,1),f=c.length+d.length,e=c,h=0;h<d.length;h++)0<=H(e,d[h])||e.push(d[h]);a.className=c.join(" ");return c.length==f}function Va(a,b){var c=Ta(a),d=Ra(arguments,1),c=Wa(c,d);a.className=c.join(" ")}function Wa(a,b){return Ma(a,function(a){return!(0<=H(b,a))})};var Xa=!A||A&&9<=Ea;!B&&!A||A&&A&&9<=Ea||B&&E("1.9.1");A&&E("9");function Ya(a){return a?new Za($a(a)):Sa||(Sa=new Za)}function ab(a,b){var c,d,f,e;c=document;c=b||c;if(c.querySelectorAll&&c.querySelector&&a)return c.querySelectorAll(""+(a?"."+a:""));if(a&&c.getElementsByClassName){var h=c.getElementsByClassName(a);return h}h=c.getElementsByTagName("*");if(a){e={};for(d=f=0;c=h[d];d++){var k=c.className;"function"==typeof k.split&&0<=H(k.split(/\s+/),a)&&(e[f++]=c)}e.length=f;return e}return h}
function bb(a,b){Fa(b,function(b,d){"style"==d?a.style.cssText=b:"class"==d?a.className=b:"for"==d?a.htmlFor=b:d in cb?a.setAttribute(cb[d],b):0==d.lastIndexOf("aria-",0)||0==d.lastIndexOf("data-",0)?a.setAttribute(d,b):a[d]=b})}var cb={cellpadding:"cellPadding",cellspacing:"cellSpacing",colspan:"colSpan",frameborder:"frameBorder",height:"height",maxlength:"maxLength",role:"role",rowspan:"rowSpan",type:"type",usemap:"useMap",valign:"vAlign",width:"width"};
function db(a,b,c,d){function f(c){c&&b.appendChild(t(c)?a.createTextNode(c):c)}for(;d<c.length;d++){var e=c[d];!s(e)||ba(e)&&0<e.nodeType?f(e):I(eb(e)?Qa(e):e,f)}}function $a(a){return 9==a.nodeType?a:a.ownerDocument||a.document}function eb(a){if(a&&"number"==typeof a.length){if(ba(a))return"function"==typeof a.item||"string"==typeof a.item;if("function"==q(a))return"function"==typeof a.item}return!1}function fb(a,b){for(var c=0;a;){if(b(a))return a;a=a.parentNode;c++}return null}
function Za(a){this.s=a||n.document||document}g=Za.prototype;g.ba=Ya;g.oa=function(a){return t(a)?this.s.getElementById(a):a};g.J=function(a,b){var c=b||this.s,d=c||document;d.querySelectorAll&&d.querySelector?c=d.querySelector("."+a):(d=c||document,c=(d.querySelectorAll&&d.querySelector?d.querySelectorAll("."+a):d.getElementsByClassName?d.getElementsByClassName(a):ab(a,c))[0]);return c||null};
g.f=function(a,b,c){var d=this.s,f=arguments,e=f[0],h=f[1];if(!Xa&&h&&(h.name||h.type)){e=["<",e];h.name&&e.push(' name="',ja(h.name),'"');if(h.type){e.push(' type="',ja(h.type),'"');var k={};Ja(k,h);delete k.type;h=k}e.push(">");e=e.join("")}e=d.createElement(e);h&&(t(h)?e.className=h:"array"==q(h)?Ua.apply(null,[e].concat(h)):bb(e,h));2<f.length&&db(d,e,f,2);return e};g.createElement=function(a){return this.s.createElement(a)};g.createTextNode=function(a){return this.s.createTextNode(String(a))};
g.appendChild=function(a,b){a.appendChild(b)};g.append=function(a,b){db($a(a),a,arguments,1)};g.Y=function(a){for(var b;b=a.firstChild;)a.removeChild(b)};function gb(a){return fb(a,function(a){return"LI"==a.nodeName&&!0})};function J(){0!=hb&&u(this)}var hb=0;function K(a,b){this.type=a;this.currentTarget=this.target=b}K.prototype.ga=!1;K.prototype.defaultPrevented=!1;K.prototype.preventDefault=function(){this.defaultPrevented=!0};var ib=0;function jb(){}g=jb.prototype;g.key=0;g.v=!1;g.O=!1;g.S=function(a,b,c,d,f,e){if("function"==q(a))this.sa=!0;else if(a&&a.handleEvent&&"function"==q(a.handleEvent))this.sa=!1;else throw Error("Invalid listener argument");this.p=a;this.xa=b;this.src=c;this.type=d;this.capture=!!f;this.da=e;this.O=!1;this.key=++ib;this.v=!1};g.handleEvent=function(a){return this.sa?this.p.call(this.da||this.src,a):this.p.handleEvent.call(this.p,a)};var kb=!A||A&&9<=Ea,lb=A&&!E("9");!C||E("528");B&&E("1.9b")||A&&E("8")||va&&E("9.5")||C&&E("528");B&&!E("8")||A&&E("9");function mb(a){mb[" "](a);return a}mb[" "]=p;function L(a,b){a&&this.S(a,b)}w(L,K);g=L.prototype;g.target=null;g.relatedTarget=null;g.offsetX=0;g.offsetY=0;g.clientX=0;g.clientY=0;g.screenX=0;g.screenY=0;g.button=0;g.keyCode=0;g.charCode=0;g.ctrlKey=!1;g.altKey=!1;g.shiftKey=!1;g.metaKey=!1;g.na=null;
g.S=function(a,b){var c=this.type=a.type;K.call(this,c);this.target=a.target||a.srcElement;this.currentTarget=b;var d=a.relatedTarget;if(d){if(B){var f;a:{try{mb(d.nodeName);f=!0;break a}catch(e){}f=!1}f||(d=null)}}else"mouseover"==c?d=a.fromElement:"mouseout"==c&&(d=a.toElement);this.relatedTarget=d;this.offsetX=C||void 0!==a.offsetX?a.offsetX:a.layerX;this.offsetY=C||void 0!==a.offsetY?a.offsetY:a.layerY;this.clientX=void 0!==a.clientX?a.clientX:a.pageX;this.clientY=void 0!==a.clientY?a.clientY:
a.pageY;this.screenX=a.screenX||0;this.screenY=a.screenY||0;this.button=a.button;this.keyCode=a.keyCode||0;this.charCode=a.charCode||("keypress"==c?a.keyCode:0);this.ctrlKey=a.ctrlKey;this.altKey=a.altKey;this.shiftKey=a.shiftKey;this.metaKey=a.metaKey;this.state=a.state;this.na=a;a.defaultPrevented&&this.preventDefault();delete this.ga};
g.preventDefault=function(){L.w.preventDefault.call(this);var a=this.na;if(a.preventDefault)a.preventDefault();else if(a.returnValue=!1,lb)try{if(a.ctrlKey||112<=a.keyCode&&123>=a.keyCode)a.keyCode=-1}catch(b){}};var nb={},M={},N={},O={};
function ob(a,b,c,d,f){if("array"==q(b)){for(var e=0;e<b.length;e++)ob(a,b[e],c,d,f);return null}a:{if(!b)throw Error("Invalid event type");d=!!d;var h=M;b in h||(h[b]={a:0,n:0});h=h[b];d in h||(h[d]={a:0,n:0},h.a++);var h=h[d],e=u(a),k;h.n++;if(h[e]){k=h[e];for(var l=0;l<k.length;l++)if(h=k[l],h.p==c&&h.da==f){if(h.v)break;k[l].O=!1;a=k[l];break a}}else k=h[e]=[],h.a++;l=pb();h=new jb;h.S(c,l,a,b,d,f);h.O=!1;l.src=a;l.p=h;k.push(h);N[e]||(N[e]=[]);N[e].push(h);a.addEventListener?a!=n&&a.la||a.addEventListener(b,
l,d):a.attachEvent(b in O?O[b]:O[b]="on"+b,l);a=h}b=a.key;nb[b]=a;return b}function pb(){var a=qb,b=kb?function(c){return a.call(b.src,b.p,c)}:function(c){c=a.call(b.src,b.p,c);if(!c)return c};return b}function rb(a,b,c,d,f){if("array"==q(b))for(var e=0;e<b.length;e++)rb(a,b[e],c,d,f);else{d=!!d;a:{e=M;if(b in e&&(e=e[b],d in e&&(e=e[d],a=u(a),e[a]))){a=e[a];break a}a=null}if(a)for(e=0;e<a.length;e++)if(a[e].p==c&&a[e].capture==d&&a[e].da==f){sb(a[e].key);break}}}
function sb(a){var b=nb[a];if(!b||b.v)return!1;var c=b.src,d=b.type,f=b.xa,e=b.capture;c.removeEventListener?c!=n&&c.la||c.removeEventListener(d,f,e):c.detachEvent&&c.detachEvent(d in O?O[d]:O[d]="on"+d,f);c=u(c);N[c]&&(f=N[c],Oa(f,b),0==f.length&&delete N[c]);b.v=!0;if(b=M[d][e][c])b.va=!0,tb(d,e,c,b);delete nb[a];return!0}
function tb(a,b,c,d){if(!d.T&&d.va){for(var f=0,e=0;f<d.length;f++)d[f].v?d[f].xa.src=null:(f!=e&&(d[e]=d[f]),e++);d.length=e;d.va=!1;0==e&&(delete M[a][b][c],M[a][b].a--,0==M[a][b].a&&(delete M[a][b],M[a].a--),0==M[a].a&&delete M[a])}}function ub(a,b,c,d,f){var e=1;b=u(b);if(a[b]){var h=--a.n,k=a[b];k.T?k.T++:k.T=1;try{for(var l=k.length,x=0;x<l;x++){var m=k[x];m&&!m.v&&(e&=!1!==vb(m,f))}}finally{a.n=Math.max(h,a.n),k.T--,tb(c,d,b,k)}}return Boolean(e)}
function vb(a,b){a.O&&sb(a.key);return a.handleEvent(b)}
function qb(a,b){if(a.v)return!0;var c=a.type,d=M;if(!(c in d))return!0;var d=d[c],f,e;if(!kb){var h;if(!(h=b))a:{h=["window","event"];for(var k=n;f=h.shift();)if(null!=k[f])k=k[f];else{h=null;break a}h=k}f=h;h=!0 in d;k=!1 in d;if(h){if(0>f.keyCode||void 0!=f.returnValue)return!0;a:{var l=!1;if(0==f.keyCode)try{f.keyCode=-1;break a}catch(x){l=!0}if(l||void 0==f.returnValue)f.returnValue=!0}}l=new L;l.S(f,this);f=!0;try{if(h){for(var m=[],r=l.currentTarget;r;r=r.parentNode)m.push(r);e=d[!0];e.n=e.a;
for(var z=m.length-1;!l.ga&&0<=z&&e.n;z--)l.currentTarget=m[z],f&=ub(e,m[z],c,!0,l);if(k)for(e=d[!1],e.n=e.a,z=0;!l.ga&&z<m.length&&e.n;z++)l.currentTarget=m[z],f&=ub(e,m[z],c,!1,l)}else f=vb(a,l)}finally{m&&(m.length=0)}return f}c=new L(b,this);return f=vb(a,c)};function wb(a){J.call(this);this.Na=a;this.d=[]}w(wb,J);var xb=[];function yb(a,b,c,d){var f="click";"array"!=q(f)&&(xb[0]=f,f=xb);for(var e=0;e<f.length;e++){var h=ob(b,f[e],c||a,!0,d||a.Na||a);a.d.push(h)}}function zb(a){I(a.d,sb);a.d.length=0}wb.prototype.handleEvent=function(){throw Error("EventHandler.handleEvent not implemented");};function Ab(){}aa(Ab);Ab.prototype.Ra=0;Ab.ca();function P(){J.call(this)}w(P,J);P.prototype.la=!0;P.prototype.ja=function(){};P.prototype.addEventListener=function(a,b,c,d){ob(this,a,b,c,d)};P.prototype.removeEventListener=function(a,b,c,d){rb(this,a,b,c,d)};function Q(a){J.call(this);this.t=a||Ya()}w(Q,P);g=Q.prototype;g.Oa=Ab.ca();g.pa=null;g.o=!1;g.e=null;g.h=null;g.M=null;g.r=null;g.$=null;g.oa=function(){return this.e};g.J=function(a){return this.e?this.t.J(a,this.e):null};g.ja=function(a){if(this.M&&this.M!=a)throw Error("Method not supported");Q.w.ja.call(this,a)};g.ba=function(){return this.t};g.f=function(){this.e=this.t.createElement("div")};
g.za=function(a){if(this.o)throw Error("Component already rendered");this.e||this.f();a?a.insertBefore(this.e,null):this.t.s.body.appendChild(this.e);this.M&&!this.M.o||this.u()};g.Ea=function(a){if(this.o)throw Error("Component already rendered");if(a)this.t&&this.t.s==$a(a)||(this.t=Ya(a)),this.P(a),this.u();else throw Error("Invalid element to decorate");};g.P=function(a){this.e=a};g.u=function(){this.o=!0;Bb(this,function(a){!a.o&&a.oa()&&a.u()})};
g.I=function(){Bb(this,function(a){a.o&&a.I()});this.K&&zb(this.K);this.o=!1};function Bb(a,b){a.r&&I(a.r,b,void 0)}
g.removeChild=function(a,b){if(a){var c=t(a)?a:a.pa||(a.pa=":"+(a.Oa.Ra++).toString(36)),d;this.$&&c?(d=this.$,d=(c in d?d[c]:void 0)||null):d=null;a=d;if(c&&a){d=this.$;c in d&&delete d[c];Oa(this.r,a);b&&(a.I(),a.e&&(c=a.e)&&c.parentNode&&c.parentNode.removeChild(c));c=a;if(null==c)throw Error("Unable to set parent component");c.M=null;Q.w.ja.call(c,null)}}if(!a)throw Error("Child is not in parent component");return a};
g.Y=function(a){for(var b=[];this.r&&0!=this.r.length;)b.push(this.removeChild(this.r?this.r[0]||null:null,a));return b};var Cb=RegExp("^(?:([^:/?#.]+):)?(?://(?:([^/?#]*)@)?([^/#?]*?)(?::([0-9]+))?(?=[/#?]|$))?([^?#]+)?(?:\\?([^#]*))?(?:#(.*))?$");function Db(a){if("function"==typeof a.l)return a.l();if(t(a))return a.split("");if(s(a)){for(var b=[],c=a.length,d=0;d<c;d++)b.push(a[d]);return b}return Ga(a)}function Eb(a,b,c){if("function"==typeof a.forEach)a.forEach(b,c);else if(s(a)||t(a))I(a,b,c);else{var d;if("function"==typeof a.B)d=a.B();else if("function"!=typeof a.l)if(s(a)||t(a)){d=[];for(var f=a.length,e=0;e<f;e++)d.push(e)}else d=Ha(a);else d=void 0;for(var f=Db(a),e=f.length,h=0;h<e;h++)b.call(c,f[h],d&&d[h],a)}};function Fb(a,b){this.j={};this.d=[];var c=arguments.length;if(1<c){if(c%2)throw Error("Uneven number of arguments");for(var d=0;d<c;d+=2)this.set(arguments[d],arguments[d+1])}else if(a){a instanceof Fb?(c=a.B(),d=a.l()):(c=Ha(a),d=Ga(a));for(var f=0;f<c.length;f++)this.set(c[f],d[f])}}g=Fb.prototype;g.a=0;g.l=function(){Gb(this);for(var a=[],b=0;b<this.d.length;b++)a.push(this.j[this.d[b]]);return a};g.B=function(){Gb(this);return this.d.concat()};g.G=function(a){return R(this.j,a)};
g.clear=function(){this.j={};this.a=this.d.length=0};g.remove=function(a){return R(this.j,a)?(delete this.j[a],this.a--,this.d.length>2*this.a&&Gb(this),!0):!1};function Gb(a){if(a.a!=a.d.length){for(var b=0,c=0;b<a.d.length;){var d=a.d[b];R(a.j,d)&&(a.d[c++]=d);b++}a.d.length=c}if(a.a!=a.d.length){for(var f={},c=b=0;b<a.d.length;)d=a.d[b],R(f,d)||(a.d[c++]=d,f[d]=1),b++;a.d.length=c}}g.get=function(a,b){return R(this.j,a)?this.j[a]:b};
g.set=function(a,b){R(this.j,a)||(this.a++,this.d.push(a));this.j[a]=b};g.F=function(){return new Fb(this)};function R(a,b){return Object.prototype.hasOwnProperty.call(a,b)};function S(a,b){var c;if(a instanceof S)this.i=void 0!==b?b:a.i,Hb(this,a.D),c=a.Z,T(this),this.Z=c,c=a.H,T(this),this.H=c,Ib(this,a.W),c=a.U,T(this),this.U=c,Jb(this,a.m.F()),c=a.R,T(this),this.R=c;else if(a&&(c=String(a).match(Cb))){this.i=!!b;Hb(this,c[1]||"",!0);var d=c[2]||"";T(this);this.Z=d?decodeURIComponent(d):"";d=c[3]||"";T(this);this.H=d?decodeURIComponent(d):"";Ib(this,c[4]);d=c[5]||"";T(this);this.U=d?decodeURIComponent(d):"";Jb(this,c[6]||"",!0);c=c[7]||"";T(this);this.R=c?decodeURIComponent(c):
""}else this.i=!!b,this.m=new U(null,0,this.i)}g=S.prototype;g.D="";g.Z="";g.H="";g.W=null;g.U="";g.R="";g.Pa=!1;g.i=!1;g.toString=function(){var a=[],b=this.D;b&&a.push(V(b,Kb),":");if(b=this.H){a.push("//");var c=this.Z;c&&a.push(V(c,Kb),"@");a.push(encodeURIComponent(String(b)));b=this.W;null!=b&&a.push(":",String(b))}if(b=this.U)this.H&&"/"!=b.charAt(0)&&a.push("/"),a.push(V(b,"/"==b.charAt(0)?Lb:Mb));(b=this.m.toString())&&a.push("?",b);(b=this.R)&&a.push("#",V(b,Nb));return a.join("")};
g.F=function(){return new S(this)};function Hb(a,b,c){T(a);a.D=c?b?decodeURIComponent(b):"":b;a.D&&(a.D=a.D.replace(/:$/,""))}function Ib(a,b){T(a);if(b){b=Number(b);if(isNaN(b)||0>b)throw Error("Bad port number "+b);a.W=b}else a.W=null}function Jb(a,b,c){T(a);b instanceof U?(a.m=b,a.m.ia(a.i)):(c||(b=V(b,Ob)),a.m=new U(b,0,a.i))}function T(a){if(a.Pa)throw Error("Tried to modify a read-only Uri");}g.ia=function(a){this.i=a;this.m&&this.m.ia(a);return this};
function V(a,b){return t(a)?encodeURI(a).replace(b,Pb):null}function Pb(a){a=a.charCodeAt(0);return"%"+(a>>4&15).toString(16)+(a&15).toString(16)}var Kb=/[#\/\?@]/g,Mb=/[\#\?:]/g,Lb=/[\#\?]/g,Ob=/[\#\?@]/g,Nb=/#/g;function U(a,b,c){this.g=a||null;this.i=!!c}
function W(a){if(!a.b&&(a.b=new Fb,a.a=0,a.g))for(var b=a.g.split("&"),c=0;c<b.length;c++){var d=b[c].indexOf("="),f=null,e=null;0<=d?(f=b[c].substring(0,d),e=b[c].substring(d+1)):f=b[c];f=decodeURIComponent(f.replace(/\+/g," "));f=X(a,f);a.add(f,e?decodeURIComponent(e.replace(/\+/g," ")):"")}}g=U.prototype;g.b=null;g.a=null;g.add=function(a,b){W(this);this.g=null;a=X(this,a);var c=this.b.get(a);c||this.b.set(a,c=[]);c.push(b);this.a++;return this};
g.remove=function(a){W(this);a=X(this,a);return this.b.G(a)?(this.g=null,this.a-=this.b.get(a).length,this.b.remove(a)):!1};g.clear=function(){this.b=this.g=null;this.a=0};g.G=function(a){W(this);a=X(this,a);return this.b.G(a)};g.B=function(){W(this);for(var a=this.b.l(),b=this.b.B(),c=[],d=0;d<b.length;d++)for(var f=a[d],e=0;e<f.length;e++)c.push(b[d]);return c};g.l=function(a){W(this);var b=[];if(a)this.G(a)&&(b=Pa(b,this.b.get(X(this,a))));else{a=this.b.l();for(var c=0;c<a.length;c++)b=Pa(b,a[c])}return b};
g.set=function(a,b){W(this);this.g=null;a=X(this,a);this.G(a)&&(this.a-=this.b.get(a).length);this.b.set(a,[b]);this.a++;return this};g.get=function(a,b){var c=a?this.l(a):[];return 0<c.length?String(c[0]):b};g.toString=function(){if(this.g)return this.g;if(!this.b)return"";for(var a=[],b=this.b.B(),c=0;c<b.length;c++)for(var d=b[c],f=encodeURIComponent(String(d)),d=this.l(d),e=0;e<d.length;e++){var h=f;""!==d[e]&&(h+="="+encodeURIComponent(String(d[e])));a.push(h)}return this.g=a.join("&")};
g.F=function(){var a=new U;a.g=this.g;this.b&&(a.b=this.b.F(),a.a=this.a);return a};function X(a,b){var c=String(b);a.i&&(c=c.toLowerCase());return c}g.ia=function(a){a&&!this.i&&(W(this),this.g=null,Eb(this.b,function(a,c){var d=c.toLowerCase();c!=d&&(this.remove(c),this.remove(d),0<a.length&&(this.g=null,this.b.set(X(this,d),Qa(a)),this.a+=a.length))},this));this.i=a};function Qb(){}g=Qb.prototype;g.name=null;g.wa=null;g.N=null;g.ha=null;g.aa=null;function Rb(a){var b=new Qb;b.name=a.user_name;b.wa=a.user_pic;b.ha=a.score;b.N=a.answered;b.aa=a.clues;return b};function Sb(){J.call(this);this.k=[];this.A={}}w(Sb,J);g=Sb.prototype;g.ta=1;g.X=0;function Tb(a,b,c,d){var f=a.A[b];f||(f=a.A[b]=[]);var e=a.ta;a.k[e]=b;a.k[e+1]=c;a.k[e+2]=d;a.ta=e+3;f.push(e)}g.Ba=function(a){if(0!=this.X)return this.V||(this.V=[]),this.V.push(a),!1;var b=this.k[a];if(b){var c=this.A[b];c&&Oa(c,a);delete this.k[a];delete this.k[a+1];delete this.k[a+2]}return!!b};
g.ya=function(a,b){var c=this.A[a];if(c){this.X++;for(var d=Ra(arguments,1),f=0,e=c.length;f<e;f++){var h=c[f];this.k[h+1].apply(this.k[h+2],d)}this.X--;if(this.V&&0==this.X)for(;c=this.V.pop();)this.Ba(c)}};g.clear=function(a){if(a){var b=this.A[a];b&&(I(b,this.Ba,this),delete this.A[a])}else this.k.length=0,this.A={}};function Ub(){this.q="pending";this.C=[];this.ma=this.ka=void 0}function Vb(){F.call(this,"Multiple attempts to set the state of this Result")}w(Vb,F);Ub.prototype.getError=function(){return this.ma};function Wb(a,b){if("pending"==a.q)for(a.ka=b,a.q="success";a.C.length;)a.C.shift()(a);else throw new Vb;}function Xb(a,b){if("pending"==a.q)for(a.ma=b,a.q="error";a.C.length;)a.C.shift()(a);else throw new Vb;};function Yb(a,b,c){b=c?v(b,c):b;"pending"==a.q?a.C.push(b):b(a)}function Zb(a,b){Yb(a,function(a){"error"==a.q&&b.call(this,a)},void 0)}function $b(a,b){var c=new ac;Yb(a,function(a){"success"==a.q?Wb(c,b(a.ka)):Xb(c,a.getError())});return c}function ac(){Ub.call(this)}w(ac,Ub);function bc(a){a=String(a);if(/^\s*$/.test(a)?0:/^[\],:{}\s\u2028\u2029]*$/.test(a.replace(/\\["\\\/bfnrtu]/g,"@").replace(/"[^"\\\n\r\u2028\u2029\x00-\x08\x0a-\x1f]*"|true|false|null|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?/g,"]").replace(/(?:^|:|,)(?:[\s\u2028\u2029]*\[)+/g,"")))try{return eval("("+a+")")}catch(b){}throw Error("Invalid JSON string: "+a);};function cc(){};var dc;function ec(){}w(ec,cc);function fc(){var a;a:{var b=dc;if(!b.qa&&"undefined"==typeof XMLHttpRequest&&"undefined"!=typeof ActiveXObject){for(var c=["MSXML2.XMLHTTP.6.0","MSXML2.XMLHTTP.3.0","MSXML2.XMLHTTP","Microsoft.XMLHTTP"],d=0;d<c.length;d++){var f=c[d];try{new ActiveXObject(f);a=b.qa=f;break a}catch(e){}}throw Error("Could not create ActiveXObject. ActiveX might be disabled, or MSXML might not be installed");}a=b.qa}return a?new ActiveXObject(a):new XMLHttpRequest}dc=new ec;function gc(a,b){var c=hc(a,b),d=c=$b(c,ic);b&&b.Va&&(d=$b(c,ga(jc,b.Va)));return $b(d,bc)}function hc(a,b){var c=new Ub;Zb(c,function(){});kc(a,b,function(a){Wb(c,a)},function(a){Xb(c,a)});return c}
function kc(a,b,c,d){b=b||{};var f=c||p,e=d||p,h,k=fc();try{k.open("GET",a,!0)}catch(l){e(new Y("Error opening XHR: "+l.message,a));return}k.onreadystatechange=function(){if(4==k.readyState){window.clearTimeout(h);var b;a:switch(k.status){case 200:case 201:case 202:case 204:case 206:case 304:case 1223:b=!0;break a;default:b=!1}!b&&(b=0===k.status)&&(b=a.match(Cb)[1]||null,!b&&self.location&&(b=self.location.protocol,b=b.substr(0,b.length-1)),b=b?b.toLowerCase():"",b=!("http"==b||"https"==b||""==b));
b?f(k):e(new lc(k.status,a))}};if(b.headers)for(var x in b.headers)k.setRequestHeader(x,b.headers[x]);b.withCredentials&&(k.withCredentials=b.withCredentials);b.Qa&&k.overrideMimeType(b.Qa);0<b.Sa&&(h=window.setTimeout(function(){k.onreadystatechange=p;k.abort();e(new mc(a))},b.Sa));try{k.send(null)}catch(m){k.onreadystatechange=p,window.clearTimeout(h),e(new Y("Error sending XHR: "+m.message,a))}}function ic(a){return a.responseText}
function jc(a,b){0==b.lastIndexOf(a,0)&&(b=b.substring(a.length));return b}function Y(a,b){F.call(this,a+", url="+b);this.url=b}w(Y,F);Y.prototype.name="XhrError";function lc(a,b){Y.call(this,"Request Failed, status="+a,b);this.status=a}w(lc,Y);lc.prototype.name="XhrHttpError";function mc(a){Y.call(this,"Request timed out",a)}w(mc,Y);mc.prototype.name="XhrTimeoutError";function nc(){}aa(nc);ha("ffc.api.Client.getInstance",nc.ca);nc.prototype.Ja=function(a,b){return gc.apply(null,arguments)};nc.prototype.Ia=function(a,b,c){a=ia(oc,a);a=a instanceof S?a.F():new S(a,void 0);b&&(T(a),a.m.set("offset",b));c&&(T(a),a.m.set("limit",c));return this.Ja(a)};var oc="/api/leaderboard/%s";function pc(a,b){Sb.call(this);this.id=a;this.page=0;this.ea=qc;this.Ha=v(b.Ia,b,a)}w(pc,Sb);ha("ffc.leaderboard.LeaderBoardModel",pc);pc.prototype.getData=function(){var a=this.Ha(this.page*this.ea,this.ea),b=this.La.bind(this);"pending"==a.q?a.C.push(b):b(a)};pc.prototype.La=function(a){a=a.ka;this.Ta=a.count;this.ya(rc);this.Ua=Na(a.users,Rb);this.ya(sc)};var qc=20,sc="usersUpdated",rc="totalUpdated";var tc={};A&&E(8);function uc(a,b){var c;a:{c=(new Za(void 0)||Ya()).createElement("DIV");var d;d=a(b||tc,void 0,void 0);ba(d)?(La("Soy template output is unsafe for use as HTML: "+d),d="zSoyz"):d=String(d);c.innerHTML=d;if(1==c.childNodes.length&&(d=c.firstChild,1==d.nodeType)){c=d;break a}}return c}
var vc={"\x00":"&#0;",'"':"&quot;","&":"&amp;","'":"&#39;","<":"&lt;",">":"&gt;","\t":"&#9;","\n":"&#10;","\x0B":"&#11;","\f":"&#12;","\r":"&#13;"," ":"&#32;","-":"&#45;","/":"&#47;","=":"&#61;","`":"&#96;","\u0085":"&#133;","\u00a0":"&#160;","\u2028":"&#8232;","\u2029":"&#8233;"};function wc(a){return vc[a]}var xc=/[\x00\x22\x26\x27\x3c\x3e]/g;function yc(){return'<table class="table table-striped table-hover"><thead><tr><th colspan="2">User</th><th class="leaderboard-clues">Clues</th><th class="leaderboard-score">Score</th><th class="leaderboard-answered">Answered</th><th class="leaderboard-averageclues">Av. Clues</th><th class="leaderboard-average">Av. Score</th></tr></thead><tbody class="leaderboard-users"></tbody></table>'}function zc(){return'<div class="leaderboard-pagination"><ul class="pagination pagination-sm"></ul></div>'}
function Ac(a){return"<li"+(a.Da?' class="active"':"")+'><a href="#">'+("object"===typeof a.L&&a.L&&0===a.L.Wa?a.L.content:String(a.L).replace(xc,wc))+"</a></li>"};function Z(a){Q.call(this);this.Q=this.K||(this.K=new wb(this));this.c=this.ba();this.h=a}w(Z,Q);ha("ffc.leaderboard.LeaderBoard",Z);Z.prototype.render=Z.prototype.za;g=Z.prototype;g.f=function(){var a=this.c.f("DIV");this.c.append(a,uc(yc));this.c.append(a,uc(zc));this.P(a)};g.P=function(a){Z.w.P.call(this,a);this.Aa=this.J("leaderboard-users");this.fa=this.J("pagination")};
g.u=function(){Z.w.u.call(this);Tb(this.h,rc,this.Ga,this);Tb(this.h,sc,this.Fa,this);yb(this.Q,this.fa,this.Ka,this);this.h.getData();this.e.style.display="block"};g.I=function(){Z.w.I.call(this);this.h.clear();zb(this.Q);this.c.Y(this.e);this.e=null};
g.Fa=function(){this.c.Y(this.Aa);for(var a=[this.Aa],b=this.h.Ua,c=0,d=b.length;c<d;c++){var f=b[c];a.push(this.c.f("TR",null,this.c.f("TD",null,this.c.f("IMG",{src:f.wa,alt:f.name,width:20,height:20})),this.c.f("TD",null,this.c.f("A",{href:"/u/"+f.name},f.name)),this.c.f("TD","leaderboard-clues",f.aa+""),this.c.f("TD","leaderboard-score",f.ha+""),this.c.f("TD","leaderboard-answered",f.N+""),this.c.f("TD","leaderboard-averageclues",(f.aa/f.N||0).toFixed(1)+""),this.c.f("TD","leaderboard-average",
(f.ha/f.N||0).toFixed(1)+"")))}this.c.append.apply(this.Ca,a)};g.Ga=function(){this.c.Y(this.fa);var a=[this.fa],b;b=[];var c=Math.ceil(this.h.Ta/this.h.ea);if(0>1*(c-0))b=[];else for(var d=0;d<c;d+=1)b.push(d);if(1<b.length){c=0;for(d=b.length;c<d;c++)a.push(uc(Ac,{L:b[c],Da:c==this.h.page}));this.c.append.apply(this.Ca,a)}};g.Ka=function(a){a.preventDefault();"A"==a.target.nodeName&&(a=parseInt(a.target.innerHTML,10)-1,a!=this.h.page&&(this.h.page=a,this.h.getData()))};function $(a){Q.call(this);this.Q=this.K||(this.K=new wb(this));this.c=this.ba();this.ua=a}w($,Q);ha("ffc.leaderboard.LeaderBoardToggler",$);$.prototype.decorate=$.prototype.Ea;$.prototype.u=function(){$.w.u.call(this);yb(this.Q,this.e,this.Ma,this)};
$.prototype.Ma=function(a){a.preventDefault();var b=gb(a.target),c;if(c="A"==a.target.nodeName)if(c=b)c=Ta(b),c=!(0<=H(c,"active"));if(c)for(a=a.target,a=a.dataset?a.dataset.leaderboard:a.getAttribute("data-"+"leaderboard".replace(/([A-Z])/g,"-$1").toLowerCase()),Va(this.c.J("active",this.e),"active"),Ua(b,"active"),b=0,c=this.ua.length;b<c;b++){var d=this.ua[b];d.h.id==a?d.za(document.getElementById("leaderboard-container-"+a)):d.o&&d.I()}};})();
