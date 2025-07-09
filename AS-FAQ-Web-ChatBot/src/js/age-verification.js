document.addEventListener('DOMContentLoaded', function() {
    if (!sessionStorage.getItem('ageVerified')) {
        var ageModal = document.createElement('div');
        ageModal.innerHTML = `
            <div class="fixed inset-0 bg-gray-800 bg-opacity-75 flex items-center justify-center z-50">
                <div class="bg-white p-6 rounded-md text-center">
                    <p class="text-xl mb-4">請詳閱<a href="tos.html" id="tos-link" target="_blank" class="text-blue-500 underline">使用條款</a>後開始使用</p>
                    <button id="yes" class="bg-green-500 text-white px-4 py-2 rounded-md mr-2">了解</button>
                    <button id="no" class="bg-red-500 text-white px-4 py-2 rounded-md">離開</button>
                </div>
            </div>
        `;
        document.body.appendChild(ageModal);

        document.getElementById('yes').addEventListener('click', function() {
            sessionStorage.setItem('ageVerified', 'true');
            ageModal.remove();
        });

        document.getElementById('no').addEventListener('click', function() {
            window.location.href = 'https://www.google.com';
        });
    }
});
