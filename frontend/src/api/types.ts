

export const Datasets = ["ChlorineConcentration", "Coffee", "ElectricDevices", "EthanolLevel", "PhalangesOutlinesCorrect", "StarLightCurves", "UWaveGestureLibraryAll"]
export const Models = ["FCN", "MLP", "RESNET"]
export const DatasetTypes = ["time_series", "images"] as const;
export const DataTypes = ['Sensor', 'Spectro', 'Image', 'Other'] as const;
export const ModelTypes = ['SIMPLE_CNN', 'SIMPLE_MLP', 'RESNET', 'Other'] as const;
export const Metrics = ["f1_score"] as const;
export const DetailLevels = ["0", "1", "2"] as const;
export const ReducingMethods = ["keep_distributions", "balance_classes"] as const;

export type DatasetTypesTypes = typeof DatasetTypes[number];
export type DataTypesTypes = typeof DataTypes[number];
export type ModelTypesTypes = typeof ModelTypes[number];
export type MetricTypes = typeof Metrics[number];
export type DetailLevelsTypes = typeof DetailLevels[number];
export type ReducingMethodsTypes = typeof ReducingMethods[number];


export interface IDBRun {
  id: number
  iteration: number
  dataQualityDimensionPercentage: number
  loss: number
  categoricalAccuracy: number
  categoricalCrossentropy: number
  top3Accuracy: number
  top5Accuracy: number
  precision: number
  recall: number
  auc: number
  f1Score: number
  effectiveEpochs: number
  usedDataSize: number
  actualDataPercentageUsed: number
  emissionsKg: number
  duration: number
}

export interface IDBCompletenessCurve {
    id: number
    metric: MetricTypes
    coefficient: number
    intercept: number
}

export interface IDatasetDataQualityInfo {
  completeness: number
  consistency: number
  accuracy: number
}

export interface IDatasetDataQualityInfoInitial {
  completeness: number | null
  consistency: number | null
  accuracy: number | null
}

export interface IDatasetInfo {
  datasetType: DatasetTypesTypes
  dataType: DataTypesTypes
  originalDataSize: number
  numClasses: number
  classesCounts: {[classNumber: number]: number}
  datapointW: number
  datapointH: number
  dimensions: number
}

export interface IModelInfo {
  modelType: ModelTypesTypes
  nParameters: number
}

export interface IDatasetInfoInitial {
  datasetType: DatasetTypesTypes | null
  dataType: DataTypesTypes | null
  originalDataSize: number | null
  numClasses: number | null
  classesCounts: {[classNumber: number]: number} | null
  datapointW: number | null
  datapointH: number | null
  dimensions: number | null
}

export interface IModelInfoInitial {
  modelType: ModelTypesTypes | null
  nParameters: number | null
}

export interface IGoalInfoInitial {
  metric: MetricTypes | null
  baseMetricResultPercentage: number | null
  baseMetricResult: number | null
  goalMetric: number | null
}

export interface IGoalInfo {
  metric: MetricTypes
  baseMetricResultPercentage: number
  baseMetricResult: number
  goalMetric: number
}

export interface IGetUserPredictionDataInitial extends IDatasetInfoInitial, IModelInfoInitial, IGoalInfoInitial {}
export interface IGetUserPredictionData extends IDatasetInfo, IModelInfo, IGoalInfo {}

export interface ICleanDatasetData {
  file: File
  datasetPercent: number,
  reducingMethod:  ReducingMethodsTypes
}


export interface IDBExperiment extends IModelInfo, IDatasetInfo {
    id: number
    dataset: string
    model: string
    runs?: IDBRun[]
    completenessCurves?: IDBCompletenessCurve[]
}


export interface EmptyResponse {
}

export interface ILoadExperimentsOnDbInput {
  resetDb: boolean;
}
export interface ILoadCompletenessCurvesInput {
  loadOnlyMissing: boolean;
}
export interface ITrainRegressorInput {
  datasetType: DatasetTypesTypes
  metric: MetricTypes
}

export interface IGetExperimentsInput {
  detailLevel: DetailLevelsTypes
  datasetType: DatasetTypesTypes
}

export interface IGetExperimentsResponse extends Array<IDBExperiment>{}

export interface IGetPredictionResponse {
  metricCoefficient: number
  datasetPercent: number
  ready: boolean
}

export interface IGetDatasetInfoResponse {
  numClasses: number,
  classesCounts: {[classNumber: number]: number},
  originalDataSize: number,
  datapointW: number,
  datapointH: number,
  dimensions: number,
  completeness: number,
  consistency: number
}

export interface ICleanDatasetResponse {
  numClasses: number,
  originalDataSize: number,
  datapointW: number,
  datapointH: number,
  dimensions: number,
  completeness: number,
  consistency: number,
  textDataset: string
}
