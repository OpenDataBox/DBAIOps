/**
 * AWR 分析与历史记录模块，将相关方法绑定到 BicQAPopup 实例。
 * @param {import('../app.js').BicQAPopup} app
 */
import { escapeHtml } from '../utils/common.js';

export function attachAwrModule(app) {
    app.showAwrAnalysisDialog = showAwrAnalysisDialog.bind(app);
    app.hideAwrAnalysisDialog = hideAwrAnalysisDialog.bind(app);
    app.loadStoredAwrDatabaseType = loadStoredAwrDatabaseType.bind(app);
    app.loadAwrDatabaseTypes = loadAwrDatabaseTypes.bind(app);
    app.handleAwrDatabaseTypeChange = handleAwrDatabaseTypeChange.bind(app);
    app.resetAwrForm = resetAwrForm.bind(app);
    app.handleFileSelect = handleFileSelect.bind(app);
    app.handleAwrAnalysisSubmit = handleAwrAnalysisSubmit.bind(app);
    app.submitAwrAnalysis = submitAwrAnalysis.bind(app);
    app.showAwrFileValidationDialog = showAwrFileValidationDialog.bind(app);
    app.validateAwrEmail = validateAwrEmail.bind(app);
    app.setupAwrEmailValidation = setupAwrEmailValidation.bind(app);
    app.clearAwrEmailValidation = clearAwrEmailValidation.bind(app);

    app.switchAwrTab = switchAwrTab.bind(app);
    app.handleAwrSearch = handleAwrSearch.bind(app);
    app.handleAwrReset = handleAwrReset.bind(app);
    app.loadAwrHistoryList = loadAwrHistoryList.bind(app);
    app.convertStatusNumberToString = convertStatusNumberToString.bind(app);
    app.convertStatusToString = convertStatusToString.bind(app);
    app.parseDateTime = parseDateTime.bind(app);
    app.renderAwrHistoryList = renderAwrHistoryList.bind(app);
    app.createAwrHistoryTableRow = createAwrHistoryTableRow.bind(app);
    app.getAwrStatusText = getAwrStatusText.bind(app);
    app.getAwrStatusClass = getAwrStatusClass.bind(app);
    app.getAwrNotifyStatusText = getAwrNotifyStatusText.bind(app);
    app.getAwrNotifyStatusClass = getAwrNotifyStatusClass.bind(app);
    app.updateAwrPagination = updateAwrPagination.bind(app);
    app.handleReanalyze = handleReanalyze.bind(app);
    app.handleAwrDownload = handleAwrDownload.bind(app);

    // 新增方法绑定
    app.bindAwrDatabaseTypeChange = bindAwrDatabaseTypeChange.bind(app);
    app.updateAwrDatabaseDescription = updateAwrDatabaseDescription.bind(app);
    app.updateAwrDesensitizationScriptDownloadLinks = updateAwrDesensitizationScriptDownloadLinks.bind(app);
}

async function showAwrAnalysisDialog() {
    if (this.awrAnalysisDialog) {
        this.awrAnalysisDialog.style.display = 'flex';
        this.resetAwrForm();

        // 确保更新图标仍然可见（如果应该显示）
        if (this.ensureUpdateIconVisible) {
            setTimeout(() => {
                this.ensureUpdateIconVisible();
            }, 100);
        }

        // 加载数据库类型选项
        await this.loadAwrDatabaseTypes();

        // 根据环境类型控制邮箱输入框显示
        const envType = await this.getEnvType();
        const emailGroup = document.querySelector('#awrEmail')?.closest('.form-group');
        if (emailGroup) {
            emailGroup.style.display = envType === 'in_env' ? 'none' : 'block';
        }

        // 设置邮箱实时验证
        this.setupAwrEmailValidation();

        await this.loadRegistrationEmail();
        try {
            await this.populateUserProfileFromApi();
        } catch (e) {
            console.error('加载用户信息失败:', e);
        }

        // 重新初始化全局日期时间过滤器（因为对话框关闭时被清理了）
        this.setupDateTimeFilters();

        // 确保切换到新建分析选项卡
        if (typeof this.switchAwrTab === 'function') {
            this.switchAwrTab('new');
        }
    }
}

function hideAwrAnalysisDialog() {
    // 清理日期时间过滤器的事件监听器
    this.cleanupDateTimeFilters();

    // 关闭日期选择器
    this.closeDateTimePicker();

    if (this.awrAnalysisDialog) {
        this.awrAnalysisDialog.style.display = 'none';
        if (this.awrCountdownInterval) {
            clearInterval(this.awrCountdownInterval);
            this.awrCountdownInterval = null;
        }
        if (this.awrSaveBtn) {
            this.awrSaveBtn.disabled = false;
            this.awrSaveBtn.textContent = this.t('popup.main.action.runAnalysis');
        }
        // 移除邮箱验证事件监听器
        if (this.awrEmail && this._awrEmailInputHandler) {
            this.awrEmail.removeEventListener('input', this._awrEmailInputHandler);
            this.awrEmail.removeEventListener('blur', this._awrEmailBlurHandler);
            this._awrEmailInputHandler = null;
            this._awrEmailBlurHandler = null;
        }
        // 移除数据库类型选择事件监听器
        if (this.awrDatabaseType && this._awrDatabaseTypeChangeHandler) {
            this.awrDatabaseType.removeEventListener('change', this._awrDatabaseTypeChangeHandler);
            this._awrDatabaseTypeChangeHandler = null;
        }
        // 隐藏描述信息
        const descriptionElement = document.getElementById('awrDatabaseDescription');
        if (descriptionElement) {
            descriptionElement.style.display = 'none';
        }
        this.resetAwrForm();
    }
}

/**
 * 从API加载AWR数据库类型选项
 */
