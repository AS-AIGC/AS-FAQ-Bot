const chatInput = $('#chat-input');
const chatSubmit = $('#chat-submit');
const chatMessages = $('#chat-messages');
const chatBubble = $('#chat-bubble');
const chatPopup = $('#chat-popup');
const closePopup = $('#close-popup');

// 設定聊天視窗尺寸
$('#size-selector').on('change', function () {
    const size = $(this).val();
    chatPopup.removeClass('w-chat-sm w-chat-md');
    chatPopup.addClass('w-chat-' + size);
    // 用localStorage記錄尺寸
    localStorage.setItem('chat-size', size);
});

// 用localStorage設定尺寸
const size = localStorage.getItem('chat-size') || 'sm';
$('#size-selector').val(size).change();

// 點擊預設問題
$('.question').click(function () {
    const question = $(this).data('question');
    chatInput.val(question);
    chatSubmit.click();
});

// 送出問題
chatSubmit.on('click', function () {
    // divider出現
    $('.divider').removeClass('hidden');
    const message = sanitize(chatInput.val().trim());
    if (!message) return;

    chatMessages.scrollTop(chatMessages.prop('scrollHeight'));

    chatInput.val('');

    // 送出按鈕變成loding，然後disable，取消enter送出，避免重複送出
    $('#chat-submit').html('<span class="loading loading-bars loading-sm"></span>');
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
        // chatBubble.html('<img class="w-10 h-10" src="../img/times.svg" alt="chatbot">');
        chatBubble.html('<img class="w-10 h-10" src="./img/times.svg" alt="chatbot">');
    } else {
        // chatBubble.html('<img class="w-12 h-12" src="../img/bubble.svg" alt="chatbot">');
        chatBubble.html('<img class="w-12 h-12" src="./img/bubble.svg" alt="chatbot">');
    }
}

// 處理用戶輸入
function onUserRequest(message) {
    // Handle user request here
    console.log('User request:', message);

    // Display user message
    const messageElement = $('<div>', { class: 'flex justify-end mb-3' }).html(`
        <div class="chat chat-end">
            <div class="chat-bubble max-w-full text-lg break-words">
                `+ message + `
            </div>
        </div>
    `);
    chatMessages.append(messageElement);
    chatMessages.scrollTop(chatMessages.prop('scrollHeight'));

    chatInput.val('');
    const randomId = Math.random().toString(36).substr(2, 9);
    reply('', randomId);
    // 呼叫API
    fetch('/eip/askbot', { // /eip/askbot
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: message })
      })
    .then(response => {
        if (!response.ok) {
            if (response.status === 429) {
                throw new Error('🔄 請求過多，請稍後再試。');
            }
            throw new Error('Network Error: ' + response.status);
        }
        return response.json();
    })
    .then(data => {
        if (data.error) {
            $('#' + randomId).find('.chat-bubble').html('發生錯誤: ' + data.error);
        } else {
            console.log('Answer:', data.answer);
            // console.log('Sources:', data.sources);
            // 將換行字元替換為 <br> 標籤
            const formattedAnswer = data.answer.replace(/\n/g, '<br>');
            $('#' + randomId).find('.chat-bubble').html(formattedAnswer);
        }
        // 送出按鈕變成送出，然後enable，可以再次送出
        $('#chat-submit').html('送出');
        $('#chat-submit').prop('disabled', false);
        chatInput.prop('disabled', false);
        $('.question').prop('disabled', false);
    })
    .catch(error => {
        $('#' + randomId).find('.chat-bubble').html('發生錯誤: ' + error.message);
        // 送出按鈕變成送出，然後enable，可以再次送出
        $('#chat-submit').html('送出');
        $('#chat-submit').prop('disabled', false);
        chatInput.prop('disabled', false);
        $('.question').prop('disabled', false);
    });
}

// 顯示回覆
function reply(message, id) {
    const replyElement = $('<div>', { class: 'flex mb-3' }).html(`
        <div class="chat chat-start" id="`+ id + `">
            <div class="chat-bubble bg-gray-300 text-black max-w-full text-lg break-words">
                <span class="loading loading-dots loading-md"></span>
            </div>
        </div>
    `);
    chatMessages.append(replyElement);
    chatMessages.scrollTop(chatMessages.prop('scrollHeight'));
}

function sanitize(input) {
    return input
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}