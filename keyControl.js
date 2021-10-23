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

(function () {
  "use strict";
  main();

  const KEY_CODE_ENTER = 13;
  const KEY_CODE_ESCAPE = 27;

  let isFullscreen = false;
  const hostUrlActions = {
    "www.bilibili.com": () => {
      document.querySelector("[data-text=进入全屏]").click();
    },
    "www.youtube.com": () => {
      document.querySelector(".ytp-fullscreen-button.ytp-button").click();
    },
  };
  const excluded = new Set();
  excluded.add("www.baidu.com");
  excluded.add("input");

  function excludeTag(tagName) {
    return excluded.has(tagName.toLowerCase());
  }

  function excludeHostname(hostname) {
    return excluded.has(hostname);
  }

  function main() {
    window.addEventListener("keyup", (event) => {
      const hostname = window.location.hostname;
      if (excludeHostname(hostname)) {
        return;
      }
      doKeyEvent(event);
    });
  }

  function handleKeyEnter(event) {
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

    if (excludeTag(event.target.tagName)) {
      console.log("exclude tag: ", event.target.tagName);
      return;
    }

    const action = hostUrlActions[window.location.hostname];
    if (action) {
      action();
      return;
    }

    const videoEle = document.querySelector("video");
    if (videoEle) {
      isFullscreen
        ? exitFullScreen().apply(document)
        : enterFullScreen().apply(videoEle);
      isFullscreen = !isFullscreen;
    }
  }

  function doKeyEvent(event) {
    const keyCode = event.keyCode;
    if (keyCode === KEY_CODE_ENTER) {
      handleKeyEnter(event);
    } else if (keyCode === KEY_CODE_ESCAPE) {
      console.log("press key escape");
      isFullscreen = false;
    }
  }
})();
