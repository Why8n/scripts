// ==UserScript==
// @name         auto click more comments
// @namespace    http://tampermonkey.net/
// @version      2025-03-06
// @description  try to take over the world!
// @author       Whyn
// @match        *://*/*
// @icon         data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==
// @grant        none
// ==/UserScript==


(function() {
    'use strict';

    // ==UserScript==
    // @name         B站自动加载更多评论
    // @namespace    http://tampermonkey.net/
    // @version      0.1
    // @description  自动点击“查看全部评论”或“查看更多”按钮
    // @author       You
    // @match        https://www.bilibili.com/video/*
    // @grant        none
    // ==/UserScript==

    (function() {
        'use strict';

        // 自动点击“查看全部评论”的函数
        function autoLoadComments() {
            // 定位“查看全部评论”按钮（可能的元素选择器）
            const loadMoreButton = document.querySelector('#view-more');

            if (loadMoreButton) {
                // 模拟点击按钮
                loadMoreButton.click();
                console.log('已自动点击“加载更多评论”');

                // 延迟后再检查是否有更多按钮（防止重复点击）
                setTimeout(autoLoadComments, 2000); // 每2秒检查一次
            } else {
                console.log('没有找到“加载更多”按钮');
            }
        }

        // 监听页面变化（如动态加载内容）
        const observer = new MutationObserver((mutations) => {
            mutations.forEach(mutation => {
                if (mutation.addedNodes) {
                    autoLoadComments(); // 检测到DOM变化后重新查找按钮
                }
            });
        });

        // 开始观察整个文档的子节点变化
        observer.observe(document.querySelector('#commentapp'), {
            childList: true,
            subtree: true
        });

        // 初始触发一次
        autoLoadComments();
    })();
})();

