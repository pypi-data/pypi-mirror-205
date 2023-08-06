/*! For license information please see 36187-4FxcNqM8WuY.js.LICENSE.txt */
"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[36187],{51644:(e,t,n)=>{n.d(t,{$:()=>i,P:()=>r});n(56299),n(26110);var o=n(8621),a=n(87156);const i={properties:{pressed:{type:Boolean,readOnly:!0,value:!1,reflectToAttribute:!0,observer:"_pressedChanged"},toggles:{type:Boolean,value:!1,reflectToAttribute:!0},active:{type:Boolean,value:!1,notify:!0,reflectToAttribute:!0},pointerDown:{type:Boolean,readOnly:!0,value:!1},receivedFocusFromKeyboard:{type:Boolean,readOnly:!0},ariaActiveAttribute:{type:String,value:"aria-pressed",observer:"_ariaActiveAttributeChanged"}},listeners:{down:"_downHandler",up:"_upHandler",tap:"_tapHandler"},observers:["_focusChanged(focused)","_activeChanged(active, ariaActiveAttribute)"],keyBindings:{"enter:keydown":"_asyncClick","space:keydown":"_spaceKeyDownHandler","space:keyup":"_spaceKeyUpHandler"},_mouseEventRe:/^mouse/,_tapHandler:function(){this.toggles?this._userActivate(!this.active):this.active=!1},_focusChanged:function(e){this._detectKeyboardFocus(e),e||this._setPressed(!1)},_detectKeyboardFocus:function(e){this._setReceivedFocusFromKeyboard(!this.pointerDown&&e)},_userActivate:function(e){this.active!==e&&(this.active=e,this.fire("change"))},_downHandler:function(e){this._setPointerDown(!0),this._setPressed(!0),this._setReceivedFocusFromKeyboard(!1)},_upHandler:function(){this._setPointerDown(!1),this._setPressed(!1)},_spaceKeyDownHandler:function(e){var t=e.detail.keyboardEvent,n=(0,a.vz)(t).localTarget;this.isLightDescendant(n)||(t.preventDefault(),t.stopImmediatePropagation(),this._setPressed(!0))},_spaceKeyUpHandler:function(e){var t=e.detail.keyboardEvent,n=(0,a.vz)(t).localTarget;this.isLightDescendant(n)||(this.pressed&&this._asyncClick(),this._setPressed(!1))},_asyncClick:function(){this.async((function(){this.click()}),1)},_pressedChanged:function(e){this._changedButtonState()},_ariaActiveAttributeChanged:function(e,t){t&&t!=e&&this.hasAttribute(t)&&this.removeAttribute(t)},_activeChanged:function(e,t){this.toggles?this.setAttribute(this.ariaActiveAttribute,e?"true":"false"):this.removeAttribute(this.ariaActiveAttribute),this._changedButtonState()},_controlStateChanged:function(){this.disabled?this._setPressed(!1):this._changedButtonState()},_changedButtonState:function(){this._buttonStateChanged&&this._buttonStateChanged()}},r=[o.G,i]},70019:(e,t,n)=>{n(56299);const o=n(50856).d`<custom-style>
  <style is="custom-style">
    html {

      /* Shared Styles */
      --paper-font-common-base: {
        font-family: 'Roboto', 'Noto', sans-serif;
        -webkit-font-smoothing: antialiased;
      };

      --paper-font-common-code: {
        font-family: 'Roboto Mono', 'Consolas', 'Menlo', monospace;
        -webkit-font-smoothing: antialiased;
      };

      --paper-font-common-expensive-kerning: {
        text-rendering: optimizeLegibility;
      };

      --paper-font-common-nowrap: {
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
      };

      /* Material Font Styles */

      --paper-font-display4: {
        @apply --paper-font-common-base;
        @apply --paper-font-common-nowrap;

        font-size: 112px;
        font-weight: 300;
        letter-spacing: -.044em;
        line-height: 120px;
      };

      --paper-font-display3: {
        @apply --paper-font-common-base;
        @apply --paper-font-common-nowrap;

        font-size: 56px;
        font-weight: 400;
        letter-spacing: -.026em;
        line-height: 60px;
      };

      --paper-font-display2: {
        @apply --paper-font-common-base;

        font-size: 45px;
        font-weight: 400;
        letter-spacing: -.018em;
        line-height: 48px;
      };

      --paper-font-display1: {
        @apply --paper-font-common-base;

        font-size: 34px;
        font-weight: 400;
        letter-spacing: -.01em;
        line-height: 40px;
      };

      --paper-font-headline: {
        @apply --paper-font-common-base;

        font-size: 24px;
        font-weight: 400;
        letter-spacing: -.012em;
        line-height: 32px;
      };

      --paper-font-title: {
        @apply --paper-font-common-base;
        @apply --paper-font-common-nowrap;

        font-size: 20px;
        font-weight: 500;
        line-height: 28px;
      };

      --paper-font-subhead: {
        @apply --paper-font-common-base;

        font-size: 16px;
        font-weight: 400;
        line-height: 24px;
      };

      --paper-font-body2: {
        @apply --paper-font-common-base;

        font-size: 14px;
        font-weight: 500;
        line-height: 24px;
      };

      --paper-font-body1: {
        @apply --paper-font-common-base;

        font-size: 14px;
        font-weight: 400;
        line-height: 20px;
      };

      --paper-font-caption: {
        @apply --paper-font-common-base;
        @apply --paper-font-common-nowrap;

        font-size: 12px;
        font-weight: 400;
        letter-spacing: 0.011em;
        line-height: 20px;
      };

      --paper-font-menu: {
        @apply --paper-font-common-base;
        @apply --paper-font-common-nowrap;

        font-size: 13px;
        font-weight: 500;
        line-height: 24px;
      };

      --paper-font-button: {
        @apply --paper-font-common-base;
        @apply --paper-font-common-nowrap;

        font-size: 14px;
        font-weight: 500;
        letter-spacing: 0.018em;
        line-height: 24px;
        text-transform: uppercase;
      };

      --paper-font-code2: {
        @apply --paper-font-common-code;

        font-size: 14px;
        font-weight: 700;
        line-height: 20px;
      };

      --paper-font-code1: {
        @apply --paper-font-common-code;

        font-size: 14px;
        font-weight: 500;
        line-height: 20px;
      };

    }

  </style>