async function loadAwrDatabaseTypes() {
    const select = this.awrDatabaseType;
    if (!select) return;

    try {
        // 使用知识库管理器的方法，传递 'awr' 类型参数
        const apiResult = await this.loadKnowledgeBasesFromAPI('awr');

        if (apiResult.success && apiResult.data && apiResult.data.length > 0) {
            // 存储知识库数据以便后续使用
            this.awrKnowledgeBases = apiResult.data;

            // 清空现有选项（保留占位符选项）
            const placeholderOption = select.querySelector('option[value=""]');
            select.innerHTML = '';
            if (placeholderOption) {
                select.appendChild(placeholderOption);
            } else {
                // 如果没有占位符，创建一个
                const defaultOption = document.createElement('option');
                defaultOption.value = '';
                defaultOption.textContent = this.t('popup.awr.form.databasePlaceholder');
                select.appendChild(defaultOption);
            }

            // 添加从API获取的选项
            apiResult.data.forEach(kb => {
                const option = document.createElement('option');
                option.value = kb.id || kb.code;
                // 使用本地化名称
                const localizedName = this.formatKnowledgeBaseName(kb.name);
                option.textContent = localizedName || kb.name;
                select.appendChild(option);
            });

            // 恢复之前保存的值
            await this.loadStoredAwrDatabaseType();

            // 检查当前选中的值是否有效（在选项中存在）
            const currentValue = select.value;
            const isValidValue = currentValue && Array.from(select.options).some(opt => opt.value === currentValue && opt.value !== '');

            // 如果当前选中的是空值（占位符）或保存的值不在选项中，则选中第一项（排除占位符）
            if ((!currentValue || !isValidValue) && apiResult.data.length > 0) {
                const firstDataItem = apiResult.data[0];
                const firstValue = firstDataItem.id || firstDataItem.code;
                if (firstValue) {
                    select.value = firstValue;
                    this.storedAwrDatabaseType = firstValue;
                    // 保存到存储
                    if (typeof chrome !== 'undefined' && chrome.storage?.sync) {
                        chrome.storage.sync.set({ awrDatabaseType: firstValue }, () => {
                            if (chrome.runtime?.lastError) {
                                console.error('保存AWR数据库类型失败:', chrome.runtime.lastError);
                            }
                        });
                    }
                }
            }

            // 绑定数据库类型选择变化事件
            this.bindAwrDatabaseTypeChange();

            // 初始化显示当前选中数据库类型的描述
            this.updateAwrDatabaseDescription();

            // 初始化显示脱敏脚本下载地址
            this.updateAwrDesensitizationScriptDownloadLinks();

            console.log(`成功加载 ${apiResult.data.length} 个AWR数据库类型选项`);
        } else {
            console.warn('从API加载AWR数据库类型失败，使用默认值');
            // API失败时，保持现有的硬编码选项
            await this.loadStoredAwrDatabaseType();
        }
    } catch (error) {
        console.error('加载AWR数据库类型失败:', error);
        // 出错时，保持现有的硬编码选项
        await this.loadStoredAwrDatabaseType();
    }
}

async function loadStoredAwrDatabaseType() {
    const defaultValue = this.defaultAwrDatabaseType;
    let storedValue = defaultValue;

    if (typeof chrome === 'undefined' || !chrome.storage?.sync?.get) {
        this.storedAwrDatabaseType = storedValue;
        if (this.awrDatabaseType) {
            this.awrDatabaseType.value = storedValue;
        }
        return storedValue;
    }

    try {
        storedValue = await new Promise((resolve) => {
            try {
                chrome.storage.sync.get({ awrDatabaseType: defaultValue }, (items) => {
                    if (chrome.runtime?.lastError) {
                        console.error('读取AWR数据库类型失败:', chrome.runtime.lastError);
                        resolve(defaultValue);
                    } else {
                        resolve(items.awrDatabaseType || defaultValue);
                    }
                });
            } catch (error) {
                console.error('读取AWR数据库类型异常:', error);
                resolve(defaultValue);
            }
        });
    } catch (error) {
        console.error('读取AWR数据库类型异常:', error);
        storedValue = defaultValue;
    }

    this.storedAwrDatabaseType = storedValue;

    if (this.awrDatabaseType) {
        this.awrDatabaseType.value = storedValue;
    }

    return storedValue;
}

function handleAwrDatabaseTypeChange(event) {
    const rawValue = event?.target?.value || '';
    const valueToStore = rawValue || this.defaultAwrDatabaseType;
    this.storedAwrDatabaseType = valueToStore;

    if (!rawValue && this.awrDatabaseType) {
        this.awrDatabaseType.value = valueToStore;
    }

    if (typeof chrome === 'undefined' || !chrome.storage?.sync) {
        return;
    }

    try {
        if (rawValue) {
            chrome.storage.sync.set({ awrDatabaseType: valueToStore }, () => {
                if (chrome.runtime?.lastError) {
                    console.error('保存AWR数据库类型失败:', chrome.runtime.lastError);
                }
            });
        } else if (chrome.storage.sync.remove) {
            chrome.storage.sync.remove('awrDatabaseType', () => {
                if (chrome.runtime?.lastError) {
                    console.error('移除AWR数据库类型失败:', chrome.runtime.lastError);
                }
            });
        }
    } catch (error) {
        console.error('保存AWR数据库类型异常:', error);
    }
}

function resetAwrForm() {
    if (this.awrProblemDescription) {
        this.awrProblemDescription.value = '';
    }
    if (this.awrFileDisplay) {
        this.awrFileDisplay.value = '';
        this.awrFileDisplay.placeholder = this.t('popup.awr.form.uploadPlaceholder');
    }
    if (this.awrFileInput) {
        this.awrFileInput.value = '';
    }
    if (this.awrLanguage) {
        this.awrLanguage.value = 'zh';
    }
    if (this.awrDatabaseType) {
        const defaultValue = this.storedAwrDatabaseType || this.defaultAwrDatabaseType;
        this.awrDatabaseType.value = defaultValue;
    }
    if (this.awrAgreeTerms) {
        this.awrAgreeTerms.checked = false;
    }
    // 清理邮箱验证状态
    if (this.awrEmail) {
        this.awrEmail.value = '';
        this.clearAwrEmailValidation();
    }
    this.selectedFile = null;
}

// 设置邮箱实时验证
function setupAwrEmailValidation() {
    if (!this.awrEmail) {
        return;
    }

    // 移除旧的事件监听器（如果存在）
    if (this._awrEmailInputHandler) {
        this.awrEmail.removeEventListener('input', this._awrEmailInputHandler);
        this.awrEmail.removeEventListener('blur', this._awrEmailBlurHandler);
    }

    // 创建新的事件处理器
    this._awrEmailInputHandler = (e) => {
        const email = e.target.value.trim();
        if (email) {
            // 输入时实时验证，但不显示错误提示（只改变边框颜色）
            this.validateAwrEmail(email, false);
        } else {
            this.clearAwrEmailValidation();
        }
    };

    this._awrEmailBlurHandler = (e) => {
        const email = e.target.value.trim();
        if (email) {
            // 失焦时显示错误提示
            this.validateAwrEmail(email, true);
        } else {
            this.clearAwrEmailValidation();
        }
    };

    // 添加事件监听器
    this.awrEmail.addEventListener('input', this._awrEmailInputHandler);
    this.awrEmail.addEventListener('blur', this._awrEmailBlurHandler);
}

// 验证邮箱格式
function validateAwrEmail(email, showError = true) {
    if (!this.awrEmail) {
        return false;
    }

    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const isValid = emailPattern.test(email);

    // 获取或创建错误提示元素
    let errorElement = this.awrEmail.parentElement.querySelector('.email-error-message');
    if (!errorElement) {
        errorElement = document.createElement('div');
        errorElement.className = 'email-error-message';
        this.awrEmail.parentElement.appendChild(errorElement);
    }

    if (isValid) {
        // 邮箱格式正确
        this.awrEmail.classList.remove('input-invalid');
        this.awrEmail.classList.add('input-valid');
        errorElement.textContent = '';
        errorElement.style.display = 'none';
        return true;
    } else {
        // 邮箱格式错误
        this.awrEmail.classList.remove('input-valid');
        this.awrEmail.classList.add('input-invalid');
        if (showError) {
            errorElement.textContent = this.t('popup.message.invalidEmail');
            errorElement.style.display = 'block';
        }
        return false;
    }
}

