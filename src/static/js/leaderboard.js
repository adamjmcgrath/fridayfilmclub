(function() {var g,n=this;function p(){}function aa(a){a.ca=function(){return a.ra?a.ra:a.ra=new a}}
function q(a){var b=typeof a;if("object"==b)if(a){if(a instanceof Array)return"array";if(a instanceof Object)return b;var c=Object.prototype.toString.call(a);if("[object Window]"==c)return"object";if("[object Array]"==c||"number"==typeof a.length&&"undefined"!=typeof a.splice&&"undefined"!=typeof a.propertyIsEnumerable&&!a.propertyIsEnumerable("splice"))return"array";if("[object Function]"==c||"undefined"!=typeof a.call&&"undefined"!=typeof a.propertyIsEnumerable&&!a.propertyIsEnumerable("call"))return"function"}else return"null";
else if("function"==b&&"undefined"==typeof a.call)return"object";return b}function s(a){return"array"==q(a)}function t(a){var b=q(a);return"array"==b||"object"==b&&"number"==typeof a.length}function u(a){return"string"==typeof a}function ba(a){var b=typeof a;return"object"==b&&null!=a||"function"==b}function v(a){return a[ca]||(a[ca]=++da)}var ca="closure_uid_"+(1E9*Math.random()>>>0),da=0;function ea(a,b,c){return a.call.apply(a.bind,arguments)}
function fa(a,b,c){if(!a)throw Error();if(2<arguments.length){var d=Array.prototype.slice.call(arguments,2);return function(){var c=Array.prototype.slice.call(arguments);Array.prototype.unshift.apply(c,d);return a.apply(b,c)}}return function(){return a.apply(b,arguments)}}function ga(a,b,c){ga=Function.prototype.bind&&-1!=Function.prototype.bind.toString().indexOf("native code")?ea:fa;return ga.apply(null,arguments)}
function ha(a,b){var c=Array.prototype.slice.call(arguments,1);return function(){var b=Array.prototype.slice.call(arguments);b.unshift.apply(b,c);return a.apply(this,b)}}function ia(a,b){var c=a.split("."),d=n;c[0]in d||!d.execScript||d.execScript("var "+c[0]);for(var e;c.length&&(e=c.shift());)c.length||void 0===b?d=d[e]?d[e]:d[e]={}:d[e]=b}function w(a,b){function c(){}c.prototype=b.prototype;a.w=b.prototype;a.prototype=new c};function ja(a,b){for(var c=1;c<arguments.length;c++){var d=String(arguments[c]).replace(/\$/g,"$$$$");a=a.replace(/\%s/,d)}return a}function ka(a){if(!la.test(a))return a;-1!=a.indexOf("&")&&(a=a.replace(ma,"&amp;"));-1!=a.indexOf("<")&&(a=a.replace(na,"&lt;"));-1!=a.indexOf(">")&&(a=a.replace(oa,"&gt;"));-1!=a.indexOf('"')&&(a=a.replace(pa,"&quot;"));return a}var ma=/&/g,na=/</g,oa=/>/g,pa=/\"/g,la=/[&<>\"]/;var y,qa,ra,sa;function ta(){return n.navigator?n.navigator.userAgent:null}sa=ra=qa=y=!1;var ua;if(ua=ta()){var va=n.navigator;y=0==ua.indexOf("Opera");qa=!y&&-1!=ua.indexOf("MSIE");ra=!y&&-1!=ua.indexOf("WebKit");sa=!y&&!ra&&"Gecko"==va.product}var wa=y,A=qa,B=sa,C=ra;function xa(){var a=n.document;return a?a.documentMode:void 0}var ya;
a:{var za="",D;if(wa&&n.opera)var Aa=n.opera.version,za="function"==typeof Aa?Aa():Aa;else if(B?D=/rv\:([^\);]+)(\)|;)/:A?D=/MSIE\s+([^\);]+)(\)|;)/:C&&(D=/WebKit\/(\S+)/),D)var Ba=D.exec(ta()),za=Ba?Ba[1]:"";if(A){var Ca=xa();if(Ca>parseFloat(za)){ya=String(Ca);break a}}ya=za}var Da={};
function E(a){var b;if(!(b=Da[a])){b=0;for(var c=String(ya).replace(/^[\s\xa0]+|[\s\xa0]+$/g,"").split("."),d=String(a).replace(/^[\s\xa0]+|[\s\xa0]+$/g,"").split("."),e=Math.max(c.length,d.length),f=0;0==b&&f<e;f++){var h=c[f]||"",k=d[f]||"",l=RegExp("(\\d*)(\\D*)","g"),x=RegExp("(\\d*)(\\D*)","g");do{var m=l.exec(h)||["","",""],r=x.exec(k)||["","",""];if(0==m[0].length&&0==r[0].length)break;b=((0==m[1].length?0:parseInt(m[1],10))<(0==r[1].length?0:parseInt(r[1],10))?-1:(0==m[1].length?0:parseInt(m[1],
10))>(0==r[1].length?0:parseInt(r[1],10))?1:0)||((0==m[2].length)<(0==r[2].length)?-1:(0==m[2].length)>(0==r[2].length)?1:0)||(m[2]<r[2]?-1:m[2]>r[2]?1:0)}while(0==b)}b=Da[a]=0<=b}return b}var Ea=n.document,Fa=Ea&&A?xa()||("CSS1Compat"==Ea.compatMode?parseInt(ya,10):5):void 0;function Ga(a,b){for(var c in a)b.call(void 0,a[c],c,a)}function Ha(a){var b=[],c=0,d;for(d in a)b[c++]=a[d];return b}function Ia(a){var b=[],c=0,d;for(d in a)b[c++]=d;return b}var Ja="constructor hasOwnProperty isPrototypeOf propertyIsEnumerable toLocaleString toString valueOf".split(" ");function Ka(a,b){for(var c,d,e=1;e<arguments.length;e++){d=arguments[e];for(c in d)a[c]=d[c];for(var f=0;f<Ja.length;f++)c=Ja[f],Object.prototype.hasOwnProperty.call(d,c)&&(a[c]=d[c])}};function F(a){Error.captureStackTrace?Error.captureStackTrace(this,F):this.stack=Error().stack||"";a&&(this.message=String(a))}w(F,Error);F.prototype.name="CustomError";function La(a,b){b.unshift(a);F.call(this,ja.apply(null,b));b.shift()}w(La,F);La.prototype.name="AssertionError";function Ma(a,b){throw new La("Failure"+(a?": "+a:""),Array.prototype.slice.call(arguments,1));};var G=Array.prototype,H=G.indexOf?function(a,b,c){return G.indexOf.call(a,b,c)}:function(a,b,c){c=null==c?0:0>c?Math.max(0,a.length+c):c;if(u(a))return u(b)&&1==b.length?a.indexOf(b,c):-1;for(;c<a.length;c++)if(c in a&&a[c]===b)return c;return-1},Na=G.forEach?function(a,b,c){G.forEach.call(a,b,c)}:function(a,b,c){for(var d=a.length,e=u(a)?a.split(""):a,f=0;f<d;f++)f in e&&b.call(c,e[f],f,a)},Oa=G.filter?function(a,b,c){return G.filter.call(a,b,c)}:function(a,b,c){for(var d=a.length,e=[],f=0,h=u(a)?
a.split(""):a,k=0;k<d;k++)if(k in h){var l=h[k];b.call(c,l,k,a)&&(e[f++]=l)}return e},Pa=G.map?function(a,b,c){return G.map.call(a,b,c)}:function(a,b,c){for(var d=a.length,e=Array(d),f=u(a)?a.split(""):a,h=0;h<d;h++)h in f&&(e[h]=b.call(c,f[h],h,a));return e};function Qa(a,b){var c;a:{c=a.length;for(var d=u(a)?a.split(""):a,e=0;e<c;e++)if(e in d&&b.call(void 0,d[e],e,a)){c=e;break a}c=-1}return 0>c?null:u(a)?a.charAt(c):a[c]}function Ra(a,b){var c=H(a,b);0<=c&&G.splice.call(a,c,1)}
function Sa(a){return G.concat.apply(G,arguments)}function Ta(a){var b=a.length;if(0<b){for(var c=Array(b),d=0;d<b;d++)c[d]=a[d];return c}return[]}function Ua(a,b,c){return 2>=arguments.length?G.slice.call(a,b):G.slice.call(a,b,c)};var Va;function Wa(a){a=a.className;return u(a)&&a.match(/\S+/g)||[]}function Xa(a,b){for(var c=Wa(a),d=Ua(arguments,1),e=c.length+d.length,f=c,h=0;h<d.length;h++)0<=H(f,d[h])||f.push(d[h]);a.className=c.join(" ");return c.length==e}function Ya(a,b){var c=Wa(a),d=Ua(arguments,1),c=Za(c,d);a.className=c.join(" ")}function Za(a,b){return Oa(a,function(a){return!(0<=H(b,a))})};var $a=!A||A&&9<=Fa;!B&&!A||A&&A&&9<=Fa||B&&E("1.9.1");A&&E("9");function ab(a){return a?new bb(cb(a)):Va||(Va=new bb)}function db(a,b){var c,d,e,f;c=document;c=b||c;if(c.querySelectorAll&&c.querySelector&&a)return c.querySelectorAll(""+(a?"."+a:""));if(a&&c.getElementsByClassName){var h=c.getElementsByClassName(a);return h}h=c.getElementsByTagName("*");if(a){f={};for(d=e=0;c=h[d];d++){var k=c.className;"function"==typeof k.split&&0<=H(k.split(/\s+/),a)&&(f[e++]=c)}f.length=e;return f}return h}
function eb(a,b){Ga(b,function(b,d){"style"==d?a.style.cssText=b:"class"==d?a.className=b:"for"==d?a.htmlFor=b:d in fb?a.setAttribute(fb[d],b):0==d.lastIndexOf("aria-",0)||0==d.lastIndexOf("data-",0)?a.setAttribute(d,b):a[d]=b})}var fb={cellpadding:"cellPadding",cellspacing:"cellSpacing",colspan:"colSpan",frameborder:"frameBorder",height:"height",maxlength:"maxLength",role:"role",rowspan:"rowSpan",type:"type",usemap:"useMap",valign:"vAlign",width:"width"};
function gb(a,b,c,d){function e(c){c&&b.appendChild(u(c)?a.createTextNode(c):c)}for(;d<c.length;d++){var f=c[d];!t(f)||ba(f)&&0<f.nodeType?e(f):Na(hb(f)?Ta(f):f,e)}}function cb(a){return 9==a.nodeType?a:a.ownerDocument||a.document}function hb(a){if(a&&"number"==typeof a.length){if(ba(a))return"function"==typeof a.item||"string"==typeof a.item;if("function"==q(a))return"function"==typeof a.item}return!1}function ib(a,b){for(var c=0;a;){if(b(a))return a;a=a.parentNode;c++}return null}
function bb(a){this.t=a||n.document||document}g=bb.prototype;g.ba=ab;g.na=function(a){return u(a)?this.t.getElementById(a):a};g.I=function(a,b){var c=b||this.t,d=c||document;d.querySelectorAll&&d.querySelector?c=d.querySelector("."+a):(d=c||document,c=(d.querySelectorAll&&d.querySelector?d.querySelectorAll("."+a):d.getElementsByClassName?d.getElementsByClassName(a):db(a,c))[0]);return c||null};
g.g=function(a,b,c){var d=this.t,e=arguments,f=e[0],h=e[1];if(!$a&&h&&(h.name||h.type)){f=["<",f];h.name&&f.push(' name="',ka(h.name),'"');if(h.type){f.push(' type="',ka(h.type),'"');var k={};Ka(k,h);delete k.type;h=k}f.push(">");f=f.join("")}f=d.createElement(f);h&&(u(h)?f.className=h:s(h)?Xa.apply(null,[f].concat(h)):eb(f,h));2<e.length&&gb(d,f,e,2);return f};g.createElement=function(a){return this.t.createElement(a)};g.createTextNode=function(a){return this.t.createTextNode(String(a))};
g.appendChild=function(a,b){a.appendChild(b)};g.append=function(a,b){gb(cb(a),a,arguments,1)};g.Y=function(a){for(var b;b=a.firstChild;)a.removeChild(b)};function jb(a){return ib(a,function(a){return"LI"==a.nodeName&&!0})};function I(){0!=kb&&v(this)}var kb=0;function J(a,b){this.type=a;this.currentTarget=this.target=b}J.prototype.fa=!1;J.prototype.defaultPrevented=!1;J.prototype.preventDefault=function(){this.defaultPrevented=!0};var lb=0;function mb(){}g=mb.prototype;g.key=0;g.q=!1;g.N=!1;g.S=function(a,b,c,d,e,f){if("function"==q(a))this.ta=!0;else if(a&&a.handleEvent&&"function"==q(a.handleEvent))this.ta=!1;else throw Error("Invalid listener argument");this.l=a;this.ya=b;this.src=c;this.type=d;this.capture=!!e;this.R=f;this.N=!1;this.key=++lb;this.q=!1};g.handleEvent=function(a){return this.ta?this.l.call(this.R||this.src,a):this.l.handleEvent.call(this.l,a)};var nb=!A||A&&9<=Fa,ob=A&&!E("9");!C||E("528");B&&E("1.9b")||A&&E("8")||wa&&E("9.5")||C&&E("528");B&&!E("8")||A&&E("9");function pb(a){pb[" "](a);return a}pb[" "]=p;function K(a,b){a&&this.S(a,b)}w(K,J);g=K.prototype;g.target=null;g.relatedTarget=null;g.offsetX=0;g.offsetY=0;g.clientX=0;g.clientY=0;g.screenX=0;g.screenY=0;g.button=0;g.keyCode=0;g.charCode=0;g.ctrlKey=!1;g.altKey=!1;g.shiftKey=!1;g.metaKey=!1;g.ma=null;
g.S=function(a,b){var c=this.type=a.type;J.call(this,c);this.target=a.target||a.srcElement;this.currentTarget=b;var d=a.relatedTarget;if(d){if(B){var e;a:{try{pb(d.nodeName);e=!0;break a}catch(f){}e=!1}e||(d=null)}}else"mouseover"==c?d=a.fromElement:"mouseout"==c&&(d=a.toElement);this.relatedTarget=d;this.offsetX=C||void 0!==a.offsetX?a.offsetX:a.layerX;this.offsetY=C||void 0!==a.offsetY?a.offsetY:a.layerY;this.clientX=void 0!==a.clientX?a.clientX:a.pageX;this.clientY=void 0!==a.clientY?a.clientY:
a.pageY;this.screenX=a.screenX||0;this.screenY=a.screenY||0;this.button=a.button;this.keyCode=a.keyCode||0;this.charCode=a.charCode||("keypress"==c?a.keyCode:0);this.ctrlKey=a.ctrlKey;this.altKey=a.altKey;this.shiftKey=a.shiftKey;this.metaKey=a.metaKey;this.state=a.state;this.ma=a;a.defaultPrevented&&this.preventDefault();delete this.fa};
g.preventDefault=function(){K.w.preventDefault.call(this);var a=this.ma;if(a.preventDefault)a.preventDefault();else if(a.returnValue=!1,ob)try{if(a.ctrlKey||112<=a.keyCode&&123>=a.keyCode)a.keyCode=-1}catch(b){}};var qb={},L={},M={},N={};
function rb(a,b,c,d,e){if(s(b)){for(var f=0;f<b.length;f++)rb(a,b[f],c,d,e);return null}a:{if(!b)throw Error("Invalid event type");d=!!d;var h=L;b in h||(h[b]={a:0,o:0});h=h[b];d in h||(h[d]={a:0,o:0},h.a++);var h=h[d],f=v(a),k;h.o++;if(h[f]){k=h[f];for(var l=0;l<k.length;l++)if(h=k[l],h.l==c&&h.R==e){if(h.q)break;k[l].N=!1;a=k[l];break a}}else k=h[f]=[],h.a++;l=sb();h=new mb;h.S(c,l,a,b,d,e);h.N=!1;l.src=a;l.l=h;k.push(h);M[f]||(M[f]=[]);M[f].push(h);a.addEventListener?a!=n&&a.ka||a.addEventListener(b,
l,d):a.attachEvent(b in N?N[b]:N[b]="on"+b,l);a=h}b=a.key;qb[b]=a;return b}function sb(){var a=tb,b=nb?function(c){return a.call(b.src,b.l,c)}:function(c){c=a.call(b.src,b.l,c);if(!c)return c};return b}function ub(a,b,c,d,e){if(s(b))for(var f=0;f<b.length;f++)ub(a,b[f],c,d,e);else if(d=!!d,a=vb(a,b,d))for(f=0;f<a.length;f++)if(a[f].l==c&&a[f].capture==d&&a[f].R==e){wb(a[f].key);break}}
function wb(a){var b=qb[a];if(!b||b.q)return!1;var c=b.src,d=b.type,e=b.ya,f=b.capture;c.removeEventListener?c!=n&&c.ka||c.removeEventListener(d,e,f):c.detachEvent&&c.detachEvent(d in N?N[d]:N[d]="on"+d,e);c=v(c);M[c]&&(e=M[c],Ra(e,b),0==e.length&&delete M[c]);b.q=!0;if(b=L[d][f][c])b.wa=!0,xb(d,f,c,b);delete qb[a];return!0}
function xb(a,b,c,d){if(!d.T&&d.wa){for(var e=0,f=0;e<d.length;e++)d[e].q?d[e].ya.src=null:(e!=f&&(d[f]=d[e]),f++);d.length=f;d.wa=!1;0==f&&(delete L[a][b][c],L[a][b].a--,0==L[a][b].a&&(delete L[a][b],L[a].a--),0==L[a].a&&delete L[a])}}function vb(a,b,c){var d=L;return b in d&&(d=d[b],c in d&&(d=d[c],a=v(a),d[a]))?d[a]:null}
function yb(a,b,c,d,e){var f=1;b=v(b);if(a[b]){var h=--a.o,k=a[b];k.T?k.T++:k.T=1;try{for(var l=k.length,x=0;x<l;x++){var m=k[x];m&&!m.q&&(f&=!1!==zb(m,e))}}finally{a.o=Math.max(h,a.o),k.T--,xb(c,d,b,k)}}return Boolean(f)}function zb(a,b){a.N&&wb(a.key);return a.handleEvent(b)}
function tb(a,b){if(a.q)return!0;var c=a.type,d=L;if(!(c in d))return!0;var d=d[c],e,f;if(!nb){var h;if(!(h=b))a:{h=["window","event"];for(var k=n;e=h.shift();)if(null!=k[e])k=k[e];else{h=null;break a}h=k}e=h;h=!0 in d;k=!1 in d;if(h){if(0>e.keyCode||void 0!=e.returnValue)return!0;a:{var l=!1;if(0==e.keyCode)try{e.keyCode=-1;break a}catch(x){l=!0}if(l||void 0==e.returnValue)e.returnValue=!0}}l=new K;l.S(e,this);e=!0;try{if(h){for(var m=[],r=l.currentTarget;r;r=r.parentNode)m.push(r);f=d[!0];f.o=f.a;
for(var z=m.length-1;!l.fa&&0<=z&&f.o;z--)l.currentTarget=m[z],e&=yb(f,m[z],c,!0,l);if(k)for(f=d[!1],f.o=f.a,z=0;!l.fa&&z<m.length&&f.o;z++)l.currentTarget=m[z],e&=yb(f,m[z],c,!1,l)}else e=zb(a,l)}finally{m&&(m.length=0)}return e}c=new K(b,this);return e=zb(a,c)};function Ab(a){I.call(this);this.oa=a;this.c=[]}w(Ab,I);var Bb=[];function Cb(a,b,c,d){var e="click";s(e)||(Bb[0]=e,e=Bb);for(var f=0;f<e.length;f++){var h=rb(b,e[f],c||a,!0,d||a.oa||a);a.c.push(h)}}function Db(a,b,c,d,e,f){if(s(c))for(var h=0;h<c.length;h++)Db(a,b,c[h],d,e,f);else{a:{d=d||a;f=f||a.oa||a;e=!!e;if(b=vb(b,c,e))for(c=0;c<b.length;c++)if(!b[c].q&&b[c].l==d&&b[c].capture==e&&b[c].R==f){b=b[c];break a}b=null}b&&(b=b.key,wb(b),Ra(a.c,b))}}function Eb(a){Na(a.c,wb);a.c.length=0}
Ab.prototype.handleEvent=function(){throw Error("EventHandler.handleEvent not implemented");};function Fb(){}aa(Fb);Fb.prototype.Qa=0;Fb.ca();function O(){I.call(this)}w(O,I);O.prototype.ka=!0;O.prototype.ia=function(){};O.prototype.addEventListener=function(a,b,c,d){rb(this,a,b,c,d)};O.prototype.removeEventListener=function(a,b,c,d){ub(this,a,b,c,d)};function P(a){I.call(this);this.u=a||ab()}w(P,O);g=P.prototype;g.Na=Fb.ca();g.pa=null;g.p=!1;g.e=null;g.f=null;g.L=null;g.s=null;g.aa=null;g.na=function(){return this.e};g.I=function(a){return this.e?this.u.I(a,this.e):null};g.ia=function(a){if(this.L&&this.L!=a)throw Error("Method not supported");P.w.ia.call(this,a)};g.ba=function(){return this.u};g.g=function(){this.e=this.u.createElement("div")};
g.Aa=function(a){if(this.p)throw Error("Component already rendered");this.e||this.g();a?a.insertBefore(this.e,null):this.u.t.body.appendChild(this.e);this.L&&!this.L.p||this.v()};g.Ea=function(a){if(this.p)throw Error("Component already rendered");if(a)this.u&&this.u.t==cb(a)||(this.u=ab(a)),this.O(a),this.v();else throw Error("Invalid element to decorate");};g.O=function(a){this.e=a};g.v=function(){this.p=!0;Gb(this,function(a){!a.p&&a.na()&&a.v()})};
g.H=function(){Gb(this,function(a){a.p&&a.H()});this.J&&Eb(this.J);this.p=!1};function Gb(a,b){a.s&&Na(a.s,b,void 0)}
g.removeChild=function(a,b){if(a){var c=u(a)?a:a.pa||(a.pa=":"+(a.Na.Qa++).toString(36)),d;this.aa&&c?(d=this.aa,d=(c in d?d[c]:void 0)||null):d=null;a=d;if(c&&a){d=this.aa;c in d&&delete d[c];Ra(this.s,a);b&&(a.H(),a.e&&(c=a.e)&&c.parentNode&&c.parentNode.removeChild(c));c=a;if(null==c)throw Error("Unable to set parent component");c.L=null;P.w.ia.call(c,null)}}if(!a)throw Error("Child is not in parent component");return a};
g.Y=function(a){for(var b=[];this.s&&0!=this.s.length;)b.push(this.removeChild(this.s?this.s[0]||null:null,a));return b};var Hb=RegExp("^(?:([^:/?#.]+):)?(?://(?:([^/?#]*)@)?([^/#?]*?)(?::([0-9]+))?(?=[/#?]|$))?([^?#]+)?(?:\\?([^#]*))?(?:#(.*))?$");function Ib(a){if("function"==typeof a.k)return a.k();if(u(a))return a.split("");if(t(a)){for(var b=[],c=a.length,d=0;d<c;d++)b.push(a[d]);return b}return Ha(a)}function Jb(a,b,c){if("function"==typeof a.forEach)a.forEach(b,c);else if(t(a)||u(a))Na(a,b,c);else{var d;if("function"==typeof a.A)d=a.A();else if("function"!=typeof a.k)if(t(a)||u(a)){d=[];for(var e=a.length,f=0;f<e;f++)d.push(f)}else d=Ia(a);else d=void 0;for(var e=Ib(a),f=e.length,h=0;h<f;h++)b.call(c,e[h],d&&d[h],a)}};function Kb(a,b){this.m={};this.c=[];var c=arguments.length;if(1<c){if(c%2)throw Error("Uneven number of arguments");for(var d=0;d<c;d+=2)this.set(arguments[d],arguments[d+1])}else if(a){a instanceof Kb?(c=a.A(),d=a.k()):(c=Ia(a),d=Ha(a));for(var e=0;e<c.length;e++)this.set(c[e],d[e])}}g=Kb.prototype;g.a=0;g.k=function(){Lb(this);for(var a=[],b=0;b<this.c.length;b++)a.push(this.m[this.c[b]]);return a};g.A=function(){Lb(this);return this.c.concat()};g.F=function(a){return Q(this.m,a)};
g.remove=function(a){return Q(this.m,a)?(delete this.m[a],this.a--,this.c.length>2*this.a&&Lb(this),!0):!1};function Lb(a){if(a.a!=a.c.length){for(var b=0,c=0;b<a.c.length;){var d=a.c[b];Q(a.m,d)&&(a.c[c++]=d);b++}a.c.length=c}if(a.a!=a.c.length){for(var e={},c=b=0;b<a.c.length;)d=a.c[b],Q(e,d)||(a.c[c++]=d,e[d]=1),b++;a.c.length=c}}g.get=function(a,b){return Q(this.m,a)?this.m[a]:b};g.set=function(a,b){Q(this.m,a)||(this.a++,this.c.push(a));this.m[a]=b};g.D=function(){return new Kb(this)};
function Q(a,b){return Object.prototype.hasOwnProperty.call(a,b)};function R(a,b){var c;if(a instanceof R)this.i=void 0!==b?b:a.i,Mb(this,a.C),c=a.Z,S(this),this.Z=c,c=a.G,S(this),this.G=c,Nb(this,a.W),c=a.U,S(this),this.U=c,Ob(this,a.n.D()),c=a.Q,S(this),this.Q=c;else if(a&&(c=String(a).match(Hb))){this.i=!!b;Mb(this,c[1]||"",!0);var d=c[2]||"";S(this);this.Z=d?decodeURIComponent(d):"";d=c[3]||"";S(this);this.G=d?decodeURIComponent(d):"";Nb(this,c[4]);d=c[5]||"";S(this);this.U=d?decodeURIComponent(d):"";Ob(this,c[6]||"",!0);c=c[7]||"";S(this);this.Q=c?decodeURIComponent(c):
""}else this.i=!!b,this.n=new T(null,0,this.i)}g=R.prototype;g.C="";g.Z="";g.G="";g.W=null;g.U="";g.Q="";g.Oa=!1;g.i=!1;g.toString=function(){var a=[],b=this.C;b&&a.push(U(b,Pb),":");if(b=this.G){a.push("//");var c=this.Z;c&&a.push(U(c,Pb),"@");a.push(encodeURIComponent(String(b)));b=this.W;null!=b&&a.push(":",String(b))}if(b=this.U)this.G&&"/"!=b.charAt(0)&&a.push("/"),a.push(U(b,"/"==b.charAt(0)?Qb:Rb));(b=this.n.toString())&&a.push("?",b);(b=this.Q)&&a.push("#",U(b,Sb));return a.join("")};
g.D=function(){return new R(this)};function Mb(a,b,c){S(a);a.C=c?b?decodeURIComponent(b):"":b;a.C&&(a.C=a.C.replace(/:$/,""))}function Nb(a,b){S(a);if(b){b=Number(b);if(isNaN(b)||0>b)throw Error("Bad port number "+b);a.W=b}else a.W=null}function Ob(a,b,c){S(a);b instanceof T?(a.n=b,a.n.ha(a.i)):(c||(b=U(b,Tb)),a.n=new T(b,0,a.i))}function S(a){if(a.Oa)throw Error("Tried to modify a read-only Uri");}g.ha=function(a){this.i=a;this.n&&this.n.ha(a);return this};
function U(a,b){return u(a)?encodeURI(a).replace(b,Ub):null}function Ub(a){a=a.charCodeAt(0);return"%"+(a>>4&15).toString(16)+(a&15).toString(16)}var Pb=/[#\/\?@]/g,Rb=/[\#\?:]/g,Qb=/[\#\?]/g,Tb=/[\#\?@]/g,Sb=/#/g;function T(a,b,c){this.h=a||null;this.i=!!c}
function V(a){if(!a.b&&(a.b=new Kb,a.a=0,a.h))for(var b=a.h.split("&"),c=0;c<b.length;c++){var d=b[c].indexOf("="),e=null,f=null;0<=d?(e=b[c].substring(0,d),f=b[c].substring(d+1)):e=b[c];e=decodeURIComponent(e.replace(/\+/g," "));e=W(a,e);a.add(e,f?decodeURIComponent(f.replace(/\+/g," ")):"")}}g=T.prototype;g.b=null;g.a=null;g.add=function(a,b){V(this);this.h=null;a=W(this,a);var c=this.b.get(a);c||this.b.set(a,c=[]);c.push(b);this.a++;return this};
g.remove=function(a){V(this);a=W(this,a);return this.b.F(a)?(this.h=null,this.a-=this.b.get(a).length,this.b.remove(a)):!1};g.F=function(a){V(this);a=W(this,a);return this.b.F(a)};g.A=function(){V(this);for(var a=this.b.k(),b=this.b.A(),c=[],d=0;d<b.length;d++)for(var e=a[d],f=0;f<e.length;f++)c.push(b[d]);return c};g.k=function(a){V(this);var b=[];if(a)this.F(a)&&(b=Sa(b,this.b.get(W(this,a))));else{a=this.b.k();for(var c=0;c<a.length;c++)b=Sa(b,a[c])}return b};
g.set=function(a,b){V(this);this.h=null;a=W(this,a);this.F(a)&&(this.a-=this.b.get(a).length);this.b.set(a,[b]);this.a++;return this};g.get=function(a,b){var c=a?this.k(a):[];return 0<c.length?String(c[0]):b};g.toString=function(){if(this.h)return this.h;if(!this.b)return"";for(var a=[],b=this.b.A(),c=0;c<b.length;c++)for(var d=b[c],e=encodeURIComponent(String(d)),d=this.k(d),f=0;f<d.length;f++){var h=e;""!==d[f]&&(h+="="+encodeURIComponent(String(d[f])));a.push(h)}return this.h=a.join("&")};
g.D=function(){var a=new T;a.h=this.h;this.b&&(a.b=this.b.D(),a.a=this.a);return a};function W(a,b){var c=String(b);a.i&&(c=c.toLowerCase());return c}g.ha=function(a){a&&!this.i&&(V(this),this.h=null,Jb(this.b,function(a,c){var d=c.toLowerCase();c!=d&&(this.remove(c),this.remove(d),0<a.length&&(this.h=null,this.b.set(W(this,d),Ta(a)),this.a+=a.length))},this));this.i=a};function Vb(){}g=Vb.prototype;g.name=null;g.sa=null;g.xa=null;g.$=null;g.ga=null;function Wb(a){var b=new Vb;b.name=a.user_name;b.sa=a.is_admin;b.xa=a.user_pic;b.ga=a.score;b.$=a.answered;return b};function X(){I.call(this);this.j=[];this.M={}}w(X,I);X.prototype.ua=1;X.prototype.X=0;function Xb(a,b,c,d){var e=a.M[b];e||(e=a.M[b]=[]);var f=a.ua;a.j[f]=b;a.j[f+1]=c;a.j[f+2]=d;a.ua=f+3;e.push(f)}function Yb(a){var b=a.M[void 0];if(b){var c=a.j;(b=Qa(b,function(a){return void 0==c[a+1]&&void 0==c[a+2]}))&&Zb(a,b)}}function Zb(a,b){if(0!=a.X)a.V||(a.V=[]),a.V.push(b);else{var c=a.j[b];c&&((c=a.M[c])&&Ra(c,b),delete a.j[b],delete a.j[b+1],delete a.j[b+2])}}
X.prototype.za=function(a,b){var c=this.M[a];if(c){this.X++;for(var d=Ua(arguments,1),e=0,f=c.length;e<f;e++){var h=c[e];this.j[h+1].apply(this.j[h+2],d)}this.X--;if(this.V&&0==this.X)for(;c=this.V.pop();)Zb(this,c)}};function $b(){this.r="pending";this.B=[];this.la=this.ja=void 0}function ac(){F.call(this,"Multiple attempts to set the state of this Result")}w(ac,F);$b.prototype.getError=function(){return this.la};function bc(a,b){if("pending"==a.r)for(a.ja=b,a.r="success";a.B.length;)a.B.shift()(a);else throw new ac;}function cc(a,b){if("pending"==a.r)for(a.la=b,a.r="error";a.B.length;)a.B.shift()(a);else throw new ac;};function dc(a,b,c){b=c?ga(b,c):b;"pending"==a.r?a.B.push(b):b(a)}function ec(a,b){dc(a,function(a){"error"==a.r&&b.call(this,a)},void 0)}function fc(a,b){var c=new gc;dc(a,function(a){"success"==a.r?bc(c,b(a.ja)):cc(c,a.getError())});return c}function gc(){$b.call(this)}w(gc,$b);function hc(a){a=String(a);if(/^\s*$/.test(a)?0:/^[\],:{}\s\u2028\u2029]*$/.test(a.replace(/\\["\\\/bfnrtu]/g,"@").replace(/"[^"\\\n\r\u2028\u2029\x00-\x08\x0a-\x1f]*"|true|false|null|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?/g,"]").replace(/(?:^|:|,)(?:[\s\u2028\u2029]*\[)+/g,"")))try{return eval("("+a+")")}catch(b){}throw Error("Invalid JSON string: "+a);};function ic(){};var jc;function kc(){}w(kc,ic);function lc(){var a;a:{var b=jc;if(!b.qa&&"undefined"==typeof XMLHttpRequest&&"undefined"!=typeof ActiveXObject){for(var c=["MSXML2.XMLHTTP.6.0","MSXML2.XMLHTTP.3.0","MSXML2.XMLHTTP","Microsoft.XMLHTTP"],d=0;d<c.length;d++){var e=c[d];try{new ActiveXObject(e);a=b.qa=e;break a}catch(f){}}throw Error("Could not create ActiveXObject. ActiveX might be disabled, or MSXML might not be installed");}a=b.qa}return a?new ActiveXObject(a):new XMLHttpRequest}jc=new kc;function mc(a,b){var c=nc(a,b),d=c=fc(c,oc);b&&b.Ua&&(d=fc(c,ha(pc,b.Ua)));return fc(d,hc)}function nc(a,b){var c=new $b;ec(c,function(){});qc(a,b,function(a){bc(c,a)},function(a){cc(c,a)});return c}
function qc(a,b,c,d){b=b||{};var e=c||p,f=d||p,h,k=lc();try{k.open("GET",a,!0)}catch(l){f(new Y("Error opening XHR: "+l.message,a));return}k.onreadystatechange=function(){if(4==k.readyState){window.clearTimeout(h);var b;a:switch(k.status){case 200:case 201:case 202:case 204:case 206:case 304:case 1223:b=!0;break a;default:b=!1}!b&&(b=0===k.status)&&(b=a.match(Hb)[1]||null,!b&&self.location&&(b=self.location.protocol,b=b.substr(0,b.length-1)),b=b?b.toLowerCase():"",b=!("http"==b||"https"==b||""==b));
b?e(k):f(new rc(k.status,a))}};if(b.headers)for(var x in b.headers)k.setRequestHeader(x,b.headers[x]);b.withCredentials&&(k.withCredentials=b.withCredentials);b.Pa&&k.overrideMimeType(b.Pa);0<b.Ra&&(h=window.setTimeout(function(){k.onreadystatechange=p;k.abort();f(new sc(a))},b.Ra));try{k.send(null)}catch(m){k.onreadystatechange=p,window.clearTimeout(h),f(new Y("Error sending XHR: "+m.message,a))}}function oc(a){return a.responseText}
function pc(a,b){0==b.lastIndexOf(a,0)&&(b=b.substring(a.length));return b}function Y(a,b){F.call(this,a+", url="+b);this.url=b}w(Y,F);Y.prototype.name="XhrError";function rc(a,b){Y.call(this,"Request Failed, status="+a,b);this.status=a}w(rc,Y);rc.prototype.name="XhrHttpError";function sc(a){Y.call(this,"Request timed out",a)}w(sc,Y);sc.prototype.name="XhrTimeoutError";function tc(){}aa(tc);ia("ffc.api.Client.getInstance",tc.ca);tc.prototype.Ja=function(a,b){return mc.apply(null,arguments)};tc.prototype.Ia=function(a,b,c){a=ja(uc,a);a=a instanceof R?a.D():new R(a,void 0);b&&(S(a),a.n.set("offset",b));c&&(S(a),a.n.set("limit",c));return this.Ja(a)};var uc="/api/leaderboard/%s";function vc(a,b){X.call(this);this.id=a;this.page=0;this.da=wc;this.Ha=ga(b.Ia,b,a)}w(vc,X);ia("ffc.leaderboard.LeaderBoardModel",vc);vc.prototype.getData=function(){var a=this.Ha(this.page*this.da,this.da),b=this.La.bind(this);"pending"==a.r?a.B.push(b):b(a)};vc.prototype.La=function(a){a=a.ja;this.Sa=a.count;this.za(xc);this.Ta=Pa(a.users,Wb);this.za(yc)};var wc=20,yc="usersUpdated",xc="totalUpdated";var zc={};A&&E(8);function Ac(a,b){var c;a:{c=(new bb(void 0)||ab()).createElement("DIV");var d;d=a(b||zc,void 0,void 0);ba(d)?(Ma("Soy template output is unsafe for use as HTML: "+d),d="zSoyz"):d=String(d);c.innerHTML=d;if(1==c.childNodes.length&&(d=c.firstChild,1==d.nodeType)){c=d;break a}}return c}
var Bc={"\x00":"&#0;",'"':"&quot;","&":"&amp;","'":"&#39;","<":"&lt;",">":"&gt;","\t":"&#9;","\n":"&#10;","\x0B":"&#11;","\f":"&#12;","\r":"&#13;"," ":"&#32;","-":"&#45;","/":"&#47;","=":"&#61;","`":"&#96;","\u0085":"&#133;","\u00a0":"&#160;","\u2028":"&#8232;","\u2029":"&#8233;"};function Cc(a){return Bc[a]}var Dc=/[\x00\x22\x26\x27\x3c\x3e]/g;function Ec(){return'<table class="table table-striped table-hover"><thead><tr><th colspan="2">User</th><th class="leaderboard-score">Score</th><th class="leaderboard-answered">Answered</th><th class="leaderboard-average">Av. Score</th></tr></thead><tbody class="leaderboard-users"></tbody></table>'}function Fc(){return'<div class="leaderboard-pagination"><ul class="pagination pagination-sm"></ul></div>'}
function Gc(a){return"<li"+(a.Da?' class="active"':"")+'><a href="#">'+("object"===typeof a.K&&a.K&&0===a.K.Va?a.K.content:String(a.K).replace(Dc,Cc))+"</a></li>"};function Z(a){P.call(this);this.P=this.J||(this.J=new Ab(this));this.d=this.ba();this.f=a}w(Z,P);ia("ffc.leaderboard.LeaderBoard",Z);Z.prototype.render=Z.prototype.Aa;g=Z.prototype;g.g=function(){var a=this.d.g("DIV");this.d.append(a,Ac(Ec));this.d.append(a,Ac(Fc));this.O(a)};g.O=function(a){Z.w.O.call(this,a);this.Ba=this.I("leaderboard-users");this.ea=this.I("pagination")};
g.v=function(){Z.w.v.call(this);Xb(this.f,xc,this.Ga,this);Xb(this.f,yc,this.Fa,this);Cb(this.P,this.ea,this.Ka,this);this.f.getData();this.e.style.display="block"};g.H=function(){Z.w.H.call(this);Yb(this.f);Db(this.P);this.d.Y(this.e);this.e=null};
g.Fa=function(){this.d.Y(this.Ba);for(var a=[this.Ba],b=Oa(this.f.Ta,function(a){return!a.sa}),c=0,d=b.length;c<d;c++){var e=b[c];a.push(this.d.g("TR",null,this.d.g("TD",null,this.d.g("IMG",{src:e.xa,alt:e.name,width:20,height:20})),this.d.g("TD",null,this.d.g("A",{href:"/u/"+e.name},e.name)),this.d.g("TD","leaderboard-score",e.ga+""),this.d.g("TD","leaderboard-answered",e.$+""),this.d.g("TD","leaderboard-average",((e.ga/e.$).toFixed(1)||0)+"")))}this.d.append.apply(this.Ca,a)};
g.Ga=function(){this.d.Y(this.ea);var a=[this.ea],b;b=[];var c=Math.ceil(this.f.Sa/this.f.da);if(0>1*(c-0))b=[];else for(var d=0;d<c;d+=1)b.push(d);c=0;for(d=b.length;c<d;c++)a.push(Ac(Gc,{K:b[c],Da:c==this.f.page}));this.d.append.apply(this.Ca,a)};g.Ka=function(a){a.preventDefault();"A"==a.target.nodeName&&(a=parseInt(a.target.innerHTML,10),a!=this.f.page&&(this.f.page=a,this.f.getData()))};function $(a){P.call(this);this.P=this.J||(this.J=new Ab(this));this.d=this.ba();this.va=a}w($,P);ia("ffc.leaderboard.LeaderBoardToggler",$);$.prototype.decorate=$.prototype.Ea;$.prototype.v=function(){$.w.v.call(this);Cb(this.P,this.e,this.Ma,this)};
$.prototype.Ma=function(a){a.preventDefault();var b=jb(a.target),c;if(c="A"==a.target.nodeName)if(c=b)c=Wa(b),c=!(0<=H(c,"active"));if(c)for(a=a.target,a=a.dataset?a.dataset.leaderboard:a.getAttribute("data-"+"leaderboard".replace(/([A-Z])/g,"-$1").toLowerCase()),Ya(this.d.I("active",this.e),"active"),Xa(b,"active"),b=0,c=this.va.length;b<c;b++){var d=this.va[b];d.f.id==a?d.Aa(document.getElementById("leaderboard-container-"+a)):d.p&&d.H()}};})();
