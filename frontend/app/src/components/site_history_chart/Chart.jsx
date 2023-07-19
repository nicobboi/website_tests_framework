import {
    Chart as ChartJS,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    Colors,
    TimeScale
} from 'chart.js';
import 'chartjs-adapter-date-fns';
import { Line } from 'react-chartjs-2';

ChartJS.register(
    LinearScale,
    PointElement,
    LineElement,
    Colors,
    Title,
    Tooltip,
    Legend,
    TimeScale
);


const Chart = (props) => {
    // CHAT DATA
    // All reports filtered by type for graph's y axis
    const acc_reports = props.reports_scores.filter(report_score => report_score.tool.type === "accessibility");
    const per_reports = props.reports_scores.filter(report_score => report_score.tool.type === "performance");
    const sec_reports = props.reports_scores.filter(report_score => report_score.tool.type === "security");
    const seo_reports = props.reports_scores.filter(report_score => report_score.tool.type === "seo");
    const val_reports = props.reports_scores.filter(report_score => report_score.tool.type === "validation");

    // Concatenate all timestamps for graph's x axis 
    const timestamps_concatenated = [].concat(...acc_reports.map(report => report.timestamp))
        .concat(...per_reports.map(report => report.timestamp))
        .concat(...sec_reports.map(report => report.timestamp))
        .concat(...seo_reports.map(report => report.timestamp))
        .concat(...val_reports.map(report => report.timestamp))

    const data = {
        labels: timestamps_concatenated.map(timestamp => new Date(timestamp)),
        datasets: [
            {
                label: 'Accessibility',
                data: acc_reports.map(report => report.scores.map(score => score.score)).flat(),
                // borderColor: 'rgb(255, 99, 132)',
                // backgroundColor: 'rgba(255, 99, 132, 0.5)',
            },
            {
                label: 'Performance',
                data: per_reports.map(report => report.scores.map(score => score.score)).flat(),
                // borderColor: 'rgb(255, 99, 132)',
                // backgroundColor: 'rgba(255, 99, 132, 0.5)',
            },
            {
                label: 'Security',
                data: sec_reports.map(report => report.scores.map(score => score.score)).flat(),
                // borderColor: 'rgb(255, 99, 132)',
                // backgroundColor: 'rgba(255, 99, 132, 0.5)',
            },
            {
                label: 'SEO',
                data: seo_reports.map(report => report.scores.map(score => score.score)).flat(),
                // borderColor: 'rgb(255, 99, 132)',
                // backgroundColor: 'rgba(255, 99, 132, 0.5)',
            },
            {
                label: 'Validation',
                data: val_reports.map(report => report.scores.map(score => score.score)).flat(),
                // borderColor: 'rgb(255, 99, 132)',
                // backgroundColor: 'rgba(255, 99, 132, 0.5)',
            },
        ],
    };


    // CHART CONFIGURATION
    const options = {
        responsive: true,
        plugins: {
            legend: {
                position: 'top',
            },
            title: {
                display: true,
                text: props.url + ' reports history',
            },
        },
        scales: {
            x: {
                type: 'time',
                time: {
                    unit: 'hour',
                    unitStepSize: 1,
                    displayFormats: {
                        hour: 'MMM dd hh:mm',
                        day: 'MMM dd hh:mm',
                        week: 'MMM dd',
                        month: 'MMM dd',
                        quarter: 'MMM dd',
                        year: 'MMM dd',
                    }

                }
            },
            y: {
                beginAtZero: true,
                min: 0,
                max: 100,
                offset: true
            }
        }
    };

    return (
      <>
        <Line options={options} data={data} />
      </>
    );
}

export default Chart;