(this.webpackJsonpstreamlit_lang_tts=this.webpackJsonpstreamlit_lang_tts||[]).push([[0],{24:function(e,t,s){"use strict";s.r(t);var n=s(6),r=s.n(n),i=s(15),c=s.n(i),o=s(0),a=s(1),l=s(2),p=s(3),d=s(13),h=s(5),u=function(e){Object(l.a)(s,e);var t=Object(p.a)(s);function s(){var e;Object(a.a)(this,s);for(var n=arguments.length,r=new Array(n),i=0;i<n;i++)r[i]=arguments[i];return(e=t.call.apply(t,[this].concat(r))).state={textToSpeak:e.props.args.name,isFocused:!1},e.render=function(){var t=e.props.args.name,s=e.props.args.label||"AI:",n=e.props.args.translation,r=e.props.theme,i={};if(r){var c="0px solid ".concat(e.state.isFocused?r.primaryColor:"gray");i.border=c,i.outline=c,i.border="1px solid gray",i.fontSize="20px",i.padding="3px",i.background="lightgray",i.borderRadius="5px",i.width="70px",i.height="70px",i.marginLeft="10px"}return Object(h.jsx)("div",{children:Object(h.jsxs)("div",{style:{display:"flex"},children:[Object(h.jsx)("div",{style:{width:"70px"},children:Object(h.jsx)("p",{children:Object(h.jsx)("span",{style:{fontWeight:"bold"},children:s})})}),Object(h.jsxs)("div",{style:{flex:"1"},children:[Object(h.jsxs)("p",{children:[t," \xa0"]}),Object(h.jsx)("p",{style:{fontStyle:"italic"},children:n})]}),Object(h.jsx)("button",{style:i,onClick:e.onClicked,disabled:e.props.disabled,onFocus:e._onFocus,onBlur:e._onBlur,children:"\ud83d\udde3"})]})})},e.onClicked=function(){e.state.textToSpeak;var t=new window.SpeechSynthesisUtterance,s=window.speechSynthesis.getVoices().filter((function(e){return"com.apple.voice.compact.es-ES.Monica"===e.voiceURI}))[0];t.text=e.props.args.name,t.voice=s,t.rate=.8,window.speechSynthesis.speak(t)},e._onFocus=function(){e.setState({isFocused:!0})},e._onBlur=function(){e.setState({isFocused:!1})},e}return Object(o.a)(s)}(d.a),b=Object(d.b)(u);c.a.render(Object(h.jsx)(r.a.StrictMode,{children:Object(h.jsx)(b,{})}),document.getElementById("root"))}},[[24,1,2]]]);
//# sourceMappingURL=main.d75feb69.chunk.js.map