// 清理邮箱验证状态
function clearAwrEmailValidation() {
    if (!this.awrEmail) {
        return;
    }

    this.awrEmail.classList.remove('input-invalid', 'input-valid');

    const errorElement = this.awrEmail.parentElement.querySelector('.email-error-message');
    if (errorElement) {
        errorElement.textContent = '';
        errorElement.style.display = 'none';
    }
}

function handleFileSelect(e) {
    const file = e.target.files[0];
    if (file) {
        const fileName = file.name;

        // 校验文件名，不允许包含 awr_diff_report_ 或 awrrpt_rac_
        if (fileName.includes('awr_diff_report_')) {
            // AWR 对比报告不支持
            this.showAwrFileValidationDialog();

            // 清空文件选择
            this.selectedFile = null;
            if (this.awrFileInput) {
                this.awrFileInput.value = '';
            }
            if (this.awrFileDisplay) {
                this.awrFileDisplay.value = '';
                this.awrFileDisplay.placeholder = this.t('popup.awr.form.uploadPlaceholder');
            }
            return;
        }

        if (fileName.includes('awrrpt_rac_')) {
            // RAC 全局 AWR 报告不支持
            this.showAwrFileValidationDialog();

            // 清空文件选择
            this.selectedFile = null;
            if (this.awrFileInput) {
                this.awrFileInput.value = '';
            }
            if (this.awrFileDisplay) {
                this.awrFileDisplay.value = '';
                this.awrFileDisplay.placeholder = this.t('popup.awr.form.uploadPlaceholder');
            }
            return;
        }

        // 文件名校验通过，正常处理
        this.selectedFile = file;
        if (this.awrFileDisplay) {
            this.awrFileDisplay.value = file.name;
            this.awrFileDisplay.placeholder = file.name;
        }
        console.log('已选择文件:', file.name);
    } else {
        this.selectedFile = null;
        if (this.awrFileDisplay) {
            this.awrFileDisplay.value = '';
            this.awrFileDisplay.placeholder = this.t('popup.awr.form.uploadPlaceholder');
        }
    }
}

async function handleAwrAnalysisSubmit() {
    if (this.awrSaveBtn && this.awrSaveBtn.disabled) {
        return;
    }

    if (!this.awrEmail || !this.awrEmail.value.trim()) {
        this.showMessage(this.t('popup.message.enterEmail'), 'error', { centered: true, durationMs: 5000, maxWidth: '360px' });
        this.awrEmail?.focus();
        return;
    }

    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailPattern.test(this.awrEmail.value.trim())) {
        this.showMessage(this.t('popup.message.invalidEmail'), 'error', { centered: true, durationMs: 5000, maxWidth: '360px' });
        this.awrEmail?.focus();
        return;
    }

    if (!this.selectedFile) {
        this.showMessage(this.t('popup.message.selectFile'), 'error', { centered: true, durationMs: 5000, maxWidth: '360px' });
        this.awrFileUploadBtn?.focus();
        return;
    }

    const databaseCode = this.awrDatabaseType?.value || '';
    if (!databaseCode) {
        this.showMessage(this.t('popup.message.selectDatabaseType'), 'error', { centered: true, durationMs: 5000, maxWidth: '360px' });
        this.awrDatabaseType?.focus();
        return;
    }

    if (!this.awrAgreeTerms || !this.awrAgreeTerms.checked) {
        this.showMessage(this.t('popup.message.agreeTerms'), 'error', { centered: true, durationMs: 5000, maxWidth: '360px' });
        this.awrAgreeTerms?.focus();
        return;
    }

    const username = this.awrUserName?.value.trim() || '';
    const originalButtonText = this.awrSaveBtn?.textContent || '';
    if (this.awrSaveBtn) {
        this.awrSaveBtn.disabled = true;
        this.awrSaveBtn.textContent = this.getRunAnalysisCountdownText(5);
    }

    let countdown = 5;
    if (this.awrCountdownInterval) {
        clearInterval(this.awrCountdownInterval);
    }
    this.awrCountdownInterval = setInterval(() => {
        countdown--;
        if (this.awrSaveBtn) {
            if (countdown > 0) {
                this.awrSaveBtn.textContent = this.getRunAnalysisCountdownText(countdown);
            } else {
                this.awrSaveBtn.textContent = originalButtonText;
                this.awrSaveBtn.disabled = false;
                clearInterval(this.awrCountdownInterval);
                this.awrCountdownInterval = null;
            }
        } else {
            clearInterval(this.awrCountdownInterval);
            this.awrCountdownInterval = null;
        }
    }, 1000);

    const language = this.awrLanguage?.value || 'zh';
    const formData = {
        username,
        email: this.awrEmail.value.trim(),
        problemDescription: this.awrProblemDescription?.value.trim() || '',
        file: this.selectedFile,
        language,
        databaseCode
    };

    console.log('AWR分析表单数据:', {
        username: formData.username,
        email: formData.email,
        problemDescription: formData.problemDescription,
        fileName: formData.file ? formData.file.name : '无文件',
        language: formData.language,
        databaseCode: formData.databaseCode
    });

    this.showLoadingOverlay(this.t('popup.awr.history.overlayAnalyzing'));
    try {
        const response = await this.submitAwrAnalysis(formData);
        if (response && response.status === 'success') {
            this.hideLoadingOverlay();

            // 根据环境类型显示不同的成功消息
            const envType = await this.getEnvType();
            const successMessage = envType === 'in_env'
                ? this.t('popup.message.awrSubmitSuccessInEnv')
                : this.t('popup.message.awrSubmitSuccess');

            this.showMessage(successMessage, 'success', { centered: true, durationMs: 6000, maxWidth: '380px', background: '#1e7e34' });

            const historyView = document.getElementById('awrHistoryView');
            if (historyView && historyView.classList.contains('active')) {
                this.loadAwrHistoryList(this.awrHistoryCurrentPage);
            }

            this.hideAwrAnalysisDialog();
            if (this.awrCountdownInterval) {
                clearInterval(this.awrCountdownInterval);
                this.awrCountdownInterval = null;
            }
            if (this.awrSaveBtn) {
                this.awrSaveBtn.textContent = originalButtonText;
            }
        } else {
            const fallbackError = this.t('popup.common.unknownError');
            const errorMsg = response?.message || fallbackError;
            this.hideLoadingOverlay();
            this.showMessage(this.t('popup.message.awrSubmitFailed', { error: errorMsg }), 'error', { centered: true, durationMs: 5000, maxWidth: '360px' });
        }
    } catch (error) {
        console.error('提交AWR分析失败(Submission failed):', error);
        this.hideLoadingOverlay();
        const errorText = error.message || this.t('popup.common.unknownError');
        this.showMessage(this.t('popup.message.awrSubmitFailed', { error: errorText }), 'error', { centered: true, durationMs: 5000, maxWidth: '360px' });
    }
}

