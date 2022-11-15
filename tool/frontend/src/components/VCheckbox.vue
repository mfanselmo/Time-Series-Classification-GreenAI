<script setup lang="ts">
import { CheckIcon, ChevronUpDownIcon } from '@heroicons/vue/20/solid'

interface Props {
    label?: string
    modelValue: boolean
}

const props = withDefaults(defineProps<Props>(), {
})


const emit = defineEmits<{
    (e: 'update:model-value', option: boolean): void
}>()



</script>

<template>
    <div class="flex items-center">
        <input class="" type="checkbox" :id="`checkbox-${label}`" :checked="modelValue" @input="e => emit('update:model-value', (e.target as HTMLInputElement).checked)" />
        <label v-if="label" class="block ml-2 text-sm" :for="`checkbox-${label}`">{{label}}</label>
    </div>
</template>