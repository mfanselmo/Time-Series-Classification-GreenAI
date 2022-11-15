<script setup lang="ts">
interface Props {
    text: string
}

const props = withDefaults(defineProps<Props>(), {
})
</script>
<template>
    <div class="relative py-4">
        <div class="absolute inset-0 flex items-center">
            <div class="w-full border-b border-gray-300"></div>
        </div>
        <div class="relative flex justify-center">
            <span class="bg-gray-100 px-4 text-sm text-gray-500">{{text}}</span>
        </div>
    </div>
</template>