<script setup lang="ts">
import { getPredictionFn, getDatasetInfoFn } from 'src/api/general';
import { DatasetTypes, DataTypes, Metrics, ModelTypes, ModelTypesLabels } from 'src/api/types';
import type { IGetUserPredictionData, IGetUserPredictionDataInitial } from 'src/api/types';
import { useMutation } from 'vue-query';
import { 
    userDatasetInfo, userModelInfo, userGoalInfo, userPrediction, analizeDataset, userDatasetDataQualityInfo, userDatasetFile 
} from 'src/stores/userDataset'


const {
    mutate: getPrediction,
    isLoading: getPredictionLoading,
    isError: getPredictionIsError,
} = useMutation((data: IGetUserPredictionData) => getPredictionFn(data), {
    onSuccess: (data) => {
        userPrediction.metricCoefficient = data.metricCoefficient
        userPrediction.datasetPercent = data.datasetPercent
        userPrediction.ready = data.ready
    }
});

const {
    mutate: getDatasetInfo,
    isLoading: getDatasetInfoLoading,
    isError: getDatasetInfoIsError,
} = useMutation((data: File) => getDatasetInfoFn(data), {
    onSuccess: (data) => {
        const { datapointH, datapointW, numClasses, originalDataSize, dimensions, completeness, consistency, classesCounts } = data
        userDatasetInfo.datapointH = datapointH
        userDatasetInfo.datapointW = datapointW
        userDatasetInfo.numClasses = numClasses
        userDatasetInfo.originalDataSize = originalDataSize
        userDatasetInfo.dimensions = dimensions
        userDatasetInfo.classesCounts = classesCounts
        userDatasetDataQualityInfo.consistency = consistency
        userDatasetDataQualityInfo.completeness = completeness
    }
});





const userDatasetInfoHasNull = computed(() => {
    const userPredictionData: IGetUserPredictionDataInitial = { ...userDatasetInfo, ...userModelInfo, ...userGoalInfo }
    console.log(userPredictionData)
    return Object.values(userPredictionData).some(x => x === null)
})



watch(userDatasetFile, (value) => {
    if (value) {
        getDatasetInfo(value)
    } else {
        // reset values
        userDatasetInfo.datapointH = null
        userDatasetInfo.datapointW = null
        userDatasetInfo.numClasses = null
        userDatasetInfo.originalDataSize = null
        userDatasetInfo.dimensions = null


    }

})

const getFullPrediction = () => {

    if (userDatasetInfoHasNull.value) return 

    const userPredictionData: IGetUserPredictionData = { ...userDatasetInfo, ...userModelInfo, ...userGoalInfo } as IGetUserPredictionData
    getPrediction(userPredictionData)
}


</script>

<template>
    <div class="grid grid-cols-1">
        <div>
            <v-separator text="Dataset Info" />
            <div class="mt-2 mb-4">
                <v-checkbox v-model="analizeDataset" label="Analyze and clean dataset automatically"/>
            </div>
            <div class="flex mb-2 space-x-2">
                <!-- <v-select class="w-full" label="Dataset Type" v-model:selected="userDatasetInfo.datasetType"
                    :options="DatasetTypes" /> -->
                <v-select class="w-full" label="Data Type" v-model:selected="userDatasetInfo.dataType"
                    :options="DataTypes.map(d => ({label: d, value: d}))" />
            </div>
            <div v-if="analizeDataset">
                <v-file-input v-model="userDatasetFile" label="Upload Dataset File" />
                <!-- <show-data class="mt-6" :data="{...userDatasetInfo, ...userDatasetDataQualityInfo}"/> -->
            </div>
        
            <div v-else>
                <div class="flex mb-2 space-x-2">
                    <v-input placeholder="128" label="Series width" v-model="userDatasetInfo.datapointW" number />
                    <v-input placeholder="1" label="Series height" v-model="userDatasetInfo.datapointH" number />
                    <v-input placeholder="1" label="Number of dimensions" v-model="userDatasetInfo.dimensions" number />
                </div>
                <v-input class="mb-2" placeholder="3" label="Number of classes" v-model="userDatasetInfo.numClasses" number />
                <v-input class="mb-2" placeholder="5000" label="Number of available samples"
                    v-model="userDatasetInfo.originalDataSize" number />
                <!-- <div class="flex mb-2 space-x-2">
                    <v-input placeholder="0.8" label="Completeness" v-model="userDatasetDataQualityInfo.completeness" number />
                    <v-input placeholder="0.7" label="Accuracy" v-model="userDatasetDataQualityInfo.accuracy" number />
                    <v-input placeholder="1" label="Consistency" v-model="userDatasetDataQualityInfo.consistency" number />
                </div> -->
            </div>
            <v-separator text="Model Info" />
            <v-select class="mb-2"  label="Model Type" v-model:selected="userModelInfo.modelType" :options="ModelTypes.map(m => ({label: ModelTypesLabels[m], value: m}))" />
            <v-input  class="mb-2" placeholder="25000" label="Number of parameters" v-model="userModelInfo.nParameters" number />
        </div>

        <div>
            <div>
                <v-separator text="Goals" />
                <!-- <v-select class="mb-2" label="Metric" v-model:selected="userGoalInfo.metric" :options="Metrics" /> -->
                <!-- <v-input class="mb-2" placeholder="0.40" label="Percent of data used for base result" v-model="userGoalInfo.baseMetricResultPercentage" number /> -->
                <v-input class="mb-2" placeholder="0.65" label="Base result at 50% of the dataset" v-model="userGoalInfo.baseMetricResult" number />
                <v-input class="mb-2" placeholder="0.80" label="Goal in F1-Score" v-model="userGoalInfo.goalMetric" number />
            </div>
            <v-button class="w-full" :loading="getPredictionLoading" :disabled="userDatasetInfoHasNull"
                @click="getFullPrediction">Get prediction
            </v-button>
        </div>
    </div>
</template>
