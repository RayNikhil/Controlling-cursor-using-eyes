document.addEventListener('DOMContentLoaded', () => {
    const startButton = document.getElementById('startControl');
    const videoContainer = document.getElementById('videoContainer');
    const demoArea = document.getElementById('demoArea');
    const clickBox = document.getElementById('clickBox');

    // Start eye control and show the demo area
     startButton.addEventListener('click', () => {
        videoContainer.style.display = 'block';
        demoArea.style.display = 'block';
        startButton.style.display = 'none';

        console.log("Eye control started!");
     });

    // Add click effect on the click-box
    clickBox.addEventListener('click', () => {
        alert("Box clicked! Well done!");
        clickBox.style.backgroundColor = '#4caf50';
    });
});