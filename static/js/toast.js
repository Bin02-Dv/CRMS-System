// Automatically remove toasts after animation
setTimeout(() => {
    const toasts = document.querySelectorAll('.toast');
    toasts.forEach(toast => {
        toast.style.display = 'none';
    });
}, 5000);