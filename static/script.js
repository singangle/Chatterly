let isEnglish = true;

function toggleLanguage() {
    isEnglish = !isEnglish;
    const elements = document.querySelectorAll('[data-en]');
    const buttons = document.querySelectorAll('.btn');
    const inputs = document.querySelectorAll('input[data-zh-placeholder]');

    elements.forEach(el => {
        el.textContent = isEnglish ? el.getAttribute('data-en') : el.getAttribute('data-zh');
    });

    inputs.forEach(input => {
        input.placeholder = isEnglish ? 
            input.getAttribute('placeholder') :
            input.getAttribute('data-zh-placeholder');
    });

    // Update language toggle button text
    document.querySelector('.language-toggle .btn').textContent = isEnglish ? '中文' : 'English';
}

function validateEmail(email) {
    const emailPattern = /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/;
    return emailPattern.test(email);
}

function validatePassword(password) {
    return password.length >= 6 && /\d/.test(password) && /[a-zA-Z]/.test(password);
}

function showError(elementId, message) {
    const errorElement = document.getElementById(elementId);
    errorElement.textContent = message;
    errorElement.style.display = 'block';
}

function hideError(elementId) {
    const errorElement = document.getElementById(elementId);
    errorElement.style.display = 'none';
}

function toggleLanguage() {
    isEnglish = !isEnglish;
    const elements = document.querySelectorAll('[data-en]');
    const buttons = document.querySelectorAll('.btn');
    const inputs = document.querySelectorAll('input[data-zh-placeholder]');

    elements.forEach(el => {
        el.textContent = isEnglish ? el.getAttribute('data-en') : el.getAttribute('data-zh');
    });

    inputs.forEach(input => {
        input.placeholder = isEnglish ? 
            input.getAttribute('placeholder') :
            input.getAttribute('data-zh-placeholder');
    });

    // Update language toggle button text
    document.querySelector('.language-toggle .btn').textContent = isEnglish ? '中文' : 'English';
}

if (currentLang === 'en') {
    usernameInput.placeholder = usernameInput.getAttribute('data-en-placeholder') || 'Username';
    passwordInput.placeholder = passwordInput.getAttribute('data-en-placeholder') || 'Password';
} else {
    usernameInput.placeholder = usernameInput.getAttribute('data-zh-placeholder') || '用户名';
    passwordInput.placeholder = passwordInput.getAttribute('data-zh-placeholder') || '密码';
}