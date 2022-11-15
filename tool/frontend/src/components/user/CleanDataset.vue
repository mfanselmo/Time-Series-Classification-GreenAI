<script setup lang="ts">
import { cleanDatasetFn } from 'src/api/general';
import { ReducingMethods, ReducingMethodsLabels, type ICleanDatasetData } from 'src/api/types';
import { userPrediction, userGoalInfo, analizeDataset, userDatasetFile, reducingMethod } from 'src/stores/userDataset';
import { useMutation } from 'vue-query';


function download(filename: string, text: string) {
    var element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
    element.setAttribute('download', filename);

    element.style.display = 'none';
    document.body.appendChild(element);

    element.click();

    document.body.removeChild(element);
}

const newDatasetData = ref({})
const ready = ref(false)


const {
    mutate: cleanDataset,
    isLoading: cleanDatasetLoading,
    isError: cleanDatasetIsError,
} = useMutation(() => {

    return cleanDatasetFn({
        file: (userDatasetFile.value as File),
        datasetPercent: userPrediction.datasetPercent,
        reducingMethod: reducingMethod.value
    })
}, {
    onSuccess: (data) => {
        ready.value = true
        const { textDataset, ...rest } = data 
        newDatasetData.value = rest
        download('cleaned_dataset.txt', textDataset)
    }
});

</script>

<template>
    <div v-if="userPrediction.ready">
        <v-info-alert v-if="!analizeDataset">This option is only available if you upload your dataset in the form on the left</v-info-alert>
        <div v-if="analizeDataset && ready">
            <v-title size="h3">Result dataset information</v-title>
            <show-data  :data="newDatasetData" class="mt-2 mb-4"/>

        </div>
        <v-select label="Reducing Method" v-model:selected="reducingMethod" :options="ReducingMethods.map(r => ({ label: ReducingMethodsLabels[r], value: r}))" placeholder="Choose an option"/>
        <v-button class="w-full mt-7" :loading="cleanDatasetLoading" :disabled="!analizeDataset" @click="cleanDataset">
            Reduce Dataset
        </v-button>
    </div>
</template>
