import type { DatasetTypesTypes } from "src/api/types"

interface AdminFilter {
    selectedMetric: string | null
    selectedModel: string | null
    selectedDataset: string | null
    selectedDatasetType: string | null
}
export const adminFilters : AdminFilter = reactive({
    selectedDatasetType: null,
    selectedMetric: 'f1_score',
    selectedModel: null,
    selectedDataset: null
})