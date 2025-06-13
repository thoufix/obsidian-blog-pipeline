document.addEventListener('DOMContentLoaded', function() {
  // Simulate loading progress
  const loadingProgress = document.getElementById('loadingProgress');
  const statusElement = document.getElementById('status');
  const totalTasks = document.querySelectorAll('input[type="checkbox"]').length;
  
  if (loadingProgress && statusElement) {
    let progress = 0;
    const interval = setInterval(() => {
      progress += 10;
      loadingProgress.style.width = `${progress}%`;
      
      if (progress >= 100) {
        clearInterval(interval);
        statusElement.textContent = 'MISSION CONTROL ONLINE - ALL SYSTEMS READY';
        setTimeout(() => {
          statusElement.style.display = 'none';
          document.querySelector('.loading-bar').style.display = 'none';
        }, 3000);
        
        // Enable all checkboxes
        document.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
          checkbox.disabled = false;
          checkbox.addEventListener('change', function() {
            const descId = this.id.replace('task', 'desc');
            const descElement = document.getElementById(descId);
            if (descElement) {
              descElement.classList.toggle('done', this.checked);
            }
          });
        });
      }
    }, 200);
  }
});