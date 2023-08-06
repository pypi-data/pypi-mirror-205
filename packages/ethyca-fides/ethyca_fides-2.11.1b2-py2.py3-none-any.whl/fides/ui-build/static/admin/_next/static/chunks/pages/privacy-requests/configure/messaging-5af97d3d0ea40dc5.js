(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[8593],{11739:function(e,i,n){"use strict";n.d(i,{At:function(){return h},aG:function(){return x},gN:function(){return f}});var t=n(81439),r=n(15031),s=n(26450),a=n(67294);function c(){return c=Object.assign||function(e){for(var i=1;i<arguments.length;i++){var n=arguments[i];for(var t in n)Object.prototype.hasOwnProperty.call(n,t)&&(e[t]=n[t])}return e},c.apply(this,arguments)}function o(e,i){if(null==e)return{};var n,t,r={},s=Object.keys(e);for(t=0;t<s.length;t++)n=s[t],i.indexOf(n)>=0||(r[n]=e[n]);return r}var l=["spacing"],u=["isCurrentPage","as","className","href"],d=["isCurrentPage","separator","isLastChild","spacing","children","className"],m=["children","spacing","separator","className"],p=(0,t.Gp)((function(e,i){var n=e.spacing,r=o(e,l),s=c({mx:n},(0,t.yK)().separator);return a.createElement(t.m$.span,c({ref:i,role:"presentation"},r,{__css:s}))}));r.Ts&&(p.displayName="BreadcrumbSeparator");var h=(0,t.Gp)((function(e,i){var n=e.isCurrentPage,s=e.as,l=e.className,d=e.href,m=o(e,u),p=(0,t.yK)(),h=c({ref:i,as:s,className:(0,r.cx)("chakra-breadcrumb__link",l)},m);return n?a.createElement(t.m$.span,c({"aria-current":"page",__css:p.link},h)):a.createElement(t.m$.a,c({__css:p.link,href:d},h))}));r.Ts&&(h.displayName="BreadcrumbLink");var f=(0,t.Gp)((function(e,i){var n=e.isCurrentPage,l=e.separator,u=e.isLastChild,m=e.spacing,f=e.children,x=e.className,v=o(e,d),g=(0,s.WR)(f).map((function(e){return e.type===h?a.cloneElement(e,{isCurrentPage:n}):e.type===p?a.cloneElement(e,{spacing:m,children:e.props.children||l}):e})),j=c({display:"inline-flex",alignItems:"center"},(0,t.yK)().item),y=(0,r.cx)("chakra-breadcrumb__list-item",x);return a.createElement(t.m$.li,c({ref:i,className:y},v,{__css:j}),g,!u&&a.createElement(p,{spacing:m},l))}));r.Ts&&(f.displayName="BreadcrumbItem");var x=(0,t.Gp)((function(e,i){var n=(0,t.jC)("Breadcrumb",e),l=(0,t.Lr)(e),u=l.children,d=l.spacing,p=void 0===d?"0.5rem":d,h=l.separator,f=void 0===h?"/":h,x=l.className,v=o(l,m),g=(0,s.WR)(u),j=g.length,y=g.map((function(e,i){return a.cloneElement(e,{separator:f,spacing:p,isLastChild:j===i+1})})),_=(0,r.cx)("chakra-breadcrumb",x);return a.createElement(t.m$.nav,c({ref:i,"aria-label":"breadcrumb",className:_,__css:n.container},v),a.createElement(t.Fo,{value:n},a.createElement(t.m$.ol,{className:"chakra-breadcrumb__list"},y)))}));r.Ts&&(x.displayName="Breadcrumb")},18343:function(e,i,n){"use strict";n.d(i,{Z:function(){return x}});var t=n(68527),r=n(9008),s=n.n(r),a=n(11163),c=(n(67294),n(53700)),o=n(26308),l=n(93549),u=n(31444),d=n(70918),m=n(15193),p=n(45035),h=n(85893),f=function(){var e=(0,a.useRouter)();return(0,h.jsx)(t.xu,{bg:"gray.50",border:"1px solid",borderColor:"blue.400",borderRadius:"md",justifyContent:"space-between",p:5,mb:5,mt:5,children:(0,h.jsxs)(t.xu,{children:[(0,h.jsxs)(t.Kq,{direction:{base:"column",sm:"row"},justifyContent:"space-between",children:[(0,h.jsx)(t.xv,{fontWeight:"semibold",children:"Configure your storage and messaging provider"}),(0,h.jsx)(m.zx,{size:"sm",variant:"outline",onClick:function(){e.push(p.fz)},children:"Configure"})]}),(0,h.jsxs)(t.xv,{children:["Before Fides can process your privacy requests we need two simple steps to configure your storage and email client."," "]})]})})},x=function(e){var i=e.children,n=e.title,r=(0,c.hz)(),m=(0,a.useRouter)(),p="/privacy-requests"===m.pathname||"/datastore-connection"===m.pathname,x=!(r.flags.privacyRequestsConfiguration&&p),v=(0,d.JE)(void 0,{skip:x}).data,g=(0,d.PW)(void 0,{skip:x}).data,j=r.flags.privacyRequestsConfiguration&&(!v||!g)&&p;return(0,h.jsxs)(t.kC,{"data-testid":n,direction:"column",children:[(0,h.jsxs)(s(),{children:[(0,h.jsxs)("title",{children:["Fides Admin UI - ",n]}),(0,h.jsx)("meta",{name:"description",content:"Privacy Engineering Platform"}),(0,h.jsx)("link",{rel:"icon",href:"/favicon.ico"})]}),(0,h.jsx)(o.Z,{}),(0,h.jsx)(u.Z,{}),(0,h.jsxs)(t.kC,{as:"main",flexGrow:1,padding:10,gap:10,children:[(0,h.jsx)(t.xu,{flex:0,flexShrink:0,children:(0,h.jsx)(l.U,{})}),(0,h.jsxs)(t.kC,{direction:"column",flex:1,minWidth:0,children:[j?(0,h.jsx)(f,{}):null,i]})]})]})}},70783:function(e,i,n){"use strict";n.d(i,{HK:function(){return s},VY:function(){return t.V}});var t=n(63719),r=n(65698),s=function(){var e=(0,t.V)().errorAlert;return{handleError:function(i){var n="An unexpected error occurred. Please try again.";(0,r.Ot)(i)?n=i.data.detail:(0,r.tB)(i)&&(n=i.data.detail[0].msg),e(n)}}};n(67294)},63719:function(e,i,n){"use strict";n.d(i,{V:function(){return d}});var t=n(59499),r=n(28609),s=n(6886),a=n(68527),c=n(84746),o=n(85893);function l(e,i){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var t=Object.getOwnPropertySymbols(e);i&&(t=t.filter((function(i){return Object.getOwnPropertyDescriptor(e,i).enumerable}))),n.push.apply(n,t)}return n}function u(e){for(var i=1;i<arguments.length;i++){var n=null!=arguments[i]?arguments[i]:{};i%2?l(Object(n),!0).forEach((function(i){(0,t.Z)(e,i,n[i])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):l(Object(n)).forEach((function(i){Object.defineProperty(e,i,Object.getOwnPropertyDescriptor(n,i))}))}return e}var d=function(){var e=(0,r.pm)();return{errorAlert:function(i,n,t){var r=u(u({},t),{},{position:(null===t||void 0===t?void 0:t.position)||"top",render:function(e){var t=e.onClose;return(0,o.jsxs)(s.bZ,{alignItems:"normal",status:"error",children:[(0,o.jsx)(s.zM,{}),(0,o.jsxs)(a.xu,{children:[n&&(0,o.jsx)(s.Cd,{children:n}),(0,o.jsx)(s.X,{children:i})]}),(0,o.jsx)(c.P,{onClick:t,position:"relative",right:0,size:"sm",top:-1})]})}});null!==t&&void 0!==t&&t.id&&e.isActive(t.id)?e.update(t.id,r):e(r)},successAlert:function(i,n,t){var r=u(u({},t),{},{position:(null===t||void 0===t?void 0:t.position)||"top",render:function(e){var t=e.onClose;return(0,o.jsxs)(s.bZ,{alignItems:"normal",status:"success",variant:"subtle",children:[(0,o.jsx)(s.zM,{}),(0,o.jsxs)(a.xu,{children:[n&&(0,o.jsx)(s.Cd,{children:n}),(0,o.jsx)(s.X,{children:i})]}),(0,o.jsx)(c.P,{onClick:t,position:"relative",right:0,size:"sm",top:-1})]})}});null!==t&&void 0!==t&&t.id&&e.isActive(t.id)?e.update(t.id,r):e(r)}}}},83689:function(e,i,n){"use strict";n.d(i,{DE:function(){return s},MP:function(){return t},qX:function(){return r}});var t=new Map([["Approved","approved"],["Canceled","canceled"],["Completed","complete"],["Denied","denied"],["Error","error"],["In Progress","in_processing"],["New","pending"],["Paused","paused"],["Unverified","identity_unverified"],["Requires input","requires_input"]]),r={mailgun:"mailgun",twilio_email:"twilio_email",twilio_text:"twilio_text"},s={local:"local",s3:"s3"}},49063:function(e,i,n){"use strict";n.r(i),n.d(i,{default:function(){return C}});var t=n(50029),r=n(16835),s=n(87794),a=n.n(s),c=n(68527),o=n(11739),l=n(9680),u=n(41664),d=n.n(u),m=n(67294),p=n(65698),h=n(70783),f=n(18343),x=n(83689),v=n(70918),g=n(15193),j=n(82175),y=n(96016),_=n(85893),b=function(e){var i=e.messagingDetails,n=(0,h.VY)().successAlert,s=(0,h.HK)().handleError,o=(0,v.SU)(),l=(0,r.Z)(o,1)[0],u=i.service_type===x.qX.twilio_email||i.service_type===x.qX.mailgun,d=i.service_type===x.qX.twilio_text,m=function(){var e=(0,t.Z)(a().mark((function e(i){var t,r;return a().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(!u){e.next=5;break}return e.next=3,l({email:i.email});case 3:t=e.sent,(0,p.D4)(t)?s(t.error):n("Test message successfully sent.");case 5:if(!d){e.next=10;break}return e.next=8,l({phone_number:i.phone});case 8:r=e.sent,(0,p.D4)(r)?s(r.error):n("Test message successfully sent.");case 10:case"end":return e.stop()}}),e)})));return function(i){return e.apply(this,arguments)}}();return(0,_.jsxs)(_.Fragment,{children:[(0,_.jsx)(c.iz,{mt:10}),(0,_.jsx)(c.X6,{fontSize:"md",fontWeight:"semibold",mt:10,mb:5,children:"Test connection"}),(0,_.jsx)(c.Kq,{children:(0,_.jsx)(j.J9,{initialValues:{email:"",phone:""},onSubmit:m,children:function(e){var i=e.isSubmitting,n=e.resetForm;return(0,_.jsxs)(j.l0,{children:[u?(0,_.jsx)(y.j0,{name:"email",label:"Email",placeholder:"youremail@domain.com",isRequired:!0}):null,d?(0,_.jsx)(y.j0,{name:"phone",label:"Phone",placeholder:"+10000000000",isRequired:!0}):null,(0,_.jsxs)(c.xu,{mt:10,children:[(0,_.jsx)(g.zx,{onClick:function(){return n()},mr:2,size:"sm",variant:"outline",children:"Cancel"}),(0,_.jsx)(g.zx,{isDisabled:i,type:"submit",colorScheme:"primary",size:"sm","data-testid":"save-btn",children:"Save"})]})]})}})})]})},w=function(){var e,i=(0,h.VY)().successAlert,n=(0,m.useState)(""),s=n[0],o=n[1],l=(0,h.HK)().handleError,u=(0,v.S3)({type:x.qX.mailgun}).data,d=(0,v.h9)(),f=(0,r.Z)(d,1)[0],w=(0,v.iI)(),q=(0,r.Z)(w,1)[0],k=function(){var e=(0,t.Z)(a().mark((function e(n){var t;return a().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,f({service_type:x.qX.mailgun,details:{is_eu_domain:"false",domain:n.domain}});case 2:t=e.sent,(0,p.D4)(t)?l(t.error):(i("Mailgun email successfully updated. You can now enter your security key."),o("apiKey"));case 4:case"end":return e.stop()}}),e)})));return function(i){return e.apply(this,arguments)}}(),S=function(){var e=(0,t.Z)(a().mark((function e(n){var t;return a().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,q({details:{mailgun_api_key:n.api_key},service_type:x.qX.mailgun});case 2:t=e.sent,(0,p.D4)(t)?l(t.error):(i("Mailgun security key successfully updated."),o("testConnection"));case 4:case"end":return e.stop()}}),e)})));return function(i){return e.apply(this,arguments)}}(),C={domain:null!==(e=null===u||void 0===u?void 0:u.details.domain)&&void 0!==e?e:""};return(0,_.jsxs)(c.xu,{children:[(0,_.jsx)(c.X6,{fontSize:"md",fontWeight:"semibold",mt:10,children:"Mailgun messaging configuration"}),(0,_.jsx)(c.Kq,{children:(0,_.jsx)(j.J9,{initialValues:C,onSubmit:k,enableReinitialize:!0,children:function(e){var i=e.isSubmitting,n=e.handleReset;return(0,_.jsxs)(j.l0,{children:[(0,_.jsx)(c.Kq,{mt:5,spacing:5,children:(0,_.jsx)(y.j0,{name:"domain",label:"Domain",placeholder:"Enter domain","data-testid":"option-twilio-domain",isRequired:!0})}),(0,_.jsxs)(c.xu,{mt:10,children:[(0,_.jsx)(g.zx,{onClick:n,mr:2,size:"sm",variant:"outline",children:"Cancel"}),(0,_.jsx)(g.zx,{isDisabled:i,type:"submit",colorScheme:"primary",size:"sm","data-testid":"save-btn",children:"Save"})]})]})}})}),"apiKey"===s||"testConnection"===s?(0,_.jsxs)(_.Fragment,{children:[(0,_.jsx)(c.iz,{mt:10}),(0,_.jsx)(c.X6,{fontSize:"md",fontWeight:"semibold",mt:10,children:"Security key"}),(0,_.jsx)(c.Kq,{children:(0,_.jsx)(j.J9,{initialValues:{api_key:""},onSubmit:S,children:function(e){var i=e.isSubmitting,n=e.handleReset;return(0,_.jsxs)(j.l0,{children:[(0,_.jsx)(y.j0,{name:"api_key",label:"API key",type:"password",isRequired:!0}),(0,_.jsxs)(c.xu,{mt:10,children:[(0,_.jsx)(g.zx,{onClick:n,mr:2,size:"sm",variant:"outline",children:"Cancel"}),(0,_.jsx)(g.zx,{isDisabled:i,type:"submit",colorScheme:"primary",size:"sm","data-testid":"save-btn",children:"Save"})]})]})}})})]}):null,"testConnection"===s?(0,_.jsx)(b,{messagingDetails:u||{service_type:x.qX.mailgun}}):null]})},q=function(){var e,i=(0,m.useState)(""),n=i[0],s=i[1],o=(0,h.VY)().successAlert,l=(0,h.HK)().handleError,u=(0,v.S3)({type:x.qX.twilio_email}).data,d=(0,v.h9)(),f=(0,r.Z)(d,1)[0],w=(0,v.iI)(),q=(0,r.Z)(w,1)[0],k=function(){var e=(0,t.Z)(a().mark((function e(i){var n;return a().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,f({service_type:x.qX.twilio_email,details:{twilio_email_from:i.email}});case 2:n=e.sent,(0,p.D4)(n)?l(n.error):(o("Twilio email successfully updated. You can now enter your security key."),s("configureTwilioEmailSecrets"));case 4:case"end":return e.stop()}}),e)})));return function(i){return e.apply(this,arguments)}}(),S=function(){var e=(0,t.Z)(a().mark((function e(i){var n;return a().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,q({details:{twilio_api_key:i.api_key},service_type:x.qX.twilio_email});case 2:n=e.sent,(0,p.D4)(n)?l(n.error):(o("Twilio email secrets successfully updated."),s("testConnection"));case 4:case"end":return e.stop()}}),e)})));return function(i){return e.apply(this,arguments)}}(),C={email:null!==(e=null===u||void 0===u?void 0:u.details.twilio_email_from)&&void 0!==e?e:""};return(0,_.jsxs)(c.xu,{children:[(0,_.jsx)(c.X6,{fontSize:"md",fontWeight:"semibold",mt:10,children:"Twilio Email messaging configuration"}),(0,_.jsx)(c.Kq,{children:(0,_.jsx)(j.J9,{initialValues:C,onSubmit:k,enableReinitialize:!0,children:function(e){var i=e.isSubmitting,n=e.handleReset;return(0,_.jsxs)(j.l0,{children:[(0,_.jsx)(c.Kq,{mt:5,spacing:5,children:(0,_.jsx)(y.j0,{name:"email",label:"Email",placeholder:"Enter email",isRequired:!0})}),(0,_.jsxs)(c.xu,{mt:10,children:[(0,_.jsx)(g.zx,{onClick:function(){return n()},mr:2,size:"sm",variant:"outline",children:"Cancel"}),(0,_.jsx)(g.zx,{isDisabled:i,type:"submit",colorScheme:"primary",size:"sm","data-testid":"save-btn",children:"Save"})]})]})}})}),"configureTwilioEmailSecrets"===n||"testConnection"===n?(0,_.jsxs)(_.Fragment,{children:[(0,_.jsx)(c.iz,{mt:10}),(0,_.jsx)(c.X6,{fontSize:"md",fontWeight:"semibold",mt:10,children:"Security key"}),(0,_.jsx)(c.Kq,{children:(0,_.jsx)(j.J9,{initialValues:{api_key:""},onSubmit:S,children:function(e){var i=e.isSubmitting,n=e.handleReset;return(0,_.jsxs)(j.l0,{children:[(0,_.jsx)(c.Kq,{mt:5,spacing:5,children:(0,_.jsx)(y.j0,{name:"api_key",label:"API key",type:"password",isRequired:!0})}),(0,_.jsxs)(c.xu,{mt:10,children:[(0,_.jsx)(g.zx,{onClick:function(){return n()},mr:2,size:"sm",variant:"outline",children:"Cancel"}),(0,_.jsx)(g.zx,{isDisabled:i,type:"submit",colorScheme:"primary",size:"sm","data-testid":"save-btn",children:"Save"})]})]})}})})]}):null,"testConnection"===n?(0,_.jsx)(b,{messagingDetails:u||{service_type:x.qX.twilio_email}}):null]})},k=function(){var e=(0,h.VY)().successAlert,i=(0,h.HK)().handleError,n=(0,m.useState)(""),s=n[0],o=n[1],l=(0,v.S3)({type:"twilio_text"}).data,u=(0,v.iI)(),d=(0,r.Z)(u,1)[0],f=function(){var n=(0,t.Z)(a().mark((function n(t){var r;return a().wrap((function(n){for(;;)switch(n.prev=n.next){case 0:return n.next=2,d({details:{twilio_account_sid:t.account_sid,twilio_auth_token:t.auth_token,twilio_messaging_service_sid:t.messaging_service_sid,twilio_sender_phone_number:t.phone},service_type:x.qX.twilio_text});case 2:r=n.sent,(0,p.D4)(r)?i(r.error):(e("Twilio text secrets successfully updated."),o("testConnection"));case 4:case"end":return n.stop()}}),n)})));return function(e){return n.apply(this,arguments)}}();return(0,_.jsxs)(c.xu,{children:[(0,_.jsx)(c.X6,{fontSize:"md",fontWeight:"semibold",mt:10,children:"Twilio SMS messaging configuration"}),(0,_.jsx)(c.Kq,{children:(0,_.jsx)(j.J9,{initialValues:{account_sid:"",auth_token:"",messaging_service_sid:"",phone:""},onSubmit:f,enableReinitialize:!0,children:function(e){var i=e.isSubmitting,n=e.handleReset;return(0,_.jsxs)(j.l0,{children:[(0,_.jsxs)(c.Kq,{mt:5,spacing:5,children:[(0,_.jsx)(y.j0,{name:"account_sid",label:"Account SID",placeholder:"Enter account SID",isRequired:!0}),(0,_.jsx)(y.j0,{name:"auth_token",label:"Auth token",placeholder:"Enter auth token",type:"password",isRequired:!0}),(0,_.jsx)(y.j0,{name:"messaging_service_sid",label:"Messaging Service SID",placeholder:"Enter messaging service SID"}),(0,_.jsx)(y.j0,{name:"phone",label:"Phone Number",placeholder:"Enter phone number"})]}),(0,_.jsxs)(c.xu,{mt:10,children:[(0,_.jsx)(g.zx,{onClick:function(){return n()},mr:2,size:"sm",variant:"outline",children:"Cancel"}),(0,_.jsx)(g.zx,{isDisabled:i,type:"submit",colorScheme:"primary",size:"sm","data-testid":"save-btn",children:"Save"})]})]})}})}),"testConnection"===s?(0,_.jsx)(b,{messagingDetails:l||{service_type:x.qX.twilio_text}}):null]})},S=function(){var e=(0,h.VY)().successAlert,i=(0,h.HK)().handleError,n=(0,m.useState)(""),s=n[0],u=n[1],g=(0,v.h9)(),j=(0,r.Z)(g,1)[0],y=(0,v.QG)(),b=(0,r.Z)(y,1)[0],S=(0,v.JE)().data;(0,m.useEffect)((function(){S&&u(null===S||void 0===S?void 0:S.service_type)}),[S]);var C=function(){var n=(0,t.Z)(a().mark((function n(t){var r,s;return a().wrap((function(n){for(;;)switch(n.prev=n.next){case 0:return n.next=2,b({notifications:{notification_service_type:t,send_request_completion_notification:!0,send_request_receipt_notification:!0,send_request_review_notification:!0},execution:{subject_identity_verification_required:!0}});case 2:if(r=n.sent,!(0,p.D4)(r)){n.next=7;break}i(r.error),n.next=15;break;case 7:if(t===x.qX.twilio_text){n.next=11;break}u(t),n.next=15;break;case 11:return n.next=13,j({service_type:x.qX.twilio_text});case 13:s=n.sent,(0,p.D4)(s)?i(s.error):(e("Messaging provider saved successfully."),u(t));case 15:case"end":return n.stop()}}),n)})));return function(e){return n.apply(this,arguments)}}();return(0,_.jsxs)(f.Z,{title:"Configure Privacy Requests - Messaging",children:[(0,_.jsx)(c.xu,{mb:8,children:(0,_.jsxs)(o.aG,{fontWeight:"medium",fontSize:"sm",color:"gray.600",children:[(0,_.jsx)(o.gN,{children:(0,_.jsx)(o.At,{as:d(),href:"/privacy-requests",children:"Privacy requests"})}),(0,_.jsx)(o.gN,{children:(0,_.jsx)(o.At,{as:d(),href:"/privacy-requests/configure",children:"Configuration"})}),(0,_.jsx)(o.gN,{color:"complimentary.500",children:(0,_.jsx)(o.At,{as:d(),href:"/privacy-requests/configure/messaging",isCurrentPage:!0,children:"Configure messaging provider"})})]})}),(0,_.jsx)(c.X6,{mb:5,fontSize:"2xl",fontWeight:"semibold",children:"Configure your messaging provider"}),(0,_.jsxs)(c.xu,{display:"flex",flexDirection:"column",width:"50%",children:[(0,_.jsxs)(c.xu,{children:["Fides requires a messsaging provider for sending processing notices to privacy request subjects, and allows for Subject Identity Verification in privacy requests. Please follow the"," ",(0,_.jsx)(c.xv,{as:"span",color:"complimentary.500",children:"documentation"})," ","to setup a messaging service that Fides supports. Ensure you have completed the setup for the preferred messaging provider and have the details handy prior to the following steps."]}),(0,_.jsx)(c.X6,{fontSize:"md",fontWeight:"semibold",mt:10,children:"Choose service type to configure"}),(0,_.jsx)(l.Ee,{onChange:C,value:s,"data-testid":"privacy-requests-messaging-provider-selection",colorScheme:"secondary",p:3,children:(0,_.jsxs)(c.Kq,{direction:"row",children:[(0,_.jsx)(l.Y8,{value:x.qX.mailgun,"data-testid":"option-mailgun",mr:5,children:"Mailgun Email"},x.qX.mailgun),(0,_.jsx)(l.Y8,{value:x.qX.twilio_email,"data-testid":"option-twilio-email",children:"Twilio Email"},x.qX.twilio_email),(0,_.jsx)(l.Y8,{value:x.qX.twilio_text,"data-testid":"option-twilio-sms",children:"Twilio SMS"},x.qX.twilio_text)]})}),s===x.qX.mailgun?(0,_.jsx)(w,{}):null,s===x.qX.twilio_email?(0,_.jsx)(q,{}):null,s===x.qX.twilio_text?(0,_.jsx)(k,{}):null]})]})},C=function(){return(0,_.jsx)(S,{})}},68528:function(e,i,n){(window.__NEXT_P=window.__NEXT_P||[]).push(["/privacy-requests/configure/messaging",function(){return n(49063)}])}},function(e){e.O(0,[2437,3880,3879,9774,2888,179],(function(){return i=68528,e(e.s=i);var i}));var i=e.O();_N_E=i}]);