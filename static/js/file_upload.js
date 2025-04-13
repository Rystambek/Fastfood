document.addEventListener('DOMContentLoaded', function() {
    const fileInputs = document.querySelectorAll('input[type="file"][multiple]');
    
    fileInputs.forEach(input => {
        input.addEventListener('change', function(e) {
            const files = e.target.files;
            const formData = new FormData();
            const uploadUrl = input.dataset.url;
            
            // Add CSRF token
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            
            // Add files to FormData
            for (let i = 0; i < files.length; i++) {
                formData.append('images', files[i]);
            }
            
            // Show progress bar
            const progressContainer = input.closest('.custom-file-upload').querySelector('.upload-progress');
            const progressBar = progressContainer.querySelector('.progress-bar');
            const uploadStatus = progressContainer.querySelector('.upload-status');
            const messagesContainer = input.closest('.custom-file-upload').querySelector('.upload-messages');
            
            progressContainer.style.display = 'block';
            
            // Make AJAX request
            const xhr = new XMLHttpRequest();
            xhr.open('POST', uploadUrl, true);
            xhr.setRequestHeader('X-CSRFToken', csrfToken);
            
            // Progress tracking
            xhr.upload.addEventListener('progress', function(e) {
                if (e.lengthComputable) {
                    const percentComplete = (e.loaded / e.total) * 100;
                    progressBar.style.width = percentComplete + '%';
                    uploadStatus.textContent = `Uploading: ${Math.round(percentComplete)}%`;
                }
            });
            
            // Handle response
            xhr.onload = function() {
                if (xhr.status === 200) {
                    const response = JSON.parse(xhr.responseText);
                    if (response.success) {
                        messagesContainer.innerHTML = `
                            <div class="alert alert-success">
                                ${response.message}
                            </div>
                        `;
                        // Update current files display
                        const currentFiles = input.closest('.custom-file-upload').querySelector('.current-files');
                        if (currentFiles) {
                            const ul = currentFiles.querySelector('ul') || document.createElement('ul');
                            response.uploaded_files.forEach(file => {
                                const li = document.createElement('li');
                                li.textContent = file.name;
                                ul.appendChild(li);
                            });
                            if (!currentFiles.querySelector('ul')) {
                                currentFiles.appendChild(ul);
                            }
                        }
                    } else {
                        messagesContainer.innerHTML = `
                            <div class="alert alert-danger">
                                ${response.message}
                            </div>
                        `;
                    }
                } else {
                    messagesContainer.innerHTML = `
                        <div class="alert alert-danger">
                            An error occurred during upload. Please try again.
                        </div>
                    `;
                }
                
                // Reset progress bar
                progressBar.style.width = '0%';
                uploadStatus.textContent = '';
                progressContainer.style.display = 'none';
            };
            
            xhr.onerror = function() {
                messagesContainer.innerHTML = `
                    <div class="alert alert-danger">
                        Network error occurred. Please try again.
                    </div>
                `;
                progressContainer.style.display = 'none';
            };
            
            xhr.send(formData);
        });
    });
}); 