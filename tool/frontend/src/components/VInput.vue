<script setup lang="ts">

interface Props {
    modelValue: null | string | number
    label: string
    placeholder: string
    number?: boolean
    disabled?: boolean
}

const props = withDefaults(defineProps<Props>(), {
    number: false,
    disabled: false
})



const emit = defineEmits<{
    (e: 'update:modelValue', val: string | number | null): void
}>()
</script>

<template>
    <div>
        <label class="block mb-1 text-sm">{{label}}:</label>

        <input 
            :type="number? 'number': 'text'" 
            class="w-full px-4 py-2 border rounded outline-none focus:border-blue-500 focus:shadow-outline"
            autofocus 
            :placeholder="placeholder" 
            :value="modelValue" 
            @input="e => emit('update:modelValue', (e.target as HTMLInputElement)[number ? 'valueAsNumber': 'value'] || null)" 
            :disabled="disabled" />
    </div>
</template>
