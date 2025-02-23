<script setup></script>

<template>
    <div class="container">
        <div class="box">
            <RouterLink :to="{ name: 'ExcerciseSelection' }" class="box_link">
                <!--<i class="fa-solid fa-video"></i>-->
                <img src="../views/video.png" alt="Real Time" class="icon" />
                <p class="box__description">Real Time</p>
            </RouterLink>
        </div>

        <div class="box">
            <RouterLink :to="{ name: 'VideoStreaming' }" class="box_link">
                <!--<i class="fa-solid fa-upload"></i>-->
                <img src="../views/upload.png" alt="Real Time" class="icon" />
                <p class="box__description">Upload a video</p>
            </RouterLink>
        </div>
    </div>
</template>

<style lang="scss" scoped>
.container {
    margin-top: 10rem;
    width: 100%;
    display: flex;
    justify-content: space-around;
}

.box {
    width: 200px;
    height: 200px;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: #f3f3f3; /* Light gray background */
    border-radius: 10px; /* Rounded corners */
    box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1); /* Subtle shadow */
    transition: transform 0.3s ease-in-out;
}

.box:hover {
    transform: rotate(5deg) scale(1.05);
    transition: transform 0.3s ease-in-out;
}

.box_link {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-decoration: none;
    color: inherit;
}

.box__description {
    margin-top: 0.5rem;
    font-size: 1.5rem;
    font-weight:lighter;
}
.icon {
    width: 50px;  
    height: 50px; 
    object-fit: contain; /* Ensures image is properly fitted */
}
</style>