</custom-style>`;o.setAttribute("style","display: none;"),document.head.appendChild(o.content)},79021:(e,t,n)=>{n.d(t,{Z:()=>r});var o=n(90394),a=n(34327),i=n(23682);function r(e,t){(0,i.Z)(2,arguments);var n=(0,a.Z)(e),r=(0,o.Z)(t);return isNaN(r)?new Date(NaN):r?(n.setDate(n.getDate()+r),n):n}},59699:(e,t,n)=>{n.d(t,{Z:()=>s});var o=n(90394),a=n(39244),i=n(23682),r=36e5;function s(e,t){(0,i.Z)(2,arguments);var n=(0,o.Z)(t);return(0,a.Z)(e,n*r)}},39244:(e,t,n)=>{n.d(t,{Z:()=>r});var o=n(90394),a=n(34327),i=n(23682);function r(e,t){(0,i.Z)(2,arguments);var n=(0,a.Z)(e).getTime(),r=(0,o.Z)(t);return new Date(n+r)}},32182:(e,t,n)=>{n.d(t,{Z:()=>r});var o=n(90394),a=n(34327),i=n(23682);function r(e,t){(0,i.Z)(2,arguments);var n=(0,a.Z)(e),r=(0,o.Z)(t);if(isNaN(r))return new Date(NaN);if(!r)return n;var s=n.getDate(),p=new Date(n.getTime());return p.setMonth(n.getMonth()+r+1,0),s>=p.getDate()?p:(n.setFullYear(p.getFullYear(),p.getMonth(),s),n)}},33651:(e,t,n)=>{n.d(t,{Z:()=>r});var o=n(90394),a=n(79021),i=n(23682);function r(e,t){(0,i.Z)(2,arguments);var n=7*(0,o.Z)(t);return(0,a.Z)(e,n)}},27605:(e,t,n)=>{n.d(t,{Z:()=>r});var o=n(90394),a=n(32182),i=n(23682);function r(e,t){(0,i.Z)(2,arguments);var n=(0,o.Z)(t);return(0,a.Z)(e,12*n)}},93752:(e,t,n)=>{n.d(t,{Z:()=>i});var o=n(34327),a=n(23682);function i(e){(0,a.Z)(1,arguments);var t=(0,o.Z)(e);return t.setHours(23,59,59,999),t}},1905:(e,t,n)=>{n.d(t,{Z:()=>i});var o=n(34327),a=n(23682);function i(e){(0,a.Z)(1,arguments);var t=(0,o.Z)(e),n=t.getMonth();return t.setFullYear(t.getFullYear(),n+1,0),t.setHours(23,59,59,999),t}},70390:(e,t,n)=>{n.d(t,{Z:()=>a});var o=n(93752);function a(){return(0,o.Z)(Date.now())}},59281:(e,t,n)=>{n.d(t,{Z:()=>s});var o=n(55020),a=n(34327),i=n(90394),r=n(23682);function s(e,t){var n,s,p,l,c,u,f,d;(0,r.Z)(1,arguments);var h=(0,o.j)(),g=(0,i.Z)(null!==(n=null!==(s=null!==(p=null!==(l=null==t?void 0:t.weekStartsOn)&&void 0!==l?l:null==t||null===(c=t.locale)||void 0===c||null===(u=c.options)||void 0===u?void 0:u.weekStartsOn)&&void 0!==p?p:h.weekStartsOn)&&void 0!==s?s:null===(f=h.locale)||void 0===f||null===(d=f.options)||void 0===d?void 0:d.weekStartsOn)&&void 0!==n?n:0);if(!(g>=0&&g<=6))throw new RangeError("weekStartsOn must be between 0 and 6 inclusively");var v=(0,a.Z)(e),m=v.getDay(),y=6+(m<g?-7:0)-(m-g);return v.setDate(v.getDate()+y),v.setHours(23,59,59,999),v}},70451:(e,t,n)=>{n.d(t,{Z:()=>i});var o=n(34327),a=n(23682);function i(e){(0,a.Z)(1,arguments);var t=(0,o.Z)(e),n=t.getFullYear();return t.setFullYear(n+1,0,0),t.setHours(23,59,59,999),t}},47538:(e,t,n)=>{function o(){var e=new Date,t=e.getFullYear(),n=e.getMonth(),o=e.getDate(),a=new Date(0);return a.setFullYear(t,n,o-1),a.setHours(23,59,59,999),a}n.d(t,{Z:()=>o})},82045:(e,t,n)=>{n.d(t,{Z:()=>i});var o=n(34327),a=n(23682);function i(e,t){(0,a.Z)(2,arguments);var n=(0,o.Z)(e).getTime(),i=(0,o.Z)(t.start).getTime(),r=(0,o.Z)(t.end).getTime();if(!(i<=r))throw new RangeError("Invalid interval");return n>=i&&n<=r}},13250:(e,t,n)=>{n.d(t,{Z:()=>i});var o=n(34327),a=n(23682);function i(e){(0,a.Z)(1,arguments);var t=(0,o.Z)(e);return t.setDate(1),t.setHours(0,0,0,0),t}},27088:(e,t,n)=>{n.d(t,{Z:()=>a});var o=n(59429);function a(){return(0,o.Z)(Date.now())}},69388:(e,t,n)=>{n.d(t,{Z:()=>i});var o=n(34327),a=n(23682);function i(e){(0,a.Z)(1,arguments);var t=(0,o.Z)(e),n=new Date(0);return n.setFullYear(t.getFullYear(),0,1),n.setHours(0,0,0,0),n}},83008:(e,t,n)=>{function o(){var e=new Date,t=e.getFullYear(),n=e.getMonth(),o=e.getDate(),a=new Date(0);return a.setFullYear(t,n,o-1),a.setHours(0,0,0,0),a}n.d(t,{Z:()=>o})}}]);
//# sourceMappingURL=36187-4FxcNqM8WuY.js.map