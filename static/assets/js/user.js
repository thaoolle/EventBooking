document.querySelectorAll('.tab-btn').forEach(button => {
    button.addEventListener('click', () => {
        // Remove active class from all buttons and panels
        document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
        document.querySelectorAll('.panel').forEach(panel => panel.classList.remove('active'));
        
        // Add active class to clicked button
        button.classList.add('active');
        
        // Show corresponding panel
        const tabId = button.dataset.tab;
        document.querySelectorAll('.panel')[tabId - 1].classList.add('active');
    });
});

document.addEventListener("DOMContentLoaded", function () {
    const messageContainer = document.getElementById("error-message");
    if (messageContainer) {
      setTimeout(() => {
        messageContainer.style.transition = "opacity 0.5s ease";
        messageContainer.style.opacity = "0";
  
        setTimeout(() => {
          messageContainer.style.display = "none";
        }, 200);
      }, 2000);
    }
  });