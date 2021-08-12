StackExchange.postValidation=function(){function e(e,t,n){var i={"Title":".js-post-title-field","Body":".js-post-body-field[data-post-type-id="+t+"]","Tags":".js-post-tags-field","Mentions":".js-post-mentions-field","EditComment":".js-post-edit-comment-field","Excerpt":".js-post-excerpt-field","Email":".js-post-email-field"};return i[n]?e.find(i[n]):$()}function t(t,n,i){var r=e(t,n,i);return i===D||i===L?t.find(".js-tag-editor").filter(function(){return $(this).data("target-field")===r.get(0)}):r}function n(e,t,n,i){var r=e.find('input[type="submit"]:visible, button[type="submit"]:visible'),o=r.length&&r.is(":enabled");o&&r.prop("disabled",!0),u(e,t,n),l(e,t,n,i),f(e,t,n),h(e,t,n),g(e,t,n),w(e,t,function(){d(e,t,n),o&&r.prop("disabled",!1)})}function i(i,s,c,u,l){n(i,s,c,u);var d,f=function(e){if(i.trigger("post:submit-completed",[c,e]),e.success)if(l)l(e);else{var t=window.location.href.split("#")[0],n=e.redirectTo.split("#")[0];0===n.indexOf("/")&&(n=window.location.protocol+"//"+window.location.hostname+n),d=!0,window.location=e.redirectTo,t.toLowerCase()===n.toLowerCase()&&window.location.reload(!0)}else e.captchaHtml?StackExchange.nocaptcha.init(e.captchaHtml,f):e.errors?(i.find(".js-post-prior-attempt-count").val(function(e,t){return(+t+1||0).toString()}),k(i,s,c,e.errors,e.warnings)):b(i,c,{"General":[$("<span/>").text(e.message).html()]},0)};i.submit(function(){if(i.find(".js-post-answer-while-asking-checkbox").is(":checked"))return!0;if(p(i,s,c))return StackExchange.helpers.enableSubmitButton(i),!1;if(a(),StackExchange.navPrevention&&StackExchange.navPrevention.stop(),i.find('input[type="submit"]:visible, button[type="submit"]').addClass("is-loading"),StackExchange.helpers.disableSubmitButton(i),StackExchange.options.site.enableNewTagCreationWarning){var n=e(i,s,D),u=n.prop("defaultValue");if(n.val()!==u)return $.ajax({"type":"GET","url":"/posts/new-tags-warning","dataType":"json","data":{"tags":n.val()},"success":function(e){if(e.showWarning){var n={"closeOthers":!0,"shown":function(){$(".js-confirm-tag-creation").on("click",function(e){return StackExchange.helpers.closePopups(),o(i,c,d,f),e.preventDefault(),!1})},"dismissing":function(){r(i,d)},"returnElements":t(i,s,D).find("input:visible")};StackExchange.helpers.showModal($(e.html).elementNodesOnly(),n),StackExchange.helpers.bindMovablePopups()}else o(i,c,d,f)}}),!1}return setTimeout(function(){o(i,c,d,f)},0),!1})}function r(e,t){e.find('input[type="submit"]:visible, button[type="submit"]').removeClass("is-loading"),t||StackExchange.helpers.enableSubmitButton(e)}function o(e,t,n,i){$.ajax({"type":"POST","dataType":"json","data":e.serialize(),"url":e.attr("action"),"success":i,"error":function(){var n=v(t,0);b(e,t,{"General":[$("<span/>").text(n).html()]},0)},"complete":function(){r(e,n)}})}function a(){for(var e=0;e<R.length;e++)clearTimeout(R[e]);R=[]}function s(t,n,i,r,o){e(t,n,r).blur(function(){var e=this,a=$(this),s=function(e){E(t,n,i,r,e)},c=function(e){return x(e,t,n,i,[r])};R.push(setTimeout(function(){var t=StackExchange.stacksValidation.handlerFor(a);t&&!A&&t.clear(),o.call(e,a,s,c)},V))})}function c(t,n,i,r,o){if(1===n&&"question"===i)return x({"type":"POST","url":"/posts/validate-question","data":{"title":e(t,n,M).val(),"body":e(t,n,U).val(),"tags":e(t,n,D).val(),"fkey":StackExchange.options.user.fkey}},t,n,i,[M,U,D],o).promise();if(2===n)return x({"type":"POST","url":"/posts/validate-body","data":{"body":e(t,n,U).val(),"oldBody":e(t,n,U).prop("defaultValue"),"isQuestion":!1,"isSuggestedEdit":r||!1,"fkey":StackExchange.options.user.fkey}},t,n,i,[U],o).promise();var a=$.Deferred();return a.reject(),a.promise()}function u(e,t,n){s(e,t,n,M,function(e,t,n){var i=e.val(),r=$.trim(i).length,o=e.data("min-length"),a=e.data("max-length");return 0!==r||A?o&&o>r?(t(function(e){return 1==e.minLength?"Title must be at least "+e.minLength+" character.":"Title must be at least "+e.minLength+" characters."}({"minLength":o})),void 0):a&&r>a?(t(function(e){return 1==e.maxLength?"Title cannot be longer than "+e.maxLength+" character.":"Title cannot be longer than "+e.maxLength+" characters."}({"maxLength":a})),void 0):(n({"type":"POST","url":"/posts/validate-title","data":{"title":i,"fkey":StackExchange.options.user.fkey}}),void 0):(t(),void 0)})}function l(e,t,n,i){s(e,t,n,U,function(e,n,r){var o=e.val(),a=$.trim(o).length,s=e.data("min-length");return 0!==a||A?5===t?(s&&s>a?n(function(e){return"Wiki Body must be at least "+e.minLength+" characters. You entered "+e.actual+"."}({"minLength":s,"actual":a})):n(),void 0):((1===t||2===t)&&r({"type":"POST","url":"/posts/validate-body","data":{"body":o,"oldBody":e.prop("defaultValue"),"isQuestion":1===t,"isSuggestedEdit":i,"fkey":StackExchange.options.user.fkey}}),void 0):(n(),void 0)})}function d(e,t,n){s(e,t,n,D,function(e,t,n){var i=e.val(),r=$.trim(i).length;return 0!==r||A?(n({"type":"POST","url":"/posts/validate-tags","data":{"tags":i,"oldTags":e.prop("defaultValue"),"fkey":StackExchange.options.user.fkey},"success":function(t){var n=e.closest(".js-post-form").find(".js-warned-tags-field");if(n.length){var i=n.val(),r=n.data("warned-tags")||[],o=((t.source||{}).Tags||[]).filter(function(e){return e&&-1===r.indexOf(e)});o.length>0&&StackExchange.using("gps",function(){o.forEach(function(e){StackExchange.gps.track("tag_warning.show",{"tag":e},!0),i+=" "+e,r.push(e)}),n.val($.trim(i)).data("warned-tags",r),StackExchange.gps.sendPending()})}}}),void 0):(t(),void 0)})}function p(t,n,i){return"[Edit removed during grace period]"===$.trim(e(t,n,N).val())?(E(t,n,i,N,"Comment reserved for system use. Please use an appropriate comment."),!0):!1}function f(e,t,n){s(e,t,n,N,function(i,r){var o=i.val(),a=$.trim(o).length,s=i.data("min-length"),c=i.data("max-length");return 0===a?(r(),void 0):s&&s>a?(r(function(e){return 1==e.minLength?"Your edit summary must be at least "+e.minLength+" character.":"Your edit summary must be at least "+e.minLength+" characters."}({"minLength":s})),void 0):c&&a>c?(r(function(e){return 1==e.maxLength?"Your edit summary cannot be longer than "+e.maxLength+" character.":"Your edit summary cannot be longer than "+e.maxLength+" characters."}({"maxLength":c})),void 0):(p(e,t,n)||r(),void 0)})}function h(e,t,n){s(e,t,n,q,function(e,t){var n=e.val(),i=$.trim(n).length,r=e.data("min-length"),o=e.data("max-length");return 0===i?(t(),void 0):r&&r>i?(t(function(e){return"Wiki Excerpt must be at least "+e.minLength+" characters; you entered "+e.actual+"."}({"minLength":r,"actual":i})),void 0):o&&i>o?(t(function(e){return"Wiki Excerpt cannot be longer than "+e.maxLength+" characters; you entered "+e.actual+"."}({"maxLength":o,"actual":i})),void 0):(t(),void 0)})}function g(e,t,n){s(e,t,n,F,function(e,t){var n=e.val(),i=$.trim(n),r=i.length;return 0===r?(t(),void 0):StackExchange.helpers.isEmailAddress(i)?(t(),void 0):(t("This email does not appear to be valid."),void 0)})}function m(e,t){var n=$("#sidebar, .sidebar").first().width()||270,i="lg"===StackExchange.responsive.currentRange();return e===B?{"position":"inline","css":{"display":"inline-block","margin-bottom":"10px"},"closeOthers":!1,"dismissable":!1,"type":t}:{"position":{"my":i?"left top":"top center","at":i?"right center":"bottom center"},"css":{"max-width":n,"min-width":n},"closeOthers":!1,"type":t}}function v(e,t){if(t>0)switch(e){case"question":return function(e){return 1==e.specificErrorCount?"Your question couldn't be submitted. Please see the error above.":"Your question couldn't be submitted. Please see the errors above."}({"specificErrorCount":t});case"answer":return function(e){return 1==e.specificErrorCount?"Your answer couldn't be submitted. Please see the error above.":"Your answer couldn't be submitted. Please see the errors above."}({"specificErrorCount":t});case"edit":return function(e){return 1==e.specificErrorCount?"Your edit couldn't be submitted. Please see the error above.":"Your edit couldn't be submitted. Please see the errors above."}({"specificErrorCount":t});case"tags":return function(e){return 1==e.specificErrorCount?"Your tags couldn't be submitted. Please see the error above.":"Your tags couldn't be submitted. Please see the errors above."}({"specificErrorCount":t});default:return function(e){return 1==e.specificErrorCount?"Your post couldn't be submitted. Please see the error above.":"Your post couldn't be submitted. Please see the errors above."}({"specificErrorCount":t})}else switch(e){case"question":return"An error occurred submitting the question.";case"answer":return"An error occurred submitting the answer.";case"edit":return"An error occurred submitting the edit.";case"tags":return"An error occurred submitting the tags.";default:return"An error occurred submitting the post."}}function b(e,t,n,i){var r=e.find(".js-general-error").text("").removeClass("d-none");if(!C(e,r,n,null,B,t))return i>0?(r.text(v(t,i)),void 0):(r.addClass("d-none"),void 0)}function y(e){var t=$(".js-post-review-summary").closest(".js-post-review-summary-container");if(t.length>0)return t.filter(":visible").scrollIntoView(),void 0;var n;P()&&($("#sidebar").animate({"opacity":.4},500),n=setInterval(function(){P()||($("#sidebar").animate({"opacity":1},500),clearInterval(n))},500));var i;e.find(".validation-error, .js-stacks-validation.has-error").each(function(){var e=$(this).offset().top;(!i||i>e)&&(i=e)});var r=function(){for(var t=0;3>t;t++)e.find(".message").animate({"left":"+=5px"},100).animate({"left":"-=5px"},100)};if(i){var o=$(".review-bar").length;i=Math.max(0,i-(o?125:30)),$("html, body").animate({"scrollTop":i},r)}else r()}function k(e,t,n,i,r){i&&w(e,t,function(){var o=S(e,t,n,[M,U,D,L,N,q,F],i,r).length;b(e,n,i,o),y(e)})}function w(e,n,i){var r=function(){1!==n||t(e,n,D).length?i():setTimeout(r,250)};r()}function x(e,t,n,i,r,o){return $.ajax(e).then(function(e){return o?$.when(o()).then(function(){return e}):e}).done(function(e){S(t,n,i,r,e.errors,e.warnings)}).fail(function(){S(t,n,i,r,{},{})})}function S(e,n,i,r,o,a){for(var s=[],c=0;c<r.length;c++){var u=r[c];C(e,t(e,n,u),o,a,u,i)&&s.push(u)}return s}function E(e,n,i,r,o){j(e,t(e,n,r),o?[$("<span/>").text(o).html()]:[],[],r,i)}function C(e,t,n,i,r,o){var a=n[r]||[],s=(i||{})[r]||[];return j(e,t,a,s,r,o)}function j(e,t,n,i,r,o){var a=StackExchange.stacksValidation.handlerFor(t);return a?T(a,o,n,i,r):O(t,r,n),e.find(".validation-error, .js-stacks-validation.has-error").length||e.find(".js-general-error").text(""),t.trigger("post:validated-field",[o,r,n,i]),n.length>0}function T(e,t,n,i){e.clear("error"),n.forEach(function(t){e.add("error",t)}),"edit"===t||"question"===t&&A||(e.clear("warning"),i.forEach(function(t){e.add("warning",t)}))}function O(e,t,n){e&&e.length&&(0===n.length||1===n.length&&""===n[0]||!$("html").has(e).length?_(e):I(e,n,m(t,"error")))}function I(e,t,n){var i=1===t.length?t[0]:"<ul><li>"+t.join("</li><li>")+"</li></ul>",r=e.data("error-popup");if(r&&r.is(":visible")){var o=e.data("error-message");if(o===i)return r.animateOffsetTop&&r.animateOffsetTop(0),void 0;r.fadeOutAndRemove()}var s=StackExchange.helpers.showMessage(e,i,n);s.find("a").attr("target","_blank"),s.click(a),e.addClass("validation-error").data("error-popup",s).data("error-message",i)}function _(e){var t=e.data("error-popup");t&&t.is(":visible")&&t.fadeOutAndRemove(),e.removeClass("validation-error"),e.removeData("error-popup"),e.removeData("error-message")}function P(){var e=!1,t=$("#sidebar, .sidebar").first();if(!t.length)return!1;var n=t.offset().left;return $(".message").each(function(){var t=$(this);return t.offset().left+t.outerWidth()>n?(e=!0,!1):void 0}),e}var A=$("body").hasClass("js-ask-page-v2"),M="Title",U="Body",D="Tags",L="Mentions",N="EditComment",q="Excerpt",F="Email",B="General",R=[],V=250;return{"initOnBlur":n,"initOnBlurAndSubmit":i,"showErrorsAfterSubmission":k,"validatePostFields":c,"scrollToErrors":y}}();