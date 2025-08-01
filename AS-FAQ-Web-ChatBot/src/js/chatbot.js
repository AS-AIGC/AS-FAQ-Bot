// 動態注入 chat-bubble 內 markdown 清單樣式
(function() {
  const style = document.createElement('style');
  style.textContent = `
    .chat-bubble ol {
      list-style-type: decimal;
      margin-left: 1.5em;
      padding-left: 1em;
    }
    .chat-bubble ul {
      list-style-type: disc;
      margin-left: 1.5em;
      padding-left: 1em;
    }
    .chat-bubble li {
      margin-bottom: 0.25em;
    }
    .chat-bubble code {
      background: #f5f5f5;
      color: #d6336c;
      padding: 0.2em 0.4em;
      border-radius: 4px;
      font-family: 'Fira Mono', 'Consolas', 'Menlo', monospace;
      font-size: 0.95em;
      word-break: break-all;
    }
    .chat-bubble pre {
      background: #23272e;
      color: #f8f8f2;
      padding: 1em;
      border-radius: 6px;
      font-family: 'Fira Mono', 'Consolas', 'Menlo', monospace;
      font-size: 1em;
      overflow-x: auto;
      margin: 0.5em 0;
      white-space: pre; /* 保持原格式 */
      max-width: 100%;
      box-sizing: border-box;
      /* 讓 code block 可左右捲動 */
      display: block;
    }
    .chat-bubble pre code {
      background: none;
      color: inherit;
      padding: 0;
      border-radius: 0;
      font-size: inherit;
    }
    .chat-bubble a {
      color: #2563eb;
      text-decoration: underline;
      word-break: break-all;
    }
  `;
  document.head.appendChild(style);
})();

const chatInput = $('#chat-input');
const chatSubmit = $('#chat-submit');
const chatMessages = $('#chat-messages');
const chatBubble = $('#chat-bubble');
const chatPopup = $('#chat-popup');
const closePopup = $('#close-popup');
let chatHistory = []; // 本地對話歷史紀錄

// 載入語言資源並切換語言
const langToggle = $('#lang-toggle');
const langText = $('#lang-text');
let currentLanguage = 'zh-TW';
let languages = {};

// 載入語言 JSON
$.getJSON('./js/lang.json', function (langData) {
    languages = langData;
    
    function updateLanguage(lang) {
        currentLanguage = lang;
        $('#chat-header h3').text(languages[lang].welcome);
        $('#chat-input').attr('placeholder', languages[lang].ask);
        $('#chat-submit').text(languages[lang].submit);
        $('#disclaimer').text(languages[lang].disclaimer);
        $('#terms').text(languages[lang].terms);
        $('#tos-link').text(languages[lang].tosLink);
        $('#privacy-policy-link').text(languages[lang].privacyLink);
        $('#start-chat').text(languages[lang].startChat);
        
        // 更新語言顯示文字
        langText.text(lang === 'zh-TW' ? 'En' : '中');
        
        // 更新預設問題的文字
        $('.question').each(function() {
            if (lang === 'en') {
                $(this).text($(this).data('question-en'));
            } else {
                $(this).text($(this).data('question'));
            }
        });
        
        // 儲存語言偏好設定
        localStorage.setItem('preferred-language', lang);
    }

    // 初始化語言
    const savedLanguage = localStorage.getItem('preferred-language') || 'zh-TW';
    updateLanguage(savedLanguage);

    // 切換語言按鈕事件處理
    langToggle.on('click', function () {
        const newLanguage = currentLanguage === 'zh-TW' ? 'en' : 'zh-TW';
        updateLanguage(newLanguage);
    });
});

// 設定聊天視窗尺寸
const sizeToggle = $('#size-toggle');
const sizeIcon = $('#size-icon');

// 用localStorage設定尺寸
let size = localStorage.getItem('chat-size') || 'sm';
updateSize(size);

sizeToggle.on('click', function () {
    size = size === 'sm' ? 'md' : 'sm';
    updateSize(size);
    localStorage.setItem('chat-size', size);
});

function updateSize(size) {
    chatPopup.removeClass('w-chat-sm w-chat-md');
    chatPopup.addClass('w-chat-' + size);
    sizeIcon.attr('src', size === 'sm' ? './img/expand.svg' : './img/collapse.svg');
}

// 點擊預設問題
$('.question').on("click", function () {
    // 根據當前選擇的語言來決定使用哪個版本的問題
    const question = (currentLanguage === 'en') ? $(this).data('question-en') : $(this).data('question');
    chatInput.val(question);
    chatSubmit.trigger('click');
});

// 送出問題
chatSubmit.on('click', function () {
    // divider出現
    $('.divider').removeClass('hidden');
    const message = DOMPurify.sanitize(chatInput.val().trim());
    if (!message) return;

    chatMessages.scrollTop(chatMessages.prop('scrollHeight'));

    chatInput.val('');

    // 送出按鈕變成loding，然後disable，取消enter送出，避免重複送出
    // 使用安全的方式創建DOM元素，避免HTML拼接
    $('#chat-submit').empty(); // 先清空現有內容
    const loadingSpan = $('<span>', { 
        class: 'loading loading-bars loading-sm' 
    });
    $('#chat-submit').append(loadingSpan);
    $('#chat-submit').prop('disabled', true);
    chatInput.prop('disabled', true);
    $('.question').prop('disabled', true);

    onUserRequest(message);
});

