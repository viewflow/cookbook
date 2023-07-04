(function(){const t=document.createElement("link").relList;if(t&&t.supports&&t.supports("modulepreload"))return;for(const r of document.querySelectorAll('link[rel="modulepreload"]'))s(r);new MutationObserver(r=>{for(const o of r)if(o.type==="childList")for(const n of o.addedNodes)n.tagName==="LINK"&&n.rel==="modulepreload"&&s(n)}).observe(document,{childList:!0,subtree:!0});function e(r){const o={};return r.integrity&&(o.integrity=r.integrity),r.referrerPolicy&&(o.referrerPolicy=r.referrerPolicy),r.crossOrigin==="use-credentials"?o.credentials="include":r.crossOrigin==="anonymous"?o.credentials="omit":o.credentials="same-origin",o}function s(r){if(r.ep)return;r.ep=!0;const o=e(r);fetch(r.href,o)}})();/**
 * @license
 * Copyright 2019 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */const q=window,ut=q.ShadowRoot&&(q.ShadyCSS===void 0||q.ShadyCSS.nativeShadow)&&"adoptedStyleSheets"in Document.prototype&&"replace"in CSSStyleSheet.prototype,Pt=Symbol(),vt=new WeakMap;let Ut=class{constructor(t,e,s){if(this._$cssResult$=!0,s!==Pt)throw Error("CSSResult is not constructable. Use `unsafeCSS` or `css` instead.");this.cssText=t,this.t=e}get styleSheet(){let t=this.o;const e=this.t;if(ut&&t===void 0){const s=e!==void 0&&e.length===1;s&&(t=vt.get(e)),t===void 0&&((this.o=t=new CSSStyleSheet).replaceSync(this.cssText),s&&vt.set(e,t))}return t}toString(){return this.cssText}};const Mt=i=>new Ut(typeof i=="string"?i:i+"",void 0,Pt),Ht=(i,t)=>{ut?i.adoptedStyleSheets=t.map(e=>e instanceof CSSStyleSheet?e:e.styleSheet):t.forEach(e=>{const s=document.createElement("style"),r=q.litNonce;r!==void 0&&s.setAttribute("nonce",r),s.textContent=e.cssText,i.appendChild(s)})},gt=ut?i=>i:i=>i instanceof CSSStyleSheet?(t=>{let e="";for(const s of t.cssRules)e+=s.cssText;return Mt(e)})(i):i;/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */var Y;const W=window,$t=W.trustedTypes,It=$t?$t.emptyScript:"",yt=W.reactiveElementPolyfillSupport,ot={toAttribute(i,t){switch(t){case Boolean:i=i?It:null;break;case Object:case Array:i=i==null?i:JSON.stringify(i)}return i},fromAttribute(i,t){let e=i;switch(t){case Boolean:e=i!==null;break;case Number:e=i===null?null:Number(i);break;case Object:case Array:try{e=JSON.parse(i)}catch{e=null}}return e}},kt=(i,t)=>t!==i&&(t==t||i==i),G={attribute:!0,type:String,converter:ot,reflect:!1,hasChanged:kt},nt="finalized";let A=class extends HTMLElement{constructor(){super(),this._$Ei=new Map,this.isUpdatePending=!1,this.hasUpdated=!1,this._$El=null,this.u()}static addInitializer(t){var e;this.finalize(),((e=this.h)!==null&&e!==void 0?e:this.h=[]).push(t)}static get observedAttributes(){this.finalize();const t=[];return this.elementProperties.forEach((e,s)=>{const r=this._$Ep(s,e);r!==void 0&&(this._$Ev.set(r,s),t.push(r))}),t}static createProperty(t,e=G){if(e.state&&(e.attribute=!1),this.finalize(),this.elementProperties.set(t,e),!e.noAccessor&&!this.prototype.hasOwnProperty(t)){const s=typeof t=="symbol"?Symbol():"__"+t,r=this.getPropertyDescriptor(t,s,e);r!==void 0&&Object.defineProperty(this.prototype,t,r)}}static getPropertyDescriptor(t,e,s){return{get(){return this[e]},set(r){const o=this[t];this[e]=r,this.requestUpdate(t,o,s)},configurable:!0,enumerable:!0}}static getPropertyOptions(t){return this.elementProperties.get(t)||G}static finalize(){if(this.hasOwnProperty(nt))return!1;this[nt]=!0;const t=Object.getPrototypeOf(this);if(t.finalize(),t.h!==void 0&&(this.h=[...t.h]),this.elementProperties=new Map(t.elementProperties),this._$Ev=new Map,this.hasOwnProperty("properties")){const e=this.properties,s=[...Object.getOwnPropertyNames(e),...Object.getOwnPropertySymbols(e)];for(const r of s)this.createProperty(r,e[r])}return this.elementStyles=this.finalizeStyles(this.styles),!0}static finalizeStyles(t){const e=[];if(Array.isArray(t)){const s=new Set(t.flat(1/0).reverse());for(const r of s)e.unshift(gt(r))}else t!==void 0&&e.push(gt(t));return e}static _$Ep(t,e){const s=e.attribute;return s===!1?void 0:typeof s=="string"?s:typeof t=="string"?t.toLowerCase():void 0}u(){var t;this._$E_=new Promise(e=>this.enableUpdating=e),this._$AL=new Map,this._$Eg(),this.requestUpdate(),(t=this.constructor.h)===null||t===void 0||t.forEach(e=>e(this))}addController(t){var e,s;((e=this._$ES)!==null&&e!==void 0?e:this._$ES=[]).push(t),this.renderRoot!==void 0&&this.isConnected&&((s=t.hostConnected)===null||s===void 0||s.call(t))}removeController(t){var e;(e=this._$ES)===null||e===void 0||e.splice(this._$ES.indexOf(t)>>>0,1)}_$Eg(){this.constructor.elementProperties.forEach((t,e)=>{this.hasOwnProperty(e)&&(this._$Ei.set(e,this[e]),delete this[e])})}createRenderRoot(){var t;const e=(t=this.shadowRoot)!==null&&t!==void 0?t:this.attachShadow(this.constructor.shadowRootOptions);return Ht(e,this.constructor.elementStyles),e}connectedCallback(){var t;this.renderRoot===void 0&&(this.renderRoot=this.createRenderRoot()),this.enableUpdating(!0),(t=this._$ES)===null||t===void 0||t.forEach(e=>{var s;return(s=e.hostConnected)===null||s===void 0?void 0:s.call(e)})}enableUpdating(t){}disconnectedCallback(){var t;(t=this._$ES)===null||t===void 0||t.forEach(e=>{var s;return(s=e.hostDisconnected)===null||s===void 0?void 0:s.call(e)})}attributeChangedCallback(t,e,s){this._$AK(t,s)}_$EO(t,e,s=G){var r;const o=this.constructor._$Ep(t,s);if(o!==void 0&&s.reflect===!0){const n=(((r=s.converter)===null||r===void 0?void 0:r.toAttribute)!==void 0?s.converter:ot).toAttribute(e,s.type);this._$El=t,n==null?this.removeAttribute(o):this.setAttribute(o,n),this._$El=null}}_$AK(t,e){var s;const r=this.constructor,o=r._$Ev.get(t);if(o!==void 0&&this._$El!==o){const n=r.getPropertyOptions(o),p=typeof n.converter=="function"?{fromAttribute:n.converter}:((s=n.converter)===null||s===void 0?void 0:s.fromAttribute)!==void 0?n.converter:ot;this._$El=o,this[o]=p.fromAttribute(e,n.type),this._$El=null}}requestUpdate(t,e,s){let r=!0;t!==void 0&&(((s=s||this.constructor.getPropertyOptions(t)).hasChanged||kt)(this[t],e)?(this._$AL.has(t)||this._$AL.set(t,e),s.reflect===!0&&this._$El!==t&&(this._$EC===void 0&&(this._$EC=new Map),this._$EC.set(t,s))):r=!1),!this.isUpdatePending&&r&&(this._$E_=this._$Ej())}async _$Ej(){this.isUpdatePending=!0;try{await this._$E_}catch(e){Promise.reject(e)}const t=this.scheduleUpdate();return t!=null&&await t,!this.isUpdatePending}scheduleUpdate(){return this.performUpdate()}performUpdate(){var t;if(!this.isUpdatePending)return;this.hasUpdated,this._$Ei&&(this._$Ei.forEach((r,o)=>this[o]=r),this._$Ei=void 0);let e=!1;const s=this._$AL;try{e=this.shouldUpdate(s),e?(this.willUpdate(s),(t=this._$ES)===null||t===void 0||t.forEach(r=>{var o;return(o=r.hostUpdate)===null||o===void 0?void 0:o.call(r)}),this.update(s)):this._$Ek()}catch(r){throw e=!1,this._$Ek(),r}e&&this._$AE(s)}willUpdate(t){}_$AE(t){var e;(e=this._$ES)===null||e===void 0||e.forEach(s=>{var r;return(r=s.hostUpdated)===null||r===void 0?void 0:r.call(s)}),this.hasUpdated||(this.hasUpdated=!0,this.firstUpdated(t)),this.updated(t)}_$Ek(){this._$AL=new Map,this.isUpdatePending=!1}get updateComplete(){return this.getUpdateComplete()}getUpdateComplete(){return this._$E_}shouldUpdate(t){return!0}update(t){this._$EC!==void 0&&(this._$EC.forEach((e,s)=>this._$EO(s,this[s],e)),this._$EC=void 0),this._$Ek()}updated(t){}firstUpdated(t){}};A[nt]=!0,A.elementProperties=new Map,A.elementStyles=[],A.shadowRootOptions={mode:"open"},yt==null||yt({ReactiveElement:A}),((Y=W.reactiveElementVersions)!==null&&Y!==void 0?Y:W.reactiveElementVersions=[]).push("1.6.2");/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */var tt;const K=window,S=K.trustedTypes,bt=S?S.createPolicy("lit-html",{createHTML:i=>i}):void 0,lt="$lit$",b=`lit$${(Math.random()+"").slice(9)}$`,Ot="?"+b,Bt=`<${Ot}>`,w=document,L=()=>w.createComment(""),D=i=>i===null||typeof i!="object"&&typeof i!="function",Tt=Array.isArray,Ft=i=>Tt(i)||typeof(i==null?void 0:i[Symbol.iterator])=="function",et=`[ 	
\f\r]`,N=/<(?:(!--|\/[^a-zA-Z])|(\/?[a-zA-Z][^>\s]*)|(\/?$))/g,mt=/-->/g,_t=/>/g,m=RegExp(`>|${et}(?:([^\\s"'>=/]+)(${et}*=${et}*(?:[^ 	
\f\r"'\`<>=]|("|')|))|$)`,"g"),wt=/'/g,xt=/"/g,Rt=/^(?:script|style|textarea|title)$/i,Vt=i=>(t,...e)=>({_$litType$:i,strings:t,values:e}),a=Vt(1),x=Symbol.for("lit-noChange"),f=Symbol.for("lit-nothing"),At=new WeakMap,_=w.createTreeWalker(w,129,null,!1),zt=(i,t)=>{const e=i.length-1,s=[];let r,o=t===2?"<svg>":"",n=N;for(let l=0;l<e;l++){const d=i[l];let y,c,u=-1,g=0;for(;g<d.length&&(n.lastIndex=g,c=n.exec(d),c!==null);)g=n.lastIndex,n===N?c[1]==="!--"?n=mt:c[1]!==void 0?n=_t:c[2]!==void 0?(Rt.test(c[2])&&(r=RegExp("</"+c[2],"g")),n=m):c[3]!==void 0&&(n=m):n===m?c[0]===">"?(n=r??N,u=-1):c[1]===void 0?u=-2:(u=n.lastIndex-c[2].length,y=c[1],n=c[3]===void 0?m:c[3]==='"'?xt:wt):n===xt||n===wt?n=m:n===mt||n===_t?n=N:(n=m,r=void 0);const z=n===m&&i[l+1].startsWith("/>")?" ":"";o+=n===N?d+Bt:u>=0?(s.push(y),d.slice(0,u)+lt+d.slice(u)+b+z):d+b+(u===-2?(s.push(void 0),l):z)}const p=o+(i[e]||"<?>")+(t===2?"</svg>":"");if(!Array.isArray(i)||!i.hasOwnProperty("raw"))throw Error("invalid template strings array");return[bt!==void 0?bt.createHTML(p):p,s]};class j{constructor({strings:t,_$litType$:e},s){let r;this.parts=[];let o=0,n=0;const p=t.length-1,l=this.parts,[d,y]=zt(t,e);if(this.el=j.createElement(d,s),_.currentNode=this.el.content,e===2){const c=this.el.content,u=c.firstChild;u.remove(),c.append(...u.childNodes)}for(;(r=_.nextNode())!==null&&l.length<p;){if(r.nodeType===1){if(r.hasAttributes()){const c=[];for(const u of r.getAttributeNames())if(u.endsWith(lt)||u.startsWith(b)){const g=y[n++];if(c.push(u),g!==void 0){const z=r.getAttribute(g.toLowerCase()+lt).split(b),J=/([.?@])?(.*)/.exec(g);l.push({type:1,index:o,name:J[2],strings:z,ctor:J[1]==="."?qt:J[1]==="?"?Kt:J[1]==="@"?Qt:Z})}else l.push({type:6,index:o})}for(const u of c)r.removeAttribute(u)}if(Rt.test(r.tagName)){const c=r.textContent.split(b),u=c.length-1;if(u>0){r.textContent=S?S.emptyScript:"";for(let g=0;g<u;g++)r.append(c[g],L()),_.nextNode(),l.push({type:2,index:++o});r.append(c[u],L())}}}else if(r.nodeType===8)if(r.data===Ot)l.push({type:2,index:o});else{let c=-1;for(;(c=r.data.indexOf(b,c+1))!==-1;)l.push({type:7,index:o}),c+=b.length-1}o++}}static createElement(t,e){const s=w.createElement("template");return s.innerHTML=t,s}}function C(i,t,e=i,s){var r,o,n,p;if(t===x)return t;let l=s!==void 0?(r=e._$Co)===null||r===void 0?void 0:r[s]:e._$Cl;const d=D(t)?void 0:t._$litDirective$;return(l==null?void 0:l.constructor)!==d&&((o=l==null?void 0:l._$AO)===null||o===void 0||o.call(l,!1),d===void 0?l=void 0:(l=new d(i),l._$AT(i,e,s)),s!==void 0?((n=(p=e)._$Co)!==null&&n!==void 0?n:p._$Co=[])[s]=l:e._$Cl=l),l!==void 0&&(t=C(i,l._$AS(i,t.values),l,s)),t}class Jt{constructor(t,e){this._$AV=[],this._$AN=void 0,this._$AD=t,this._$AM=e}get parentNode(){return this._$AM.parentNode}get _$AU(){return this._$AM._$AU}u(t){var e;const{el:{content:s},parts:r}=this._$AD,o=((e=t==null?void 0:t.creationScope)!==null&&e!==void 0?e:w).importNode(s,!0);_.currentNode=o;let n=_.nextNode(),p=0,l=0,d=r[0];for(;d!==void 0;){if(p===d.index){let y;d.type===2?y=new M(n,n.nextSibling,this,t):d.type===1?y=new d.ctor(n,d.name,d.strings,this,t):d.type===6&&(y=new Zt(n,this,t)),this._$AV.push(y),d=r[++l]}p!==(d==null?void 0:d.index)&&(n=_.nextNode(),p++)}return _.currentNode=w,o}v(t){let e=0;for(const s of this._$AV)s!==void 0&&(s.strings!==void 0?(s._$AI(t,s,e),e+=s.strings.length-2):s._$AI(t[e])),e++}}class M{constructor(t,e,s,r){var o;this.type=2,this._$AH=f,this._$AN=void 0,this._$AA=t,this._$AB=e,this._$AM=s,this.options=r,this._$Cp=(o=r==null?void 0:r.isConnected)===null||o===void 0||o}get _$AU(){var t,e;return(e=(t=this._$AM)===null||t===void 0?void 0:t._$AU)!==null&&e!==void 0?e:this._$Cp}get parentNode(){let t=this._$AA.parentNode;const e=this._$AM;return e!==void 0&&(t==null?void 0:t.nodeType)===11&&(t=e.parentNode),t}get startNode(){return this._$AA}get endNode(){return this._$AB}_$AI(t,e=this){t=C(this,t,e),D(t)?t===f||t==null||t===""?(this._$AH!==f&&this._$AR(),this._$AH=f):t!==this._$AH&&t!==x&&this._(t):t._$litType$!==void 0?this.g(t):t.nodeType!==void 0?this.$(t):Ft(t)?this.T(t):this._(t)}k(t){return this._$AA.parentNode.insertBefore(t,this._$AB)}$(t){this._$AH!==t&&(this._$AR(),this._$AH=this.k(t))}_(t){this._$AH!==f&&D(this._$AH)?this._$AA.nextSibling.data=t:this.$(w.createTextNode(t)),this._$AH=t}g(t){var e;const{values:s,_$litType$:r}=t,o=typeof r=="number"?this._$AC(t):(r.el===void 0&&(r.el=j.createElement(r.h,this.options)),r);if(((e=this._$AH)===null||e===void 0?void 0:e._$AD)===o)this._$AH.v(s);else{const n=new Jt(o,this),p=n.u(this.options);n.v(s),this.$(p),this._$AH=n}}_$AC(t){let e=At.get(t.strings);return e===void 0&&At.set(t.strings,e=new j(t)),e}T(t){Tt(this._$AH)||(this._$AH=[],this._$AR());const e=this._$AH;let s,r=0;for(const o of t)r===e.length?e.push(s=new M(this.k(L()),this.k(L()),this,this.options)):s=e[r],s._$AI(o),r++;r<e.length&&(this._$AR(s&&s._$AB.nextSibling,r),e.length=r)}_$AR(t=this._$AA.nextSibling,e){var s;for((s=this._$AP)===null||s===void 0||s.call(this,!1,!0,e);t&&t!==this._$AB;){const r=t.nextSibling;t.remove(),t=r}}setConnected(t){var e;this._$AM===void 0&&(this._$Cp=t,(e=this._$AP)===null||e===void 0||e.call(this,t))}}class Z{constructor(t,e,s,r,o){this.type=1,this._$AH=f,this._$AN=void 0,this.element=t,this.name=e,this._$AM=r,this.options=o,s.length>2||s[0]!==""||s[1]!==""?(this._$AH=Array(s.length-1).fill(new String),this.strings=s):this._$AH=f}get tagName(){return this.element.tagName}get _$AU(){return this._$AM._$AU}_$AI(t,e=this,s,r){const o=this.strings;let n=!1;if(o===void 0)t=C(this,t,e,0),n=!D(t)||t!==this._$AH&&t!==x,n&&(this._$AH=t);else{const p=t;let l,d;for(t=o[0],l=0;l<o.length-1;l++)d=C(this,p[s+l],e,l),d===x&&(d=this._$AH[l]),n||(n=!D(d)||d!==this._$AH[l]),d===f?t=f:t!==f&&(t+=(d??"")+o[l+1]),this._$AH[l]=d}n&&!r&&this.j(t)}j(t){t===f?this.element.removeAttribute(this.name):this.element.setAttribute(this.name,t??"")}}class qt extends Z{constructor(){super(...arguments),this.type=3}j(t){this.element[this.name]=t===f?void 0:t}}const Wt=S?S.emptyScript:"";class Kt extends Z{constructor(){super(...arguments),this.type=4}j(t){t&&t!==f?this.element.setAttribute(this.name,Wt):this.element.removeAttribute(this.name)}}class Qt extends Z{constructor(t,e,s,r,o){super(t,e,s,r,o),this.type=5}_$AI(t,e=this){var s;if((t=(s=C(this,t,e,0))!==null&&s!==void 0?s:f)===x)return;const r=this._$AH,o=t===f&&r!==f||t.capture!==r.capture||t.once!==r.once||t.passive!==r.passive,n=t!==f&&(r===f||o);o&&this.element.removeEventListener(this.name,this,r),n&&this.element.addEventListener(this.name,this,t),this._$AH=t}handleEvent(t){var e,s;typeof this._$AH=="function"?this._$AH.call((s=(e=this.options)===null||e===void 0?void 0:e.host)!==null&&s!==void 0?s:this.element,t):this._$AH.handleEvent(t)}}class Zt{constructor(t,e,s){this.element=t,this.type=6,this._$AN=void 0,this._$AM=e,this.options=s}get _$AU(){return this._$AM._$AU}_$AI(t){C(this,t)}}const Et=K.litHtmlPolyfillSupport;Et==null||Et(j,M),((tt=K.litHtmlVersions)!==null&&tt!==void 0?tt:K.litHtmlVersions=[]).push("2.7.4");const Xt=(i,t,e)=>{var s,r;const o=(s=e==null?void 0:e.renderBefore)!==null&&s!==void 0?s:t;let n=o._$litPart$;if(n===void 0){const p=(r=e==null?void 0:e.renderBefore)!==null&&r!==void 0?r:null;o._$litPart$=n=new M(t.insertBefore(L(),p),p,void 0,e??{})}return n._$AI(i),n};/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */var st,rt;class v extends A{constructor(){super(...arguments),this.renderOptions={host:this},this._$Do=void 0}createRenderRoot(){var t,e;const s=super.createRenderRoot();return(t=(e=this.renderOptions).renderBefore)!==null&&t!==void 0||(e.renderBefore=s.firstChild),s}update(t){const e=this.render();this.hasUpdated||(this.renderOptions.isConnected=this.isConnected),super.update(t),this._$Do=Xt(e,this.renderRoot,this.renderOptions)}connectedCallback(){var t;super.connectedCallback(),(t=this._$Do)===null||t===void 0||t.setConnected(!0)}disconnectedCallback(){var t;super.disconnectedCallback(),(t=this._$Do)===null||t===void 0||t.setConnected(!1)}render(){return x}}v.finalized=!0,v._$litElement$=!0,(st=globalThis.litElementHydrateSupport)===null||st===void 0||st.call(globalThis,{LitElement:v});const St=globalThis.litElementPolyfillSupport;St==null||St({LitElement:v});((rt=globalThis.litElementVersions)!==null&&rt!==void 0?rt:globalThis.litElementVersions=[]).push("3.3.2");/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */const $=i=>t=>typeof t=="function"?((e,s)=>(customElements.define(e,s),s))(i,t):((e,s)=>{const{kind:r,elements:o}=s;return{kind:r,elements:o,finisher(n){customElements.define(e,n)}}})(i,t);/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */const Yt=(i,t)=>t.kind==="method"&&t.descriptor&&!("value"in t.descriptor)?{...t,finisher(e){e.createProperty(t.key,i)}}:{kind:"field",key:Symbol(),placement:"own",descriptor:{},originalKey:t.key,initializer(){typeof t.initializer=="function"&&(this[t.key]=t.initializer.call(this))},finisher(e){e.createProperty(t.key,i)}},Gt=(i,t,e)=>{t.constructor.createProperty(e,i)};function h(i){return(t,e)=>e!==void 0?Gt(i,t,e):Yt(i,t)}/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */const te=({finisher:i,descriptor:t})=>(e,s)=>{var r;if(s===void 0){const o=(r=e.originalKey)!==null&&r!==void 0?r:e.key,n=t!=null?{kind:"method",placement:"prototype",key:o,descriptor:t(e.key)}:{...e,key:o};return i!=null&&(n.finisher=function(p){i(p,o)}),n}{const o=e.constructor;t!==void 0&&Object.defineProperty(e,s,t(s)),i==null||i(o,s)}};/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */function ee(i,t){return te({descriptor:e=>{const s={get(){var r,o;return(o=(r=this.renderRoot)===null||r===void 0?void 0:r.querySelector(i))!==null&&o!==void 0?o:null},enumerable:!0,configurable:!0};if(t){const r=typeof e=="symbol"?Symbol():"__"+e;s.get=function(){var o,n;return this[r]===void 0&&(this[r]=(n=(o=this.renderRoot)===null||o===void 0?void 0:o.querySelector(i))!==null&&n!==void 0?n:null),this[r]}}return s}})}/**
 * @license
 * Copyright 2021 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */var it;((it=window.HTMLSlotElement)===null||it===void 0?void 0:it.prototype.assignedElements)!=null;const E={flow_class:"ALL",title:"All flows",description:"",start_actions:[],process_list:"/api/process/",task_list:"/api/task/",chart:""};var se=Object.defineProperty,re=Object.getOwnPropertyDescriptor,H=(i,t,e,s)=>{for(var r=s>1?void 0:s?re(t,e):t,o=i.length-1,n;o>=0;o--)(n=i[o])&&(r=(s?n(t,e,r):n(r))||r);return s&&r&&se(t,e,r),r};let P=class extends v{constructor(){super(),this.selected=E,this.flows=[],this.loading=!0,this.fetchFlows()}createRenderRoot(){return this}async fetchFlows(){try{this.loading=!0;const i=await fetch("/api/flows/");if(!i.ok)throw new Error("An error occurred while fetching the flow list.");const t=await i.json();this.flows=t}catch(i){this.error=i.message||"An error occurred while fetching the flow list."}finally{this.loading=!1}}handleClick(i){const e=i.target.getAttribute("data-flow-class");this.selected=this.flows.find(s=>s.flow_class===e)||E,this.dispatchEvent(new CustomEvent("link-clicked",{detail:this.selected}))}renderFlowsLinks(i){return a`
      <a
        href="#"
        @click="${this.handleClick}"
        data-flow-class="${i.flow_class}"
        class="${this.selected.flow_class===i.flow_class?"bg-blue-50 ":""}text-blue-500 hover:text-blue-700 hover:bg-blue-100 w-full py-2 px-4 rounded-lg text-center">
        ${i.title}
      </a>
    `}renderErrorMessage(){return a`
      <div class="mt-4 text-red-500 error-message px-2">
        ${this.error}
      </div>
    `}renderSpin(){return a`
      <div class="flex justify-center items-center py-4">
        <div class="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    `}render(){return a`
    <div class="bg-gray-800 text-white py-4">
      <h1 class="text-2xl text-center">Flows</h1>
    </div>

    <div class="py-6">
        <nav class="flex flex-col items-center mx-2">
          <a
            href="#"
            @click="${this.handleClick}"
            class="${this.selected.flow_class===E.flow_class?"bg-blue-50 ":""}text-blue-500 hover:text-blue-700 hover:bg-blue-100 w-full py-2 px-4 rounded-lg text-center">All flows</a>
          ${this.loading?this.renderSpin():this.flows.map(i=>this.renderFlowsLinks(i))}
        </nav>

        ${this.error?this.renderErrorMessage():""}
    </div>
    `}};H([h({type:JSON})],P.prototype,"selected",2);H([h({type:Array})],P.prototype,"flows",2);H([h({type:Boolean})],P.prototype,"loading",2);H([h({type:String})],P.prototype,"error",2);P=H([$("vf-flows-list")],P);var ie=Object.defineProperty,oe=Object.getOwnPropertyDescriptor,ft=(i,t,e,s)=>{for(var r=s>1?void 0:s?oe(t,e):t,o=i.length-1,n;o>=0;o--)(n=i[o])&&(r=(s?n(t,e,r):n(r))||r);return s&&r&&ie(t,e,r),r};let Q=class extends v{constructor(){super(...arguments),this.flow=E,this.selected=""}createRenderRoot(){return this}handleLinkClick(t){const e=t.target;this.selected=e.getAttribute("data-list-url")||"",this.dispatchEvent(new CustomEvent("link-clicked",{detail:this.selected}))}handleActionClick(t){const s=t.target.getAttribute("data-action-url")||"";this.dispatchEvent(new CustomEvent("action-clicked",{detail:s}))}updated(t){t.has("flow")&&(this.selected=this.flow.process_list)}renderLink(t,e){const s="text-blue-500 hover:text-blue-700 hover:bg-blue-100 w-full py-2 px-4 rounded-lg text-center";return a`
      <a
        href="#"
        class="${this.selected==e?"bg-blue-50 ":""} ${s}"
        data-list-url="${e}"
        @click="${this.handleLinkClick}"
      >${t}</a>
    `}renderStartAction(t){return a`
      <div class="flex justify-center py-2">
        <button
          data-action-url="${t.url}"
          @click="${this.handleActionClick}"
          class="bg-blue-500 hover:bg-blue-700 text-white py-2 px-4 rounded-lg">${t.title}</button>
      </div>
    `}render(){return a`
      <div class="bg-gray-600 text-white py-4">
        <h1 class="text-2xl text-center">${this.flow.title}</h1>

      </div>

      <div class="py-2">
        <nav class="flex flex-col items-center mx-2">
          ${this.renderLink("Process",this.flow.process_list)}
          <div class="h-4"></div>
          <h4 class="text-sm font-bold">Tasks</h4>
          ${this.renderLink("Inbox",this.flow.task_list+"?task_list=INBOX")}
          ${this.renderLink("Queue",this.flow.task_list+"?task_list=QUEUE")}
          ${this.renderLink("Archive",this.flow.task_list+"?task_list=ARCHIVE")}
        </nav>
      </div>

      <div class="flex py-2 mx-2">
        ${this.flow.chart?a`<vf-flow-chart url="${this.flow.chart}">`:""}
      </div>

      ${this.flow.start_actions.map(t=>this.renderStartAction(t))}    `}};ft([h({type:JSON})],Q.prototype,"flow",2);ft([h({type:String})],Q.prototype,"selected",2);Q=ft([$("vf-flow-menu")],Q);/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */const ne={ATTRIBUTE:1,CHILD:2,PROPERTY:3,BOOLEAN_ATTRIBUTE:4,EVENT:5,ELEMENT:6},le=i=>(...t)=>({_$litDirective$:i,values:t});class ae{constructor(t){}get _$AU(){return this._$AM._$AU}_$AT(t,e,s){this._$Ct=t,this._$AM=e,this._$Ci=s}_$AS(t,e){return this.update(t,e)}update(t,e){return this.render(...e)}}/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */class at extends ae{constructor(t){if(super(t),this.et=f,t.type!==ne.CHILD)throw Error(this.constructor.directiveName+"() can only be used in child bindings")}render(t){if(t===f||t==null)return this.ft=void 0,this.et=t;if(t===x)return t;if(typeof t!="string")throw Error(this.constructor.directiveName+"() called with a non-string value");if(t===this.et)return this.ft;this.et=t;const e=[t];return e.raw=e,this.ft={_$litType$:this.constructor.resultType,strings:e,values:[]}}}at.directiveName="unsafeHTML",at.resultType=1;const Ct=le(at);var de=Object.defineProperty,ce=Object.getOwnPropertyDescriptor,I=(i,t,e,s)=>{for(var r=s>1?void 0:s?ce(t,e):t,o=i.length-1,n;o>=0;o--)(n=i[o])&&(r=(s?n(t,e,r):n(r))||r);return s&&r&&de(t,e,r),r};let k=class extends v{constructor(){super(...arguments),this.url="",this.svg="",this.loading=!0,this.error=""}createRenderRoot(){return this}updated(i){i.has("url")&&this.fetchChart()}async fetchChart(){try{this.loading=!0;const i=await fetch(this.url);if(!i.ok)throw new Error("An error occurred while fetching the flow list.");const t=await i.text();this.svg=t}catch(i){this.error=i.message||"An error occurred while fetching the flow list."}finally{this.loading=!1}}renderErrorMessage(){return a`
      <div class="mt-4 text-red-500 error-message px-2">
        ${this.error}
      </div>
    `}render(){return a`
      <div id="chart" class="popup">
        <a href="#" class="close">&times;</a>
        <a href="#">
          <div class="content">
            ${Ct(this.svg)}
          </div>
        </a>
      </div>
      <a href="#chart" class="chart">
        ${Ct(this.svg)}
      </a>

      ${this.error?this.renderErrorMessage():""}
    `}};I([h({type:String})],k.prototype,"url",2);I([h({type:String})],k.prototype,"svg",2);I([h({type:Boolean})],k.prototype,"loading",2);I([h({type:String})],k.prototype,"error",2);k=I([$("vf-flow-chart")],k);var he=Object.defineProperty,pe=Object.getOwnPropertyDescriptor,B=(i,t,e,s)=>{for(var r=s>1?void 0:s?pe(t,e):t,o=i.length-1,n;o>=0;o--)(n=i[o])&&(r=(s?n(t,e,r):n(r))||r);return s&&r&&he(t,e,r),r};let O=class extends v{constructor(){super(...arguments),this.url="",this.processes=[],this.loading=!0,this.controller=new AbortController}createRenderRoot(){return this}disconnectedCallback(){super.disconnectedCallback(),this.controller.abort()}updated(i){i.has("url")&&this.fetchProcesses()}async fetchProcesses(){if(this.url)try{this.loading=!0;const i=await fetch(this.url,{signal:this.controller.signal});if(!i.ok)throw new Error("An error occurred while fetching the flow list.");const t=await i.json();this.processes=t,this.processes&&this.dispatchEvent(new CustomEvent("link-clicked",{detail:this.processes[0]}))}catch(i){this.error=i.message||"An error occurred while fetching the flow list."}finally{this.loading=!1}}handleClick(i){const t=i.target,e=this.processes.find(s=>s.id.toString()===t.textContent)||null;e&&this.dispatchEvent(new CustomEvent("link-clicked",{detail:e}))}renderSpin(){return a`
      <div class="flex justify-center items-center py-4 animate-spin-container">
        <div class="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    `}renderTableRow(i){return a`
      <tr>
        <td class="py-3 px-4 border-b border-gray-200">
          <a href="#" @click="${this.handleClick}">${i.id}</a>
        </td>
        <td class="py-3 px-4 border-b border-gray-200 text-sm">${i.status}</td>
        <td class="py-3 px-4 border-b border-gray-200 text-sm">${i.brief}</td>
        <td class="py-3 px-4 border-b border-gray-200 text-sm">${new Date(i.created).toLocaleString()}</td>
      </tr>
    `}renderTable(){return a`
      <div class="container mx-auto py-2 px-2">
        <table class="min-w-full bg-white border border-gray-200 rounded-lg">
          <thead>
            <tr>
              <th class="py-3 px-4 border-b border-gray-200 bg-gray-100 text-left text-sm">#</th>
              <th class="py-3 px-4 border-b border-gray-200 bg-gray-100 text-left text-sm">Status</th>
              <th class="py-3 px-4 border-b border-gray-200 bg-gray-100 text-left text-sm">Process Brief</th>
              <th class="py-3 px-4 border-b border-gray-200 bg-gray-100 text-left text-sm">Created</th>
            </tr>
          </thead>
          <tbody>
            ${this.processes.map(i=>this.renderTableRow(i))}
          </tbody>
        </table>
      </div>
    `}renderErrorMessage(){return a`
      <div class="mt-4 text-red-500 error-message px-2">
        ${this.error}
      </div>
    `}render(){return a`
      <div class="bg-gray-500 text-white py-4">
        <h1 class="text-2xl text-center">Processes</h1>
      </div>
      ${this.loading?this.renderSpin():this.renderTable()}
      ${this.error?this.renderErrorMessage():""}
    `}};B([h({type:String})],O.prototype,"url",2);B([h({type:Array})],O.prototype,"processes",2);B([h({type:Boolean})],O.prototype,"loading",2);B([h({type:String})],O.prototype,"error",2);O=B([$("vf-process-list")],O);var ue=Object.defineProperty,fe=Object.getOwnPropertyDescriptor,Nt=(i,t,e,s)=>{for(var r=s>1?void 0:s?fe(t,e):t,o=i.length-1,n;o>=0;o--)(n=i[o])&&(r=(s?n(t,e,r):n(r))||r);return s&&r&&ue(t,e,r),r};let dt=class extends v{constructor(){super(...arguments),this.process=null}createRenderRoot(){return this}toTitleCase(t){return t.replace(/_/g," ").replace(/\w\S*/g,e=>e.charAt(0).toUpperCase()+e.substr(1).toLowerCase())}formatValue(t){if(!t)return"N/A";if(typeof t=="object")return JSON.stringify(t,null,2);const s=/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{6}\+\d{2}:\d{2}$/.test(t)?new Date(t):null;return s&&!isNaN(s.getTime())?s.toLocaleString():t}render(){var t;return a`
      <div class="bg-gray-400 text-white py-4">
        <h1 class="text-2xl text-center">Process #${(t=this.process)==null?void 0:t.id}</h1>
      </div>

      <div class="table-auto container mx-auto py-2 px-2">
        <table class="min-w-full bg-white border border-gray-200 rounded-lg">
          <tbody>
            ${Object.entries(this.process||{}).map(([e,s])=>a`
              <tr>
                <td class="border px-3 py-2 font-bold text-sm">${this.toTitleCase(e)}</td>
                <td class="border px-3 py-2 text-sm">${this.formatValue(s)}</td>
              </tr>
            `)}
          </tbody>
        </table>
      </div>
    `}};Nt([h({type:JSON})],dt.prototype,"process",2);dt=Nt([$("vf-process-detail")],dt);var ve=Object.defineProperty,ge=Object.getOwnPropertyDescriptor,F=(i,t,e,s)=>{for(var r=s>1?void 0:s?ge(t,e):t,o=i.length-1,n;o>=0;o--)(n=i[o])&&(r=(s?n(t,e,r):n(r))||r);return s&&r&&ve(t,e,r),r};let T=class extends v{constructor(){super(...arguments),this.url="",this.tasks=[],this.loading=!0,this.controller=new AbortController}createRenderRoot(){return this}disconnectedCallback(){super.disconnectedCallback(),this.controller.abort()}updated(i){i.has("url")&&this.fetchTasks()}async fetchTasks(){if(this.url)try{this.loading=!0;const i=await fetch(this.url,{signal:this.controller.signal});if(!i.ok)throw new Error("An error occurred while fetching the flow list.");const t=await i.json();this.tasks=t,this.tasks&&this.dispatchEvent(new CustomEvent("link-clicked",{detail:this.tasks[0]}))}catch(i){this.error=i.message||"An error occurred while fetching the flow list."}finally{this.loading=!1}}handleClick(i){const t=i.target,e=this.tasks.find(s=>s.id.toString()===t.textContent)||null;e&&this.dispatchEvent(new CustomEvent("link-clicked",{detail:e}))}renderSpin(){return a`
      <div class="flex justify-center items-center py-4 animate-spin-container">
        <div class="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    `}renderTableRow(i){return a`
      <tr>
        <td class="py-3 px-4 border-b border-gray-200 text-sm">
          <a href="#" @click=${this.handleClick}>${i.id}</a>
        </td>
        <td class="py-3 px-4 border-b border-gray-200 text-sm">${i.status}</td>
        <td class="py-3 px-4 border-b border-gray-200 text-sm">${i.brief}</td>
        <td class="py-3 px-4 border-b border-gray-200 text-sm">${i.process_brief}</td>
        <td class="py-3 px-4 border-b border-gray-200 text-sm">${new Date(i.created).toLocaleString()}</td>
      </tr>
    `}renderTable(){return a`
      <div class="container mx-auto py-2 px-2">
        <table class="min-w-full bg-white border border-gray-200 rounded-lg">
          <thead>
            <tr>
            <th class="py-3 px-4 border-b border-gray-200 bg-gray-100 text-left text-sm">#</th>
              <th class="py-3 px-4 border-b border-gray-200 bg-gray-100 text-left text-sm">Status</th>
              <th class="py-3 px-4 border-b border-gray-200 bg-gray-100 text-left text-sm">Task</th>
              <th class="py-3 px-4 border-b border-gray-200 bg-gray-100 text-left text-sm">Process Brief</th>
              <th class="py-3 px-4 border-b border-gray-200 bg-gray-100 text-left text-sm">Created</th>
            </tr>
          </thead>
          <tbody>
            ${this.tasks.map(i=>this.renderTableRow(i))}
          </tbody>
        </table>
      </div>
    `}renderErrorMessage(){return a`
      <div class="mt-4 text-red-500 error-message px-2">
        ${this.error}
      </div>
    `}render(){return a`
      <div class="bg-gray-500 text-white py-4">
        <h1 class="text-2xl text-center">Tasks</h1>
      </div>

      ${this.loading?this.renderSpin():this.renderTable()}
      ${this.error?this.renderErrorMessage():""}
    `}};F([h({type:String})],T.prototype,"url",2);F([h({type:Array})],T.prototype,"tasks",2);F([h({type:Boolean})],T.prototype,"loading",2);F([h({type:String})],T.prototype,"error",2);T=F([$("vf-task-list")],T);var $e=Object.defineProperty,ye=Object.getOwnPropertyDescriptor,Lt=(i,t,e,s)=>{for(var r=s>1?void 0:s?ye(t,e):t,o=i.length-1,n;o>=0;o--)(n=i[o])&&(r=(s?n(t,e,r):n(r))||r);return s&&r&&$e(t,e,r),r};let ct=class extends v{constructor(){super(...arguments),this.task=null}createRenderRoot(){return this}toTitleCase(i){return i.replace(/_/g," ").replace(/\w\S*/g,t=>t.charAt(0).toUpperCase()+t.substr(1).toLowerCase())}formatValue(i){if(!i)return"N/A";if(typeof i=="object")return JSON.stringify(i,null,2);const e=/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{6}\+\d{2}:\d{2}$/.test(i)?new Date(i):null;return e&&!isNaN(e.getTime())?e.toLocaleString():i}render(){var i,t,e,s,r,o;return a`
      <div class="bg-gray-400 text-white py-4">
        <h1 class="text-2xl text-center">Task #${(i=this.task)==null?void 0:i.id}</h1>
      </div>

      <div class="table-auto container mx-auto py-2 px-2">
        <table class="min-w-full bg-white border border-gray-200 rounded-lg">
          <tbody>
            <tr>
              <td class="border px-3 py-2 font-bold text-sm w-1/4">Title</td>
              <td class="border px-3 py-2 text-sm">${this.formatValue((t=this.task)==null?void 0:t.title)}</td>
            </tr>
            <tr>
              <td class="border px-3 py-2 font-bold text-sm">Description</td>
              <td class="border px-3 py-2 text-sm">${this.formatValue((e=this.task)==null?void 0:e.description)}</td>
            </tr>
            <tr>
              <td class="border px-3 py-2 font-bold text-sm">Brief</td>
              <td class="border px-3 py-2 text-sm">${this.formatValue((s=this.task)==null?void 0:s.brief)}</td>
            </tr>
            <tr>
              <td class="border px-3 py-2 font-bold text-sm">Status</td>
              <td class="border px-3 py-2 text-sm">${this.formatValue((r=this.task)==null?void 0:r.status)}</td>
            </tr>
            <tr>
              <td class="border px-3 py-2 font-bold text-sm">Details</td>
              <td class="border px-3 py-2 text-sm">${this.formatValue((o=this.task)==null?void 0:o.url)}</td>
            </tr>
          </tbody>
        </table>
      </div>
    `}};Lt([h({type:JSON})],ct.prototype,"task",2);ct=Lt([$("vf-task-detail")],ct);var be=Object.defineProperty,me=Object.getOwnPropertyDescriptor,Dt=(i,t,e,s)=>{for(var r=s>1?void 0:s?me(t,e):t,o=i.length-1,n;o>=0;o--)(n=i[o])&&(r=(s?n(t,e,r):n(r))||r);return s&&r&&be(t,e,r),r};let ht=class extends v{constructor(){super(...arguments),this.task=null}createRenderRoot(){return this}render(){return a`
    `}};Dt([h({type:JSON})],ht.prototype,"task",2);ht=Dt([$("vf-task-assign")],ht);var _e=Object.defineProperty,we=Object.getOwnPropertyDescriptor,V=(i,t,e,s)=>{for(var r=s>1?void 0:s?we(t,e):t,o=i.length-1,n;o>=0;o--)(n=i[o])&&(r=(s?n(t,e,r):n(r))||r);return s&&r&&_e(t,e,r),r};let R=class extends v{constructor(){super(...arguments),this.task=null,this.loading=!1}createRenderRoot(){return this}async submitForm(i){i.preventDefault();try{this.loading=!0;const t=new FormData(this.form);if(!(await fetch("/api/hellorest/task/start/",{method:"POST",body:t})).ok)throw new Error("An error occurred while submitting form.")}catch(t){this.error=t.message||"An error occurred while submitting form."}finally{this.loading=!1}}renderSpin(){return a`
      <div class="flex justify-center items-center py-4 animate-spin-container">
        <div class="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    `}renderButton(){return a`
      <button
        ?disabled=${this.loading}
        class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline" type="submit">
        Submit
      </button>
    `}renderErrorMessage(){return a`
      <div class="mt-4 text-red-500 error-message px-2">
        ${this.error}
      </div>
    `}render(){return a`
      <div class="bg-gray-400 text-white py-4">
        <h1 class="text-2xl text-center">Start</h1>
      </div>

      <div class="container mx-2 my-2 py-2 px-2 bg-white rounded-lg shadow-md">
        <form @submit="${this.submitForm}">
          <div class="mb-4">
            <label class="block text-gray-700 text-sm font-bold mb-2" for="text">
              Text
            </label>
            <input class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" id="text" type="text" name="text" placeholder="Enter text">
          </div>
          <div class="flex items-center justify-between">
            ${this.renderButton()}
          </div>
        </form>
        ${this.error?this.renderErrorMessage():""}
      </div>
    `}};V([h({type:JSON})],R.prototype,"task",2);V([h({type:Boolean})],R.prototype,"loading",2);V([h({type:String})],R.prototype,"error",2);V([ee("form")],R.prototype,"form",2);R=V([$("vf-hellorest-start")],R);var xe=Object.defineProperty,Ae=Object.getOwnPropertyDescriptor,jt=(i,t,e,s)=>{for(var r=s>1?void 0:s?Ae(t,e):t,o=i.length-1,n;o>=0;o--)(n=i[o])&&(r=(s?n(t,e,r):n(r))||r);return s&&r&&xe(t,e,r),r};let pt=class extends v{constructor(){super(...arguments),this.task=null}createRenderRoot(){return this}render(){return a`
    `}};jt([h({type:JSON})],pt.prototype,"task",2);pt=jt([$("vf-hellorest-approve")],pt);var Ee=Object.defineProperty,Se=Object.getOwnPropertyDescriptor,X=(i,t,e,s)=>{for(var r=s>1?void 0:s?Se(t,e):t,o=i.length-1,n;o>=0;o--)(n=i[o])&&(r=(s?n(t,e,r):n(r))||r);return s&&r&&Ee(t,e,r),r};let U=class extends v{constructor(){super(...arguments),this.selectedFlow=E,this.selectedList=E.process_list,this.selectedItem=null}createRenderRoot(){return this}handleFlowChange(i){this.selectedFlow=i.detail,this.selectedList=this.selectedFlow.process_list}handleListChange(i){this.selectedList=i.detail}handleProcessLinkClick(i){this.selectedItem={kind:"process",data:i.detail}}handleTaskLinkClick(i){this.selectedItem={kind:"task",data:i.detail}}handleActionLinkClick(i){this.selectedItem={kind:"action",data:i.detail}}renderDetailTab(){var i;switch((i=this.selectedItem)==null?void 0:i.kind){case"process":return a`<vf-process-detail class="w-3/12 bg-red-200" .process=${this.selectedItem.data}></vf-process-detail>`;case"task":return a`<vf-task-detail class="w-3/12 bg-red-200" .task=${this.selectedItem.data}></vf-task-detail>`;case"action":if(/\/api\/\w+\/task\/4\/approve\/\d+\/approve/.test(this.selectedItem.data))return a`<vf-task-assign class="w-3/12 bg-red-200" .task=${this.selectedItem.data}></vf-task-assign>`;if(this.selectedItem.data==="/api/hellorest/task/start/")return a`<vf-hellorest-start class="w-3/12 bg-red-200"></vf-hellorest-start>`;if(/\/api\/hellorest\/task\/4\/approve\/\d+/.test(this.selectedItem.data))return a`<vf-hellorest-approve class="w-3/12 bg-red-200" .task=${this.selectedItem.data}></vf-hellorest-approve>`}return a`
        <div class="w-3/12 bg-red-200">
          <div class="bg-gray-400 text-white py-4">
            <h1 class="text-2xl text-center">No active item</h1>
          </div>
        </div>
      `}render(){return a`
      <div class="flex min-h-screen w-screen">
        <vf-flows-list
          class="w-2/12 bg-gray-200"
          .selected=${this.selectedFlow}
          @link-clicked=${this.handleFlowChange}>
        </vf-flows-list>

        <vf-flow-menu
          class="w-2/12 bg-blue-200"
          .flow=${this.selectedFlow}
          @action-clicked=${this.handleActionLinkClick}
          @link-clicked=${this.handleListChange}>
        </vf-flow-menu>

        ${this.selectedList==this.selectedFlow.process_list?a`<vf-process-list
                  class="w-5/12 bg-green-200"
                  url=${this.selectedList}
                  @link-clicked="${this.handleProcessLinkClick}">
               </vf-process-list>
          `:a`<vf-task-list
                  class="w-5/12 bg-yellow-200"
                  url=${this.selectedList}
                  @link-clicked="${this.handleTaskLinkClick}">
               </vf-task-list>
          `}

        ${this.renderDetailTab()}
      </div>
    `}};X([h({type:JSON})],U.prototype,"selectedFlow",2);X([h({type:JSON})],U.prototype,"selectedList",2);X([h({type:JSON})],U.prototype,"selectedItem",2);U=X([$("vf-app")],U);