async function submitAwrAnalysis(formData) {
    const apiKey = this.resolveApiKey();
    if (!apiKey) {
        throw new Error(this.t('popup.message.apiKeyNotConfigured'));
    }

    // 获取当前选择的模型信息（仅在内网环境下）
    let modelParams = null;
    try {
        // 检查环境类型，只有内网环境才传递 modelParams
        const envType = await this.getEnvType();
        console.log('AWR分析 - 当前环境类型:', envType);

        if (envType === 'in_env') {
            const selectedModelValue = this.modelSelect?.value;
            if (selectedModelValue) {
                // 解析选中的模型（模型名 + 服务商）
                let selectedKey;
                try {
                    selectedKey = JSON.parse(selectedModelValue);
                } catch (_) {
                    selectedKey = { name: selectedModelValue };
                }

                // 获取选中的模型和服务商
                const selectedModel = this.models.find(m => m.name === selectedKey.name && (!selectedKey.provider || m.provider === selectedKey.provider));
                const provider = selectedModel ? this.providers.find(p => p.name === selectedModel.provider) : null;

                if (selectedModel && provider) {
                    modelParams = {
                        modelName: selectedModel.displayName || selectedModel.name,
                        apiEndpoint: provider.apiEndpoint || ''
                    };
                    console.log('AWR分析 - 模型参数:', modelParams);
                } else {
                    console.warn('AWR分析 - 未找到选中的模型或服务商:', { selectedModelValue, selectedKey, selectedModel: !!selectedModel, provider: !!provider });
                }
            } else {
                console.warn('AWR分析 - 未选择模型，modelSelect.value 为空');
            }
        } else {
            console.log('AWR分析 - 外网环境，不传递 modelParams');
        }
    } catch (error) {
        console.warn('获取模型参数失败，继续执行AWR分析:', error);
    }

    const formDataToSend = new FormData();
    formDataToSend.append('file', formData.file);

    const queryParams = new URLSearchParams();
    queryParams.append('username', formData.username);
    queryParams.append('email', formData.email);
    queryParams.append('language', formData.language || 'zh');
    if (formData.databaseCode) {
        queryParams.append('code', formData.databaseCode);
    }
    if (formData.problemDescription) {
        queryParams.append('backgroundHint', formData.problemDescription);
    }
    // 添加 modelParams 参数（JSON格式）- 仅在内网环境下
    if (modelParams) {
        queryParams.append('modelParams', JSON.stringify(modelParams));
        console.log('AWR分析 - 已添加 modelParams 到查询参数');
    } else {
        console.log('AWR分析 - modelParams 为空，未添加到查询参数');
    }

    const url = `/api/awr/upload?${queryParams.toString()}`;

    try {
        // 使用请求工具
        const tempProvider = {
            authType: 'Bearer',
            apiKey: apiKey
        };
        const result = await this.requestUtil.upload(url, formDataToSend, {
            provider: tempProvider
        });
        return result;
    } catch (error) {
        console.error('AWR分析接口调用失败(AWR analysis interface call failed):', error);
        throw error;
    }
}

function switchAwrTab(tabName) {
    document.querySelectorAll('.awr-tab-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.tab === tabName);
    });

    const newView = document.getElementById('awrNewAnalysisView');
    const historyView = document.getElementById('awrHistoryView');

    if (tabName === 'new') {
        if (newView) newView.classList.add('active');
        if (historyView) historyView.classList.remove('active');
        if (!this.awrUserName?.value.trim()) {
            this.populateUserProfileFromApi().catch(e => {
                console.error('切换到新建分析时获取用户信息失败:', e);
            });
        }
    } else {
        if (newView) newView.classList.remove('active');
        if (historyView) historyView.classList.add('active');

        // 延迟执行以确保DOM完全渲染
        setTimeout(() => {
            // 确保日期时间过滤器已初始化
            console.log('初始化AWR日期时间过滤器');
            const historyView = document.getElementById('awrHistoryView');
            if (historyView) {
                // 强制清理之前的设置，确保干净的状态
                this.cleanupDateTimeFilters();
                // 重新初始化
                this.setupDateTimeFilters(true, historyView);
                console.log('AWR日期时间过滤器初始化完成');

                // 检查输入框是否存在
                const startInput = document.getElementById('awrStartTime');
                const endInput = document.getElementById('awrEndTime');
                console.log('AWR输入框存在:', !!startInput, !!endInput);
                if (startInput) {
                    console.log('开始时间输入框:', startInput, 'data-role:', startInput.getAttribute('data-role'), 'setup:', startInput.dataset.datetimePickerSetup);
                }
            } else {
                console.error('找不到awrHistoryView元素');
            }
        }, 100);

        // 重置时间过滤器
        this.clearDateTimeInputValue('awrStartTime');
        this.clearDateTimeInputValue('awrEndTime');

        const startTime = '';
        const endTime = '';
        const status = document.getElementById('awrStatusFilter')?.value || '';
        this.loadAwrHistoryList(1, this.awrHistoryPageSize, '', startTime, endTime, status);
    }
}

function handleAwrSearch() {
    const startTime = this.getDateTimeInputValue('awrStartTime');
    const endTime = this.getDateTimeInputValue('awrEndTime');
    const status = document.getElementById('awrStatusFilter')?.value || '';
    this.loadAwrHistoryList(1, this.awrHistoryPageSize, '', startTime, endTime, status);
}

function handleAwrReset() {
    const statusSelect = document.getElementById('awrStatusFilter');
    this.clearDateTimeInputValue('awrStartTime');
    this.clearDateTimeInputValue('awrEndTime');
    if (statusSelect) statusSelect.value = '';
    this.loadAwrHistoryList(1, this.awrHistoryPageSize, '', '', '', '');
}

