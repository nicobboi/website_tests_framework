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
    Colors,
    elements
} from 'chart.js';
import 'chartjs-adapter-date-fns';
import { useState } from 'react';
import { Scatter, getElementAtEvent } from 'react-chartjs-2';

import ReportDetails from '../report_details/ReportDetails';
import ReportTypeDetails from '../report_type_details/ReportTypeDetails';


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
    const getTypeFromIndex = (datasetIndex) => {
        switch(datasetIndex) {
            case 0: return "accessibility";
            case 1: return "performance";
            case 2: return "security";
            case 3: return "seo";
            case 4: return "validation";
        }
    }

    // scroll behaviour on render chidl component
    const scrollToChild = () => {
        const child = document.getElementById("child-render");
        if (child) 
            child.scrollIntoView({behavior: 'smooth'});
    }
    // function called from the report details component child to change it
    const changeReportDetails = (new_index, type) => {
        if (type >= 0 && type <= 5) {
            var reports = props.reports_scores.filter(report_score => report_score.tool.type === getTypeFromIndex(type));
        }
        if (new_index >= 0 && new_index < reports.length) {
            setReportDetails({
                report_id: reports[new_index].id,
                graph_index: new_index,
                dataset_index: type
            })
        }
    }

    // handle the click on the chart's points and redirect to report's details
    const [reportDetails, setReportDetails] = useState(null);
    const [reportTypeDetails, setReportTypeDetails] = useState(null);

    const chartRef = useRef();
    const onChartClicked = (event) => {
        const el_event = getElementAtEvent(chartRef.current, event);
        if (el_event.length > 0) {
            const index = el_event[0].element.$context.index;
            const datasetIndex = el_event[0].datasetIndex;
            var reports = props.reports_scores.filter(report_score => report_score.tool.type === getTypeFromIndex(datasetIndex));

            setReportTypeDetails(null);
            setReportDetails({
                report_id: reports[index].id,
                graph_index: index,
                dataset_index: datasetIndex
            });
            scrollToChild();
        }
    }


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
                borderWidth: 3
            },
            {
                label: 'Performance',
                data: fetchChartData("performance"),
                showLine: true,
                borderWidth: 3
            },
            {
                label: 'Security',
                data: fetchChartData("security"),
                showLine: true,
                borderWidth: 3
            },
            {
                label: 'SEO',
                data: fetchChartData("seo"),
                showLine: true,
                borderWidth: 3
            },
            {
                label: 'Validation',
                data: fetchChartData("validation"),
                showLine: true,
                borderWidth: 3
            },
        ],
    };
    
    // CHART CONFIGURATION
    const initialOptions = {
        responsive: true,
        interaction: {
            mode: 'nearest',
            intersect: false
        },
        elements: {
            point: {
                display: true,
                hoverRadius: 15,
                radius: 3
            },
        },
        tooltip: {
            usePointStyle: true,
        },
        plugins: {
            legend: {
                events: ['click', 'mousemove', 'mouseout'],
                labels: {
                    // color: "#0f0f0f",
                    font: {
                        size: 16,
                        weight: 'bold'
                    },
                    padding: 30,
                    usePointStyle: true,
                    pointStyle: 'triangle',
                    useBorderRadius: true,
                    borderRadius: 5
                },
                onHover: (event, legendItem, legend) => {
                    event.native.target.style.cursor = "pointer";
                },
                onLeave: (event, legendItem, legend) => {
                    event.native.target.style.cursor = "default";
                },
                onClick: function(e, legendItem) {
                    // chart update
                    var index = legendItem.datasetIndex;
                    var ci = this.chart;
                    var alreadyHidden = (ci.getDatasetMeta(index).hidden === null) ? false : ci.getDatasetMeta(index).hidden;
                    var hiddenList = [];
          
                    ci.data.datasets.forEach(function(e, i) {
                        var meta = ci.getDatasetMeta(i);
            
                        if (i !== index) {
                            if (!alreadyHidden) {
                                meta.hidden = meta.hidden === null ? !meta.hidden : null;
                            } else if (meta.hidden === null) {
                                meta.hidden = true;
                            }
                        } else if (i === index) {
                            meta.hidden = null;
                        }

                        hiddenList.push(meta.hidden);
                    });
          
                    ci.update();

                    // report type details render
                    if (hiddenList.some((element) => element === true)) {
                        setReportDetails(null);
                        setReportTypeDetails({
                            reports_type: getTypeFromIndex(index)
                        });
                    } else 
                        setReportTypeDetails(null);
                },
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

    return (
      <>
        <Scatter
          options={options}
          data={data}
        //   plugins={plugins}
          onClick={onChartClicked}
          ref={chartRef}
        />
        <button
          className="btn bg-primary text-white my-3 px-4 py-2"
          onClick={() => updateTimeRender("week")}
        >
          WEEK
        </button>
        <button
          className="btn bg-primary text-white ms-4 my-3 px-4 py-2"
          onClick={() => updateTimeRender("day")}
        >
          DAY
        </button>

        <div id="child-render">
          {reportDetails && !reportTypeDetails && (
            <ReportDetails
              report_id={reportDetails["report_id"]}
              report_index={reportDetails["graph_index"]}
              dataset_index={reportDetails["dataset_index"]}
              change_details={changeReportDetails}
            />
          )}
          {reportTypeDetails && !reportDetails && (
            <ReportTypeDetails 
                reports_type={reportTypeDetails["reports_type"]}
            />
          )}
        </div>
      </>
    );
}

export default Chart;