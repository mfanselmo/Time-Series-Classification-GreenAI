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
        
        <Switch :model-value="modelValue" @update:model-value="val => emit('update:model-value', val)"
            :class="modelValue ? 'bg-blue-600' : 'bg-gray-200'"
            class="relative inline-flex items-center h-6 rounded-full w-11">
            <span :class="modelValue ? 'translate-x-6' : 'translate-x-1'"
            class="inline-block w-4 h-4 transition transform bg-white rounded-full" />
        </Switch>
        <label v-if="label" class="block ml-2 text-sm">{{label}}</label>
    </div>
</template>