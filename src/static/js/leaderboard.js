(function() {function aa(a){return function(){return this[a]}}var g,n=this;function p(){}function ba(a){a.da=function(){return a.sa?a.sa:a.sa=new a}}
function q(a){var b=typeof a;if("object"==b)if(a){if(a instanceof Array)return"array";if(a instanceof Object)return b;var c=Object.prototype.toString.call(a);if("[object Window]"==c)return"object";if("[object Array]"==c||"number"==typeof a.length&&"undefined"!=typeof a.splice&&"undefined"!=typeof a.propertyIsEnumerable&&!a.propertyIsEnumerable("splice"))return"array";if("[object Function]"==c||"undefined"!=typeof a.call&&"undefined"!=typeof a.propertyIsEnumerable&&!a.propertyIsEnumerable("call"))return"function"}else return"null";
else if("function"==b&&"undefined"==typeof a.call)return"object";return b}function s(a){return"array"==q(a)}function ca(a){var b=q(a);return"array"==b||"object"==b&&"number"==typeof a.length}function t(a){return"string"==typeof a}function da(a){var b=typeof a;return"object"==b&&null!=a||"function"==b}function u(a){return a[ea]||(a[ea]=++fa)}var ea="closure_uid_"+(1E9*Math.random()>>>0),fa=0;function ga(a,b,c){return a.call.apply(a.bind,arguments)}
function ha(a,b,c){if(!a)throw Error();if(2<arguments.length){var d=Array.prototype.slice.call(arguments,2);return function(){var c=Array.prototype.slice.call(arguments);Array.prototype.unshift.apply(c,d);return a.apply(b,c)}}return function(){return a.apply(b,arguments)}}function ia(a,b,c){ia=Function.prototype.bind&&-1!=Function.prototype.bind.toString().indexOf("native code")?ga:ha;return ia.apply(null,arguments)}
function ja(a,b){var c=Array.prototype.slice.call(arguments,1);return function(){var b=Array.prototype.slice.call(arguments);b.unshift.apply(b,c);return a.apply(this,b)}}function ka(a,b){var c=a.split("."),d=n;c[0]in d||!d.execScript||d.execScript("var "+c[0]);for(var e;c.length&&(e=c.shift());)c.length||void 0===b?d=d[e]?d[e]:d[e]={}:d[e]=b}function v(a,b){function c(){}c.prototype=b.prototype;a.w=b.prototype;a.prototype=new c};function la(a,b){for(var c=1;c<arguments.length;c++){var d=String(arguments[c]).replace(/\$/g,"$$$$");a=a.replace(/\%s/,d)}return a}function ma(a){if(!na.test(a))return a;-1!=a.indexOf("&")&&(a=a.replace(oa,"&amp;"));-1!=a.indexOf("<")&&(a=a.replace(pa,"&lt;"));-1!=a.indexOf(">")&&(a=a.replace(qa,"&gt;"));-1!=a.indexOf('"')&&(a=a.replace(ra,"&quot;"));return a}var oa=/&/g,pa=/</g,qa=/>/g,ra=/\"/g,na=/[&<>\"]/;var w,sa,ta,ua;function va(){return n.navigator?n.navigator.userAgent:null}ua=ta=sa=w=!1;var wa;if(wa=va()){var xa=n.navigator;w=0==wa.indexOf("Opera");sa=!w&&-1!=wa.indexOf("MSIE");ta=!w&&-1!=wa.indexOf("WebKit");ua=!w&&!ta&&"Gecko"==xa.product}var ya=w,y=sa,A=ua,B=ta;function za(){var a=n.document;return a?a.documentMode:void 0}var Aa;
a:{var Ba="",C;if(ya&&n.opera)var Ca=n.opera.version,Ba="function"==typeof Ca?Ca():Ca;else if(A?C=/rv\:([^\);]+)(\)|;)/:y?C=/MSIE\s+([^\);]+)(\)|;)/:B&&(C=/WebKit\/(\S+)/),C)var Da=C.exec(va()),Ba=Da?Da[1]:"";if(y){var Ea=za();if(Ea>parseFloat(Ba)){Aa=String(Ea);break a}}Aa=Ba}var Fa={};
function D(a){var b;if(!(b=Fa[a])){b=0;for(var c=String(Aa).replace(/^[\s\xa0]+|[\s\xa0]+$/g,"").split("."),d=String(a).replace(/^[\s\xa0]+|[\s\xa0]+$/g,"").split("."),e=Math.max(c.length,d.length),f=0;0==b&&f<e;f++){var h=c[f]||"",k=d[f]||"",l=RegExp("(\\d*)(\\D*)","g"),x=RegExp("(\\d*)(\\D*)","g");do{var m=l.exec(h)||["","",""],r=x.exec(k)||["","",""];if(0==m[0].length&&0==r[0].length)break;b=((0==m[1].length?0:parseInt(m[1],10))<(0==r[1].length?0:parseInt(r[1],10))?-1:(0==m[1].length?0:parseInt(m[1],
10))>(0==r[1].length?0:parseInt(r[1],10))?1:0)||((0==m[2].length)<(0==r[2].length)?-1:(0==m[2].length)>(0==r[2].length)?1:0)||(m[2]<r[2]?-1:m[2]>r[2]?1:0)}while(0==b)}b=Fa[a]=0<=b}return b}var Ga=n.document,Ha=Ga&&y?za()||("CSS1Compat"==Ga.compatMode?parseInt(Aa,10):5):void 0;function Ia(a,b){for(var c in a)b.call(void 0,a[c],c,a)}function Ja(a){var b=[],c=0,d;for(d in a)b[c++]=a[d];return b}function Ka(a){var b=[],c=0,d;for(d in a)b[c++]=d;return b}var La="constructor hasOwnProperty isPrototypeOf propertyIsEnumerable toLocaleString toString valueOf".split(" ");function Ma(a,b){for(var c,d,e=1;e<arguments.length;e++){d=arguments[e];for(c in d)a[c]=d[c];for(var f=0;f<La.length;f++)c=La[f],Object.prototype.hasOwnProperty.call(d,c)&&(a[c]=d[c])}};function E(a){Error.captureStackTrace?Error.captureStackTrace(this,E):this.stack=Error().stack||"";a&&(this.message=String(a))}v(E,Error);E.prototype.name="CustomError";function Na(a,b){b.unshift(a);E.call(this,la.apply(null,b));b.shift()}v(Na,E);Na.prototype.name="AssertionError";function Oa(a,b){throw new Na("Failure"+(a?": "+a:""),Array.prototype.slice.call(arguments,1));};var F=Array.prototype,G=F.indexOf?function(a,b,c){return F.indexOf.call(a,b,c)}:function(a,b,c){c=null==c?0:0>c?Math.max(0,a.length+c):c;if(t(a))return t(b)&&1==b.length?a.indexOf(b,c):-1;for(;c<a.length;c++)if(c in a&&a[c]===b)return c;return-1},Pa=F.forEach?function(a,b,c){F.forEach.call(a,b,c)}:function(a,b,c){for(var d=a.length,e=t(a)?a.split(""):a,f=0;f<d;f++)f in e&&b.call(c,e[f],f,a)},Qa=F.filter?function(a,b,c){return F.filter.call(a,b,c)}:function(a,b,c){for(var d=a.length,e=[],f=0,h=t(a)?
a.split(""):a,k=0;k<d;k++)if(k in h){var l=h[k];b.call(c,l,k,a)&&(e[f++]=l)}return e},Ra=F.map?function(a,b,c){return F.map.call(a,b,c)}:function(a,b,c){for(var d=a.length,e=Array(d),f=t(a)?a.split(""):a,h=0;h<d;h++)h in f&&(e[h]=b.call(c,f[h],h,a));return e};function Sa(a,b){var c;a:{c=a.length;for(var d=t(a)?a.split(""):a,e=0;e<c;e++)if(e in d&&b.call(void 0,d[e],e,a)){c=e;break a}c=-1}return 0>c?null:t(a)?a.charAt(c):a[c]}function Ta(a,b){var c=G(a,b);0<=c&&F.splice.call(a,c,1)}
function Ua(a){return F.concat.apply(F,arguments)}function Va(a){var b=a.length;if(0<b){for(var c=Array(b),d=0;d<b;d++)c[d]=a[d];return c}return[]}function Wa(a,b,c){return 2>=arguments.length?F.slice.call(a,b):F.slice.call(a,b,c)};var Xa;function Ya(a){a=a.className;return t(a)&&a.match(/\S+/g)||[]}function Za(a,b){for(var c=Ya(a),d=Wa(arguments,1),e=c.length+d.length,f=c,h=0;h<d.length;h++)0<=G(f,d[h])||f.push(d[h]);a.className=c.join(" ");return c.length==e}function $a(a,b){var c=Ya(a),d=Wa(arguments,1),c=ab(c,d);a.className=c.join(" ")}function ab(a,b){return Qa(a,function(a){return!(0<=G(b,a))})};var bb=!y||y&&9<=Ha;!A&&!y||y&&y&&9<=Ha||A&&D("1.9.1");y&&D("9");function cb(a){return a?new db(eb(a)):Xa||(Xa=new db)}function fb(a,b){var c,d,e,f;c=document;c=b||c;if(c.querySelectorAll&&c.querySelector&&a)return c.querySelectorAll(""+(a?"."+a:""));if(a&&c.getElementsByClassName){var h=c.getElementsByClassName(a);return h}h=c.getElementsByTagName("*");if(a){f={};for(d=e=0;c=h[d];d++){var k=c.className;"function"==typeof k.split&&0<=G(k.split(/\s+/),a)&&(f[e++]=c)}f.length=e;return f}return h}
function gb(a,b){Ia(b,function(b,d){"style"==d?a.style.cssText=b:"class"==d?a.className=b:"for"==d?a.htmlFor=b:d in hb?a.setAttribute(hb[d],b):0==d.lastIndexOf("aria-",0)||0==d.lastIndexOf("data-",0)?a.setAttribute(d,b):a[d]=b})}var hb={cellpadding:"cellPadding",cellspacing:"cellSpacing",colspan:"colSpan",frameborder:"frameBorder",height:"height",maxlength:"maxLength",role:"role",rowspan:"rowSpan",type:"type",usemap:"useMap",valign:"vAlign",width:"width"};
function ib(a,b,c,d){function e(c){c&&b.appendChild(t(c)?a.createTextNode(c):c)}for(;d<c.length;d++){var f=c[d];!ca(f)||da(f)&&0<f.nodeType?e(f):Pa(jb(f)?Va(f):f,e)}}function eb(a){return 9==a.nodeType?a:a.ownerDocument||a.document}function jb(a){if(a&&"number"==typeof a.length){if(da(a))return"function"==typeof a.item||"string"==typeof a.item;if("function"==q(a))return"function"==typeof a.item}return!1}function kb(a,b){for(var c=0;a;){if(b(a))return a;a=a.parentNode;c++}return null}
function db(a){this.s=a||n.document||document}g=db.prototype;g.ca=cb;g.oa=function(a){return t(a)?this.s.getElementById(a):a};g.J=function(a,b){var c=b||this.s,d=c||document;d.querySelectorAll&&d.querySelector?c=d.querySelector("."+a):(d=c||document,c=(d.querySelectorAll&&d.querySelector?d.querySelectorAll("."+a):d.getElementsByClassName?d.getElementsByClassName(a):fb(a,c))[0]);return c||null};
g.i=function(a,b,c){var d=this.s,e=arguments,f=e[0],h=e[1];if(!bb&&h&&(h.name||h.type)){f=["<",f];h.name&&f.push(' name="',ma(h.name),'"');if(h.type){f.push(' type="',ma(h.type),'"');var k={};Ma(k,h);delete k.type;h=k}f.push(">");f=f.join("")}f=d.createElement(f);h&&(t(h)?f.className=h:s(h)?Za.apply(null,[f].concat(h)):gb(f,h));2<e.length&&ib(d,f,e,2);return f};g.createElement=function(a){return this.s.createElement(a)};g.createTextNode=function(a){return this.s.createTextNode(String(a))};
g.appendChild=function(a,b){a.appendChild(b)};g.append=function(a,b){ib(eb(a),a,arguments,1)};g.Z=function(a){for(var b;b=a.firstChild;)a.removeChild(b)};function lb(a){return kb(a,function(a){return"LI"==a.nodeName&&!0})};function H(){0!=mb&&u(this)}var mb=0;function I(a,b){this.type=a;this.currentTarget=this.target=b}I.prototype.ga=!1;I.prototype.defaultPrevented=!1;I.prototype.preventDefault=function(){this.defaultPrevented=!0};var nb=0;function ob(){}g=ob.prototype;g.key=0;g.p=!1;g.O=!1;g.T=function(a,b,c,d,e,f){if("function"==q(a))this.ta=!0;else if(a&&a.handleEvent&&"function"==q(a.handleEvent))this.ta=!1;else throw Error("Invalid listener argument");this.l=a;this.ya=b;this.src=c;this.type=d;this.capture=!!e;this.S=f;this.O=!1;this.key=++nb;this.p=!1};g.handleEvent=function(a){return this.ta?this.l.call(this.S||this.src,a):this.l.handleEvent.call(this.l,a)};var pb=!y||y&&9<=Ha,qb=y&&!D("9");!B||D("528");A&&D("1.9b")||y&&D("8")||ya&&D("9.5")||B&&D("528");A&&!D("8")||y&&D("9");function rb(a){rb[" "](a);return a}rb[" "]=p;function J(a,b){a&&this.T(a,b)}v(J,I);g=J.prototype;g.target=null;g.relatedTarget=null;g.offsetX=0;g.offsetY=0;g.clientX=0;g.clientY=0;g.screenX=0;g.screenY=0;g.button=0;g.keyCode=0;g.charCode=0;g.ctrlKey=!1;g.altKey=!1;g.shiftKey=!1;g.metaKey=!1;g.na=null;
g.T=function(a,b){var c=this.type=a.type;I.call(this,c);this.target=a.target||a.srcElement;this.currentTarget=b;var d=a.relatedTarget;if(d){if(A){var e;a:{try{rb(d.nodeName);e=!0;break a}catch(f){}e=!1}e||(d=null)}}else"mouseover"==c?d=a.fromElement:"mouseout"==c&&(d=a.toElement);this.relatedTarget=d;this.offsetX=B||void 0!==a.offsetX?a.offsetX:a.layerX;this.offsetY=B||void 0!==a.offsetY?a.offsetY:a.layerY;this.clientX=void 0!==a.clientX?a.clientX:a.pageX;this.clientY=void 0!==a.clientY?a.clientY:
a.pageY;this.screenX=a.screenX||0;this.screenY=a.screenY||0;this.button=a.button;this.keyCode=a.keyCode||0;this.charCode=a.charCode||("keypress"==c?a.keyCode:0);this.ctrlKey=a.ctrlKey;this.altKey=a.altKey;this.shiftKey=a.shiftKey;this.metaKey=a.metaKey;this.state=a.state;this.na=a;a.defaultPrevented&&this.preventDefault();delete this.ga};
g.preventDefault=function(){J.w.preventDefault.call(this);var a=this.na;if(a.preventDefault)a.preventDefault();else if(a.returnValue=!1,qb)try{if(a.ctrlKey||112<=a.keyCode&&123>=a.keyCode)a.keyCode=-1}catch(b){}};var sb={},K={},L={},M={};
function tb(a,b,c,d,e){if(s(b)){for(var f=0;f<b.length;f++)tb(a,b[f],c,d,e);return null}a:{if(!b)throw Error("Invalid event type");d=!!d;var h=K;b in h||(h[b]={a:0,o:0});h=h[b];d in h||(h[d]={a:0,o:0},h.a++);var h=h[d],f=u(a),k;h.o++;if(h[f]){k=h[f];for(var l=0;l<k.length;l++)if(h=k[l],h.l==c&&h.S==e){if(h.p)break;k[l].O=!1;a=k[l];break a}}else k=h[f]=[],h.a++;l=ub();h=new ob;h.T(c,l,a,b,d,e);h.O=!1;l.src=a;l.l=h;k.push(h);L[f]||(L[f]=[]);L[f].push(h);a.addEventListener?a!=n&&a.la||a.addEventListener(b,
l,d):a.attachEvent(b in M?M[b]:M[b]="on"+b,l);a=h}b=a.key;sb[b]=a;return b}function ub(){var a=vb,b=pb?function(c){return a.call(b.src,b.l,c)}:function(c){c=a.call(b.src,b.l,c);if(!c)return c};return b}function wb(a,b,c,d,e){if(s(b))for(var f=0;f<b.length;f++)wb(a,b[f],c,d,e);else if(d=!!d,a=xb(a,b,d))for(f=0;f<a.length;f++)if(a[f].l==c&&a[f].capture==d&&a[f].S==e){yb(a[f].key);break}}
function yb(a){var b=sb[a];if(!b||b.p)return!1;var c=b.src,d=b.type,e=b.ya,f=b.capture;c.removeEventListener?c!=n&&c.la||c.removeEventListener(d,e,f):c.detachEvent&&c.detachEvent(d in M?M[d]:M[d]="on"+d,e);c=u(c);L[c]&&(e=L[c],Ta(e,b),0==e.length&&delete L[c]);b.p=!0;if(b=K[d][f][c])b.wa=!0,zb(d,f,c,b);delete sb[a];return!0}
function zb(a,b,c,d){if(!d.U&&d.wa){for(var e=0,f=0;e<d.length;e++)d[e].p?d[e].ya.src=null:(e!=f&&(d[f]=d[e]),f++);d.length=f;d.wa=!1;0==f&&(delete K[a][b][c],K[a][b].a--,0==K[a][b].a&&(delete K[a][b],K[a].a--),0==K[a].a&&delete K[a])}}function xb(a,b,c){var d=K;return b in d&&(d=d[b],c in d&&(d=d[c],a=u(a),d[a]))?d[a]:null}
function Ab(a,b,c,d,e){var f=1;b=u(b);if(a[b]){var h=--a.o,k=a[b];k.U?k.U++:k.U=1;try{for(var l=k.length,x=0;x<l;x++){var m=k[x];m&&!m.p&&(f&=!1!==Bb(m,e))}}finally{a.o=Math.max(h,a.o),k.U--,zb(c,d,b,k)}}return Boolean(f)}function Bb(a,b){a.O&&yb(a.key);return a.handleEvent(b)}
function vb(a,b){if(a.p)return!0;var c=a.type,d=K;if(!(c in d))return!0;var d=d[c],e,f;if(!pb){var h;if(!(h=b))a:{h=["window","event"];for(var k=n;e=h.shift();)if(null!=k[e])k=k[e];else{h=null;break a}h=k}e=h;h=!0 in d;k=!1 in d;if(h){if(0>e.keyCode||void 0!=e.returnValue)return!0;a:{var l=!1;if(0==e.keyCode)try{e.keyCode=-1;break a}catch(x){l=!0}if(l||void 0==e.returnValue)e.returnValue=!0}}l=new J;l.T(e,this);e=!0;try{if(h){for(var m=[],r=l.currentTarget;r;r=r.parentNode)m.push(r);f=d[!0];f.o=f.a;
for(var z=m.length-1;!l.ga&&0<=z&&f.o;z--)l.currentTarget=m[z],e&=Ab(f,m[z],c,!0,l);if(k)for(f=d[!1],f.o=f.a,z=0;!l.ga&&z<m.length&&f.o;z++)l.currentTarget=m[z],e&=Ab(f,m[z],c,!1,l)}else e=Bb(a,l)}finally{m&&(m.length=0)}return e}c=new J(b,this);return e=Bb(a,c)};function Cb(a){H.call(this);this.pa=a;this.c=[]}v(Cb,H);var Db=[];function Eb(a,b,c,d){var e="click";s(e)||(Db[0]=e,e=Db);for(var f=0;f<e.length;f++){var h=tb(b,e[f],c||a,!0,d||a.pa||a);a.c.push(h)}}function Fb(a,b,c,d,e,f){if(s(c))for(var h=0;h<c.length;h++)Fb(a,b,c[h],d,e,f);else{a:{d=d||a;f=f||a.pa||a;e=!!e;if(b=xb(b,c,e))for(c=0;c<b.length;c++)if(!b[c].p&&b[c].l==d&&b[c].capture==e&&b[c].S==f){b=b[c];break a}b=null}b&&(b=b.key,yb(b),Ta(a.c,b))}}function Gb(a){Pa(a.c,yb);a.c.length=0}
Cb.prototype.handleEvent=function(){throw Error("EventHandler.handleEvent not implemented");};function Hb(){}ba(Hb);Hb.prototype.Qa=0;Hb.da();function N(){H.call(this)}v(N,H);N.prototype.la=!0;N.prototype.ja=function(){};N.prototype.addEventListener=function(a,b,c,d){tb(this,a,b,c,d)};N.prototype.removeEventListener=function(a,b,c,d){wb(this,a,b,c,d)};function O(a){H.call(this);this.t=a||cb()}v(O,N);g=O.prototype;g.Na=Hb.da();g.qa=null;g.v=!1;g.e=null;g.f=null;g.M=null;g.r=null;g.ba=null;g.oa=aa("e");g.J=function(a){return this.e?this.t.J(a,this.e):null};g.ja=function(a){if(this.M&&this.M!=a)throw Error("Method not supported");O.w.ja.call(this,a)};g.ca=aa("t");g.i=function(){this.e=this.t.createElement("div")};
g.Aa=function(a){if(this.v)throw Error("Component already rendered");this.e||this.i();a?a.insertBefore(this.e,null):this.t.s.body.appendChild(this.e);this.M&&!this.M.v||this.u()};g.Ea=function(a){if(this.v)throw Error("Component already rendered");if(a)this.t&&this.t.s==eb(a)||(this.t=cb(a)),this.P(a),this.u();else throw Error("Invalid element to decorate");};g.P=function(a){this.e=a};g.u=function(){this.v=!0;Ib(this,function(a){!a.v&&a.oa()&&a.u()})};
g.I=function(){Ib(this,function(a){a.v&&a.I()});this.K&&Gb(this.K);this.v=!1};function Ib(a,b){a.r&&Pa(a.r,b,void 0)}
g.removeChild=function(a,b){if(a){var c=t(a)?a:a.qa||(a.qa=":"+(a.Na.Qa++).toString(36)),d;this.ba&&c?(d=this.ba,d=(c in d?d[c]:void 0)||null):d=null;a=d;if(c&&a){d=this.ba;c in d&&delete d[c];Ta(this.r,a);b&&(a.I(),a.e&&(c=a.e)&&c.parentNode&&c.parentNode.removeChild(c));c=a;if(null==c)throw Error("Unable to set parent component");c.M=null;O.w.ja.call(c,null)}}if(!a)throw Error("Child is not in parent component");return a};
g.Z=function(a){for(var b=[];this.r&&0!=this.r.length;)b.push(this.removeChild(this.r?this.r[0]||null:null,a));return b};var Jb=RegExp("^(?:([^:/?#.]+):)?(?://(?:([^/?#]*)@)?([^/#?]*?)(?::([0-9]+))?(?=[/#?]|$))?([^?#]+)?(?:\\?([^#]*))?(?:#(.*))?$");function Kb(a){if("function"==typeof a.k)return a.k();if(t(a))return a.split("");if(ca(a)){for(var b=[],c=a.length,d=0;d<c;d++)b.push(a[d]);return b}return Ja(a)}function Lb(a,b,c){if("function"==typeof a.forEach)a.forEach(b,c);else if(ca(a)||t(a))Pa(a,b,c);else{var d;if("function"==typeof a.B)d=a.B();else if("function"!=typeof a.k)if(ca(a)||t(a)){d=[];for(var e=a.length,f=0;f<e;f++)d.push(f)}else d=Ka(a);else d=void 0;for(var e=Kb(a),f=e.length,h=0;h<f;h++)b.call(c,e[h],d&&d[h],a)}};function Mb(a,b){this.m={};this.c=[];var c=arguments.length;if(1<c){if(c%2)throw Error("Uneven number of arguments");for(var d=0;d<c;d+=2)this.set(arguments[d],arguments[d+1])}else if(a){a instanceof Mb?(c=a.B(),d=a.k()):(c=Ka(a),d=Ja(a));for(var e=0;e<c.length;e++)this.set(c[e],d[e])}}g=Mb.prototype;g.a=0;g.k=function(){Nb(this);for(var a=[],b=0;b<this.c.length;b++)a.push(this.m[this.c[b]]);return a};g.B=function(){Nb(this);return this.c.concat()};g.G=function(a){return P(this.m,a)};
g.remove=function(a){return P(this.m,a)?(delete this.m[a],this.a--,this.c.length>2*this.a&&Nb(this),!0):!1};function Nb(a){if(a.a!=a.c.length){for(var b=0,c=0;b<a.c.length;){var d=a.c[b];P(a.m,d)&&(a.c[c++]=d);b++}a.c.length=c}if(a.a!=a.c.length){for(var e={},c=b=0;b<a.c.length;)d=a.c[b],P(e,d)||(a.c[c++]=d,e[d]=1),b++;a.c.length=c}}g.get=function(a,b){return P(this.m,a)?this.m[a]:b};g.set=function(a,b){P(this.m,a)||(this.a++,this.c.push(a));this.m[a]=b};g.F=function(){return new Mb(this)};
function P(a,b){return Object.prototype.hasOwnProperty.call(a,b)};function Q(a,b){var c;if(a instanceof Q)this.h=void 0!==b?b:a.h,Ob(this,a.D),c=a.$,R(this),this.$=c,c=a.H,R(this),this.H=c,Pb(this,a.X),c=a.V,R(this),this.V=c,Qb(this,a.n.F()),c=a.R,R(this),this.R=c;else if(a&&(c=String(a).match(Jb))){this.h=!!b;Ob(this,c[1]||"",!0);var d=c[2]||"";R(this);this.$=d?decodeURIComponent(d):"";d=c[3]||"";R(this);this.H=d?decodeURIComponent(d):"";Pb(this,c[4]);d=c[5]||"";R(this);this.V=d?decodeURIComponent(d):"";Qb(this,c[6]||"",!0);c=c[7]||"";R(this);this.R=c?decodeURIComponent(c):
""}else this.h=!!b,this.n=new S(null,0,this.h)}g=Q.prototype;g.D="";g.$="";g.H="";g.X=null;g.V="";g.R="";g.Oa=!1;g.h=!1;g.toString=function(){var a=[],b=this.D;b&&a.push(T(b,Rb),":");if(b=this.H){a.push("//");var c=this.$;c&&a.push(T(c,Rb),"@");a.push(encodeURIComponent(String(b)));b=this.X;null!=b&&a.push(":",String(b))}if(b=this.V)this.H&&"/"!=b.charAt(0)&&a.push("/"),a.push(T(b,"/"==b.charAt(0)?Sb:Tb));(b=this.n.toString())&&a.push("?",b);(b=this.R)&&a.push("#",T(b,Ub));return a.join("")};
g.F=function(){return new Q(this)};function Ob(a,b,c){R(a);a.D=c?b?decodeURIComponent(b):"":b;a.D&&(a.D=a.D.replace(/:$/,""))}function Pb(a,b){R(a);if(b){b=Number(b);if(isNaN(b)||0>b)throw Error("Bad port number "+b);a.X=b}else a.X=null}function Qb(a,b,c){R(a);b instanceof S?(a.n=b,a.n.ia(a.h)):(c||(b=T(b,Vb)),a.n=new S(b,0,a.h))}function R(a){if(a.Oa)throw Error("Tried to modify a read-only Uri");}g.ia=function(a){this.h=a;this.n&&this.n.ia(a);return this};
function T(a,b){return t(a)?encodeURI(a).replace(b,Wb):null}function Wb(a){a=a.charCodeAt(0);return"%"+(a>>4&15).toString(16)+(a&15).toString(16)}var Rb=/[#\/\?@]/g,Tb=/[\#\?:]/g,Sb=/[\#\?]/g,Vb=/[\#\?@]/g,Ub=/#/g;function S(a,b,c){this.g=a||null;this.h=!!c}
function U(a){if(!a.b&&(a.b=new Mb,a.a=0,a.g))for(var b=a.g.split("&"),c=0;c<b.length;c++){var d=b[c].indexOf("="),e=null,f=null;0<=d?(e=b[c].substring(0,d),f=b[c].substring(d+1)):e=b[c];e=decodeURIComponent(e.replace(/\+/g," "));e=V(a,e);a.add(e,f?decodeURIComponent(f.replace(/\+/g," ")):"")}}g=S.prototype;g.b=null;g.a=null;g.add=function(a,b){U(this);this.g=null;a=V(this,a);var c=this.b.get(a);c||this.b.set(a,c=[]);c.push(b);this.a++;return this};
g.remove=function(a){U(this);a=V(this,a);return this.b.G(a)?(this.g=null,this.a-=this.b.get(a).length,this.b.remove(a)):!1};g.G=function(a){U(this);a=V(this,a);return this.b.G(a)};g.B=function(){U(this);for(var a=this.b.k(),b=this.b.B(),c=[],d=0;d<b.length;d++)for(var e=a[d],f=0;f<e.length;f++)c.push(b[d]);return c};g.k=function(a){U(this);var b=[];if(a)this.G(a)&&(b=Ua(b,this.b.get(V(this,a))));else{a=this.b.k();for(var c=0;c<a.length;c++)b=Ua(b,a[c])}return b};
g.set=function(a,b){U(this);this.g=null;a=V(this,a);this.G(a)&&(this.a-=this.b.get(a).length);this.b.set(a,[b]);this.a++;return this};g.get=function(a,b){var c=a?this.k(a):[];return 0<c.length?String(c[0]):b};g.toString=function(){if(this.g)return this.g;if(!this.b)return"";for(var a=[],b=this.b.B(),c=0;c<b.length;c++)for(var d=b[c],e=encodeURIComponent(String(d)),d=this.k(d),f=0;f<d.length;f++){var h=e;""!==d[f]&&(h+="="+encodeURIComponent(String(d[f])));a.push(h)}return this.g=a.join("&")};
g.F=function(){var a=new S;a.g=this.g;this.b&&(a.b=this.b.F(),a.a=this.a);return a};function V(a,b){var c=String(b);a.h&&(c=c.toLowerCase());return c}g.ia=function(a){a&&!this.h&&(U(this),this.g=null,Lb(this.b,function(a,c){var d=c.toLowerCase();c!=d&&(this.remove(c),this.remove(d),0<a.length&&(this.g=null,this.b.set(V(this,d),Va(a)),this.a+=a.length))},this));this.h=a};function Xb(){}Xb.prototype.name=null;Xb.prototype.xa=null;Xb.prototype.aa=null;Xb.prototype.ha=null;function Yb(a){var b=new Xb;b.name=a.user_name;b.xa=a.user_pic;b.ha=a.score;b.aa=a.answered;return b};function W(){H.call(this);this.j=[];this.N={}}v(W,H);W.prototype.ua=1;W.prototype.Y=0;function Zb(a,b,c,d){var e=a.N[b];e||(e=a.N[b]=[]);var f=a.ua;a.j[f]=b;a.j[f+1]=c;a.j[f+2]=d;a.ua=f+3;e.push(f)}function $b(a){var b=a.N[void 0];if(b){var c=a.j;(b=Sa(b,function(a){return void 0==c[a+1]&&void 0==c[a+2]}))&&ac(a,b)}}function ac(a,b){if(0!=a.Y)a.W||(a.W=[]),a.W.push(b);else{var c=a.j[b];c&&((c=a.N[c])&&Ta(c,b),delete a.j[b],delete a.j[b+1],delete a.j[b+2])}}
W.prototype.za=function(a,b){var c=this.N[a];if(c){this.Y++;for(var d=Wa(arguments,1),e=0,f=c.length;e<f;e++){var h=c[e];this.j[h+1].apply(this.j[h+2],d)}this.Y--;if(this.W&&0==this.Y)for(;c=this.W.pop();)ac(this,c)}};function bc(){this.q="pending";this.C=[];this.ma=this.ka=void 0}function cc(){E.call(this,"Multiple attempts to set the state of this Result")}v(cc,E);bc.prototype.getError=aa("ma");function dc(a,b){if("pending"==a.q)for(a.ka=b,a.q="success";a.C.length;)a.C.shift()(a);else throw new cc;}function ec(a,b){if("pending"==a.q)for(a.ma=b,a.q="error";a.C.length;)a.C.shift()(a);else throw new cc;};function fc(a,b,c){b=c?ia(b,c):b;"pending"==a.q?a.C.push(b):b(a)}function gc(a,b){fc(a,function(a){"error"==a.q&&b.call(this,a)},void 0)}function hc(a,b){var c=new ic;fc(a,function(a){"success"==a.q?dc(c,b(a.ka)):ec(c,a.getError())});return c}function ic(){bc.call(this)}v(ic,bc);function jc(a){a=String(a);if(/^\s*$/.test(a)?0:/^[\],:{}\s\u2028\u2029]*$/.test(a.replace(/\\["\\\/bfnrtu]/g,"@").replace(/"[^"\\\n\r\u2028\u2029\x00-\x08\x0a-\x1f]*"|true|false|null|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?/g,"]").replace(/(?:^|:|,)(?:[\s\u2028\u2029]*\[)+/g,"")))try{return eval("("+a+")")}catch(b){}throw Error("Invalid JSON string: "+a);};function kc(){};var lc;function mc(){}v(mc,kc);function nc(){var a;a:{var b=lc;if(!b.ra&&"undefined"==typeof XMLHttpRequest&&"undefined"!=typeof ActiveXObject){for(var c=["MSXML2.XMLHTTP.6.0","MSXML2.XMLHTTP.3.0","MSXML2.XMLHTTP","Microsoft.XMLHTTP"],d=0;d<c.length;d++){var e=c[d];try{new ActiveXObject(e);a=b.ra=e;break a}catch(f){}}throw Error("Could not create ActiveXObject. ActiveX might be disabled, or MSXML might not be installed");}a=b.ra}return a?new ActiveXObject(a):new XMLHttpRequest}lc=new mc;function oc(a,b){var c=pc(a,b),d=c=hc(c,qc);b&&b.Ua&&(d=hc(c,ja(rc,b.Ua)));return hc(d,jc)}function pc(a,b){var c=new bc;gc(c,function(){});sc(a,b,function(a){dc(c,a)},function(a){ec(c,a)});return c}
function sc(a,b,c,d){b=b||{};var e=c||p,f=d||p,h,k=nc();try{k.open("GET",a,!0)}catch(l){f(new X("Error opening XHR: "+l.message,a));return}k.onreadystatechange=function(){if(4==k.readyState){window.clearTimeout(h);var b;a:switch(k.status){case 200:case 201:case 202:case 204:case 206:case 304:case 1223:b=!0;break a;default:b=!1}!b&&(b=0===k.status)&&(b=a.match(Jb)[1]||null,!b&&self.location&&(b=self.location.protocol,b=b.substr(0,b.length-1)),b=b?b.toLowerCase():"",b=!("http"==b||"https"==b||""==b));
b?e(k):f(new tc(k.status,a))}};if(b.headers)for(var x in b.headers)k.setRequestHeader(x,b.headers[x]);b.withCredentials&&(k.withCredentials=b.withCredentials);b.Pa&&k.overrideMimeType(b.Pa);0<b.Ra&&(h=window.setTimeout(function(){k.onreadystatechange=p;k.abort();f(new uc(a))},b.Ra));try{k.send(null)}catch(m){k.onreadystatechange=p,window.clearTimeout(h),f(new X("Error sending XHR: "+m.message,a))}}function qc(a){return a.responseText}
function rc(a,b){0==b.lastIndexOf(a,0)&&(b=b.substring(a.length));return b}function X(a,b){E.call(this,a+", url="+b);this.url=b}v(X,E);X.prototype.name="XhrError";function tc(a,b){X.call(this,"Request Failed, status="+a,b);this.status=a}v(tc,X);tc.prototype.name="XhrHttpError";function uc(a){X.call(this,"Request timed out",a)}v(uc,X);uc.prototype.name="XhrTimeoutError";function vc(){}ba(vc);ka("ffc.api.Client.getInstance",vc.da);vc.prototype.Ja=function(a,b){return oc.apply(null,arguments)};vc.prototype.Ia=function(a,b,c){a=la(wc,a);a=a instanceof Q?a.F():new Q(a,void 0);b&&(R(a),a.n.set("offset",b));c&&(R(a),a.n.set("limit",c));return this.Ja(a)};var wc="/api/leaderboard/%s";function xc(a,b){W.call(this);this.id=a;this.page=0;this.ea=yc;this.Ha=ia(b.Ia,b,a)}v(xc,W);ka("ffc.leaderboard.LeaderBoardModel",xc);xc.prototype.getData=function(){var a=this.Ha(this.page*this.ea,this.ea),b=this.La.bind(this);"pending"==a.q?a.C.push(b):b(a)};xc.prototype.La=function(a){a=a.ka;this.Sa=a.count;this.za(zc);this.Ta=Ra(a.users,Yb);this.za(Ac)};var yc=20,Ac="usersUpdated",zc="totalUpdated";function Y(a,b){null!=a&&this.append.apply(this,arguments)}Y.prototype.A="";Y.prototype.set=function(a){this.A=""+a};Y.prototype.append=function(a,b,c){this.A+=a;if(null!=b)for(var d=1;d<arguments.length;d++)this.A+=arguments[d];return this};Y.prototype.toString=aa("A");var Bc={};y&&D(8);function Cc(a,b){var c;a:{c=(new db(void 0)||cb()).createElement("DIV");var d;d=a(b||Bc,void 0,void 0);da(d)?(Oa("Soy template output is unsafe for use as HTML: "+d),d="zSoyz"):d=String(d);c.innerHTML=d;if(1==c.childNodes.length&&(d=c.firstChild,1==d.nodeType)){c=d;break a}}return c}
var Dc={"\x00":"&#0;",'"':"&quot;","&":"&amp;","'":"&#39;","<":"&lt;",">":"&gt;","\t":"&#9;","\n":"&#10;","\x0B":"&#11;","\f":"&#12;","\r":"&#13;"," ":"&#32;","-":"&#45;","/":"&#47;","=":"&#61;","`":"&#96;","\u0085":"&#133;","\u00a0":"&#160;","\u2028":"&#8232;","\u2029":"&#8233;"};function Ec(a){return Dc[a]}var Fc=/[\x00\x22\x26\x27\x3c\x3e]/g;function Gc(a,b){var c=b||new Y;c.append('<table class="table table-striped table-hover"><thead><tr><th colspan="2">User</th><th class="leaderboard-number">Score</th><th class="leaderboard-number">Answered</th><th class="leaderboard-number">Av. Score</th></tr></thead><tbody class="leaderboard-users"></tbody></table>');return b?"":c.toString()}function Hc(a,b){var c=b||new Y;c.append('<div class="leaderboard-pagination"><ul class="pagination pagination-sm"></ul></div>');return b?"":c.toString()}
function Ic(a,b){var c=b||new Y;c.append("<li",a.Da?' class="active"':"",'><a href="#">',"object"===typeof a.L&&a.L&&0===a.L.Va?a.L.content:String(a.L).replace(Fc,Ec),"</a></li>");return b?"":c.toString()};function Z(a){O.call(this);this.Q=this.K||(this.K=new Cb(this));this.d=this.ca();this.f=a}v(Z,O);ka("ffc.leaderboard.LeaderBoard",Z);Z.prototype.render=Z.prototype.Aa;g=Z.prototype;g.i=function(){var a=this.d.i("DIV");this.d.append(a,Cc(Gc));this.d.append(a,Cc(Hc));this.P(a)};g.P=function(a){Z.w.P.call(this,a);this.Ba=this.J("leaderboard-users");this.fa=this.J("pagination")};
g.u=function(){Z.w.u.call(this);Zb(this.f,zc,this.Ga,this);Zb(this.f,Ac,this.Fa,this);Eb(this.Q,this.fa,this.Ka,this);this.f.getData();this.e.style.display="block"};g.I=function(){Z.w.I.call(this);$b(this.f);Fb(this.Q);this.d.Z(this.e);this.e=null};
g.Fa=function(){this.d.Z(this.Ba);for(var a=[this.Ba],b=this.f.Ta,c=0,d=b.length;c<d;c++){var e=b[c];a.push(this.d.i("TR",null,this.d.i("TD",null,this.d.i("IMG",{src:e.xa,alt:e.name,width:20,height:20})),this.d.i("TD",null,e.name),this.d.i("TD","leaderboard-number",e.ha+""),this.d.i("TD","leaderboard-number",e.aa+""),this.d.i("TD","leaderboard-number",(e.ha/e.aa).toFixed(1)+"")))}this.d.append.apply(this.Ca,a)};
g.Ga=function(){this.d.Z(this.fa);var a=[this.fa],b;b=[];var c=Math.ceil(this.f.Sa/this.f.ea);if(0>1*(c-0))b=[];else for(var d=0;d<c;d+=1)b.push(d);c=0;for(d=b.length;c<d;c++)a.push(Cc(Ic,{L:b[c],Da:c==this.f.page}));this.d.append.apply(this.Ca,a)};g.Ka=function(a){a.preventDefault();"A"==a.target.nodeName&&(a=parseInt(a.target.innerHTML,10),a!=this.f.page&&(this.f.page=a,this.f.getData()))};function $(a){O.call(this);this.Q=this.K||(this.K=new Cb(this));this.d=this.ca();this.va=Array.prototype.slice.call(arguments,0)}v($,O);ka("ffc.leaderboard.LeaderBoardToggler",$);$.prototype.decorate=$.prototype.Ea;$.prototype.u=function(){$.w.u.call(this);Eb(this.Q,this.e,this.Ma,this)};
$.prototype.Ma=function(a){a.preventDefault();var b=lb(a.target),c;if(c="A"==a.target.nodeName)if(c=b)c=Ya(b),c=!(0<=G(c,"active"));if(c)for(a=a.target,a=a.dataset?a.dataset.leaderboard:a.getAttribute("data-"+"leaderboard".replace(/([A-Z])/g,"-$1").toLowerCase()),$a(this.d.J("active",this.e),"active"),Za(b,"active"),b=0,c=this.va.length;b<c;b++){var d=this.va[b];d.f.id==a?d.Aa(document.getElementById("leaderboard-container-"+a)):d.I()}};})();
