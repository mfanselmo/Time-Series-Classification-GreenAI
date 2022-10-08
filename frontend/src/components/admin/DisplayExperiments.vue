<script setup lang="ts">
import VueJsonPretty from 'vue-json-pretty';
import 'vue-json-pretty/lib/styles.css';

import { getExperimentsFn } from "src/api/admin";
import type { DatasetTypesTypes, IGetExperimentsInput } from 'src/api/types';
import { adminFilters } from 'src/stores/adminFilters'

import { useQuery } from 'vue-query';


const getExperimentsData: IGetExperimentsInput = reactive({
    detailLevel: "1",
    datasetType: (adminFilters.selectedDatasetType as DatasetTypesTypes) || null
})
const { isLoading, data } = useQuery("experiments", () => getExperimentsFn(getExperimentsData));

const filteredData = computed(() => {
    if (isLoading.value || !data.value) return []

    return data.value.filter(e => (
        (adminFilters.selectedDatasetType === null || adminFilters.selectedDatasetType === e.datasetType) 
            &&
        (adminFilters.selectedModel === null || adminFilters.selectedModel === e.model) 
            && 
        (adminFilters.selectedDataset === null || adminFilters.selectedDataset === e.dataset))
    )
})



</script>

<template>
    <div>
        <p v-if="isLoading">Loading...</p>
        <vue-json-pretty v-else-if="data" :data="JSON.parse(JSON.stringify(filteredData))" virtual :height="500"/>
    </div>
</template>
