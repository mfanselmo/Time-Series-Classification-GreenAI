
interface AdminFilter {
    selectedMetric: string | null
    selectedModel: string | null
    selectedDataset: string | null
}
export const adminFilters : AdminFilter = reactive({
    selectedMetric: 'f1_score',
    selectedModel: null,
    selectedDataset: null
})