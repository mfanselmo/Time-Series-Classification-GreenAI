<script setup lang="ts">

type SIZES = "h1" | "h2" | "h3"

interface Props {
  size: SIZES
}

const props = withDefaults(defineProps<Props>(), {
  size: "h1"
})



</script>

<template>
    <h1 v-if="size == 'h1'" class="text-lg font-bold text-indigo-600"><slot/></h1>
    <h2 v-if="size == 'h2'" class="text-lg font-bold"><slot/></h2>
    <h3 v-if="size == 'h3'" class="font-bold"><slot/></h3>
</template>
