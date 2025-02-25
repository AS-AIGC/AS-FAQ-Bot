document.addEventListener('DOMContentLoaded', function() {
    if (!sessionStorage.getItem('ageVerified')) {
        var ageModal = document.createElement('div');
        ageModal.innerHTML = `
            <div class="fixed inset-0 bg-gray-800 bg-opacity-75 flex items-center justify-center z-50">
                <div class="bg-white p-6 rounded-md text-center">
                    <p class="text-xl mb-4">您是否已滿18歲？</p>
                    <button id="age-yes" class="bg-green-500 text-white px-4 py-2 rounded-md mr-2">是</button>
                    <button id="age-no" class="bg-red-500 text-white px-4 py-2 rounded-md">否</button>
                </div>
            </div>
        `;
        document.body.appendChild(ageModal);

        document.getElementById('age-yes').addEventListener('click', function() {
            sessionStorage.setItem('ageVerified', 'true');
            ageModal.remove();
        });

        document.getElementById('age-no').addEventListener('click', function() {
            alert('您必須滿18歲才能使用此服務。');
            window.location.href = 'https://www.google.com';
        });
    }
});
