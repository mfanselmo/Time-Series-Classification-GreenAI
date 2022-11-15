<script setup lang="ts">

interface Props {
    data: { [key: string]: null | number | string | {[classNumber: number]: number}}
}

const props = withDefaults(defineProps<Props>(), {
})



const capitalize = (text: string) => {

    const result = text.replace(/([A-Z])/g, " $1");
    const finalResult = result.charAt(0).toUpperCase() + result.slice(1);
    return finalResult
}

</script>

<template>
    <div class="grid grid-cols-4 bg-white rounded border border-gray-500 text-sm py-1">
        <template v-for="[name, value] in Object.entries(data)">
            <p class="pl-4 rounded-l font-bold py-1.5">{{capitalize(name)}}:</p>
            <p class="pl-2 py-1.5 rounded-r">{{value}}</p>
        </template>
    </div>
</template>
