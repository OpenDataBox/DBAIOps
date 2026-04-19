function bindToPopup(fn, popup) {
    return fn.bind(popup);
}

export function createFeedbackService(popup) {
    return {
        handleFeedback: bindToPopup(handleFeedback, popup),
        saveFeedback: bindToPopup(saveFeedback, popup),
        sendFeedbackToServer: bindToPopup(sendFeedbackToServer, popup),
        doAdviceForAnswer: bindToPopup(doAdviceForAnswer, popup),
        addFeedback: bindToPopup(addFeedback, popup),
        updateFeedback: bindToPopup(updateFeedback, popup),
        deleteFeedback: bindToPopup(deleteFeedback, popup),
        updateFeedbackUI: bindToPopup(updateFeedbackUI, popup),
        saveFeedbackId: bindToPopup(saveFeedbackId, popup),
        removeFeedbackId: bindToPopup(removeFeedbackId, popup),
        removeFeedbackStyle: bindToPopup(removeFeedbackStyle, popup)
    };
}

function handleFeedback(type, container) {
    const selectedKnowledgeBase = this.knowledgeBaseSelect.value;

    if (!selectedKnowledgeBase || selectedKnowledgeBase === '不使用知识库(None)') {
        if (container) {
            const likeBtn = container.querySelector('.like-btn');
            const dislikeBtn = container.querySelector('.dislike-btn');

            if (likeBtn && dislikeBtn) {
                const isCurrentlyLiked = likeBtn.classList.contains('active');
                const isCurrentlyDisliked = dislikeBtn.classList.contains('active');

                if (type === 'like') {
                    if (isCurrentlyLiked) {
                        likeBtn.classList.remove('active');
                        this.showMessage(this.t('popup.message.likeCancelled'), 'info');
                    } else {
                        likeBtn.classList.add('active');
                        dislikeBtn.classList.remove('active');
                        this.saveFeedback('like');
                        this.showMessage(this.t('popup.message.feedbackThanksPositive'), 'success');
                    }
                } else if (type === 'dislike') {
                    if (isCurrentlyDisliked) {
                        dislikeBtn.classList.remove('active');
                        this.showMessage(this.t('popup.message.dislikeCancelled'), 'info');
                    } else {
                        dislikeBtn.classList.add('active');
                        likeBtn.classList.remove('active');
                        this.saveFeedback('dislike');
                        this.showMessage(this.t('popup.message.feedbackThanksNegative'), 'info');
                    }
                }
            }
            return;
        }
    } else {
        const questionDisplay = container ? container.querySelector('.question-text') : this.questionText;
        const question = questionDisplay ? questionDisplay.textContent : '';

        const resultText = container ? container.querySelector('.result-text-content') : this.resultText;
        const answer = resultText ? resultText.textContent : '';

        const adviceType = type === 'like' ? 'good' : 'bad';
        this.doAdviceForAnswer(question, answer, adviceType, container);
    }

    return;
    const defaultContainer = this.resultContainer.querySelector('#conversation-default');
    if (defaultContainer) {
        this.handleFeedback(type, defaultContainer);
        return;
    }

    const likeBtn = this.likeButton;
    const dislikeBtn = this.dislikeButton;

    if (!likeBtn || !dislikeBtn) return;

    const isCurrentlyLiked = likeBtn.classList.contains('active');
    const isCurrentlyDisliked = dislikeBtn.classList.contains('active');

    if (type === 'like') {
        if (isCurrentlyLiked) {
            likeBtn.classList.remove('active');
            this.showMessage(this.t('popup.message.likeCancelled'), 'info');
        } else {
            likeBtn.classList.add('active');
            dislikeBtn.classList.remove('active');
            this.saveFeedback('like');
            this.showMessage(this.t('popup.message.feedbackThanksPositive'), 'success');
        }
        this.doAdviceForAnswer(question, answer, adviceType, container);
    } else if (type === 'dislike') {
        if (isCurrentlyDisliked) {
            dislikeBtn.classList.remove('active');
            this.showMessage(this.t('popup.message.dislikeCancelled'), 'info');
        } else {
            dislikeBtn.classList.add('active');
            likeBtn.classList.remove('active');
            this.saveFeedback('dislike');
            this.showMessage(this.t('popup.message.feedbackThanksNegative'), 'info');
        }
        this.doAdviceForAnswer(question, answer, adviceType, container);
    }
}