async function loadAwrHistoryList(page = 1, pageSize = 10, keyword = '', startTime = '', endTime = '', status = '') {
    try {
        // 确保知识库列表已经加载完成
        if (!this.knowledgeBases) {
            const apiResult = await this.loadKnowledgeBasesFromAPI('awr');
            if (apiResult.success && apiResult.data) {
                this.knowledgeBases = apiResult.data;
            }
        }

        const apiKey = this.resolveApiKey();
        if (!apiKey) {
            this.showMessage(this.t('popup.message.apiKeyNotConfigured'), 'error');
            return;
        }

        let username = this.awrUserName?.value.trim() || '';

        if (!username) {
            try {
                const result = await chrome.storage.sync.get(['registration']);
                const registration = result.registration;
                if (registration && registration.status === 'registered' && registration.username) {
                    username = registration.username;
                    if (this.awrUserName) {
                        this.awrUserName.value = username;
                    }
                }
            } catch (error) {
                console.error('获取注册信息失败:', error);
            }
        }

        if (!username) {
            try {
                await this.populateUserProfileFromApi();
                username = this.awrUserName?.value.trim() || '';
            } catch (error) {
                console.error('从API获取用户信息失败:', error);
            }
        }

        if (!username || username === '-') {
            this.showMessage(this.t('popup.message.fetchUserInfoFailed'), 'error');
            return;
        }

        const requestBody = {
            pageNum: page,
            pageSize,
            username,
            apiKey: apiKey
        };

        if (status !== '') {
            requestBody.status = parseInt(status, 10);
        }

        if (startTime) {
            const startDateTime = this.parseISODateTime(startTime);
            if (startDateTime) {
                const year = startDateTime.getFullYear();
                const month = String(startDateTime.getMonth() + 1).padStart(2, '0');
                const day = String(startDateTime.getDate()).padStart(2, '0');
                const hours = String(startDateTime.getHours()).padStart(2, '0');
                const minutes = String(startDateTime.getMinutes()).padStart(2, '0');
                const seconds = String(startDateTime.getSeconds()).padStart(2, '0');
                requestBody.startTime = `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
            }
        }

        if (endTime) {
            const endDateTime = this.parseISODateTime(endTime);
            if (endDateTime) {
                endDateTime.setHours(23, 59, 59, 999);
                const year = endDateTime.getFullYear();
                const month = String(endDateTime.getMonth() + 1).padStart(2, '0');
                const day = String(endDateTime.getDate()).padStart(2, '0');
                const hours = String(endDateTime.getHours()).padStart(2, '0');
                const minutes = String(endDateTime.getMinutes()).padStart(2, '0');
                const seconds = String(endDateTime.getSeconds()).padStart(2, '0');
                requestBody.endTime = `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
            }
        }

        const url = '/api/awr/list';

        this.showLoadingOverlay(this.t('popup.awr.history.loadingHistory'));

        // 使用请求工具
        const tempProvider = {
            authType: 'Bearer',
            apiKey: apiKey
        };
        const result = await this.requestUtil.post(url, requestBody, {
            provider: tempProvider
        });

        if (result.status === 'success' || result.status === '200' || result.data) {
            const data = result.data || {};
            const list = data.list || [];

            try {
                await this.i18n.ensureLanguage(this.currentLanguage);
            } catch (ensureError) {
                console.warn('加载历史记录时语言包未准备就绪:', ensureError);
            }

            this.awrHistoryList = list.map(item => ({
                id: item.id,
                email: item.email || '',
                language: item.language || 'zh',
                problemDescription: item.backgroundHint || '',
                fileName: item.awrFilename || '',
                status: this.convertStatusNumberToString(item.status),
                createTime: this.parseDateTime(item.createdAt),
                reportUrl: item.reportFileurl || null,
                username: item.username || '',
                fileUrl: item.awrFileurl || null,
                notifyStatus: item.notifyStatus || 'unknown',
                // 尝试从API返回数据中获取数据库类型，可能的字段名
                databaseType: item.databaseType || item.dbType || item.code || ''
            }));

            this.awrHistoryTotal = data.total || 0;
            this.awrHistoryCurrentPage = data.pageNum || page;
            this.awrHistoryPageSize = data.pageSize || pageSize;

            await this.renderAwrHistoryList();
            this.updateAwrPagination();
        } else {
            throw new Error(result.message || this.t('popup.common.unknownError'));
        }

        this.hideLoadingOverlay();
    } catch (error) {
        console.error('加载AWR历史记录失败:', error);
        this.hideLoadingOverlay();
        const errorText = error.message || this.t('popup.common.unknownError');
        this.showMessage(this.t('popup.message.loadHistoryFailed', { error: errorText }), 'error');
        await this.renderAwrHistoryList();
        if (this.awrUserName) {
            this.awrUserName.value = '';
        }
        if (this.awrEmail) {
            this.awrEmail.value = '';
        }
    }
}

function convertStatusNumberToString(statusNum) {
    const statusMap = {
        0: 'pending',
        1: 'success',
        2: 'failed',
        3: 'running'
    };
    return statusMap[statusNum] || 'unknown';
}

function convertStatusToString(statusStr) {
    const statusText = this.getAwrStatusText(statusStr);
    return statusText || statusStr;
}

function parseDateTime(dateTimeObj) {
    if (!dateTimeObj) return null;
    if (typeof dateTimeObj === 'string') {
        return dateTimeObj;
    }
    if (dateTimeObj.dateTime) {
        return dateTimeObj.dateTime;
    }
    return null;
}

async function renderAwrHistoryList() {
    const tbody = document.getElementById('awrHistoryList');
    const table = document.getElementById('awrHistoryTable');
    if (!tbody || !table) return;

    if (this.awrHistoryList.length === 0) {
        tbody.innerHTML = '';
        const tableContainer = table.closest('.awr-history-table-container');
        if (tableContainer) {
            table.style.display = 'none';
            let emptyDiv = tableContainer.querySelector('.empty-history');
            if (!emptyDiv) {
                emptyDiv = document.createElement('div');
                emptyDiv.className = 'empty-history';
                tableContainer.appendChild(emptyDiv);
            }
            const emptyTitle = this.t('popup.awr.history.emptyTitle');
            const emptySubtitle = this.t('popup.awr.history.emptySubtitle');
                emptyDiv.innerHTML = `
                <div class="empty-history-icon">📝</div>
                <div class="empty-history-text">${escapeHtml(emptyTitle)}</div>
                <div class="empty-history-subtext">${escapeHtml(emptySubtitle)}</div>
            `;
            emptyDiv.style.display = 'block';
        }
        return;
    }

    table.style.display = 'table';
    const tableContainer = table.closest('.awr-history-table-container');
    if (tableContainer) {
        const emptyDiv = tableContainer.querySelector('.empty-history');
        if (emptyDiv) {
            emptyDiv.style.display = 'none';
        }
    }

    tbody.innerHTML = '';
    // 使用 Promise.all 处理异步创建行
    const rows = await Promise.all(this.awrHistoryList.map(item => this.createAwrHistoryTableRow(item)));
    rows.forEach(row => tbody.appendChild(row));

    // 根据环境类型控制表头邮箱列的显示
    const envType = await this.getEnvType();
    const isInEnv = envType === 'in_env';
    const emailHeader = table.querySelector('thead th[data-i18n="popup.awr.table.email"]');
    if (emailHeader) {
        emailHeader.style.display = isInEnv ? 'none' : '';
    }
}

