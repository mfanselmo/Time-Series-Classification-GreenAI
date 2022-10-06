import type { IGetPredictionResponse, IModelInfoInitial, IDatasetInfoInitial, IGoalInfoInitial, IDatasetDataQualityInfoInitial, ReducingMethodsTypes } from "src/api/types"


export const userDatasetInfo : IDatasetInfoInitial = reactive({
      datapointH: null,
      datapointW: null,
      datasetType: null,
      dimensions: null,
      numClasses: null,
      classesCounts: null,
      dataType: null,
      originalDataSize: null,
})

export const userDatasetDataQualityInfo: IDatasetDataQualityInfoInitial = reactive({
      completeness: null,
      accuracy: null,
      consistency: null
})

export const userModelInfo: IModelInfoInitial = reactive({
      modelType: null,
      nParameters: null,
})

export const userGoalInfo: IGoalInfoInitial = reactive({
      metric: null, 
      baseMetricResultPercentage: null, 
      baseMetricResult: null, 
      goalMetric: null, 
})

export const userPrediction : IGetPredictionResponse = reactive({
      metricCoefficient: 0,
      datasetPercent: 0,
      ready: false
})

export const analizeDataset = ref(true)
export const userDatasetFile = ref<null | File>(null)
export const reducingMethod = ref<ReducingMethodsTypes>('keep_distributions')