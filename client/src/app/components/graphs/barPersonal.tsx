import { AssignmentStatisticsResponseSchema } from '@schemas/assignment';
import { Chart, ChartConfiguration} from 'chart.js/auto';
import { useEffect, useRef } from 'react';

export interface BarGraphProps {
    canvasID: string;
    data: AssignmentStatisticsResponseSchema;
}

export default function BarGraphPersonal(props: BarGraphProps) {
    const chartRef = useRef<Chart | null>(null);
    const labels = [ 'Pendientes', 'Revisados' ];
    const data = {
        labels: labels,
        datasets: [{
            label: 'Estado de Asignaciones',
            data: [props.data.totalPending, props.data.totalRevised],
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(255, 159, 64, 0.2)',
                'rgba(255, 205, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(201, 203, 207, 0.2)'
            ],
            borderColor: [
                'rgb(255, 99, 132)',
                'rgb(255, 159, 64)',
                'rgb(255, 205, 86)',
                'rgb(75, 192, 192)',
                'rgb(54, 162, 235)',
                'rgb(153, 102, 255)',
                'rgb(201, 203, 207)'
            ],
            borderWidth: 1
        }]
    };
    const config: ChartConfiguration = {
        type: 'bar',
        data: data,
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            },
            plugins: {
                legend: {
                    position: 'top',
                    align: 'center',
                }
            }
        },
    };

    useEffect(() => {
        const canvas = document.getElementById(props.canvasID) as HTMLCanvasElement;
        if (canvas) {
            if (chartRef.current) {
                chartRef.current.destroy();
            }
            chartRef.current = new Chart(canvas, config);
        }
        return () => {
            if (chartRef.current) {
                chartRef.current.destroy();
            }
        };
    }, [props.data]);

    return (
        <div className='w-2/3 h-full'>
            <canvas id={props.canvasID}></canvas>
        </div>
    );
}