async function saveFeedback(type) {
    try {
        const currentQuestion = this.questionInput.value;
        const currentAnswer = this.resultText.textContent;
        const selectedModelValue = this.modelSelect.value;
        let currentModel = '';
        try {
            const key = JSON.parse(selectedModelValue);
            const selectedModel = this.models.find(m => m.name === key.name && (!key.provider || m.provider === key.provider));
            currentModel = selectedModel ? `${selectedModel.displayName || selectedModel.name}（${selectedModel.provider}）` : (key.name || '');
        } catch (_) {
            const selectedModel = this.models.find(m => m.name === selectedModelValue);
            currentModel = selectedModel ? `${selectedModel.displayName || selectedModel.name}（${selectedModel.provider}）` : selectedModelValue;
        }
        const currentKnowledgeBase = this.knowledgeBaseSelect.value;

        const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
        const pageUrl = tab ? tab.url : '';

        const maxLength = 500;
        const truncatedQuestion = currentQuestion.length > maxLength ? currentQuestion.substring(0, maxLength) + '...' : currentQuestion;
        const truncatedAnswer = currentAnswer.length > maxLength ? currentAnswer.substring(0, maxLength) + '...' : currentAnswer;

        const feedback = {
            id: Date.now().toString(),
            timestamp: new Date().toISOString(),
            type: type,
            question: truncatedQuestion,
            answer: truncatedAnswer,
            model: currentModel,
            knowledgeBase: currentKnowledgeBase,
            pageUrl: pageUrl ? pageUrl.substring(0, 200) : ''
        };

        const result = await chrome.storage.sync.get(['feedbackHistory']);
        const feedbackHistory = result.feedbackHistory || [];

        feedbackHistory.push(feedback);

        if (feedbackHistory.length > 30) {
            feedbackHistory.splice(0, feedbackHistory.length - 30);
        }

        await chrome.storage.sync.set({ feedbackHistory: feedbackHistory });

        console.log('反馈已保存:', feedback);

        this.sendFeedbackToServer(feedback);

    } catch (error) {
        console.error('保存反馈失败:', error);
        if (error.message && error.message.includes('quota')) {
            console.log('检测到存储配额超限，尝试清理旧数据...');
            await this.cleanupHistoryRecords();
        }
    }
}

async function sendFeedbackToServer(feedback) {
    try {
        console.log('发送反馈到服务器:', feedback);
    } catch (error) {
        console.error('发送反馈到服务器失败:', error);
    }
}

