<route lang="json">
{
  "meta": {
    "title": "Home"
  }
}
</route>

<script setup lang="ts">

useHead({
  title: 'Home',
})

</script>

<template>
  <div class="grid grid-cols-1 lg:grid-cols-2">
    <div class="lg:pr-8 lg:mb-0 mb-6">
      <get-prediction-form />
    </div>
    <div class="lg:pl-8 ">
      <show-prediction class="mt-4"/>
      <clean-dataset class="mt-6"/>
    </div>

  </div>
</template>
