<script setup lang="ts">
import { Models, Datasets, Metrics } from 'src/api/types';

import { adminFilters } from 'src/stores/adminFilters'


const updateSelected = (newVal: string, property: 'selectedDataset' | 'selectedModel') => {
    const oldVal = adminFilters[property]
    if (oldVal == newVal) {
        adminFilters[property] = null
        return
    }

    adminFilters[property] = newVal

}

</script>

<template>
    <div class="flex justify-between">
        <v-select class="flex-1 mr-2" label="Metric" v-model:selected="adminFilters.selectedMetric" :options="Metrics" />
        <v-select class="flex-1 mr-2" label="Dataset" :selected="adminFilters.selectedDataset" @update:selected="val => updateSelected(val, 'selectedDataset')" :options="Datasets" />
        <v-select class="flex-1" label="Model" :selected="adminFilters.selectedModel" @update:selected="val => updateSelected(val, 'selectedModel')" :options="Models" />
    </div>
</template>