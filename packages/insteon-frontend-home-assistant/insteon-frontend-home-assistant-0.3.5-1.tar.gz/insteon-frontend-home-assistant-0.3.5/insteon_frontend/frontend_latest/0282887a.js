"use strict";(self.webpackChunkinsteon_panel_frontend=self.webpackChunkinsteon_panel_frontend||[]).push([[969],{969:(e,t,i)=>{i.r(t);var r=i(7500),o=i(7626),n=(i(2678),i(9293),i(4516)),s=(i(9098),i(1007),i(1750));function a(){a=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var o=t.placement;if(t.kind===r&&("static"===o||"prototype"===o)){var n="static"===o?e:i;this.defineClassElement(n,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],o={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,o)}),this),e.forEach((function(e){if(!d(e))return i.push(e);var t=this.decorateElement(e,o);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var n=this.decorateConstructor(i,t);return r.push.apply(r,n.finishers),n.finishers=r,n},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],o=e.decorators,n=o.length-1;n>=0;n--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,o[n])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);i.push.apply(i,c)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var o=this.fromClassDescriptor(e),n=this.toClassDescriptor((0,t[r])(o)||o);if(void 0!==n.finisher&&i.push(n.finisher),void 0!==n.elements){e=n.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return f(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?f(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=u(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var o=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var n={kind:t,key:i,placement:r,descriptor:Object.assign({},o)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(o,"get","The property descriptor of a field descriptor"),this.disallowProperty(o,"set","The property descriptor of a field descriptor"),this.disallowProperty(o,"value","The property descriptor of a field descriptor"),n.initializer=e.initializer),n},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:p(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=p(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function l(e){var t,i=u(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function c(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function d(e){return e.decorators&&e.decorators.length}function h(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function p(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function u(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function f(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}!function(e,t,i,r){var o=a();if(r)for(var n=0;n<r.length;n++)o=r[n](o);var s=t((function(e){o.initializeInstanceElements(e,p.elements)}),i),p=o.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===n.key&&e.placement===n.placement},r=0;r<e.length;r++){var o,n=e[r];if("method"===n.kind&&(o=t.find(i)))if(h(n.descriptor)||h(o.descriptor)){if(d(n)||d(o))throw new ReferenceError("Duplicated methods ("+n.key+") can't be decorated.");o.descriptor=n.descriptor}else{if(d(n)){if(d(o))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+n.key+").");o.decorators=n.decorators}c(n,o)}else t.push(n)}return t}(s.d.map(l)),e);o.initializeClassElements(s.F,p.elements),o.runClassFinishers(s.F,p.finishers)}([(0,o.Mo)("insteon-properties-data-table")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"insteon",value:void 0},{kind:"field",decorators:[(0,o.Cb)({type:Boolean})],key:"narrow",value:()=>!1},{kind:"field",decorators:[(0,o.Cb)({type:Array})],key:"records",value:()=>[]},{kind:"field",decorators:[(0,o.Cb)()],key:"schema",value:()=>({})},{kind:"field",decorators:[(0,o.Cb)()],key:"noDataText",value:void 0},{kind:"field",decorators:[(0,o.Cb)({type:Boolean})],key:"showWait",value:()=>!1},{kind:"field",key:"_records",value(){return(0,n.Z)((e=>e.map((e=>({description:this._calcDescription(e.name),display_value:this._translateValue(e.name,e.value),...e})))))}},{kind:"method",key:"_calcDescription",value:function(e){return e.startsWith("toggle_")?this.insteon.localize("properties.descriptions.button")+" "+this._calcButtonName(e)+" "+this.insteon.localize("properties.descriptions.toggle"):e.startsWith("radio_button_group_")?this.insteon.localize("properties.descriptions.radio_button_group")+" "+this._calcButtonName(e):this.insteon.localize("properties.descriptions."+e)}},{kind:"method",key:"_calcButtonName",value:function(e){return e.endsWith("main")?this.insteon.localize("properties.descriptions.main"):e.substr(-1,1).toUpperCase()}},{kind:"field",key:"_columns",value(){return(0,n.Z)((e=>e?{name:{title:this.insteon.localize("properties.fields.name"),sortable:!0,grows:!0},modified:{title:this.insteon.localize("properties.fields.modified"),template:e=>e?r.dy`${this.hass.localize("ui.common.yes")}`:r.dy`${this.hass.localize("ui.common.no")}`,sortable:!0,width:"20%"},display_value:{title:this.insteon.localize("properties.fields.value"),sortable:!0,width:"20%"}}:{name:{title:this.insteon.localize("properties.fields.name"),sortable:!0,width:"20%"},description:{title:this.insteon.localize("properties.fields.description"),sortable:!0,grows:!0},modified:{title:this.insteon.localize("properties.fields.modified"),template:e=>e?r.dy`${this.hass.localize("ui.common.yes")}`:r.dy`${this.hass.localize("ui.common.no")}`,sortable:!0,width:"20%"},display_value:{title:this.insteon.localize("properties.fields.value"),sortable:!0,width:"20%"}}))}},{kind:"method",key:"render",value:function(){return this.showWait?r.dy`
        <ha-circular-progress class="fullwidth" active alt="Loading"></ha-circular-progress>
      `:r.dy`
      <ha-data-table
        .columns=${this._columns(this.narrow)}
        .data=${this._records(this.records)}
        .id=${"name"}
        .dir=${(0,s.Zu)(this.hass)}
        noDataText="${this.noDataText}"
      ></ha-data-table>
    `}},{kind:"method",key:"_translateValue",value:function(e,t){const i=this.schema[e];if("radio_button_groups"==i.name)return t.length+" groups";if("multi_select"===i.type&&Array.isArray(t))return t.map((e=>i.options[e])).join(", ");if("select"===i.type){var r;return(null===(r=i.options)||void 0===r?void 0:r.reduce(((e,t)=>({...e,[t[0]]:t[1]})),{}))[t.toString()]}return t}},{kind:"get",static:!0,key:"styles",value:function(){return r.iv`
      ha-circular-progress {
        align-items: center;
        justify-content: center;
        padding: 8px;
        box-sizing: border-box;
        width: 100%;
        flex-grow: 1;
      }
    `}}]}}),r.oi);var m=i(8846),v=i(8394);const y=()=>Promise.all([i.e(5084),i.e(8348),i.e(9663),i.e(4507)]).then(i.bind(i,9546));var w=i(1285),k=(i(841),i(8395)),b=i(1155);i(5878);function g(){g=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var o=t.placement;if(t.kind===r&&("static"===o||"prototype"===o)){var n="static"===o?e:i;this.defineClassElement(n,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],o={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,o)}),this),e.forEach((function(e){if(!z(e))return i.push(e);var t=this.decorateElement(e,o);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var n=this.decorateConstructor(i,t);return r.push.apply(r,n.finishers),n.finishers=r,n},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],o=e.decorators,n=o.length-1;n>=0;n--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,o[n])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);i.push.apply(i,c)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var o=this.fromClassDescriptor(e),n=this.toClassDescriptor((0,t[r])(o)||o);if(void 0!==n.finisher&&i.push(n.finisher),void 0!==n.elements){e=n.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return C(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?C(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=P(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var o=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var n={kind:t,key:i,placement:r,descriptor:Object.assign({},o)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(o,"get","The property descriptor of a field descriptor"),this.disallowProperty(o,"set","The property descriptor of a field descriptor"),this.disallowProperty(o,"value","The property descriptor of a field descriptor"),n.initializer=e.initializer),n},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:A(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=A(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function _(e){var t,i=P(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function E(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function z(e){return e.decorators&&e.decorators.length}function x(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function A(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function P(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function C(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}function T(){return T="undefined"!=typeof Reflect&&Reflect.get?Reflect.get.bind():function(e,t,i){var r=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=$(e)););return e}(e,t);if(r){var o=Object.getOwnPropertyDescriptor(r,t);return o.get?o.get.call(arguments.length<3?e:i):o.value}},T.apply(this,arguments)}function $(e){return $=Object.setPrototypeOf?Object.getPrototypeOf.bind():function(e){return e.__proto__||Object.getPrototypeOf(e)},$(e)}const D="M12,16A2,2 0 0,1 14,18A2,2 0 0,1 12,20A2,2 0 0,1 10,18A2,2 0 0,1 12,16M12,10A2,2 0 0,1 14,12A2,2 0 0,1 12,14A2,2 0 0,1 10,12A2,2 0 0,1 12,10M12,4A2,2 0 0,1 14,6A2,2 0 0,1 12,8A2,2 0 0,1 10,6A2,2 0 0,1 12,4Z";!function(e,t,i,r){var o=g();if(r)for(var n=0;n<r.length;n++)o=r[n](o);var s=t((function(e){o.initializeInstanceElements(e,a.elements)}),i),a=o.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===n.key&&e.placement===n.placement},r=0;r<e.length;r++){var o,n=e[r];if("method"===n.kind&&(o=t.find(i)))if(x(n.descriptor)||x(o.descriptor)){if(z(n)||z(o))throw new ReferenceError("Duplicated methods ("+n.key+") can't be decorated.");o.descriptor=n.descriptor}else{if(z(n)){if(z(o))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+n.key+").");o.decorators=n.decorators}E(n,o)}else t.push(n)}return t}(s.d.map(_)),e);o.initializeClassElements(s.F,a.elements),o.runClassFinishers(s.F,a.finishers)}([(0,o.Mo)("insteon-device-properties-page")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"insteon",value:void 0},{kind:"field",decorators:[(0,o.Cb)({type:Boolean,reflect:!0})],key:"narrow",value:void 0},{kind:"field",decorators:[(0,o.Cb)({type:Boolean})],key:"isWide",value:void 0},{kind:"field",decorators:[(0,o.Cb)({type:Object})],key:"route",value:void 0},{kind:"field",decorators:[(0,o.Cb)()],key:"deviceId",value:void 0},{kind:"field",decorators:[(0,o.SB)()],key:"_device",value:void 0},{kind:"field",decorators:[(0,o.SB)()],key:"_properties",value:()=>[]},{kind:"field",decorators:[(0,o.SB)()],key:"_schema",value:void 0},{kind:"field",decorators:[(0,o.SB)()],key:"_showWait",value:()=>!1},{kind:"field",decorators:[(0,o.SB)()],key:"_showAdvanced",value:()=>!1},{kind:"field",key:"_showHideAdvanced",value:()=>"show"},{kind:"method",key:"firstUpdated",value:function(e){T($(i.prototype),"firstUpdated",this).call(this,e),this.deviceId&&this.hass&&(0,m.zM)(this.hass,this.deviceId).then((e=>{this._device=e,this._getProperties()}),(()=>{this._noDeviceError()}))}},{kind:"method",key:"_dirty",value:function(){var e;return null===(e=this._properties)||void 0===e?void 0:e.reduce(((e,t)=>e||t.modified),!1)}},{kind:"method",key:"render",value:function(){var e,t;return r.dy`
      <hass-tabs-subpage
        .hass=${this.hass}
        .narrow=${this.narrow}
        .route=${this.route}
        .tabs=${k.insteonDeviceTabs}
        .localizeFunc=${this.insteon.localize}
        .backCallback=${async()=>this._handleBackTapped()}
      >
        ${this.narrow?r.dy`
                <!-- <span slot="header"> -->
                <div slot="header" class="header fullwidth">
                  <div slot="header" class="narrow-header-left">
                    ${null===(e=this._device)||void 0===e?void 0:e.name}
                  </div>
                  <div slot="header" class="narrow-header-right">
                    <ha-button-menu
                      corner="BOTTOM_START"
                      @action=${this._handleMenuAction}
                      activatable
                    >
                      <ha-icon-button
                        slot="trigger"
                        .label=${this.hass.localize("ui.common.menu")}
                        .path=${D}
                      ></ha-icon-button>

                      <mwc-list-item>
                        ${this.insteon.localize("properties.actions."+this._showHideAdvanced)}
                      </mwc-list-item>
                      <mwc-list-item>
                        ${this.insteon.localize("common.actions.load")}
                      </mwc-list-item>
                      <mwc-list-item .disabled=${!this._dirty()}>
                        ${this.insteon.localize("common.actions.write")}
                      </mwc-list-item>
                      <mwc-list-item .disabled=${!this._dirty()}>
                        ${this.insteon.localize("common.actions.reset")}
                      </mwc-list-item>
                    </ha-button-menu>
                  </div>
                </div>
                <!-- </span> -->
              `:""}
        <div class="container">
          ${this.narrow?"":r.dy`
                  <div class="page-header fullwidth">
                    <div class="device-name">
                      <h1>${null===(t=this._device)||void 0===t?void 0:t.name}</h1>
                    </div>
                    <div class="logo header-right">
                      <img
                        src="https://brands.home-assistant.io/insteon/logo.png"
                        referrerpolicy="no-referrer"
                        @load=${this._onImageLoad}
                        @error=${this._onImageError}
                      />
                    </div>
                  </div>
                  <div class="page-header fullwidth">
                    <div class="header-right">
                      <div slot="header" class="actions header-right">
                        <mwc-button @click=${this._onLoadPropertiesClick}>
                          ${this.insteon.localize("common.actions.load")}
                        </mwc-button>
                        <mwc-button
                          .disabled=${!this._dirty()}
                          @click=${this._onWritePropertiesClick}
                        >
                          ${this.insteon.localize("common.actions.write")}
                        </mwc-button>
                        <mwc-button
                          .disabled=${!this._dirty()}
                          @click=${this._onResetPropertiesClick}
                        >
                          ${this.insteon.localize("common.actions.reset")}
                        </mwc-button>
                        <ha-button-menu
                          corner="BOTTOM_START"
                          @action=${this._handleMenuAction}
                          activatable
                        >
                          <ha-icon-button
                            slot="trigger"
                            .label=${this.hass.localize("ui.common.menu")}
                            .path=${D}
                          ></ha-icon-button>

                          <mwc-list-item>
                            ${this.insteon.localize("properties.actions."+this._showHideAdvanced)}
                          </mwc-list-item>
                        </ha-button-menu>
                      </div>
                    </div>
                  </div>
                `}
          </div>
          <insteon-properties-data-table
            .hass=${this.hass}
            .insteon=${this.insteon}
            .narrow=${this.narrow}
            .records=${this._properties}
            .schema=${this._schema}
            noDataText=${this.insteon.localize("properties.no_data")}
            @row-click=${this._handleRowClicked}
            .showWait=${this._showWait}
          ></insteon-properties-data-table>
        </div>
      </hass-tabs-subpage>
    `}},{kind:"method",key:"_onImageLoad",value:function(e){e.target.style.display="inline-block"}},{kind:"method",key:"_onImageError",value:function(e){e.target.style.display="none"}},{kind:"method",key:"_onLoadPropertiesClick",value:async function(){await(0,w.g7)(this,{text:this.insteon.localize("common.warn.load"),confirmText:this.hass.localize("ui.common.yes"),dismissText:this.hass.localize("ui.common.no"),confirm:async()=>this._load()})}},{kind:"method",key:"_load",value:async function(){this._device.is_battery&&await(0,w.Ys)(this,{text:this.insteon.localize("common.warn.wake_up")}),this._showWait=!0;try{await(0,m.tw)(this.hass,this._device.address)}catch(e){(0,w.Ys)(this,{text:this.insteon.localize("common.error.load"),confirmText:this.hass.localize("ui.common.close")})}this._showWait=!1}},{kind:"method",key:"_onWritePropertiesClick",value:async function(){await(0,w.g7)(this,{text:this.insteon.localize("common.warn.write"),confirmText:this.hass.localize("ui.common.yes"),dismissText:this.hass.localize("ui.common.no"),confirm:async()=>this._write()})}},{kind:"method",key:"_write",value:async function(){this._device.is_battery&&await(0,w.Ys)(this,{text:this.insteon.localize("common.warn.wake_up")}),this._showWait=!0;try{await(0,m.CN)(this.hass,this._device.address)}catch(e){(0,w.Ys)(this,{text:this.insteon.localize("common.error.write"),confirmText:this.hass.localize("ui.common.close")})}this._getProperties(),this._showWait=!1}},{kind:"method",key:"_getProperties",value:async function(){const e=await(0,m.NC)(this.hass,this._device.address,this._showAdvanced);console.info("Properties: "+e.properties.length),this._properties=e.properties,this._schema=this._translateSchema(e.schema)}},{kind:"method",key:"_onResetPropertiesClick",value:async function(){(0,m.di)(this.hass,this._device.address),this._getProperties()}},{kind:"method",key:"_handleRowClicked",value:async function(e){const t=e.detail.id,i=this._properties.find((e=>e.name===t)),r=this._schema[i.name];var o,n;o=this,n={hass:this.hass,insteon:this.insteon,schema:[r],record:i,title:this.insteon.localize("properties.actions.change"),callback:async(e,t)=>this._handlePropertyChange(e,t)},(0,v.B)(o,"show-dialog",{dialogTag:"dialog-insteon-property",dialogImport:y,dialogParams:n}),history.back()}},{kind:"method",key:"_handlePropertyChange",value:async function(e,t){(0,m.SL)(this.hass,this._device.address,e,t),this._getProperties()}},{kind:"method",key:"_handleBackTapped",value:async function(){this._dirty()?await(0,w.g7)(this,{text:this.hass.localize("ui.panel.config.common.editor.confirm_unsaved"),confirmText:this.hass.localize("ui.common.yes"),dismissText:this.hass.localize("ui.common.no"),confirm:()=>this._goBack()}):(0,b.c)("/insteon/devices")}},{kind:"method",key:"_handleMenuAction",value:async function(e){switch(e.detail.index){case 0:await this._onShowHideAdvancedClicked();break;case 1:await this._onLoadPropertiesClick();break;case 2:await this._onWritePropertiesClick();break;case 3:await this._onResetPropertiesClick()}}},{kind:"method",key:"_onShowHideAdvancedClicked",value:async function(){this._showAdvanced=!this._showAdvanced,this._showAdvanced?this._showHideAdvanced="hide":this._showHideAdvanced="show",this._getProperties()}},{kind:"method",key:"_goBack",value:function(){(0,m.di)(this.hass,this._device.address),(0,b.c)("/insteon/devices")}},{kind:"method",key:"_noDeviceError",value:function(){(0,w.Ys)(this,{text:this.insteon.localize("common.error.device_not_found")}),this._goBack()}},{kind:"method",key:"_translateSchema",value:function(e){const t={...e};return Object.entries(t).forEach((([e,t])=>{t.description||(t.description={}),t.description[e]=this.insteon.localize("properties.descriptions."+e),"multi_select"===t.type&&Object.entries(t.options).forEach((([e,i])=>{isNaN(+i)?t.options[e]=this.insteon.localize("properties.form_options."+i):t.options[e]=i})),"select"===t.type&&Object.entries(t.options).forEach((([e,[i,r]])=>{isNaN(+r)?t.options[e][1]=this.insteon.localize("properties.form_options."+r):t.options[e][1]=r}))})),e}},{kind:"get",static:!0,key:"styles",value:function(){return r.iv`
      :host {
        --app-header-background-color: var(--sidebar-background-color);
        --app-header-text-color: var(--sidebar-text-color);
        --app-header-border-bottom: 1px solid var(--divider-color);
      }

      :host([narrow]) {
        --properties-table-height: 86vh;
      }

      :host(:not([narrow])) {
        --properties-table-height: 80vh;
      }

      .header {
        display: flex;
        justify-content: space-between;
      }

      .container {
        display: flex;
        flex-wrap: wrap;
        margin: 0px;
      }

      insteon-properties-data-table {
        width: 100%;
        height: var(--properties-table-height);
        display: block;
        --data-table-border-width: 0;
      }

      h1 {
        margin: 0;
        font-family: var(--paper-font-headline_-_font-family);
        -webkit-font-smoothing: var(
          --paper-font-headline_-_-webkit-font-smoothing
        );
        font-size: var(--paper-font-headline_-_font-size);
        font-weight: var(--paper-font-headline_-_font-weight);
        letter-spacing: var(--paper-font-headline_-_letter-spacing);
        line-height: var(--paper-font-headline_-_line-height);
        opacity: var(--dark-primary-opacity);
      }

      .page-header {
        padding: 8px;
        margin-left: 32px;
        margin-right: 32px;
        display: flex;
        justify-content: space-between;
      }

      .fullwidth {
        padding: 8px;
        box-sizing: border-box;
        width: 100%;
        flex-grow: 1;
      }

      .header-right {
        align-self: center;
        display: flex;
      }

      .header-right img {
        height: 30px;
      }

      .header-right:first-child {
        width: 100%;
        justify-content: flex-end;
      }

      .actions mwc-button {
        margin: 8px;
      }

      :host([narrow]) .container {
        margin-top: 0;
      }

      .narrow-header-left {
        padding: 8px;
        width: 90%;
      }
      .narrow-header-right {
        align-self: right;
      }
    `}}]}}),r.oi)}}]);
//# sourceMappingURL=0282887a.js.map