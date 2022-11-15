<script setup lang="ts">
import { userPrediction, userGoalInfo } from 'src/stores/userDataset';



const labels = computed(() => {
    if (!userPrediction.ready) return []

    return Array.from(Array(14).keys()).map(i => (2 ** (i+3)))

})

const datasets = computed(() => {

    const final_hyperparameter_search_count = 10
    const classic_method_emissions = (i: number) => i
    const our_method_emissions = (i: number) => i * (userGoalInfo.baseMetricResultPercentage as number) + final_hyperparameter_search_count*userPrediction.datasetPercent


    return [{
        label: 'Reduction in carbon emissions when using this tool vs the classic approach',
        backgroundColor: '#22c55e',
        borderColor: "#22c55e",
        data: labels.value.map(i => - (our_method_emissions(i) - classic_method_emissions(i)) / classic_method_emissions(i))
    }]
})

console.log(datasets)
const displayPercent = (number: number) => {
    number = number * 100
    const as_string = number.toString();
    return as_string.slice(0, (as_string.indexOf(".")) + 3);
}
const importantClass = "text-indigo-700 font-bold"

</script>

<template>
    <div v-if="userPrediction.ready">
        <v-title size="h2">Carbon Emissions Reduction Analysis</v-title>
        <div class="grid grid-cols-2 space-x-8">
            <bar-plot :labels="labels" :datasets="datasets" :min-y="Math.min(...datasets[0].data)" x-label="Initial hyperparameter iterations" y-label="Percentual carbon emissions reduced"/>

            <div class="mt-4">
                <p class="prose prose-lg text-justify">
                    By performing the initial <span :class="importantClass">hyperparameter search</span> 
                    on only <span :class="importantClass">{{ displayPercent(userGoalInfo.baseMetricResultPercentage as number)}}%</span>
                    of the dataset, you can reduce your carbon emissions by 
                    <span :class="importantClass">{{ displayPercent(userGoalInfo.baseMetricResultPercentage as number)}}%</span>.
                </p>
                <p class="prose prose-lg text-justify">
                    The plot in the left shows the reductions of using our approach (on <span :class="importantClass">different number of iterations</span> for the initial hyperparameter search) versus using the classic approach.
                </p>
            </div>
        </div>
    </div>
</template>