async function createAwrHistoryTableRow(item) {
    const tr = document.createElement('tr');
    tr.className = 'awr-history-row';
    const locale = this.i18n?.getIntlLocale(this.currentLanguage);

    let createTime = this.t('popup.awr.history.unknown');
    if (item.createTime) {
        try {
            const date = new Date(item.createTime);
            if (!isNaN(date.getTime())) {
                createTime = date.toLocaleString(locale);
            }
        } catch (e) {
            console.error('日期解析失败:', e);
        }
    }

    const statusText = this.getAwrStatusText(item.status);
    const statusClass = this.getAwrStatusClass(item.status);

    const notifyStatusText = this.getAwrNotifyStatusText(item.notifyStatus);
    const notifyStatusClass = this.getAwrNotifyStatusClass(item.notifyStatus);

    // 检查环境类型，内网环境下隐藏重发邮件按钮
    const envType = await this.getEnvType();
    const isInEnv = envType === 'in_env';

    const isResendDisabled = item.status !== 'success';
    const resendDisabledAttr = isResendDisabled ? 'disabled' : '';
    const resendDisabledClass = isResendDisabled ? 'disabled' : '';
    const resendTitle = isResendDisabled
        ? this.t('popup.awr.history.resendDisabledTooltip')
        : this.t('popup.awr.history.resendTooltip');

    const problemDesc = item.problemDescription || '';
    const problemPreview = problemDesc.length > 30 ? `${problemDesc.substring(0, 30)}...` : problemDesc;

    const fileName = item.fileName || '';
    const fileNamePreview = fileName.length > 20 ? `${fileName.substring(0, 20)}...` : fileName;

    const noFileText = this.t('popup.awr.history.notSpecified');
    const unknownText = this.t('popup.awr.history.unknown');
    const languageKeyMap = {
        'zh': 'popup.awr.history.language.zh',
        'en': 'popup.awr.history.language.en',
        'en-us': 'popup.awr.history.language.en',
        'en_US': 'popup.awr.history.language.en',
        'zh-tw': 'popup.awr.history.language.zh-tw',
        'zh_tw': 'popup.awr.history.language.zh-tw',
        'zh-TW': 'popup.awr.history.language.zh-tw'
    };

    const languageKey = languageKeyMap[item.language?.toLowerCase?.()] || 'popup.awr.history.language.zh';
    const languageText = this.t(languageKey);

    const resendButtonLabel = this.t('popup.awr.history.resendButton');
    const downloadButtonLabel = this.t('popup.awr.history.downloadButton') || '下载';
    const downloadTitle = this.t('popup.awr.history.downloadTooltip') || '下载报告';

    // 只有状态为成功时才显示下载按钮
    const canDownload = item.status === 'success';
    const downloadButtonHtml = canDownload
        ? `<button class="awr-action-btn download-btn" data-id="${item.id}" title="${escapeHtml(downloadTitle)}">
            ${escapeHtml(downloadButtonLabel)}
        </button>`
        : '';

    // 内网环境下隐藏重发邮件按钮
    const resendButtonHtml = isInEnv ? '' : `<button class="awr-action-btn resend-email-btn ${resendDisabledClass}" data-id="${item.id}" title="${escapeHtml(resendTitle)}" ${resendDisabledAttr}>
        ${escapeHtml(resendButtonLabel)}
    </button>`;

    // 内网环境下隐藏邮箱列
    const emailCellHtml = isInEnv ? '' : `<td class="awr-table-cell-email copyable-cell" data-full-text="${escapeHtml(item.email || unknownText)}" title="${escapeHtml(item.email || unknownText)}">${escapeHtml(item.email || unknownText)}</td>`;

    // 添加类型列，值为"AWR分析"
    // 根据数据库类型code获取对应的名称
    let typeText = item.databaseType;
    if (typeText && Array.isArray(this.knowledgeBases)) {
        const kb = this.knowledgeBases.find(kb => kb.code === typeText || kb.id === typeText);
        if (kb && kb.name) {
            // 使用本地化名称格式化，与选项加载保持一致
            typeText = this.formatKnowledgeBaseName(kb.name) || kb.name;
        }
    }
    // 如果没有获取到名称，则显示默认值
    if (!typeText) {
        typeText = this.t('popup.awr.history.type.awr');
    }

    tr.innerHTML = `
        <td class="awr-table-cell-filename copyable-cell" data-full-text="${escapeHtml(fileName || noFileText)}" title="${escapeHtml(fileName || noFileText)}">${escapeHtml(fileNamePreview || noFileText)}</td>
        <td class="awr-table-cell-type">${escapeHtml(typeText)}</td>
        <td class="awr-table-cell-time">${escapeHtml(createTime)}</td>
        <td class="awr-table-cell-problem copyable-cell" data-full-text="${escapeHtml(problemDesc || '-')}" title="${escapeHtml(problemDesc || '-')}">${escapeHtml(problemPreview || '-')}</td>
        ${emailCellHtml}
        <td class="awr-table-cell-status">
            <span class="awr-status-badge ${statusClass}">${escapeHtml(statusText)}</span>
        </td>
        <td class="awr-table-cell-notify-status">
            <span class="awr-status-badge ${notifyStatusClass}">${escapeHtml(notifyStatusText)}</span>
        </td>
        <td class="awr-table-cell-actions">
            ${resendButtonHtml}
            ${downloadButtonHtml}
        </td>
    `;

    const resendBtn = tr.querySelector('.resend-email-btn');
    if (resendBtn && !isResendDisabled && !isInEnv) {
        resendBtn.addEventListener('click', (event) => {
            event.preventDefault();
            this.handleReanalyze(item);
        });
    }

    const downloadBtn = tr.querySelector('.download-btn');
    if (downloadBtn && canDownload) {
        downloadBtn.addEventListener('click', (event) => {
            event.preventDefault();
            this.handleAwrDownload(item);
        });
    }

    // 添加点击复制功能
    const copyableCells = tr.querySelectorAll('.copyable-cell');
    copyableCells.forEach(cell => {
        cell.style.cursor = 'pointer';
        cell.addEventListener('click', async (event) => {
            event.stopPropagation();
            const fullText = cell.getAttribute('data-full-text') || cell.textContent.trim();
            if (fullText && fullText !== '-') {
                try {
                    await navigator.clipboard.writeText(fullText);
                    // 显示复制成功提示
                    this.showMessage(this.t('popup.common.copySuccess'), 'success', {
                        centered: true,
                        durationMs: 2000,
                        maxWidth: '200px'
                    });
                } catch (err) {
                    console.error('复制失败:', err);
                    this.showMessage('复制失败，请重试', 'error', {
                        centered: true,
                        durationMs: 2000,
                        maxWidth: '200px'
                    });
                }
            }
        });
    });

    return tr;
}

function getAwrStatusText(status) {
    const key = {
        'pending': 'popup.awr.history.status.pending',
        'success': 'popup.awr.history.status.success',
        'failed': 'popup.awr.history.status.failed',
        'running': 'popup.awr.history.status.running',
        'unknown': 'popup.awr.history.status.unknown'
    }[status] || 'popup.awr.history.status.unknown';
    return this.t(key);
}

function getAwrStatusClass(status) {
    const classMap = {
        'pending': 'status-pending',
        'success': 'status-success',
        'failed': 'status-failed',
        'running': 'status-running',
        'unknown': 'status-unknown'
    };
    return classMap[status] || '';
}

