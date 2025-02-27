import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import { AssignmentStatisticsResponseSchema } from '@schemas/assignment';
import { Chart, ChartConfiguration} from 'chart.js/auto';
import { useEffect, useRef } from 'react';

export interface BarGraphProps {
    canvasID: string;
    statistics: AssignmentStatisticsResponseSchema[];
}

export default function BarGraphGeneral(props: BarGraphProps) {
    const chartRef = useRef<Chart | null>(null);
    const userlabels: string[] = (props.statistics.map(
        (user: AssignmentStatisticsResponseSchema) => `${user.name} ${user.lastname}`)
    );

    const dataGraph = {
        labels: userlabels,
        datasets: [
            {
                label: 'Pendientes',
                data: props.statistics.map(
                    (user: AssignmentStatisticsResponseSchema) => user.totalPending
                ),
                borderWidth: 1
            },
            {
                label: 'Revisados',
                data: props.statistics.map(
                    (user: AssignmentStatisticsResponseSchema) => user.totalRevised
                ),
                borderWidth: 1
            }
        ]
    };

    const configGraph: ChartConfiguration = {
        type: 'bar',
        data: dataGraph,
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
            chartRef.current = new Chart(canvas, configGraph);
        }
        return () => {
            if (chartRef.current) {
                chartRef.current.destroy();
            }
        };
    }, [props.statistics]);

    return (
        <div className='w-full h-fit flex flex-col items-center justify-start gap-10 md:flex-row md:justify-center md:items-start'>
            <section className='w-1/2 h-full bg-white-55 p-3 rounded-md shadow-md drop-shadow-[1px_1px_2px_rgba(0,0,0,0.25)]'>
                <canvas id={props.canvasID} className='w-1/2'></canvas>
            </section>
            <section className='w-full h-full max-w-fit'>
                <TableContainer component={Paper}>
                    <Table sx={{ minWidth: 400 }} aria-label="simple table">
                        <TableHead>
                            <TableRow>
                                <TableCell>Usuario</TableCell>
                                <TableCell align="center">Asignaciones Totales</TableCell>
                                <TableCell align="center">Asignaciones Pendientes</TableCell>
                                <TableCell align="center">Asignaciones Revisadas</TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {props.statistics.map((user: AssignmentStatisticsResponseSchema) => (
                                <TableRow key={user.username} sx={{ '&:last-child td, &:last-child th': { border: 0 } }}>
                                    <TableCell component="th" scope="row">{user.name} {user.lastname}</TableCell>
                                    <TableCell component="th" scope="row" align="center">{user.totalPending + user.totalRevised}</TableCell>
                                    <TableCell component="th" scope="row" align="center">{user.totalPending}</TableCell>
                                    <TableCell component="th" scope="row" align="center">{user.totalRevised}</TableCell>
                                </TableRow> 
                            ))}
                        </TableBody>
                    </Table>
                </TableContainer>
            </section>
        </div>
    );
}