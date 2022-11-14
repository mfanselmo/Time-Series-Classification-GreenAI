<script setup lang="ts">
import { Bar } from 'vue-chartjs'
import {
    Chart as ChartJS,
    Title,
    Tooltip,
    Legend,
    BarElement,
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
    BarElement,
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
    plugins?: Plugin<'bar'>[]
    labels: number[] | string[]
    datasets: Dataset[]
}

const props = withDefaults(defineProps<Props>(), {
    chartId: "bar-chart",
    width: 400,
    height: 400,
    cssClasses: '',
    plugins: () => []
})


const chartData = computed(() => ({
    labels: props.labels,
    datasets: props.datasets
}))

const chartOptions: DeepPartial<CoreChartOptions<"bar"> & ScaleChartOptions<'bar'>> = {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
        y: {
            min: (props.minY && props.minY < 0) ? props.minY : 0,
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
    <Bar :chart-options="chartOptions" :chart-data="chartData" :chart-id="chartId" :plugins="plugins"
        :css-classes="cssClasses" :width="width" :height="height" />


</template>