function getAwrNotifyStatusText(notifyStatus) {
    // 处理 success、fail/failed 和 pending，其他都返回 unknown
    if (notifyStatus === 'success') {
        return this.t('popup.awr.history.notifyStatus.success');
    }
    if (notifyStatus === 'fail' || notifyStatus === 'failed') {
        return this.t('popup.awr.history.notifyStatus.failed');
    }
    if (notifyStatus === 'pending') {
        return this.t('popup.awr.history.notifyStatus.pending');
    }
    return this.t('popup.awr.history.notifyStatus.unknown');
}

function getAwrNotifyStatusClass(notifyStatus) {
    // 处理 success、fail/failed 和 pending，其他都返回 unknown
    if (notifyStatus === 'success') {
        return 'notify-status-success';
    }
    if (notifyStatus === 'fail' || notifyStatus === 'failed') {
        return 'notify-status-failed';
    }
    if (notifyStatus === 'pending') {
        return 'notify-status-pending';
    }
    return 'notify-status-unknown';
}

function updateAwrPagination() {
    const totalPages = Math.ceil(this.awrHistoryTotal / this.awrHistoryPageSize);
    const pageInfo = document.getElementById('awrPageInfo');
    const prevBtn = document.getElementById('awrPrevPageBtn');
    const nextBtn = document.getElementById('awrNextPageBtn');

    if (pageInfo) {
        const safeTotalPages = totalPages > 0 ? totalPages : 1;
        pageInfo.textContent = this.t('popup.awr.pagination.info', {
            current: this.awrHistoryCurrentPage,
            total: safeTotalPages,
            records: this.awrHistoryTotal
        });
    }

    if (prevBtn) {
        prevBtn.disabled = this.awrHistoryCurrentPage <= 1;
    }

    if (nextBtn) {
        nextBtn.disabled = this.awrHistoryCurrentPage >= totalPages || totalPages === 0;
    }
}

async function handleReanalyze(item) {
    if (item.status !== 'success') {
        this.showMessage(this.t('popup.message.resendEmailOnlySuccess'), 'error', { centered: true });
        return;
    }

    try {
        const apiKey = this.resolveApiKey();
        if (!apiKey) {
            this.showMessage(this.t('popup.message.apiKeyNotConfiguredShort'), 'error', { centered: true });
            return;
        }

        const url = `/api/awr/resendEmail?id=${encodeURIComponent(item.id)}`;
        this.showLoadingOverlay(this.t('popup.awr.history.resendingEmail'));

        // 使用请求工具
        const tempProvider = {
            authType: 'Bearer',
            apiKey: apiKey
        };
        const result = await this.requestUtil.post(url, null, {
            provider: tempProvider,
            redirect: 'follow'
        });

        const successStatuses = ['success', 'ok', '200'];
        const statusStr = String(result.status || '').toLowerCase().trim();
        const isSuccess = statusStr && successStatuses.includes(statusStr);
        const isEmptyStatus = !result.status || result.status === '';

        if (isSuccess || isEmptyStatus) {
            this.hideLoadingOverlay();
            this.showMessage(this.t('popup.message.resendEmailSuccess'), 'success', { centered: true });
            const startTime = this.getDateTimeInputValue('awrStartTime');
            const endTime = this.getDateTimeInputValue('awrEndTime');
            const status = document.getElementById('awrStatusFilter')?.value || '';
            // 保留现有注释，必要时可恢复刷新列表功能
            // this.loadAwrHistoryList(this.awrHistoryCurrentPage, this.awrHistoryPageSize, '', startTime, endTime, status);
        } else {
            const fallbackError = this.t('popup.common.unknownError');
            const errorDetail = result.message || (result.status ? String(result.status) : fallbackError);
            throw new Error(errorDetail);
        }
    } catch (error) {
        console.error('重新分析失败:', error);
        this.hideLoadingOverlay();
        const errorText = error.message || this.t('popup.common.unknownError');
        this.showMessage(this.t('popup.message.reanalyzeFailed', { error: errorText }), 'error', { centered: true });
    }
}

