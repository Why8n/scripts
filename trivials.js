// ==UserScript==
// @name         trivals
// @namespace    http://tampermonkey.net/
// @version      2025-03-09
// @description  some trivial scripts for websites
// @author       Whyn
// @match        *://*/*
// @icon         https://www.google.com/s2/favicons?domain=youtube.com
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    function main() {
        const domainActions = {
            'youtube.com': () => { console.log('hello youtube!')},
            'bilibili.com': () => {
                console.log('trivals for bilibili');
                const url = window.location.hostname;
                if(url === 't.bilibili.com'){
                    console.log('bilibili: on search page');
                    wrapUserPanel();

                }

                function wrapUserPanel(){
                    // 创建 MutationObserver 实例
                    const observer = new MutationObserver((mutationsList, observer) => {
                        mutationsList.forEach(mutation => {
                            if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
                                mutation.addedNodes.forEach(node => {
                                    if (node.classList && node.classList.contains('bili-dyn-up-list')) {
                                        observer.disconnect();
                                        console.log('user panel detected:', node);
                                        // wrap updated users
                                        let usersEle = node.querySelector('.bili-dyn-up-list__content')
                                        console.log('users element:',usersEle);
                                        usersEle.style.flexWrap = 'wrap';
                                    }
                                });
                            }
                        });
                    });

                    // 配置观察选项
                    const config = {
                        childList: true, // 监控子节点的变化
                        subtree: true   // 监控整个子树的变化
                    };

                    // 开始观察目标节点（通常是 .content 的父节点或 document.body）
                    const parentNode = document.body; // 假设 .content 会被插入到 body 中
                    observer.observe(parentNode, config);
                }
            },
            'telegram.org': () => {

                function shrinkDragArea(){
                    const observer = new MutationObserver( (mutations) => {
                        mutations.forEach( mutation => {
                            if (mutation.type === 'childList') {
                                mutation.addedNodes.forEach(node => {
                                    const dropTargetEle = node.querySelector('.DropTarget');
                                    console.log('dropTarget: ', dropTargetEle);
                                    if(dropTargetEle){
                                        // observer.disconnect();

                                        dropTargetEle.style.marginBottom = '200px';
                                    }
                                });
                            };
                        });
                    });


                    const parentEle = document.querySelector('#middle-column-portals')
                    observer.observe(parentEle, {
                        childList: true,  // 监听子元素变化
                        subtree: true     // 监听所有后代元素
                    });
                }

                function disableGlobalDragEvent(callback){

                    // 全局拦截拖动事件，但允许文本拖动
                    document.body.addEventListener('dragstart', function(e) {
                        // 获取当前选中的文本
                        const selection = window.getSelection();
                        console.log('selection:', selection.toString());
                        const isTextDrag = selection.toString().trim() !== '';

                        // 如果是文本拖动，允许默认行为（如拖入输入框）
                        if (isTextDrag) {
                            return;
                        }

                        // 否则阻止非文本元素的拖动
                        e.preventDefault();
                        e.stopPropagation();
                    }, { capture: true });

                    // 覆盖其余所有拖拽相关事件
                    ['dragover', 'drop', 'dragenter', 'dragleave'].forEach(eventName => {
                        document.body.addEventListener(eventName, e => {
                            e.preventDefault();
                            e.stopPropagation();
                            e.stopImmediatePropagation(); // 阻止其他监听器执行[7,8](@ref)

                            // 触发自动处理逻辑
                            callback(eventName, e);
                        }, { capture: true }); // 使用捕获阶段优先拦截[6](@ref)
                    });
                }

                console.log('enable drop event for telegram');
                // shrinkDragArea();
                disableGlobalDragEvent( (eventName, event) => {
                    // 你的自定义处理
                    switch(eventName) {
                        case 'dragover':
                            console.log('Custom dragover');
                            break;
                        case 'drop':
                            const text = event.dataTransfer.getData('text/plain');
                            console.log('dragText:', text);

                            const bottomInputEle = document.querySelector('#editable-message-text');
                            if(event.target === bottomInputEle){
                                // remove placeholder
                                bottomInputEle.classList.add('touched');
                                bottomInputEle.textContent = text; // 显示文字
                                bottomInputEle.style.backgroundColor = '#fff';
                            }

                            // const leftUpInputEle = document.querySelector('.input-search > .input-search-input');
                            const searchInputElements = document.querySelectorAll('input.form-control');
                            searchInputElements.forEach(element => {
                                if(event.target === element){
                                    element.value = text;
                                }
                            });

                            break;
                    }
                });

            },
            'google.com': () => {
                if( window.location.pathname === '/sorry/index'){
                    console.log("detected current page: google.com/sorry/index");
                    const urlEle = document.querySelector('#infoDiv').nextSibling.nextSibling.nextSibling.nextSibling.nextSibling;
                    const targetUrl = urlEle.textContent.replace('URL: ', '');

                    // 1. 创建<a>标签
                    const link = document.createElement('a');

                    // 2. 设置属性
                    link.href = targetUrl;
                    link.textContent = 'jump';
                    // link.target = '_blank'; // 可选：新标签页打开
                    link.target = '_self';

                    link.style.display = 'block';
                    link.style.marginTop = '10px';

                    // 3. 添加到DOM中
                    document.body.appendChild(link);

                }

            },
        }

        const url = new URL(window.location.href);
        const domain = url.hostname; // => www.baidu.com
        const parentDomain = domain.split(".").slice(-2).join("."); // => baidu.com
        console.log('parentDomain: ', parentDomain);

        const action = domainActions[parentDomain]
        action && action();
    }

    function enableDragText(dropElement, callback) {
        // 允许放置
        dropElement.addEventListener('dragover', (e) => {
            // 必须阻止默认行为才能触发drop事件
            e.preventDefault();
            // dropElement.style.backgroundColor = '#f0f8ff'; // 视觉反馈
            e.dataTransfer.dropEffect = "move"; // 显示移动效果的鼠标样式[6](@ref)
        });

        // 处理放置
        dropElement.addEventListener('drop', (e) => {
            e.preventDefault();
            // 仅接收文字
            if (e.dataTransfer.types.includes('text/plain')) {
                // 获取拖拽数据
                const text = e.dataTransfer.getData('text/plain');
                console.log('接收到的文字:', text);
                callback(e.target, text);
            }
        });
    }

    // match: (node) => boolean
    function mutationObserver(parentElement, match) {
        const observer = new MutationObserver( (mutations) => {
            mutations.forEach( mutation => {
                if (mutation.type === 'childList') {
                    mutation.addedNodes.forEach(node => {
                        if(match(node)){
                            observer.disconnect();
                            return;
                        }
                    });
                };
            });
        });

        observer.observe(parentElement, {
            childList: true,  // 监听子元素变化
            subtree: true     // 监听所有后代元素
        });
        return observer;
    }

    main();

})();


