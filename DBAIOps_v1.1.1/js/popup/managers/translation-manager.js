/**
 * 翻译管理器
 * 负责翻译相关的功能
 */
import { escapeHtml } from '../utils/common.js';

export function createTranslationManager(popup) {
    return {
        /**
         * 翻译选中内容
         */
        async translateSelection() {
            console.log('翻译按钮被点击');

            // 检查resultText区域是否有内容
            const resultContent = popup.resultText.textContent.trim();
            console.log('结果区域内容:', resultContent);
            console.log('结果区域长度:', resultContent.length);

            if (!resultContent) {
                console.log('没有内容，显示提示消息');
                popup.showMessage(popup.t('popup.message.translateHint'), 'info');
                return;
            }

            console.log('开始翻译，显示翻译弹窗');
            // 先显示翻译弹窗，在弹窗中显示翻译进度
            popup.showTranslationDialog(resultContent, null, true); // 第三个参数表示正在翻译

            try {
                console.log('调用translateText方法');
                // 直接翻译resultText区域的内容
                const translation = await popup.translateText(resultContent);
                console.log('翻译完成，结果:', translation);
                console.log('更新翻译弹窗内容');
                // 更新弹窗内容，显示翻译结果
                popup.updateTranslationDialog(resultContent, translation);
            } catch (error) {
                console.error('翻译失败:', error);
                // 更新弹窗显示错误信息
                popup.updateTranslationDialog(resultContent, `翻译失败: ${error.message}`, false, true);
            }
        },

        /**
         * 翻译文本
         */
        async translateText(text) {
            try {
                // 检测语言
                const hasChinese = /[\u4e00-\u9fff]/.test(text);
                const hasEnglish = /[a-zA-Z]/.test(text);

                // 确定翻译方向
                let targetLanguage, sourceLanguage;
                if (hasChinese && !hasEnglish) {
                    // 纯中文翻译为英文
                    sourceLanguage = '中文';
                    targetLanguage = '英文';
                } else if (hasEnglish && !hasChinese) {
                    // 纯英文翻译为中文
                    sourceLanguage = '英文';
                    targetLanguage = '中文';
                } else if (hasChinese && hasEnglish) {
                    // 中英混合，翻译为英文
                    sourceLanguage = '中英文混合';
                    targetLanguage = '英文';
                } else {
                    // 其他语言，尝试翻译为中文
                    sourceLanguage = '未知语言';
                    targetLanguage = '中文';
                }

                // 获取用户选择的模型和服务商
                const selectedModelValue = popup.modelSelect.value;
                if (!selectedModelValue) {
                    throw new Error(popup.t('popup.error.selectModel'));
                }

                let selectedKey;
                try {
                    selectedKey = JSON.parse(selectedModelValue);
                } catch (_) {
                    selectedKey = { name: selectedModelValue };
                }

                const selectedModel = popup.models.find(m => m.name === selectedKey.name && (!selectedKey.provider || m.provider === selectedKey.provider));
                const provider = selectedModel ? popup.providers.find(p => p.name === selectedModel.provider) : null;

                if (!selectedModel || !provider) {
                    throw new Error(popup.t('popup.error.modelOrProviderMissing'));
                }

                // 构建翻译提示词
                const translationPrompt = `请将以下${sourceLanguage}文本翻译成${targetLanguage}，要求：
1. 保持原文的意思和语气
2. 翻译要准确、自然、流畅
3. 如果是技术术语，请使用标准的翻译
4. 只返回翻译结果，不要添加任何解释或标记

原文：
${text}

翻译结果：`;

                // 使用AI API进行翻译
                const translatedText = await popup.callAIAPI(
                    translationPrompt,
                    '', // 不需要页面内容
                    '', // 不需要页面URL
                    provider,
                    selectedModel
                );

                // 清理翻译结果，移除可能的AI前缀
                let cleanTranslation = translatedText.trim();

                // 移除常见的AI前缀
                const prefixes = [
                    '翻译结果：', 'Translation:', '翻译：', 'Translated text:',
                    'AI翻译：', 'AI Translation:', '结果：', 'Result:'
                ];

                for (const prefix of prefixes) {
                    if (cleanTranslation.startsWith(prefix)) {
                        cleanTranslation = cleanTranslation.substring(prefix.length).trim();
                        break;
                    }
                }

                return cleanTranslation || translatedText;

            } catch (error) {
                console.error('翻译处理失败:', error);

                // 如果AI翻译失败，提供备用方案
                const hasChinese = /[\u4e00-\u9fff]/.test(text);
                const hasEnglish = /[a-zA-Z]/.test(text);

                if (hasChinese && !hasEnglish) {
                    return `[翻译失败] ${error.message || '请检查网络连接或AI服务配置'}。原文：${text}`;
                } else if (hasEnglish && !hasChinese) {
                    return `[Translation failed] ${error.message || 'Please check network connection or AI service configuration'}. Original text: ${text}`;
                } else {
                    return `[翻译失败] ${error.message || 'Please check network connection or AI service configuration'}. Original text: ${text}`;
                }
            }
        },

        /**
         * 显示翻译弹窗
         */
        showTranslationDialog(originalText, translatedText, isTranslating = false) {
            console.log('showTranslationDialog被调用');
            console.log('原文:', originalText);
            console.log('译文:', translatedText);
            console.log('是否正在翻译:', isTranslating);

            // 检测语言
            const hasChinese = /[\u4e00-\u9fff]/.test(originalText);
            const hasEnglish = /[a-zA-Z]/.test(originalText);

            // 确定语言信息
            let sourceLanguage, targetLanguage;
            if (hasChinese && !hasEnglish) {
                sourceLanguage = '中文';
                targetLanguage = '英文';
            } else if (hasEnglish && !hasChinese) {
                sourceLanguage = '英文';
                targetLanguage = '中文';
            } else if (hasChinese && hasEnglish) {
                sourceLanguage = '中英文混合';
                targetLanguage = '英文';
            } else {
                sourceLanguage = '未知语言';
                targetLanguage = '中文';
            }

            console.log('语言检测结果:', { sourceLanguage, targetLanguage });

            // 创建翻译弹窗
            const translationDialog = document.createElement('div');
            translationDialog.id = 'translationDialog';
            translationDialog.className = 'dialog-overlay';
            translationDialog.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.5);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 10000;
            animation: fadeIn 0.3s ease;
        `;

            console.log('创建弹窗元素完成');

            // 根据翻译状态生成不同的内容
            let translationContent;
            if (isTranslating) {
                // 翻译中的状态
                translationContent = `
                <div style="
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    padding: 40px 20px;
                    text-align: center;
                ">
                    <div style="
                        width: 40px;
                        height: 40px;
                        border: 3px solid #f3f3f3;
                        border-top: 3px solid #007bff;
                        border-radius: 50%;
                        animation: spin 1s linear infinite;
                        margin-bottom: 20px;
                    "></div>
                    <div style="
                        color: #007bff;
                        font-size: 16px;
                        font-weight: 500;
                        margin-bottom: 8px;
                    ">正在翻译中...</div>
                    <div style="
                        color: #6c757d;
                        font-size: 14px;
                    ">请稍候，AI正在为您翻译</div>
                </div>
            `;
            } else if (translatedText) {
                // 翻译完成的状态
                translationContent = `
                <div style="
                    white-space: pre-wrap;
                    line-height: 1.6;
                    color: #333;
                    font-size: 14px;
                    max-height: 200px;
                    overflow-y: auto;
                    padding: 12px;
                    background: white;
                    border-radius: 6px;
                    border: 1px solid #b3d9ff;
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                ">${escapeHtml(translatedText)}</div>
            `;
            } else {
                // 默认状态
                translationContent = `
                <div style="
                    color: #6c757d;
                    font-size: 14px;
                    text-align: center;
                    padding: 20px;
                ">准备翻译...</div>
            `;
            }

            translationDialog.innerHTML = `
            <div class="dialog-content" style="
                background: white;
                border-radius: 12px;
                padding: 24px;
                max-width: 700px;
                max-height: 85vh;
                width: 90%;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
                overflow: hidden;
                display: flex;
                flex-direction: column;
                animation: slideIn 0.3s ease;
            ">
                <div class="dialog-header" style="
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 20px;
                    padding-bottom: 15px;
                    border-bottom: 2px solid #f0f0f0;
                ">
                    <div style="display: flex; align-items: center; gap: 12px;">
                        <h3 style="
                            margin: 0;
                            color: #333;
                            font-size: 18px;
                            font-weight: 600;
                            display: flex;
                            align-items: center;
                            gap: 8px;
                        ">
                            <span style="font-size: 20px;">🌐</span>
                            翻译结果
                        </h3>
                        <div style="
                            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                            color: white;
                            padding: 4px 12px;
                            border-radius: 20px;
                            font-size: 12px;
                            font-weight: 500;
                        ">
                            ${sourceLanguage} → ${targetLanguage}
                        </div>
                    </div>
                    <button id="closeTranslationDialog" style="
                        background: none;
                        border: none;
                        font-size: 24px;
                        cursor: pointer;
                        color: #666;
                        padding: 0;
                        width: 30px;
                        height: 30px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        border-radius: 50%;
                        transition: background-color 0.2s;
                    " title="关闭">×</button>
                </div>

                <div class="dialog-body" style="
                    flex: 1;
                    overflow-y: auto;
                    padding-right: 10px;
                    margin-right: -10px;
                ">
                    <div style="
                        display: flex;
                        flex-direction: column;
                        gap: 20px;
                    ">
                        <div style="
                            background: #f8f9fa;
                            border: 1px solid #e9ecef;
                            border-radius: 8px;
                            padding: 16px;
                        ">
                            <h4 style="
                                margin: 0 0 12px 0;
                                color: #495057;
                                font-size: 14px;
                                font-weight: 600;
                                display: flex;
                                align-items: center;
                                gap: 6px;
                            ">
                                <span>📝</span>
                                原文 (${sourceLanguage})
                            </h4>
                            <div style="
                                white-space: pre-wrap;
                                line-height: 1.6;
                                color: #333;
                                font-size: 14px;
                                max-height: 200px;
                                overflow-y: auto;
                                padding: 12px;
                                background: white;
                                border-radius: 6px;
                                border: 1px solid #dee2e6;
                                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                            ">${escapeHtml(originalText)}</div>
                        </div>

                        <div style="
                            background: linear-gradient(135deg, #e7f3ff 0%, #f0f8ff 100%);
                            border: 1px solid #b3d9ff;
                            border-radius: 8px;
                            padding: 16px;
                        ">
                            <h4 style="
                                margin: 0 0 12px 0;
                                color: #0056b3;
                                font-size: 14px;
                                font-weight: 600;
                                display: flex;
                                align-items: center;
                                gap: 6px;
                            ">
                                <span>🔄</span>
                                译文 (${targetLanguage})
                            </h4>
                            <div id="translationContent">
                                ${translationContent}
                            </div>
                        </div>
                    </div>
                </div>

                <div class="dialog-footer" style="
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    gap: 12px;
                    margin-top: 20px;
                    padding-top: 15px;
                    border-top: 1px solid #f0f0f0;
                ">
                    <div style="
                        color: #6c757d;
                        font-size: 12px;
                        display: flex;
                        align-items: center;
                        gap: 6px;
                    ">
                        <span>⚡</span>
                        由AI智能翻译
                    </div>
                    <div style="display: flex; gap: 12px;">
                        <button id="copyTranslationBtn" style="
                            background: #007bff;
                            color: white;
                            border: none;
                            padding: 8px 16px;
                            border-radius: 6px;
                            cursor: pointer;
                            font-size: 14px;
                            transition: background-color 0.2s;
                            display: flex;
                            align-items: center;
                            gap: 6px;
                            ${isTranslating ? 'display: none;' : ''}
                        ">
                            <span>📋</span>
                            复制译文
                        </button>
                        <button id="closeTranslationBtn" style="
                            background: #6c757d;
                            color: white;
                            border: none;
                            padding: 8px 16px;
                            border-radius: 6px;
                            cursor: pointer;
                            font-size: 14px;
                            transition: background-color 0.2s;
                        ">关闭</button>
                    </div>
                </div>
            </div>
        `;

            // 添加CSS动画
            if (!document.getElementById('translation-dialog-animation-style')) {
                const style = document.createElement('style');
                style.id = 'translation-dialog-animation-style';
                style.textContent = `
                @keyframes fadeIn {
                    from { opacity: 0; }
                    to { opacity: 1; }
                }

                @keyframes fadeOut {
                    from { opacity: 1; }
                    to { opacity: 0; }
                }

                @keyframes slideIn {
                    from { transform: translateY(-20px); opacity: 0; }
                    to { transform: translateY(0); opacity: 1; }
                }

                @keyframes spin {
                    0% { transform: rotate(0deg); }
                    100% { transform: rotate(360deg); }
                }

                #closeTranslationDialog:hover {
                    background-color: #f0f0f0;
                }

                #copyTranslationBtn:hover {
                    background-color: #0056b3;
                }

                #closeTranslationBtn:hover {
                    background-color: #545b62;
                }

                .dialog-body::-webkit-scrollbar {
                    width: 6px;
                }

                .dialog-body::-webkit-scrollbar-track {
                    background: #f1f1f1;
                    border-radius: 3px;
                }

                .dialog-body::-webkit-scrollbar-thumb {
                    background: #c1c1c1;
                    border-radius: 3px;
                }

                .dialog-body::-webkit-scrollbar-thumb:hover {
                    background: #a8a8a8;
                }
            `;
                document.head.appendChild(style);
            }

            console.log('弹窗HTML设置完成');

            // 添加到页面
            document.body.appendChild(translationDialog);
            console.log('弹窗已添加到页面');

            // 绑定事件
            const closeTranslationDialog = document.getElementById('closeTranslationDialog');
            const closeTranslationBtn = document.getElementById('closeTranslationBtn');
            const copyTranslationBtn = document.getElementById('copyTranslationBtn');

            console.log('获取按钮元素:', { closeTranslationDialog, closeTranslationBtn, copyTranslationBtn });

            // 关闭弹窗事件
            const closeDialog = () => {
                console.log('关闭弹窗');
                translationDialog.style.animation = 'fadeOut 0.3s ease';
                setTimeout(() => {
                    if (translationDialog.parentNode) {
                        translationDialog.parentNode.removeChild(translationDialog);
                    }
                }, 300);
            };

            closeTranslationDialog.addEventListener('click', closeDialog);
            closeTranslationBtn.addEventListener('click', closeDialog);

            // 点击背景关闭
            translationDialog.addEventListener('click', (e) => {
                if (e.target === translationDialog) {
                    closeDialog();
                }
            });

            // ESC键关闭
            const handleEscKey = (e) => {
                if (e.key === 'Escape') {
                    closeDialog();
                    document.removeEventListener('keydown', handleEscKey);
                }
            };
            document.addEventListener('keydown', handleEscKey);

            // 复制译文（只在翻译完成后显示）
            if (copyTranslationBtn) {
                copyTranslationBtn.addEventListener('click', async () => {
                    try {
                        await navigator.clipboard.writeText(translatedText);

                        // 显示复制成功提示
                        const originalText = copyTranslationBtn.innerHTML;
                        copyTranslationBtn.innerHTML = popup.t('popup.translation.copiedHtml');
                        copyTranslationBtn.style.background = '#28a745';

                        setTimeout(() => {
                            copyTranslationBtn.innerHTML = originalText;
                            copyTranslationBtn.style.background = '#007bff';
                        }, 2000);

                    } catch (error) {
                        console.error('复制失败:', error);
                        popup.showMessage(popup.t('popup.message.copyManual'), 'error');
                    }
                });
            }

            // 按钮悬停效果
            [closeTranslationDialog, closeTranslationBtn, copyTranslationBtn].forEach(btn => {
                if (btn) {
                    btn.addEventListener('mouseenter', () => {
                        btn.style.transform = 'scale(1.05)';
                    });
                    btn.addEventListener('mouseleave', () => {
                        btn.style.transform = 'scale(1)';
                    });
                }
            });

            // 自动聚焦到关闭按钮
            setTimeout(() => {
                closeTranslationBtn.focus();
            }, 100);

            console.log('弹窗事件绑定完成');
        },

        /**
         * 更新翻译弹窗内容
         */
        updateTranslationDialog(originalText, translatedText, showCopyButton = true, isError = false) {
            const translationContent = document.getElementById('translationContent');
            const copyTranslationBtn = document.getElementById('copyTranslationBtn');

            if (!translationContent) {
                console.error('找不到translationContent元素');
                return;
            }

            if (isError) {
                // 显示错误信息
                translationContent.innerHTML = `
                <div style="
                    color: #dc3545;
                    font-size: 14px;
                    text-align: center;
                    padding: 20px;
                    background: #f8d7da;
                    border: 1px solid #f5c6cb;
                    border-radius: 6px;
                ">
                    <div style="margin-bottom: 8px;">❌ 翻译失败</div>
                    <div style="font-size: 12px; color: #721c24;">${translatedText}</div>
                </div>
            `;
            } else {
                // 显示翻译结果
                translationContent.innerHTML = `
                <div style="
                    white-space: pre-wrap;
                    line-height: 1.6;
                    color: #333;
                    font-size: 14px;
                    max-height: 200px;
                    overflow-y: auto;
                    padding: 12px;
                    background: white;
                    border-radius: 6px;
                    border: 1px solid #b3d9ff;
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                ">${escapeHtml(translatedText)}</div>
            `;
            }

            // 显示复制按钮
            if (copyTranslationBtn && showCopyButton && !isError) {
                copyTranslationBtn.style.display = 'flex';

                // 重新绑定复制事件
                copyTranslationBtn.onclick = async () => {
                    try {
                        await navigator.clipboard.writeText(translatedText);

                        // 显示复制成功提示
                        const originalText = copyTranslationBtn.innerHTML;
                        copyTranslationBtn.innerHTML = popup.t('popup.translation.copiedHtml');
                        copyTranslationBtn.style.background = '#28a745';

                        setTimeout(() => {
                            copyTranslationBtn.innerHTML = originalText;
                            copyTranslationBtn.style.background = '#007bff';
                        }, 2000);

                    } catch (error) {
                        console.error('复制失败:', error);
                        popup.showMessage(popup.t('popup.message.copyManual'), 'error');
                    }
                };
            }

            console.log('翻译弹窗内容已更新');
        }
    };
}
