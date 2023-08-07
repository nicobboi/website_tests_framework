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
import { Scatter, getElementAtEvent } from 'react-chartjs-2';

import { useState } from 'react';

import DateTimePicker from 'react-datetime-picker';
import 'react-datetime-picker/dist/DateTimePicker.css';
import 'react-calendar/dist/Calendar.css';

import ReportDetails from '../report_details/ReportDetails';
import ReportTypeDetails from '../report_type_details/ReportTypeDetails';
import { parse, secondsInDay, secondsInWeek } from 'date-fns';


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
    const fetchChartData = (type, start_time = null, end_time = null) => {
        // Reports filtered by type
        const reports = props.reports_scores.filter(report_score => report_score.tool.type === type)
            .filter((report_score) => (start_time ? report_score.timestamp > start_time : report_score))
            .filter((report_score) => (end_time ? report_score.timestamp < end_time : report_score))

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
    const initialData = {
        datasets: [
            {
                label: 'Accessibility',
                data: fetchChartData(getTypeFromIndex(0)),
                showLine: true,
                borderWidth: 3
            },
            {
                label: 'Performance',
                data: fetchChartData(getTypeFromIndex(1)),
                showLine: true,
                borderWidth: 3
            },
            {
                label: 'Security',
                data: fetchChartData(getTypeFromIndex(2)),
                showLine: true,
                borderWidth: 3
            },
            {
                label: 'SEO',
                data: fetchChartData(getTypeFromIndex(3)),
                showLine: true,
                borderWidth: 3
            },
            {
                label: 'Validation',
                data: fetchChartData(getTypeFromIndex(4)),
                showLine: true,
                borderWidth: 3
            },
        ],
    };

    const [data, setData] = useState(initialData);
    const updateDataRender = (start, end) => {
        const updatedData = {
            datasets: [
                {
                    ...data.datasets[0],
                    data: fetchChartData(getTypeFromIndex(0), start, end)
                },
                {
                    ...data.datasets[1],
                    data: fetchChartData(getTypeFromIndex(1), start, end)
                },
                {
                    ...data.datasets[2],
                    data: fetchChartData(getTypeFromIndex(2), start, end)
                },
                {
                    ...data.datasets[3],
                    data: fetchChartData(getTypeFromIndex(3), start, end)
                },
                {
                    ...data.datasets[4],
                    data: fetchChartData(getTypeFromIndex(4), start, end)
                }
            ]
        }

        setData(updatedData);
    }
    
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
                    unit: 'week',
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
    const [startDate, setStartDate] = useState(null);
    // format Date to string
    const formatTimestampFromDate = (date) => {
        if (!date) return null;

        const year = date.getUTCFullYear();
        const month = String(date.getUTCMonth() + 1).padStart(2, '0');
        const day = String(date.getUTCDate()).padStart(2, '0');
        const hours = String(date.getUTCHours()).padStart(2, '0');
        const minutes = String(date.getUTCMinutes()).padStart(2, '0');
        const seconds = String(date.getUTCSeconds()).padStart(2, '0');
        const milliseconds = String(date.getUTCMilliseconds()).padStart(3, '0');
        const offset = date.getTimezoneOffset();
        const offsetHours = Math.floor(Math.abs(offset) / 60).toString().padStart(2, '0');
        const offsetMinutes = (Math.abs(offset) % 60).toString().padStart(2, '0');
        const offsetSign = offset < 0 ? '+' : '-';

        const formattedTimestamp =
            `${year}-${month}-${day}T${hours}:${minutes}:${seconds}.${milliseconds}${offsetSign}${offsetHours}:${offsetMinutes}`;

        return formattedTimestamp;
    }
    const [endDate, setEndDate] = useState(formatTimestampFromDate(new Date()));
    // format string to Date
    const parseTimestampToDate = (dateString) => {
        if (!dateString) return null;

        const [isoDate, offsetPart] = dateString.split('+');
        const offsetHours = parseInt(offsetPart.slice(0, 2), 10);
        const offsetMinutes = parseInt(offsetPart.slice(3), 10);
        const totalOffsetMinutes = (offsetHours * 60) + offsetMinutes;
        
        const dateWithOffset = new Date(isoDate);
        dateWithOffset.setUTCMinutes(dateWithOffset.getUTCMinutes() - totalOffsetMinutes);

        return dateWithOffset;
    }
    // update the time render of the chart
    const updateTimeRender = (filter_time, change_date) => {
        const new_date = formatTimestampFromDate(change_date);
        if (filter_time === "start") {
            if (new_date > endDate) return;
            setStartDate(new_date);
            updateDataRender(new_date, endDate);
            var seconds_between = Math.floor((parseTimestampToDate(endDate) - parseTimestampToDate(new_date)) / 1000);
        }
        else if (filter_time === "end") {
            if (new_date < startDate) return;
            setEndDate(new_date);
            updateDataRender(startDate, new_date);
            var seconds_between = Math.floor((parseTimestampToDate(new_date) - parseTimestampToDate(startDate)) / 1000);
        }

        // Modify the chart option you want to change dynamically
        var time_format = null

        if (seconds_between < secondsInDay) {
            time_format = "hour";
        } else if (seconds_between < (secondsInWeek * 2)) {
            time_format = "day";
        } else {
            time_format = "week";
        }

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
          onClick={onChartClicked}
          ref={chartRef}
        />
        <div className="d-flex m-4 ms-5">
          <div className="d-flex flex-column">
            <span className='fs-5'>Start Date</span>
            <DateTimePicker onChange={(new_date) => updateTimeRender("start", new_date)} value={startDate} />
          </div>
          <div className="d-flex flex-column ms-5">
            <span className='fs-5'>End Date</span>
            <DateTimePicker onChange={(new_date) => updateTimeRender("end", new_date)} value={endDate} />
          </div>
        </div>

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
              reports_url={props.url}
            />
          )}
        </div>
      </>
    );
}

export default Chart;