<script setup lang="ts">
import { CheckIcon, ChevronUpDownIcon } from '@heroicons/vue/20/solid'

interface Props {
    label?: string
    selected: string | null
    options: Readonly<string[]>
    placeholder?: string
}

const props = withDefaults(defineProps<Props>(), {
    placeholder: "Select an option",
})


const emit = defineEmits<{
    (e: 'update:selected', option: string): void
}>()

onMounted(() => {
    if (props.options.length === 1) emit('update:selected', props.options[0])
})

</script>

<template>
    <div>
        <label v-if="label" class="block mb-1 text-sm">{{label}}:</label>

        <Listbox :model-value="selected || ''" >
            <div class="relative mt-1">
                <ListboxButton
                    class="relative w-full py-2 pl-4 pr-10 text-left bg-white border border-gray-500 rounded outline-none cursor-default focus:outline-blue-500 focus:outline-offset-0 focus:border-blue-500 focus:shadow-outline">
                    <span class="block truncate" :class="!selected && 'text-gray-500'">{{ selected || placeholder }}</span>
                    <span class="absolute inset-y-0 right-0 flex items-center pr-2 pointer-events-none">
                        <ChevronUpDownIcon class="w-5 h-5 text-gray-400" aria-hidden="true" />
                    </span>
                </ListboxButton>

                <transition leave-active-class="transition duration-100 ease-in" leave-from-class="opacity-100"
                    leave-to-class="opacity-0">
                    <ListboxOptions
                        class="absolute z-50 w-full py-1 mt-1 overflow-auto text-base bg-white rounded-md shadow-lg max-h-60 ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm">
                        <ListboxOption v-slot="{ active, selected }" v-for="option in options" :key="option"
                            :value="option" as="template"
                            @click="emit('update:selected', option)"
                            >
                            <li :class="[
                              active ? 'bg-blue-100 text-blue-900' : 'text-gray-900',
                              'relative cursor-default select-none py-2 pl-10 pr-4',
                            ]">
                                <span :class="[
                                  selected ? 'font-medium' : 'font-normal',
                                  'block truncate',
                                ]">{{ option }}</span>
                                <span v-if="selected"
                                    class="absolute inset-y-0 left-0 flex items-center pl-3 text-blue-600">
                                    <CheckIcon class="w-5 h-5" aria-hidden="true" />
                                </span>
                            </li>
                        </ListboxOption>
                    </ListboxOptions>
                </transition>
            </div>
        </Listbox>
    </div>
</template>