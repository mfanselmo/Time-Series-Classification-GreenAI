<script setup lang="ts">
import { userPrediction, userGoalInfo } from 'src/stores/userDataset';



const labels = computed(() => {
    if (!userPrediction.ready) return []

    return Array.from(Array(10).keys()).map(i => (i+1)/10)
    
})

const datasets = computed(() => {
    if (!userPrediction.ready) return []
    const intercept = (userGoalInfo.baseMetricResult as number) - (userGoalInfo.baseMetricResultPercentage as number) *userPrediction.metricCoefficient
    
    return [{
        label: 'User Dataset',
        backgroundColor: '#f87979',
        borderColor: "#f87979",
        data: labels.value.map(i => Math.min(intercept  + userPrediction.metricCoefficient*i,1 ))
    }]
})

const displayPercent = (number: number) => {
    number = number*100
    const    as_string = number.toString(); 
    return as_string.slice(0, (as_string.indexOf(".")) + 3);
}
const importantClass = "text-indigo-700 font-bold"

</script>

<template>
    <div>
        <v-title size="h2">Results</v-title>
        <v-info-alert class="mt-4" v-if="!userPrediction.ready" >Input your data to continue</v-info-alert>
        <div v-else>
            <line-plot :labels="labels" :datasets="datasets"/>

            <div class="mt-4">
                <p class="prose prose-lg text-justify">
                    According to our model, you need <span :class="importantClass">{{displayPercent(userPrediction.datasetPercent)}}%</span>
                    of your dataset to get the desired
                    <span :class="importantClass">{{userGoalInfo.metric}}: {{displayPercent(userGoalInfo.goalMetric as number)}}% </span>
                </p>
                <p class="prose prose-lg text-justify">
                    In order to reach this goal, we recommend focusing the 
                    <span :class="importantClass">removing</span> on removing as much low quality data.
                    You can do so automatically by clicking the button below.
                </p>
            </div>
        </div>
    </div>
</template>
