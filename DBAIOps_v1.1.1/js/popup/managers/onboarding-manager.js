/**
 * 引导管理器
 * 负责首次使用引导流程，包括注册和API密钥配置
 */
export function createOnboardingManager(popup) {
    return {
        /**
         * 检查并显示引导
         */
        async checkAndShowOnboarding() {
            // 检查是否已经完成引导
            const onboardingCompleted = await this.isOnboardingCompleted();
            if (onboardingCompleted) {
                console.log('Onboarding completed, skipping display');
                return;
            }

            // 检查用户状态
            const status = await this.checkUserStatus();

            // 如果用户已有有效的 API key，先验证一下，然后标记完成
            if (this.hasValidApiKey()) {
                console.log('Found valid API key, verifying with user profile API...');
                // 尝试验证API key并获取用户信息
                const verified = await this.verifyApiKeyAndUpdateUserInfo();
                if (verified) {
                    await this.markOnboardingCompleted();
                    console.log('API key verified successfully, onboarding marked as completed');
                    return;
                }
                // 验证失败，可能是网络问题或API key无效，继续显示引导
                console.warn('API key verification failed, showing onboarding');
            } else if (status.isComplete) {
                // 如果状态显示已完成但还没有API key验证，仍然标记完成（兼容旧逻辑）
                await this.markOnboardingCompleted();
                return;
            }

            // 否则显示第一步：输入 API key
            await this.showOnboardingStep(1);
        },

        /**
         * 检查用户状态
         */
        async checkUserStatus() {
            // 检查注册状态
            const registration = await this.getRegistrationStatus();
            const isRegistered = registration && registration.status === 'registered';

            // 检查API密钥状态
            const hasApiKey = this.hasValidApiKey();

            return {
                isRegistered,
                needsRegistration: !isRegistered,
                needsApiKey: isRegistered && !hasApiKey,
                isComplete: isRegistered && hasApiKey
            };
        },

        /**
         * 获取注册状态
         */
        async getRegistrationStatus() {
            return new Promise((resolve) => {
                if (typeof chrome === 'undefined' || !chrome.storage?.sync?.get) {
                    resolve(null);
                    return;
                }
                chrome.storage.sync.get(['registration'], (items) => {
                    if (chrome.runtime?.lastError) {
                        console.error('Failed to read registration status:', chrome.runtime.lastError);
                        resolve(null);
                        return;
                    }
                    resolve(items.registration || null);
                });
            });
        },

        /**
         * 检查是否有有效的API密钥
         */
        hasValidApiKey() {
            // 优先检查知识服务配置中的API密钥
            if (popup.knowledgeServiceConfig && popup.knowledgeServiceConfig.api_key && popup.knowledgeServiceConfig.api_key.trim() !== '') {
                return true;
            }
            // 其次检查服务商配置中的API密钥
            if (popup.providers && popup.providers.length > 0) {
                return popup.providers.some(provider =>
                    provider.apiKey && provider.apiKey.trim() !== ''
                );
            }
            // 最后检查模型配置中的API密钥
            if (popup.models && popup.models.length > 0) {
                return popup.models.some(model =>
                    model.apiKey && model.apiKey.trim() !== ''
                );
            }
            return false;
        },

        /**
         * 获取当前的API密钥
         */
        getCurrentApiKey() {
            // 优先从知识服务配置获取
            if (popup.knowledgeServiceConfig && popup.knowledgeServiceConfig.api_key && popup.knowledgeServiceConfig.api_key.trim() !== '') {
                return popup.knowledgeServiceConfig.api_key.trim();
            }
            // 其次从服务商配置获取
            if (popup.providers && popup.providers.length > 0) {
                const providerWithKey = popup.providers.find(p => p && p.apiKey && String(p.apiKey).trim());
                if (providerWithKey) return String(providerWithKey.apiKey).trim();
            }
            // 最后从模型配置获取
            if (popup.models && popup.models.length > 0) {
                const modelWithKey = popup.models.find(m => m && m.apiKey && String(m.apiKey).trim());
                if (modelWithKey) return String(modelWithKey.apiKey).trim();
            }
            return null;
        },

        /**
         * 验证API key并更新用户信息
         * 返回true表示验证成功，false表示验证失败
         */
        async verifyApiKeyAndUpdateUserInfo() {
            const apiKey = this.getCurrentApiKey();
            if (!apiKey) {
                console.log('No API key found, skip verification');
                return false;
            }

            try {
                console.log('Verifying API key by calling user profile API...');
                const testEndpoint = '/api/user/profile';

                let result;
                if (popup.requestUtil) {
                    const tempProvider = {
                        authType: 'Bearer',
                        apiKey: apiKey
                    };
                    result = await popup.requestUtil.post(testEndpoint, null, {
                        provider: tempProvider
                    });
                } else {
                    const headers = {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${apiKey}`
                    };
                    const response = await fetch(testEndpoint, {
                        method: 'POST',
                        headers: headers
                    });
                    if (!response.ok) {
                        console.warn('API key verification failed:', response.status, response.statusText);
                        return false;
                    }
                    result = await response.json();
                }

                // 检查响应是否有效
                if (result && result.code === 200 && result.success === true && result.user) {
                    const user = result.user || {};
                    const knowledgeServiceConfig = popup.knowledgeServiceConfig || {};

                    // 读取现有注册信息
                    const existingRegistration = await new Promise((resolve) => {
                        chrome.storage.sync.get(['registration'], (items) => {
                            resolve(items.registration || {});
                        });
                    });

                    // 更新注册信息
                    const registrationData = {
                        ...existingRegistration,
                        username: user.userName || user.username || existingRegistration.username || '',
                        company: user.companyName || user.company || existingRegistration.company || '',
                        email: user.email || existingRegistration.email || '',
                        serviceUrl: knowledgeServiceConfig.default_url || existingRegistration.serviceUrl || 'https://api.bic-qa.com/api/chat/message',
                        registeredAt: existingRegistration.registeredAt || new Date().toISOString(),
                        status: 'registered'
                    };

                    await chrome.storage.sync.set({ registration: registrationData });
                    console.log('User info updated from API:', registrationData);
                    return true;
                } else {
                    console.warn('API key verification failed: invalid response format', result);
                    return false;
                }
            } catch (error) {
                console.warn('API key verification failed with error:', error.message);
                // 验证失败不影响后续流程，返回false即可
                return false;
            }
        },

        /**
         * 检查引导是否已完成
         */
        async isOnboardingCompleted() {
            return new Promise((resolve) => {
                if (typeof chrome === 'undefined' || !chrome.storage?.local?.get) {
                    resolve(false);
                    return;
                }
                chrome.storage.local.get(['onboardingCompleted'], (items) => {
                    if (chrome.runtime?.lastError) {
                        console.error('Failed to read onboarding status:', chrome.runtime.lastError);
                        resolve(false);
                        return;
                    }
                    resolve(items.onboardingCompleted === true);
                });
            });
        },

        /**
         * 标记引导完成
         */
        async markOnboardingCompleted() {
            return new Promise(async (resolve) => {
                if (typeof chrome === 'undefined' || !chrome.storage?.local?.set) {
                    resolve();
                    return;
                }
                chrome.storage.local.set({ onboardingCompleted: true }, async () => {
                    if (chrome.runtime?.lastError) {
                        console.error('Failed to save onboarding status:', chrome.runtime.lastError);
                    }

                    // 引导完成时检查版本更新
                    try {
                        console.log('用户完成引导，开始检查版本更新');
                        await popup.checkVersionUpdate();
                    } catch (error) {
                        console.error('版本检查失败:', error);
                    }

                    resolve();
                });
            });
        },

        /**
         * 显示引导步骤
         */
        async showOnboardingStep(step) {
            // 创建或获取引导模态框
            let modal = document.getElementById('onboardingModal');
            if (!modal) {
                modal = this.createOnboardingModal();
                document.body.appendChild(modal);
            }

            // 显示对应步骤
            await this.renderStep(modal, step);

            // 显示模态框（带淡入动画）
            modal.style.display = 'flex';
            setTimeout(() => {
                modal.classList.add('active');
            }, 10);
        },

        /**
         * 创建引导模态框
         */
        createOnboardingModal() {
            const modal = document.createElement('div');
            modal.id = 'onboardingModal';
            modal.className = 'onboarding-modal';
            modal.innerHTML = `
                <div class="onboarding-modal-content">
                    <div class="onboarding-header">
                        <div class="onboarding-progress">
                            <span class="progress-text" id="onboardingProgressText">1/2</span>
                        </div>
                        <button class="onboarding-close" id="onboardingCloseBtn" aria-label="" data-i18n-aria-label="popup.onboarding.common.close">×</button>
                    </div>
                    <div class="onboarding-body" id="onboardingBody">
                        <!-- 步骤内容将动态渲染 -->
                    </div>
                </div>
            `;

            // 绑定关闭按钮事件
            const closeBtn = modal.querySelector('#onboardingCloseBtn');
            closeBtn.addEventListener('click', () => {
                this.handleSkip();
            });

            // 点击背景关闭
            modal.addEventListener('click', (e) => {
                if (e.target === modal) {
                    this.handleSkip();
                }
            });

            // 创建时立即应用国际化
            const currentLanguage = popup.currentLanguage || popup.i18n?.currentLanguage || popup.i18n?.defaultLanguage || 'zhcn';
            popup.applyI18nToElement(modal, currentLanguage);

            return modal;
        },

        /**
         * 渲染步骤内容
         */
        async renderStep(modal, step) {
            const body = modal.querySelector('#onboardingBody');
            const progressText = modal.querySelector('#onboardingProgressText');

            // 更新进度
            progressText.textContent = `${step}/2`;

            // 淡出当前内容
            body.style.opacity = '0';

            setTimeout(async () => {
                if (step === 1) {
                    body.innerHTML = await this.renderStep1();
                } else if (step === 2) {
                    body.innerHTML = this.renderStep2();
                }

                // 绑定事件（会应用国际化）
                // 注意：由于innerHTML会重新创建元素，所以每次都需要重新绑定事件
                this.bindStepEvents(modal, step);

                // 淡入新内容
                setTimeout(() => {
                    body.style.opacity = '1';
                }, 10);
            }, 200);
        },

        /**
         * 更新引导弹框的国际化（当语言切换时调用）
         */
        updateOnboardingI18n(language) {
            // 确保使用正确的语言进行翻译
            const targetLanguage = language || popup.currentLanguage || popup.i18n?.currentLanguage || popup.i18n?.defaultLanguage || 'zhcn';

            const modal = document.getElementById('onboardingModal');
            if (modal) {
                // 检查模态框是否可见（display不为none）
                const isVisible = modal.style.display !== 'none' && modal.style.display !== '';

                if (isVisible) {
                    // 应用国际化到整个模态框
                    popup.applyI18nToElement(modal, targetLanguage);

                    // 更新按钮文本（如果按钮不是处于特殊状态）
                    const submitBtn = modal.querySelector('button[type="submit"]');
                    if (submitBtn && submitBtn.dataset.i18n && !submitBtn.disabled) {
                        const originalText = submitBtn.dataset.i18n;
                        submitBtn.textContent = popup.i18n.t(originalText, targetLanguage);
                    }

                    const testBtn = modal.querySelector('#onboardingTestBtn');
                    if (testBtn && testBtn.dataset.i18n && !testBtn.disabled) {
                        // 只有在按钮不是禁用状态时才更新文本（避免覆盖"测试中..."等状态文本）
                        const originalText = testBtn.dataset.i18n;
                        testBtn.textContent = popup.i18n.t(originalText, targetLanguage);
                    }
                }
            }

            // 更新提醒横幅
            const reminderBanner = document.querySelector('.onboarding-reminder-banner');
            if (reminderBanner) {
                popup.applyI18nToElement(reminderBanner, targetLanguage);

                // 更新横幅中的消息文本
                const reminderText = reminderBanner.querySelector('.reminder-text');
                if (reminderText) {
                    // 从 data-i18n-reminder-key 属性获取需要使用的国际化键
                    const reminderKey = reminderText.getAttribute('data-i18n-reminder-key');
                    if (reminderKey) {
                        // 直接使用国际化键更新文本
                        const message = popup.i18n?.t(reminderKey, targetLanguage);
                        if (message) {
                            reminderText.textContent = message;
                        }
                    } else {
                        // 如果没有 data-i18n-reminder-key，则重新获取当前状态并更新消息（兼容旧代码）
                        this.checkUserStatus().then(status => {
                            let message = '';
                            if (status.needsRegistration) {
                                message = popup.i18n?.t('popup.onboarding.reminder.registration', targetLanguage);
                            } else if (status.needsApiKey) {
                                message = popup.i18n?.t('popup.onboarding.reminder.apiKey', targetLanguage);
                            }
                            if (message) {
                                reminderText.textContent = message;
                                // 同时更新 data-i18n-reminder-key 属性，以便下次语言切换时使用
                                reminderText.setAttribute('data-i18n-reminder-key', status.needsRegistration ? 'popup.onboarding.reminder.registration' : 'popup.onboarding.reminder.apiKey');
                            }
                        });
                    }
                }
            }
        },

        /**
         * 渲染步骤1：输入 API 密钥
         */
        async renderStep1() {
            return `
                <div class="onboarding-step">
                    <div class="step-icon">🔑</div>
                    <h2 class="step-title" data-i18n="popup.onboarding.step1.title">欢迎使用 DBAIOps</h2>
                    <p class="step-description" data-i18n="popup.onboarding.step1.description">如果是老用户，请输入您的 API 密钥进入使用；如果是新用户，可点击注册</p>

                    <form id="onboardingApiKeyFormStep1" class="onboarding-form">
                        <div class="form-group">
                            <label for="onboardingApiKeyStep1" data-i18n="popup.onboarding.step1.apiKeyLabel">API 密钥 *</label>
                            <div class="password-input-wrapper">
                                <input type="password" id="onboardingApiKeyStep1" name="apiKey" required
                                    data-i18n-placeholder="popup.onboarding.step1.apiKeyPlaceholder">
                                <button type="button" class="toggle-password-btn" id="toggleApiKeyStep1Btn">👁</button>
                            </div>
                        </div>
                        <div id="onboardingApiKeyValidationStep1" class="validation-message" style="display: none;"></div>
                        <div class="form-actions">
                            <button type="button" class="btn-skip" id="onboardingSkipBtn"
                                data-i18n="popup.onboarding.common.skip">稍后配置</button>
                            <button type="button" class="btn-register" id="onboardingRegisterBtn"
                                data-i18n="popup.onboarding.step1.register">注册</button>
                            <button type="button" class="btn-primary" id="onboardingEnterBtn"
                                data-i18n="popup.onboarding.step1.enter">进入</button>
                        </div>
                    </form>
                </div>
            `;
        },

        /**
         * 渲染步骤2：配置API密钥
         */
        renderStep2() {
            return `
                <div class="onboarding-step">
                    <div class="step-icon">🔑</div>
                    <h2 class="step-title" data-i18n="popup.onboarding.step2.title">配置 API 密钥</h2>
                    <p class="step-description" data-i18n="popup.onboarding.step2.description">请配置您的 API 密钥以开始使用智能问答功能</p>

                    <form id="onboardingApiKeyForm" class="onboarding-form">
                        <div class="form-group">
                            <label for="onboardingApiKey" data-i18n="popup.onboarding.step2.apiKeyLabel">API 密钥 *</label>
                            <div class="password-input-wrapper">
                                <input type="password" id="onboardingApiKey" name="apiKey" required
                                    data-i18n-placeholder="popup.onboarding.step2.apiKeyPlaceholder">
                                <button type="button" class="toggle-password-btn" id="toggleApiKeyBtn">👁</button>
                            </div>
                        </div>
                        <div id="onboardingApiKeyValidation" class="validation-message" style="display: none;"></div>
                        <div class="form-actions">
                            <button type="button" class="btn-skip" id="onboardingSkipBtn"
                                data-i18n="popup.onboarding.common.skip">稍后配置</button>
                            <button type="button" class="btn-secondary" id="onboardingTestBtn"
                                data-i18n="popup.onboarding.step2.test">测试连接</button>
                            <button type="submit" class="btn-primary"
                                data-i18n="popup.onboarding.step2.submit">保存并继续</button>
                        </div>
                    </form>
                </div>
            `;
        },

        /**
         * 绑定步骤事件
         */
        bindStepEvents(modal, step) {
            // 应用国际化 - 使用当前语言，不影响主页面的语言设置
            const currentLanguage = popup.currentLanguage || popup.i18n?.currentLanguage || popup.i18n?.defaultLanguage || 'zhcn';
            popup.applyI18nToElement(modal, currentLanguage);

            if (step === 1) {
                const form = modal.querySelector('#onboardingApiKeyFormStep1');
                const skipBtn = modal.querySelector('#onboardingSkipBtn');
                const enterBtn = modal.querySelector('#onboardingEnterBtn');
                const registerBtn = modal.querySelector('#onboardingRegisterBtn');
                const toggleBtn = modal.querySelector('#toggleApiKeyStep1Btn');
                const apiKeyInput = modal.querySelector('#onboardingApiKeyStep1');

                if (skipBtn) {
                    skipBtn.addEventListener('click', () => {
                        this.handleSkip();
                    });
                }

                // 点击进入按钮：先测试连接，成功后再进入使用
                if (enterBtn) {
                    enterBtn.addEventListener('click', () => {
                        this.handleEnterWithApiKey(popup, form);
                    });
                }

                // 点击注册按钮：显示注册表单
                if (registerBtn) {
                    registerBtn.addEventListener('click', () => {
                        this.showRegisterForm(modal);
                    });
                }

                // 切换密码显示
                if (toggleBtn && apiKeyInput) {
                    toggleBtn.addEventListener('click', () => {
                        const type = apiKeyInput.type === 'password' ? 'text' : 'password';
                        apiKeyInput.type = type;
                        toggleBtn.textContent = type === 'password' ? '👁' : '🙈';
                    });
                }

                // 监听 API key 输入变化，清空验证状态
                if (apiKeyInput) {
                    apiKeyInput.addEventListener('input', () => {
                        const validationEl = form.querySelector('#onboardingApiKeyValidationStep1');
                        if (validationEl) {
                            validationEl.style.display = 'none';
                            validationEl.className = 'validation-message';
                            validationEl.textContent = '';
                        }
                    });
                }
            } else if (step === 2) {
                const form = modal.querySelector('#onboardingApiKeyForm');
                const skipBtn = modal.querySelector('#onboardingSkipBtn');
                const testBtn = modal.querySelector('#onboardingTestBtn');
                const toggleBtn = modal.querySelector('#toggleApiKeyBtn');
                const apiKeyInput = modal.querySelector('#onboardingApiKey');

                if (form) {
                    form.addEventListener('submit', (e) => {
                        e.preventDefault();
                        this.handleApiKeySubmit(popup, form);
                    });
                }

                if (skipBtn) {
                    skipBtn.addEventListener('click', () => {
                        this.handleSkip();
                    });
                }

                if (testBtn) {
                    testBtn.addEventListener('click', () => {
                        this.handleTestApiKey(popup, form);
                    });
                }

                // 切换密码显示
                if (toggleBtn && apiKeyInput) {
                    toggleBtn.addEventListener('click', () => {
                        const type = apiKeyInput.type === 'password' ? 'text' : 'password';
                        apiKeyInput.type = type;
                        toggleBtn.textContent = type === 'password' ? '👁' : '🙈';
                    });
                }
            }
        },

        /**
         * 通过 API key 进入使用（先测试连接，成功后再进入）
         */
        async handleEnterWithApiKey(popup, form) {
            const formData = new FormData(form);
            const apiKey = formData.get('apiKey').trim();

            if (!apiKey) {
                popup.showMessage(popup.t('popup.onboarding.step1.validation.apiKeyRequired', '请输入 API 密钥'), 'error');
                return;
            }

            const validationEl = form.querySelector('#onboardingApiKeyValidationStep1');
            const enterBtn = form.querySelector('#onboardingEnterBtn');

            // 显示验证中状态
            enterBtn.disabled = true;
            enterBtn.textContent = popup.t('popup.onboarding.step1.verifying', '验证中...');
            validationEl.style.display = 'block';
            validationEl.className = 'validation-message testing';
            validationEl.textContent = popup.t('popup.onboarding.step1.verifying', '正在验证 API 密钥...');

            try {
                // 先测试连接：使用 API key 获取用户信息
                const testEndpoint = '/api/user/profile';

                let result;
                if (popup.requestUtil) {
                    // 创建临时provider用于测试
                    const tempProvider = {
                        authType: 'Bearer',
                        apiKey: apiKey
                    };

                    result = await popup.requestUtil.post(testEndpoint, null, {
                        provider: tempProvider
                    });
                } else {
                    const headers = {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${apiKey}`
                    };

                    const response = await fetch(testEndpoint, {
                        method: 'POST',
                        headers: headers
                    });

                    if (!response.ok) {
                        const errorMsg = popup.t('popup.onboarding.step1.apiKeyInvalid', 'API 密钥无效');
                        throw new Error(`${errorMsg}: HTTP ${response.status}: ${response.statusText}`);
                    }

                    result = await response.json();
                }

                // 检查响应体中的success和code字段（测试连接失败）
                if (result && (result.success === false || result.code === 400 || (result.code && result.code !== 200))) {
                    const errorMessage = result.message || result.error || 'API KEY格式无效';
                    validationEl.className = 'validation-message error';
                    validationEl.textContent = errorMessage;
                    popup.showMessage(errorMessage, 'error');
                    enterBtn.disabled = false;
                    enterBtn.textContent = popup.t('popup.onboarding.step1.enter', '进入');
                    return;
                }

                // 测试连接成功，继续进入流程

                // 验证成功，保存 API key
                const knowledgeServiceConfig = {
                    api_key: apiKey,
                    default_url: popup.knowledgeServiceConfig?.default_url || 'https://api.bic-qa.com/api/chat/message',
                    enabled: popup.knowledgeServiceConfig?.enabled !== undefined ? popup.knowledgeServiceConfig.enabled : false,
                    updated_at: new Date().toISOString()
                };

                // 保存到sync存储
                await chrome.storage.sync.set({ knowledgeServiceConfig: knowledgeServiceConfig });

                // 同时保存到local存储
                await chrome.storage.local.set({ knowledgeServiceConfig: knowledgeServiceConfig });

                // 更新popup实例中的配置
                popup.knowledgeServiceConfig = knowledgeServiceConfig;

                // 如果获取到用户信息，保存注册信息（根据 user-profile-manager.js 的结构）
                if (result && result.code === 200 && result.success === true && result.user) {
                    const user = result.user || {};
                    const registrationData = {
                        username: user.userName || user.username || '',
                        company: user.companyName || user.company || '',
                        email: user.email || '',
                        serviceUrl: knowledgeServiceConfig.default_url,
                        registeredAt: new Date().toISOString(),
                        status: 'registered'
                    };
                    await chrome.storage.sync.set({ registration: registrationData });
                    console.log('用户信息已保存:', registrationData);
                } else if (result && (result.userName || result.email)) {
                    // 兼容旧格式（直接返回用户信息）
                    const registrationData = {
                        username: result.userName || result.username || '',
                        company: result.companyName || result.company || '',
                        email: result.email || '',
                        serviceUrl: knowledgeServiceConfig.default_url,
                        registeredAt: new Date().toISOString(),
                        status: 'registered'
                    };
                    await chrome.storage.sync.set({ registration: registrationData });
                    console.log('用户信息已保存（旧格式）:', registrationData);
                }

                // 标记引导完成
                await this.markOnboardingCompleted();

                // 显示成功提示
                validationEl.className = 'validation-message success';
                validationEl.textContent = popup.t('popup.onboarding.step1.enterSuccess', '验证成功，正在进入...');
                popup.showMessage(
                    popup.t('popup.onboarding.step1.enterSuccess', '验证成功！'),
                    'success'
                );

                // 延迟后关闭引导
                setTimeout(() => {
                    this.hideOnboarding();
                }, 1000);
            } catch (error) {
                console.error('API key verification failed:', error);
                validationEl.className = 'validation-message error';
                const errorMsg = popup.t('popup.onboarding.step1.apiKeyInvalid', 'API 密钥无效');
                validationEl.textContent = `${errorMsg}: ${error.message}`;
                popup.showMessage(
                    `${errorMsg}: ${error.message}`,
                    'error'
                );
                enterBtn.disabled = false;
                enterBtn.textContent = popup.t('popup.onboarding.step1.enter', '进入');
            }
        },

        /**
         * 显示注册表单
         */
        showRegisterForm(modal) {
            const body = modal.querySelector('#onboardingBody');

            // 淡出当前内容
            body.style.opacity = '0';

            setTimeout(async () => {
                body.innerHTML = `
                    <div class="onboarding-step">
                        <div class="step-icon">📝</div>
                        <h2 class="step-title" data-i18n="popup.onboarding.step1.registerTitle">用户注册</h2>
                        <p class="step-description" data-i18n="popup.onboarding.step1.registerDescription">请填写注册信息，注册成功后 API 密钥将发送到您的邮箱</p>

                        <form id="onboardingRegisterForm" class="onboarding-form">
                            <div class="form-group">
                                <label for="onboardingUsername" data-i18n="popup.onboarding.step1.usernameLabel">用户名 *</label>
                                <input type="text" id="onboardingUsername" name="username" required
                                    data-i18n-placeholder="popup.onboarding.step1.usernamePlaceholder">
                            </div>
                            <div class="form-group">
                                <label for="onboardingCompany" data-i18n="popup.onboarding.step1.companyLabel">公司名称 *</label>
                                <input type="text" id="onboardingCompany" name="company" required
                                    data-i18n-placeholder="popup.onboarding.step1.companyPlaceholder">
                            </div>
                            <div class="form-group">
                                <label for="onboardingEmail" data-i18n="popup.onboarding.step1.emailLabel">邮箱 *</label>
                                <input type="email" id="onboardingEmail" name="email" required
                                    data-i18n-placeholder="popup.onboarding.step1.emailPlaceholder">
                            </div>
                            <div class="form-actions">
                                <button type="button" class="btn-skip" id="onboardingBackBtn"
                                    data-i18n="popup.onboarding.step1.back">返回</button>
                                <button type="submit" class="btn-primary"
                                    data-i18n="popup.onboarding.step1.submit">注册</button>
                            </div>
                        </form>
                    </div>
                `;

                // 应用国际化
                const currentLanguage = popup.currentLanguage || popup.i18n?.currentLanguage || popup.i18n?.defaultLanguage || 'zhcn';
                popup.applyI18nToElement(body, currentLanguage);

                // 绑定事件
                const form = body.querySelector('#onboardingRegisterForm');
                const backBtn = body.querySelector('#onboardingBackBtn');

                if (form) {
                    form.addEventListener('submit', (e) => {
                        e.preventDefault();
                        this.handleRegisterSubmit(popup, form);
                    });
                }

                if (backBtn) {
                    backBtn.addEventListener('click', async () => {
                        // 重新渲染第一步
                        await this.renderStep(modal, 1);
                    });
                }

                // 淡入新内容
                setTimeout(() => {
                    body.style.opacity = '1';
                }, 10);
            }, 200);
        },

        /**
         * 处理注册提交
         */
        async handleRegisterSubmit(popup, form) {
            const formData = new FormData(form);
            const username = formData.get('username').trim();
            const company = formData.get('company').trim();
            const email = formData.get('email').trim();

            if (!username || !company || !email) {
                popup.showMessage(popup.t('popup.onboarding.step1.validation.required'), 'error');
                return;
            }

            try {
                // 加载注册配置
                const registrationConfig = await this.loadRegistrationConfig();
                const serviceUrl = registrationConfig?.registration_service?.default_url ||
                    'https://api.bic-qa.com/api/user/register';

                const requestData = {
                    userName: username,
                    companyName: company,
                    email: email,
                    timestamp: new Date().toISOString()
                };

                // 显示加载状态
                const submitBtn = form.querySelector('button[type="submit"]');
                const originalText = submitBtn.textContent;
                submitBtn.disabled = true;
                submitBtn.textContent = popup.t('popup.onboarding.step1.submitting', 'Registering...');

                // 发送注册请求
                let result;
                if (popup.requestUtil) {
                    result = await popup.requestUtil.post(serviceUrl, requestData, {});
                } else {
                    const response = await fetch(serviceUrl, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'Accept-Language': popup.getAcceptLanguage()
                        },
                        body: JSON.stringify(requestData)
                    });

                    if (!response.ok) {
                        const errorMsg = popup.t('popup.onboarding.step1.error', 'Registration failed');
                        throw new Error(`${errorMsg}: HTTP ${response.status}: ${response.statusText}`);
                    }

                    result = await response.json();
                }

                submitBtn.disabled = false;
                submitBtn.textContent = originalText;

                if (result && result.status === 'success') {
                    // 保存注册信息
                    const registrationData = {
                        username: username,
                        company: company,
                        email: email,
                        serviceUrl: serviceUrl,
                        registeredAt: new Date().toISOString(),
                        status: 'registered'
                    };

                    await chrome.storage.sync.set({ registration: registrationData });

                    // 显示成功提示：注册成功，API key已发往您的邮箱请查收
                    const successMsg = popup.t('popup.onboarding.step1.registerSuccess', '注册成功，API key已发往您的邮箱请查收');
                    popup.showMessage(successMsg, 'success', { durationMs: 3000 });

                    // 延迟后进入第二步输入 API key
                    setTimeout(() => {
                        this.showOnboardingStep(2);
                    }, 1500);
                } else {
                    popup.showMessage(
                        result?.message || popup.t('popup.onboarding.step1.error', '注册失败，请重试'),
                        'error'
                    );
                }
            } catch (error) {
                console.error('Registration failed:', error);
                const submitBtn = form.querySelector('button[type="submit"]');
                submitBtn.disabled = false;
                submitBtn.textContent = popup.t('popup.onboarding.step1.submit', 'Register');
                const errorMsg = popup.t('popup.onboarding.step1.error', 'Registration failed, please try again');
                popup.showMessage(
                    `${errorMsg}: ${error.message}`,
                    'error'
                );
            }
        },

        /**
         * 处理API密钥提交
         */
        async handleApiKeySubmit(popup, form) {
            const formData = new FormData(form);
            const apiKey = formData.get('apiKey').trim();

            if (!apiKey) {
                popup.showMessage(popup.t('popup.onboarding.step2.validation.required'), 'error');
                return;
            }

            try {
                // 先读取现有的知识服务配置（从sync存储）
                const existingConfig = await new Promise((resolve) => {
                    chrome.storage.sync.get(['knowledgeServiceConfig'], (items) => {
                        resolve(items.knowledgeServiceConfig || {});
                    });
                });

                // 保存到知识服务配置
                const knowledgeServiceConfig = {
                    ...existingConfig,
                    api_key: apiKey,
                    default_url: existingConfig.default_url || 'https://api.bic-qa.com/api/chat/message',
                    enabled: existingConfig.enabled !== undefined ? existingConfig.enabled : false,
                    updated_at: new Date().toISOString()
                };

                // 保存到sync存储（设置页面从这里读取）
                await chrome.storage.sync.set({ knowledgeServiceConfig: knowledgeServiceConfig });

                // 同时保存到local存储（popup页面从这里读取）
                await chrome.storage.local.set({ knowledgeServiceConfig: knowledgeServiceConfig });

                // 更新popup实例中的配置
                popup.knowledgeServiceConfig = knowledgeServiceConfig;

                // 获取并保存用户信息
                try {
                    const testEndpoint = '/api/user/profile';
                    let userResult;
                    if (popup.requestUtil) {
                        const tempProvider = {
                            authType: 'Bearer',
                            apiKey: apiKey
                        };
                        userResult = await popup.requestUtil.post(testEndpoint, null, {
                            provider: tempProvider
                        });
                    } else {
                        const headers = {
                            'Content-Type': 'application/json',
                            'Authorization': `Bearer ${apiKey}`
                        };
                        const response = await fetch(testEndpoint, {
                            method: 'POST',
                            headers: headers
                        });
                        if (response.ok) {
                            userResult = await response.json();
                        }
                    }

                    // 如果获取到用户信息，更新注册信息
                    if (userResult && userResult.code === 200 && userResult.success === true && userResult.user) {
                        const user = userResult.user || {};
                        // 读取现有注册信息，保留原有信息，只更新用户信息
                        const existingRegistration = await new Promise((resolve) => {
                            chrome.storage.sync.get(['registration'], (items) => {
                                resolve(items.registration || {});
                            });
                        });

                        const registrationData = {
                            ...existingRegistration,
                            username: user.userName || user.username || existingRegistration.username || '',
                            company: user.companyName || user.company || existingRegistration.company || '',
                            email: user.email || existingRegistration.email || '',
                            serviceUrl: knowledgeServiceConfig.default_url,
                            registeredAt: existingRegistration.registeredAt || new Date().toISOString(),
                            status: 'registered'
                        };
                        await chrome.storage.sync.set({ registration: registrationData });
                        console.log('用户信息已更新:', registrationData);
                    }
                } catch (error) {
                    console.error('获取用户信息失败:', error);
                    // 获取用户信息失败不影响保存 API key
                }

                // 显示成功提示
                popup.showMessage(
                    popup.t('popup.onboarding.step2.success', 'API key configured successfully!'),
                    'success'
                );

                // 标记引导完成
                await this.markOnboardingCompleted();

                // 2秒后关闭引导
                setTimeout(() => {
                    this.hideOnboarding();
                    // 显示完成提示
                    popup.showMessage(
                        popup.t('popup.onboarding.completed', 'Configuration completed, you can start using now!'),
                        'success',
                        { durationMs: 2000 }
                    );
                }, 2000);
            } catch (error) {
                console.error('Failed to save API key:', error);
                const errorMsg = popup.t('popup.onboarding.step2.error', 'Save failed, please try again');
                popup.showMessage(
                    `${errorMsg}: ${error.message}`,
                    'error'
                );
            }
        },

        /**
         * 处理测试API密钥
         */
        async handleTestApiKey(popup, form) {
            const formData = new FormData(form);
            const apiKey = formData.get('apiKey').trim();

            if (!apiKey) {
                popup.showMessage(popup.t('popup.onboarding.step2.validation.required'), 'error');
                return;
            }

            const validationEl = form.querySelector('#onboardingApiKeyValidation');
            const testBtn = form.querySelector('#onboardingTestBtn');

            // 显示测试中状态
            testBtn.disabled = true;
            testBtn.textContent = popup.t('popup.onboarding.step2.testing', 'Testing...');
            validationEl.style.display = 'block';
            validationEl.className = 'validation-message testing';
            validationEl.textContent = popup.t('popup.onboarding.step2.testing', 'Testing connection...');

            try {
                // 使用知识服务的默认URL进行测试
                const knowledgeServiceConfig = popup.knowledgeServiceConfig || {};
                const testUrl = knowledgeServiceConfig.default_url || 'https://api.bic-qa.com/api/chat/message';

                // 创建临时配置用于测试
                const tempConfig = {
                    api_key: apiKey,
                    default_url: testUrl
                };

                // 尝试调用API验证（使用用户信息接口）
                const testEndpoint = '/api/user/profile';

                let result;
                if (popup.requestUtil) {
                    // 创建临时provider用于测试
                    const tempProvider = {
                        authType: 'Bearer',
                        apiKey: apiKey
                    };

                    result = await popup.requestUtil.post(testEndpoint, null, {
                        provider: tempProvider
                    });
                } else {
                    const headers = {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${apiKey}`
                    };

                    const response = await fetch(testEndpoint, {
                        method: 'POST',
                        headers: headers
                    });

                    if (!response.ok) {
                        const errorMsg = popup.t('popup.onboarding.step2.testError', '✗ API key verification failed');
                        throw new Error(`${errorMsg}: HTTP ${response.status}: ${response.statusText}`);
                    }

                    result = await response.json();
                }

                // 检查响应体中的success和code字段
                if (result && (result.success === false || result.code === 400 || (result.code && result.code !== 200))) {
                    const errorMessage = result.message || result.error || 'API KEY格式无效';
                    validationEl.className = 'validation-message error';
                    const testErrorMsg = popup.t('popup.onboarding.step2.testError', '✗ API key verification failed');
                    validationEl.textContent = `${testErrorMsg}: ${errorMessage}`;
                    popup.showMessage(
                        `${testErrorMsg}: ${errorMessage}`,
                        'error'
                    );
                    return;
                }

                // 测试成功，获取并保存用户信息
                if (result && result.code === 200 && result.success === true && result.user) {
                    const user = result.user || {};
                    // 读取现有注册信息，保留原有信息，只更新用户信息
                    const existingRegistration = await new Promise((resolve) => {
                        chrome.storage.sync.get(['registration'], (items) => {
                            resolve(items.registration || {});
                        });
                    });

                    const registrationData = {
                        ...existingRegistration,
                        username: user.userName || user.username || existingRegistration.username || '',
                        company: user.companyName || user.company || existingRegistration.company || '',
                        email: user.email || existingRegistration.email || '',
                        serviceUrl: popup.knowledgeServiceConfig?.default_url || 'https://api.bic-qa.com/api/chat/message',
                        registeredAt: existingRegistration.registeredAt || new Date().toISOString(),
                        status: 'registered'
                    };
                    await chrome.storage.sync.set({ registration: registrationData });
                    console.log('用户信息已保存（测试通过）:', registrationData);
                }

                // 测试成功
                validationEl.className = 'validation-message success';
                const successMsg = popup.t('popup.onboarding.step2.testSuccess', '✓ API key verification successful');
                validationEl.textContent = successMsg;
                popup.showMessage(successMsg, 'success');
            } catch (error) {
                console.error('API key test failed:', error);
                validationEl.className = 'validation-message error';
                const testErrorMsg = popup.t('popup.onboarding.step2.testError', '✗ API key verification failed');
                validationEl.textContent = `${testErrorMsg}: ${error.message}`;
                popup.showMessage(
                    `${testErrorMsg}: ${error.message}`,
                    'error'
                );
            } finally {
                testBtn.disabled = false;
                testBtn.textContent = popup.t('popup.onboarding.step2.test', 'Test Connection');
            }
        },

        /**
         * 处理跳过
         */
        async handleSkip() {
            this.hideOnboarding();

            // 检查状态，显示提醒横幅
            const status = await this.checkUserStatus();
            if (status.needsRegistration || status.needsApiKey) {
                this.showReminderBanner(status);
            }
        },

        /**
         * 显示提醒横幅
         */
        showReminderBanner(status) {
            // 移除现有横幅
            const existingBanner = document.querySelector('.onboarding-reminder-banner');
            if (existingBanner) {
                existingBanner.remove();
            }

            const banner = document.createElement('div');
            banner.className = 'onboarding-reminder-banner';

            // 获取当前语言
            const currentLanguage = popup.currentLanguage || popup.i18n?.currentLanguage || popup.i18n?.defaultLanguage || 'zhcn';

            let message = '';
            if (status.needsRegistration) {
                message = popup.i18n?.t('popup.onboarding.reminder.registration', currentLanguage) || popup.t('popup.onboarding.reminder.registration', 'Please complete registration to access more features');
            } else if (status.needsApiKey) {
                message = popup.i18n?.t('popup.onboarding.reminder.apiKey', currentLanguage) || popup.t('popup.onboarding.reminder.apiKey', 'Please configure API key to start using intelligent Q&A');
            }

            banner.innerHTML = `
                <span class="reminder-text" data-i18n-reminder-key="${status.needsRegistration ? 'popup.onboarding.reminder.registration' : 'popup.onboarding.reminder.apiKey'}">${message}</span>
                <button class="reminder-action-btn" data-i18n="popup.onboarding.reminder.configure">立即配置</button>
                <button class="reminder-close-btn" aria-label="" data-i18n-aria-label="popup.onboarding.common.close">×</button>
            `;

            // 绑定事件
            const actionBtn = banner.querySelector('.reminder-action-btn');
            const closeBtn = banner.querySelector('.reminder-close-btn');

            actionBtn.addEventListener('click', async () => {
                banner.remove();
                await this.checkAndShowOnboarding();
            });

            closeBtn.addEventListener('click', () => {
                banner.remove();
            });

            // 应用国际化 - 使用当前语言，不影响主页面的语言设置
            popup.applyI18nToElement(banner, currentLanguage);

            // 添加到页面
            const container = document.querySelector('.main-content') || document.body;
            container.insertBefore(banner, container.firstChild);
        },

        /**
         * 隐藏引导
         */
        hideOnboarding() {
            const modal = document.getElementById('onboardingModal');
            if (modal) {
                modal.classList.remove('active');
                setTimeout(() => {
                    modal.style.display = 'none';
                }, 300);
            }
        },

        /**
         * 加载注册配置
         */
        async loadRegistrationConfig() {
            try {
                const response = await fetch('../config/registration.json');
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}`);
                }
                return await response.json();
            } catch (error) {
                console.error('Failed to load registration config:', error);
                return null;
            }
        }
    };
}
