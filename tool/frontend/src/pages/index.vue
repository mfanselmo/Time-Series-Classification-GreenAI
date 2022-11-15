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
  <div>
    <div class="grid grid-cols-1 lg:grid-cols-2">
      <div class="mb-6 lg:pr-8 lg:mb-0">
        <get-prediction-form />
      </div>
      <div class="lg:pl-8 ">
        <show-prediction class="mt-4"/>
        <clean-dataset class="mt-6"/>
      </div>
    
    </div>
    <div class="mt-8">
      <carbon-reduction-analysis />
    </div>
  </div>
</template>
