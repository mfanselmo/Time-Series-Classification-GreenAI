<script setup lang="ts">

import { getExperimentsFn } from "src/api/admin";
import type { IGetExperimentsInput } from 'src/api/types';
import { useQuery } from 'vue-query';
import { adminFilters } from 'src/stores/adminFilters'


const getExperimentsData: IGetExperimentsInput = reactive({
    detailLevel: "1",
    datasetType: "time_series"
})
const { isLoading, data } = useQuery("experiments", () => getExperimentsFn(getExperimentsData));





const labels = computed(() => {
    if (isLoading.value) return []

    return Array.from(Array(10).keys()).map(i => (i + 1) / 10)

})


const datasets = computed(() => {
    if (isLoading.value || !(data.value)) return []
    
    if (data.value.map(e => e.completenessCurves).some(e => e === undefined)) return []


    return data.value.filter(e => {
        return (
            (adminFilters.selectedDatasetType === null || adminFilters.selectedDatasetType === e.datasetType) 
            && 
            (adminFilters.selectedModel === null || adminFilters.selectedModel === e.model) 
            && 
            (adminFilters.selectedDataset === null || adminFilters.selectedDataset === e.dataset)
        )
    }).map(e => {

        const completeness_curve = e.completenessCurves?.find(cc => cc.metric === adminFilters.selectedMetric)

        return {
            label: `${e.dataset} ${e.model}`,
            backgroundColor: '#e755ba',
            borderColor: '#bae755',
            data: labels.value.map(i => (completeness_curve?.intercept || 0) + (completeness_curve?.coefficient || 0)*Math.log(i))
        }
    })
})

</script>

<template>
    <div class="flex">
        <line-plot x-label="" y-label="" class="flex-1" v-if="!isLoading" :labels="labels" :datasets="datasets" />
    </div>
</template>