async function handleAwrDownload(item) {
    if (!item.id) {
        this.showMessage(this.t('popup.message.downloadFailed') || '下载失败：缺少记录ID', 'error', { centered: true });
        return;
    }

    try {
        const apiKey = this.resolveApiKey();
        if (!apiKey) {
            this.showMessage(this.t('popup.message.apiKeyNotConfiguredShort'), 'error', { centered: true });
            return;
        }

        // 使用基础URL构建完整URL（下载功能使用原生fetch，需要手动处理）
        const baseURL = this.requestUtil?.baseURL || 'http://api.bic-qa.com';
        const url = new URL('/api/awr/download', baseURL);
        this.showLoadingOverlay(this.t('popup.awr.history.downloading') || '正在下载...');

        // POST 请求，参数 id 作为 URL 参数
        url.searchParams.append('id', item.id);

        // 直接使用 fetch 处理 blob 响应
        const response = await fetch(url.toString(), {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${apiKey}`,
                'Accept-Language': this.getAcceptLanguage ? this.getAcceptLanguage() : 'zh'
            }
        });

        this.hideLoadingOverlay();

        if (!response.ok) {
            throw new Error(`下载失败: HTTP ${response.status} ${response.statusText}`);
        }

        // 获取 blob 数据
        const blob = await response.blob();

        // 使用邮件附件名称（如果存在），否则使用默认命名
        // 确保文件扩展名始终为 .html
        let fileName;
        if (item.fileName) {
            // 如果存在文件名，去掉原有扩展名，添加 .html 后缀
            const nameWithoutExt = item.fileName.replace(/\.[^/.]+$/, '');
            fileName = `${nameWithoutExt}.html`;
        } else {
            fileName = `awr_report_${item.id}.html`;
        }

        // 创建下载链接
        const downloadUrl = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = downloadUrl;
        link.download = fileName;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        window.URL.revokeObjectURL(downloadUrl);
        this.showMessage(this.t('popup.message.downloadSuccess') || '下载成功', 'success', { centered: true });
    } catch (error) {
        console.error('AWR下载失败:', error);
        this.hideLoadingOverlay();
        this.showMessage(this.t('popup.message.downloadFailed') || '下载失败: ' + (error.message || this.t('popup.common.unknownError')), 'error', { centered: true });
    }
}

/**
 * 显示AWR文件校验对话框
 */
/**
 * 绑定AWR数据库类型选择变化事件
 */
function bindAwrDatabaseTypeChange() {
    if (!this.awrDatabaseType) return;

    // 移除之前的事件监听器（如果存在）
    if (this._awrDatabaseTypeChangeHandler) {
        this.awrDatabaseType.removeEventListener('change', this._awrDatabaseTypeChangeHandler);
    }

    // 创建新的事件处理器
    this._awrDatabaseTypeChangeHandler = (event) => {
        this.updateAwrDatabaseDescription();
        this.updateAwrDesensitizationScriptDownloadLinks();
        // 调用原有的处理逻辑
        this.handleAwrDatabaseTypeChange(event);
    };

    // 添加事件监听器
    this.awrDatabaseType.addEventListener('change', this._awrDatabaseTypeChangeHandler);
}

/**
 * 更新AWR数据库类型描述显示
 */
function updateAwrDatabaseDescription() {
    const descriptionElement = document.getElementById('awrDatabaseDescription');
    if (!descriptionElement) return;

    const select = this.awrDatabaseType;
    if (!select || !this.awrKnowledgeBases) {
        descriptionElement.style.display = 'none';
        return;
    }

    const selectedValue = select.value;
    if (!selectedValue) {
        descriptionElement.style.display = 'none';
        return;
    }

    // 查找对应的知识库项
    const selectedKb = this.awrKnowledgeBases.find(kb => (kb.id || kb.code) === selectedValue);

    if (selectedKb && selectedKb.tips) {
        try {
            // 从tips JSON字符串中解析描述信息
            const tipsData = JSON.parse(selectedKb.tips);
            const awrTips = tipsData.awr;

            if (awrTips && awrTips.tips && awrTips.tips.trim()) {
                // 显示描述信息
                descriptionElement.textContent = awrTips.tips;
                descriptionElement.style.display = 'block';
            } else {
                // 隐藏描述信息
                descriptionElement.style.display = 'none';
            }
        } catch (error) {
            console.warn('解析tips失败:', error);
            descriptionElement.style.display = 'none';
        }
    } else {
        // 隐藏描述信息
        descriptionElement.style.display = 'none';
    }
}

/**
 * 更新AWR脱敏脚本下载地址显示
 */
function updateAwrDesensitizationScriptDownloadLinks() {
    const downloadLinksContainer = document.getElementById('awrDesensitizationScriptDownloadLinks');
    const downloadLabel = document.getElementById('awrDesensitizationScriptDownloadLabel');
    const descriptionText = document.getElementById('awrDesensitizationScriptDescriptionText');
    const giteeLink = document.getElementById('awrDesensitizationScriptGiteeLink');
    const githubLink = document.getElementById('awrDesensitizationScriptGithubLink');

    if (!downloadLinksContainer || !downloadLabel || !descriptionText || !giteeLink || !githubLink) return;

    const select = this.awrDatabaseType;
    if (!select || !this.awrKnowledgeBases) {
        downloadLinksContainer.style.display = 'none';
        return;
    }

    const selectedValue = select.value;
    if (!selectedValue) {
        downloadLinksContainer.style.display = 'none';
        return;
    }

    // 查找对应的知识库项
    const selectedKb = this.awrKnowledgeBases.find(kb => (kb.id || kb.code) === selectedValue);
    if (!selectedKb) {
        downloadLinksContainer.style.display = 'none';
        return;
    }

    const dbCode = selectedKb.id || selectedKb.code || '';

    // 根据数据库code判断显示什么文案
    let scriptType = '';
    let reportType = '';
    if (dbCode === '2101') {
        scriptType = 'AWR脱敏脚本';
        reportType = 'AWR报告';
    } else if (dbCode === '2114') {
        scriptType = 'kwr脱敏脚本';
        reportType = 'KWR报告';
    } else {
        // 其他数据库类型不显示
        downloadLinksContainer.style.display = 'none';
        return;
    }

    // 更新标签文本
    downloadLabel.textContent = `${scriptType}下载地址`;

    // 更新说明文案，根据数据库类型动态替换报告类型
    descriptionText.textContent = `使用脱敏工具处理${reportType}中的SQL文本，可有效保护敏感信息。处理后进行AI分析将更具安全性。如需安全保障，建议下载并使用该脱敏工具。`;

    // 设置下载地址
    const giteeUrl = 'https://gitee.com/DBAIOps/bic-qa/releases';
    const githubUrl = 'https://github.com/DBAIOps/DBAIOps/releases';

    // Gitee地址
    giteeLink.href = giteeUrl;
    const giteeUrlSpan = giteeLink.querySelector('.script-collector-download-url');
    if (giteeUrlSpan) {
        giteeUrlSpan.textContent = giteeUrl;
    }

    // GitHub地址
    githubLink.href = githubUrl;
    const githubUrlSpan = githubLink.querySelector('.script-collector-download-url');
    if (githubUrlSpan) {
        githubUrlSpan.textContent = githubUrl;
    }

    // 显示下载地址区域
    downloadLinksContainer.style.display = 'block';
}

function showAwrFileValidationDialog() {
    // 移除已存在的对话框
    const existingDialog = document.getElementById('awrFileValidationDialog');
    if (existingDialog) {
        existingDialog.remove();
    }

    // 获取所有错误信息和支持类型说明
    const unsupportedDiffReport = this.t('popup.awr.form.unsupportedDiffReport');
    const unsupportedRacReport = this.t('popup.awr.form.unsupportedRacReport');
    const supportedReportType = this.t('popup.awr.form.supportedReportType');

    // 创建遮罩层
    const overlay = document.createElement('div');
    overlay.id = 'awrFileValidationDialog';
    overlay.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.5);
        z-index: 20000;
        display: flex;
        align-items: center;
        justify-content: center;
    `;

    // 创建对话框
    const dialog = document.createElement('div');
    dialog.style.cssText = `
        background: white;
        border-radius: 8px;
        padding: 24px;
        max-width: 600px;
        max-height: 80vh;
        overflow-y: auto;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        position: relative;
    `;

    // 对话框内容
    dialog.innerHTML = `
        <div style="margin-bottom: 20px;">
            <div style="font-size: 16px; font-weight: 600; color: #dc2626; margin-bottom: 16px; line-height: 1.8;">
                ${unsupportedDiffReport}
                <br><br>
                ${unsupportedRacReport}
            </div>
            <div style="border-top: 1px solid #e5e7eb; padding-top: 16px; margin-top: 16px;">
                <div style="font-size: 16px; font-weight: 600; color: #059669; margin-bottom: 12px; line-height: 1.8;">
                    ${supportedReportType}
                </div>
            </div>
        </div>
        <div style="text-align: right; margin-top: 24px;">
            <button id="awrValidationDialogConfirm" style="
                background: #667eea;
                color: white;
                border: none;
                padding: 10px 24px;
                border-radius: 6px;
                font-size: 14px;
                cursor: pointer;
                font-weight: 500;
            ">${this.t('popup.common.confirm') || '确定'}</button>
        </div>
    `;

    overlay.appendChild(dialog);
    document.body.appendChild(overlay);

    // 绑定确认按钮事件
    const confirmBtn = dialog.querySelector('#awrValidationDialogConfirm');
    const closeDialog = () => {
        overlay.remove();
    };

    if (confirmBtn) {
        confirmBtn.addEventListener('click', closeDialog);
    }

    // 点击遮罩层关闭对话框
    overlay.addEventListener('click', (e) => {
        if (e.target === overlay) {
            closeDialog();
        }
    });

    // ESC键关闭对话框
    const handleEsc = (e) => {
        if (e.key === 'Escape') {
            closeDialog();
            document.removeEventListener('keydown', handleEsc);
        }
    };
    document.addEventListener('keydown', handleEsc);
}
