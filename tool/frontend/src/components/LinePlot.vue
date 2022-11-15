<script setup lang="ts">
import { Line } from 'vue-chartjs'
import {
    Chart as ChartJS,
    Title,
    Tooltip,
    Legend,
    LineElement,
    LinearScale,
    PointElement,
    CategoryScale,
type CoreChartOptions,
type ScaleChartOptions,
} from 'chart.js'

import type { Plugin, ChartOptions } from 'chart.js'
import type { DeepPartial } from 'chart.js/types/utils';

ChartJS.register(
    Title,
    Tooltip,
    Legend,
    LineElement,
    LinearScale,
    PointElement,
    CategoryScale
)

interface Dataset {
    label: string
    backgroundColor: string,
    borderColor: string,
    data: number[]
}

interface Props {
    chartId?: string
    width?: number
    height?: number
    cssClasses?: string
    minY?: number
    xLabel: string
    yLabel: string,
    plugins?: Plugin<'line'>[]
    labels: number[] | string[]
    datasets: Dataset[]
}

const props = withDefaults(defineProps<Props>(), {
    chartId: "line-chart",
    width: 400,
    height: 400,
    cssClasses: '',
    plugins: () => []
})


const chartData = computed(() => ({
    labels: props.labels,
    datasets: props.datasets
}))

const chartOptions: DeepPartial<CoreChartOptions<"line"> & ScaleChartOptions<'line'>> = {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
        y: {
            min: props.minY || 0,
            grace: "2%",
            title: {
                text: props.yLabel,
                display: true
            }
        },
        x: {
            title: {
                text: props.xLabel,
                display: true
            },
        }
    }
}

</script>
<template>
    <Line 
    :chart-options="chartOptions" 
    :chart-data="chartData" 
    :chart-id="chartId" 
    :plugins="plugins" 
    :css-classes="cssClasses" 
    :width="width" 
    :height="height" />


</template>