import { useRef } from 'react';
import {
    Chart as ChartJS,
    TimeScale,
    LinearScale,
    PointElement,
    LineElement,
    Tooltip,
    Title,
    Legend,
    Colors
} from 'chart.js';
import 'chartjs-adapter-date-fns';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Scatter, getElementAtEvent } from 'react-chartjs-2';

ChartJS.register(
    TimeScale,
    LinearScale,
    PointElement,
    LineElement,
    Tooltip,
    Colors,
    Title,
    Legend,
    TimeScale
);


const Chart = (props) => {
    // CHART DATA
    // return the dataset for the given type (timestamp - score)
    const fetchChartData = (type) => {
        // Reports filtered by type
        const reports = props.reports_scores.filter(report_score => report_score.tool.type === type);

        // scores
        const report_scores = reports.map(report => report.scores.map(score => score.score)).flat();
        // timestamps
        const report_timestamps = reports.map(report => report.timestamp);

        var dataset = [];

        if (report_scores.length === report_timestamps.length) {
            report_scores.forEach((score, index) => {
                dataset.push({
                    x: report_timestamps[index],
                    y: score
                })
            });
        } else {
            console.error('Axis data are not of the same length.');
        }

        return dataset;
    }

    // datasets of the chart
    const data = {
        datasets: [
            {
                label: 'Accessibility',
                data: fetchChartData("accessibility"),
                showLine: true,
                fill: false
                // borderColor: 'rgb(255, 99, 132)',
                // backgroundColor: 'rgba(255, 99, 132, 0.5)',
            },
            {
                label: 'Performance',
                data: fetchChartData("performance"),
                showLine: true,
                fill: false
                // borderColor: 'rgb(255, 99, 132)',
                // backgroundColor: 'rgba(255, 99, 132, 0.5)',
            },
            {
                label: 'Security',
                data: fetchChartData("security"),
                showLine: true,
                fill: false
                // borderColor: 'rgb(255, 99, 132)',
                // backgroundColor: 'rgba(255, 99, 132, 0.5)',
            },
            {
                label: 'SEO',
                data: fetchChartData("seo"),
                showLine: true,
                fill: false
                // borderColor: 'rgb(255, 99, 132)',
                // backgroundColor: 'rgba(255, 99, 132, 0.5)',
            },
            {
                label: 'Validation',
                data: fetchChartData("validation"),
                showLine: true,
                fill: false
                // borderColor: 'rgb(255, 99, 132)',
                // backgroundColor: 'rgba(255, 99, 132, 0.5)',
            },
        ],
    };

    // CHART CONFIGURATION
    const initialOptions = {
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
                    unit: 'day',
                    unitStepSize: 1,
                    displayFormats: {
                        hour: 'hh:mm',
                        day: 'MMM dd',
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

    // to update the time render on x axis of the chart
    const [options, setChartOptions] = useState(initialOptions);
    const updateTimeRender = (time_format) => {
        // Modify the chart option you want to change dynamically
        const updatedOptions = {
            ...options,
            scales: {
                ...options.scales,
                x: {
                    ...options.scales.x,
                    time: {
                        ...options.scales.x.time,
                        unit: time_format
                    }
                }
            },
        }

        setChartOptions(updatedOptions)
    }

    // handle the click on the chart's points and redirect to report's details
    const chartRef = useRef();
    const navigate = useNavigate();
    const onChartClicked = (event) => {
        const el_event = getElementAtEvent(chartRef.current, event);
        if (el_event.length > 0) {
            const index = el_event[0].element.$context.index;
            switch (el_event[0].datasetIndex) { 
                case 0: // ACCESSIBILITY
                    var reports = props.reports_scores.filter(report_score => report_score.tool.type === "accessibility");
                    break;
                case 1: // PERFORMANCE
                    var reports = props.reports_scores.filter(report_score => report_score.tool.type === "performance");
                    break;
                case 2: // SECURITY
                    var reports = props.reports_scores.filter(report_score => report_score.tool.type === "security");
                    break;
                case 3: // SEO
                    var reports = props.reports_scores.filter(report_score => report_score.tool.type === "seo");
                    break;
                case 4: // VALIDATION
                    var reports = props.reports_scores.filter(report_score => report_score.tool.type === "validation");
                    break;
            }
            navigate('/report/' + reports[index].id);
        }
    }

    return (
      <>
        <Scatter options={options} data={data} onClick={onChartClicked} ref={chartRef}/>
        <button className='btn bg-primary text-white my-3 px-4 py-2' onClick={() => updateTimeRender('week')}>WEEK</button>
        <button className='btn bg-primary text-white ms-4 my-3 px-4 py-2' onClick={() => updateTimeRender('day')}>DAY</button>
      </>
    );
}

export default Chart;