// 按Enter送出問題
chatInput.on('keyup', function (event) {
    if (event.key === 'Enter') {
        chatSubmit.click();
    }
});

// 點擊氣泡圖示，展開聊天視窗
chatBubble.on('click', function () {
    togglePopup();
});

// 點擊X，關閉聊天視窗
closePopup.on('click', function () {
    togglePopup();
});

// 開啟/關閉聊天視窗
function togglePopup() {
    chatPopup.toggleClass('hidden');
    if (!chatPopup.hasClass('hidden')) {
        chatInput.focus();
        // 使用安全的方式創建DOM元素
        chatBubble.empty(); // 先清空現有內容
        const img = $('<img>', {
            class: 'w-16 h-16',
            src: './img/back.svg',
            alt: 'chatbot'
        });
        chatBubble.append(img);
    } else {
        // 使用安全的方式創建DOM元素
        chatBubble.empty(); // 先清空現有內容
        const img = $('<img>', {
            class: 'w-16 h-16',
            src: './img/bubble.svg',
            alt: 'chatbot'
        });
        chatBubble.append(img);
    }
}

// 處理用戶輸入
function onUserRequest(message) {
    // Handle user request here
    console.log('User request:', message);

    // Sanitize the user message before displaying it
    const sanitizedMessage = DOMPurify.sanitize(message);

    // 使用安全的方式創建DOM元素，避免HTML拼接
    const messageElement = $('<div>', { class: 'flex justify-end mb-3' });
    const chatDiv = $('<div>', { class: 'chat chat-end' });
    const bubbleDiv = $('<div>', { class: 'chat-bubble max-w-full text-lg break-words' });
    
    // 安全地設置內容
    bubbleDiv.text(sanitizedMessage);
    chatDiv.append(bubbleDiv);
    messageElement.append(chatDiv);
    
    chatMessages.append(messageElement);
    chatMessages.scrollTop(chatMessages.prop('scrollHeight'));

    chatInput.val('');
    const randomId = Math.random().toString(36).substr(2, 9);
    reply('', randomId);
    // 呼叫API
    fetch('/askbot', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: message, chat_history:chatHistory })
      })
    .then(response => {
        if (!response.ok) {
            if (response.status === 429) {
                throw new Error(languages[currentLanguage].tooManyRequests);
            }
            throw new Error('Network Error: ' + response.status);
        }
        return response.json();
    })
    .then(data => {
        if (data.error) {
            // Sanitize the error message before inserting into HTML
            const sanitizedError = DOMPurify.sanitize(data.error);
            $('#' + randomId).find('.chat-bubble').text(languages[currentLanguage].error + sanitizedError);
        } else {
            console.log('Answer:', data.answer);
            // 使用 marked 解析 markdown，並用 DOMPurify 淨化
            const rawHtml = marked.parse(data.answer || '');
            const safeHtml = DOMPurify.sanitize(rawHtml);
            // 插入 HTML 內容
            const chatBubble = $('#' + randomId).find('.chat-bubble');
            chatBubble.empty();
            chatBubble.html(safeHtml);
            // 讓所有超連結在新分頁開啟
            chatBubble.find('a').attr('target', '_blank').attr('rel', 'noopener noreferrer');
        }

        if (data.chat_history) {
            chatHistory = data.chat_history;
        } else {
            chatHistory.push({
                "User": message,
                "Assistant": data.answer
            });
        }
        // 送出按鈕變成送出，然後enable，可以再次送出
        $('#chat-submit').text(languages[currentLanguage].submit);
        $('#chat-submit').prop('disabled', false);
        chatInput.prop('disabled', false);
        $('.question').prop('disabled', false);
    })
    .catch(error => {
        // Sanitize the error message before inserting into HTML
        const sanitizedErrorMessage = DOMPurify.sanitize(error.message);
        $('#' + randomId).find('.chat-bubble').text(languages[currentLanguage].error + sanitizedErrorMessage);
        // 送出按鈕變成送出，然後enable，可以再次送出
        $('#chat-submit').text(languages[currentLanguage].submit);
        $('#chat-submit').prop('disabled', false);
        chatInput.prop('disabled', false);
        $('.question').prop('disabled', false);
    });
}

// 顯示回覆
function reply(message, id) {
    // 使用安全的方式創建DOM元素，避免HTML拼接
    const replyElement = $('<div>', { class: 'flex mb-3' });
    const chatDiv = $('<div>', { class: 'chat chat-start' }).attr('id', id);
    const bubbleDiv = $('<div>', { class: 'chat-bubble bg-gray-300 text-black max-w-full text-lg break-words' });
    const loadingSpan = $('<span>', { class: 'loading loading-dots loading-md' });
    
    bubbleDiv.append(loadingSpan);
    chatDiv.append(bubbleDiv);
    replyElement.append(chatDiv);
    
    chatMessages.append(replyElement);
    chatMessages.scrollTop(chatMessages.prop('scrollHeight'));
}