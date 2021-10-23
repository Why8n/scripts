// ==UserScript==
// @name         Key Control
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  try to take over the world!
// @author       Whyn
// @match        *://*/*
// @icon         https://www.google.com/s2/favicons?domain=youtube.com
// @grant        none
// ==/UserScript==


(function() {
    'use strict';
    const KEY_CODE_ENTER = 13;
    // hostname: www.baidu.com
    const curUrl = window.location.hostname;
    let isFullScreen = false;

    const excludes = new Set();
    excludes.add('www.baidu.com');

    function isExcluded(url) {
        return excludes.has(url);
    }

      const videoEleofDomain = {
        'www.youtube.com': () => {
            const url = window.location.href;
            if(!url.includes('search_query')) {
                  document.querySelector('.ytp-fullscreen-button.ytp-button').click();
             }
        },
        'www.bilibili.com': () => { document.querySelector('[data-text=进入全屏]').click(); }
    };


    function doKeyEvent(event) {
        console.log('doKeyEvent==>',event);
        if(event.keyCode == KEY_CODE_ENTER) {
            console.log("detect key: enter");
            if(isExcluded(window.location.hostname)) {
               return;
            }
            let action = videoEleofDomain[curUrl];
            if(action){
                action();
                return;
            }
            let ele = document.querySelector('video');
            console.log('auto search first Video: ',ele);
            isFullScreen ? exitFullScreen().apply(document) : enterFullScreen().apply(ele);
            isFullScreen = !isFullScreen;
        }
    }

    //进入全屏
function enterFullScreen() {
    var ele = document.documentElement;
    if (ele.requestFullscreen) {
        return ele.requestFullscreen;
    } else if (ele.mozRequestFullScreen) {
        return ele.mozRequestFullScreen;
    } else if (ele.webkitRequestFullScreen) {
       return ele.webkitRequestFullScreen;
    }
}
//退出全屏
function exitFullScreen() {
    var de = document;
    if (de.exitFullscreen) {
        return de.exitFullscreen;
    } else if (de.mozCancelFullScreen) {
        return de.mozCancelFullScreen;
    } else if (de.webkitCancelFullScreen) {
        return de.webkitCancelFullScreen;
    }
}

    function main() {
        window.addEventListener('keyup',(event) => {
            doKeyEvent(event);
        });

    }



main();

})();
