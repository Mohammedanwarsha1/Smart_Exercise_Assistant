<script setup>
import { ref, watch, computed, onMounted } from "vue";

// Handle fade-in animation
const isPageLoaded = ref(false);

onMounted(() => {
    isPageLoaded.value = true;
});

// TODO: handle only video file
const dropzoneInput = ref(null);
const uploadedVideoFile = ref(null);
const isUploaded = computed(() => (uploadedVideoFile.value ? true : false));
const isDragOver = ref(false);

// Emit events
const emit = defineEmits(["fileUploaded"]);
watch(
    () => uploadedVideoFile.value,
    (newData, oldData) => {
        if (newData) {
            emit("fileUploaded", newData);
        }
    }
);

// * Handle Drag Events
const removeDragEventDefault = (event) => {
    event.preventDefault();
    event.stopPropagation();
};
const handleDragOver = (event) => {
    removeDragEventDefault(event);
    isDragOver.value = true;
};
const handleDragLeave = (event) => {
    removeDragEventDefault(event);
    isDragOver.value = false;
};
const handleDrop = (event) => {
    removeDragEventDefault(event);
    isDragOver.value = false;

    let videoFile = event.dataTransfer.files[0];
    
    if (videoFile && isValidVideo(videoFile)) {
        let dataTransfer = new DataTransfer();
        dataTransfer.items.add(videoFile);
        let filesToBeAdded = dataTransfer.files;

        dropzoneInput.value.files = filesToBeAdded;
        uploadedVideoFile.value = videoFile;
    } else {
        alert("Invalid video file type. Please upload a valid video.");
    }
};


// Handle File Input
const openFileInput = () => {
    dropzoneInput.value.click();
};
const handleClickUpload = (event) => {
    const target = event.target;
    if (target && target.files && target.files.length > 0) {
        uploadedVideoFile.value = target.files[0];
    } else {
        alert("Invalid video file type. Please upload a valid video.");
    }
};

// Other utils func
const byteToMB = (bytes) => {
    return Math.round(bytes / 1000000);
};
</script>

<template>
    
    <div
        class="dropzone"
        :class="{ 'dropzone-dragging': isDragOver }"
        id="dropzone"
        @drag="removeDragEventDefault"
        @dragstart="removeDragEventDefault"
        @dragend="removeDragEventDefault"
        @dragover="handleDragOver"
        @dragenter="handleDragLeave"
        @dragleave="removeDragEventDefault"
        @drop="handleDrop"
        @click.self="openFileInput"
    >
        <!-- Initial Stage -->
        <template v-if="!isUploaded">
            <!--<i class="fa-solid fa-cloud-arrow-up dropzone-icon"></i>-->
            <img src="../components/upload.png" style="width: 100px; height: 30px;"/>
            Drop files or Click here to select files to upload.
        </template>

        <!-- Uploaded State -->
        <template v-else>
            <img src="../components/uploaded.png" style="width: 100px; height: 30px;"/>
            {{ uploadedVideoFile.name }}
            ({{ byteToMB(uploadedVideoFile.size) }} MB)
        </template>

        <input
            type="file"
            name="files"
            class="dropzone-input"
            ref="dropzoneInput"
            @change="handleClickUpload"
        />
    </div>
   
</template>

<style lang="scss" scoped>
@use "sass:color";

/* Fade-in animation */
.fade-in {
    opacity: 0;
    transform: translateY(20px);
    transition: opacity 0.6s ease-in-out, transform 0.6s ease-in-out;
}

.fade-in-active {
    opacity: 1;
    transform: translateY(0);
}
.dropzone {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    border: 0.2rem dashed var(--primary-color);
    padding: 2rem;
    border-radius: 0.25rem;
    background-color: #fff;
    font-size: 1.25rem;
    text-align: center;
    transition: 0.25s background-color ease-in-out;
    cursor: pointer;

    &-dragging,
    &:hover {
        background-color: color.scale(#41b883, $lightness: 38%);
        // or
        // background-color: color.adjust(#41b883, $lightness: 38%);
    }

    &-icon {
        display: block;
        font-size: 3rem;
        margin: 0 auto 1.5rem;
        color: var(--primary-color);
    }

    &-input {
        display: none;
    }
}
</style>
