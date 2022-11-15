<script setup lang="ts">
import { loadExperimentsOnDbFn, loadCompletenessCurvesFn, trainRegressorFn } from 'src/api/admin';
import { Metrics, DatasetTypes } from 'src/api/types';
import type { ILoadExperimentsOnDbInput, ILoadCompletenessCurvesInput, ITrainRegressorInput } from 'src/api/types';

import { useMutation, useQueryClient } from 'vue-query';
import type { AxiosError } from 'axios';

const queryClient = useQueryClient()

const loadExperimentsOnDbData: ILoadExperimentsOnDbInput = reactive({
    resetDb: false
})
const loadCompletenessCurvesData: ILoadCompletenessCurvesInput = reactive({
    loadOnlyMissing: false
})

const {
    mutate: loadExperimentsOnDb,
    isLoading: loadExperimentsOnDbLoading,
    isError: loadExperimentsOnDbIsError,
} = useMutation((data: ILoadExperimentsOnDbInput) => loadExperimentsOnDbFn(data), {
    onSuccess: () => queryClient.invalidateQueries('experiments')
});

const {
    mutate: loadCompletenessCurves,
    isLoading: loadCompletenessCurvesLoading,
    isError: loadCompletenessCurvesIsError,
} = useMutation((data: ILoadCompletenessCurvesInput) => loadCompletenessCurvesFn(data), {
    onSuccess: () => queryClient.invalidateQueries('experiments')
});

const {
    mutate: trainRegressor,
    isLoading: trainRegressorLoading,
    isError: trainRegressorIsError,
    error: trainRegressorError
} = useMutation(() => trainRegressorFn());



</script>

<template>
    <div>
        <section class="mb-2">
            <v-separator text="Load Experiments On DB" />
            
            <div class="flex justify-between">
                <v-switch class="mb-2" label="Reset Database" v-model="loadExperimentsOnDbData.resetDb"/>
                <v-button  @click="loadExperimentsOnDb(loadExperimentsOnDbData)"
                    :theme="loadExperimentsOnDbIsError ? 'error': 'primary'" :loading="loadExperimentsOnDbLoading">Load
                </v-button>
            </div>
        </section>
        <section>
            <v-separator text="Load Completeness Curves" />
            <div class="flex justify-between">
                <v-switch class="mb-2" label="Load Only Missing" v-model="loadCompletenessCurvesData.loadOnlyMissing" />
                <v-button @click="loadCompletenessCurves(loadCompletenessCurvesData)"
                    :theme="loadCompletenessCurvesIsError ? 'error': 'primary'" :loading="loadCompletenessCurvesLoading">
                    Load</v-button>
            </div>
        </section>
        <section>
            <v-separator text="Train Regressors" />
            <v-danger-alert v-if="trainRegressorError">{{(trainRegressorError as any).response.data.detail}}</v-danger-alert>
            <div class="flex justify-between">
                <v-button @click="trainRegressor()" :theme="trainRegressorIsError ? 'error': 'primary'"
                    :loading="trainRegressorLoading">Load</v-button>
            </div>
        </section>
        <section>
            <v-separator text="Display Data" />
                    <filters />

        </section>
    </div>
</template>
