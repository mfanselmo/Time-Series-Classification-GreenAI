<script setup lang="ts">

interface Props {
    modelValue: null | File
    label: string
    disabled?: boolean
}

const props = withDefaults(defineProps<Props>(), {
    disabled: false
})

interface HTMLInputEvent extends Event {
    target: HTMLInputElement & EventTarget
}

const emit = defineEmits<{
    (e: 'update:modelValue', val: File | null): void
}>()

const onFileChange = (event: Event) => {
    let files =
        (event as HTMLInputEvent).target.files ||
        (event as DragEvent).dataTransfer?.files || null

    let file = files && files[0]

    emit('update:modelValue', file)
}




</script>

<template>
    <div>
        <label class="block mb-1 text-sm">{{label}}:</label>

        <input  type="file"
            class="bg-white w-full px-4 py-2 border border-gray-500 rounded outline-none focus:border-blue-500 focus:shadow-outline" autofocus
            @change="onFileChange"
            :disabled="disabled" />
    </div>
</template>