async function doAdviceForAnswer(question, answer, adviceType, container = null) {
    try {
        const targetContainer = container || this.resultContainer;
        if (!targetContainer) {
            console.error('未找到目标容器');
            return;
        }

        const likeBtn = targetContainer.querySelector('.like-btn');
        const dislikeBtn = targetContainer.querySelector('.dislike-btn');

        if (!likeBtn || !dislikeBtn) {
            console.error('未找到反馈按钮');
            return;
        }

        const isCurrentlyLiked = likeBtn.classList.contains('active');
        const isCurrentlyDisliked = dislikeBtn.classList.contains('active');

        const feedbackIdElement = targetContainer.querySelector('.feedback-id');
        const currentFeedbackId = feedbackIdElement ? feedbackIdElement.textContent : null;

        await this.loadKnowledgeServiceConfig();
        let apiKey = '';

        if (this.knowledgeServiceConfig && this.knowledgeServiceConfig.api_key) {
            apiKey = this.knowledgeServiceConfig.api_key.trim();
        }

        if (!apiKey) {
            console.error('未配置API密钥，无法提交反馈', 'error');
            this.showMessage(this.t('popup.message.feedbackThanksPositive'), 'success');
            return;
        }

        const requestData = {
            id: currentFeedbackId ? parseInt(currentFeedbackId) : null,
            question: question,
            answer: answer,
            adviceType: adviceType
        };

        const headers = {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${apiKey}`
        };

        let response;
        let operation = '';

        if (adviceType === 'good') {
            if (isCurrentlyLiked) {
                if (currentFeedbackId) {
                    operation = 'delete';
                    response = await this.deleteFeedback(currentFeedbackId, apiKey);
                } else {
                    this.removeFeedbackStyle(targetContainer);
                    this.showMessage(this.t('popup.message.likeCancelled'), 'info');
                    return;
                }
            } else {
                if (currentFeedbackId && isCurrentlyDisliked) {
                    operation = 'update';
                    response = await this.updateFeedback(requestData, apiKey);
                } else {
                    operation = 'add';
                    response = await this.addFeedback(requestData, apiKey);
                }
            }
        } else if (adviceType === 'bad') {
            if (isCurrentlyDisliked) {
                if (currentFeedbackId) {
                    operation = 'delete';
                    response = await this.deleteFeedback(currentFeedbackId, apiKey);
                } else {
                    this.removeFeedbackStyle(targetContainer);
                    this.showMessage(this.t('popup.message.dislikeCancelled'), 'info');
                    return;
                }
            } else {
                if (currentFeedbackId && isCurrentlyLiked) {
                    operation = 'update';
                    response = await this.updateFeedback(requestData, apiKey);
                } else {
                    operation = 'add';
                    response = await this.addFeedback(requestData, apiKey);
                }
            }
        }

        if (response && response.status === 'success') {
            this.updateFeedbackUI(targetContainer, adviceType, operation, response.data);

            let message = '';
            if (operation === 'add') {
                message = adviceType === 'good' ? '感谢您的反馈！👍' : '感谢您的反馈👎！我们会继续改进。';
            } else if (operation === 'update') {
                message = adviceType === 'good' ? '感谢您的反馈！👍' : '感谢您的反馈👎！我们会继续改进。';
            } else if (operation === 'delete') {
                message = adviceType === 'good' ? '已取消点赞' : '已取消否定';
            }
            this.showMessage(message, 'success');
        } else {
            const errorMsg = response ? response.message || '操作失败' : '网络错误';
            console.error('反馈操作失败:', errorMsg);
            this.showMessage(this.t('popup.message.feedbackThanksPositive'), 'success');
        }

    } catch (error) {
        console.error('反馈操作失败:', error);
        this.showMessage(this.t('popup.message.feedbackThanksPositive'), 'success');
    }
}

async function addFeedback(data, apiKey) {
    try {
        const tempProvider = {
            authType: 'Bearer',
            apiKey: apiKey
        };
        return await this.requestUtil.post('/api/chat/addFeedback', data, {
            provider: tempProvider
        });
    } catch (error) {
        console.error('新增反馈失败:', error);
        throw error;
    }
}

async function updateFeedback(data, apiKey) {
    try {
        const tempProvider = {
            authType: 'Bearer',
            apiKey: apiKey
        };
        return await this.requestUtil.post('/api/chat/updateFeedback', data, {
            provider: tempProvider
        });
    } catch (error) {
        console.error('编辑反馈失败:', error);
        throw error;
    }
}

async function deleteFeedback(id, apiKey) {
    try {
        const tempProvider = {
            authType: 'Bearer',
            apiKey: apiKey
        };
        return await this.requestUtil.post(`/api/chat/deleteFeedback?id=${id}`, null, {
            provider: tempProvider
        });
    } catch (error) {
        console.error('删除反馈失败:', error);
        throw error;
    }
}

function updateFeedbackUI(container, adviceType, operation, responseData) {
    const likeBtn = container.querySelector('.like-btn');
    const dislikeBtn = container.querySelector('.dislike-btn');

    if (!likeBtn || !dislikeBtn) return;

    likeBtn.classList.remove('active');
    dislikeBtn.classList.remove('active');

    if (operation === 'add' || operation === 'update') {
        if (adviceType === 'good') {
            likeBtn.classList.add('active');
        } else if (adviceType === 'bad') {
            dislikeBtn.classList.add('active');
        }

        this.saveFeedbackId(container, responseData.id || responseData.feedbackId);
    } else if (operation === 'delete') {
        this.removeFeedbackId(container);
    }
}

function saveFeedbackId(container, feedbackId) {
    this.removeFeedbackId(container);

    const feedbackIdElement = document.createElement('div');
    feedbackIdElement.className = 'feedback-id';
    feedbackIdElement.style.display = 'none';
    feedbackIdElement.textContent = feedbackId;

    container.appendChild(feedbackIdElement);
}

function removeFeedbackId(container) {
    const existingIdElement = container.querySelector('.feedback-id');
    if (existingIdElement) {
        existingIdElement.remove();
    }
}

function removeFeedbackStyle(container) {
    const likeBtn = container.querySelector('.like-btn');
    const dislikeBtn = container.querySelector('.dislike-btn');

    if (likeBtn) likeBtn.classList.remove('active');
    if (dislikeBtn) dislikeBtn.classList.remove('active');
}
