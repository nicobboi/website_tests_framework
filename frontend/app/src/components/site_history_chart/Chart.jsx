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
} from 'chart.js';
import 'chartjs-adapter-date-fns';
import { Scatter, getElementAtEvent } from 'react-chartjs-2';

import { useState, useEffect, useMemo, useCallback } from 'react';
import {useSearchParams, createSearchParams} from 'react-router-dom';

import DateTimePicker from 'react-datetime-picker';
import 'react-datetime-picker/dist/DateTimePicker.css';
import 'react-calendar/dist/Calendar.css';

import ReportDetails from '../report_details/ReportDetails';
import ReportTypeDetails from '../report_type_details/ReportTypeDetails';
import { secondsInDay, secondsInWeek } from 'date-fns';

import dayjs from 'dayjs';
import utc from 'dayjs-plugin-utc';
dayjs.extend(utc);


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
    /* VARIABLES ------------------------------------------------------------ */

    // ref to the chart
    const chartRef = useRef();

    // search params handler
    const [searchParams, setSearchParams] = useSearchParams();

    // handle the click on the chart's points and redirect to report's details
    const [reportDetails, setReportDetails] = useState(null);
    const [reportTypeDetails, setReportTypeDetails] = useState(null);

    // start/end dates for filtering the chart
    const [startDate, setStartDate] = useState(null);
    const [endDate, setEndDate] = useState(null);

    /* ---------------------------------------------------------------------- */

    const getTypeFromIndex = (datasetIndex) => {
        switch(datasetIndex) {
            default: return null;
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

    /* CHART CONFIGURATION ------------------------------------------- */

    // handle the click on chart's elements
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
    
    // filter the elements of the chart by legend items
    const filterCategory = (e, legendItem) => {
        // chart update
        var index = legendItem.datasetIndex;
        var ci = (this ? this.chart : chartRef.current);
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

        setSearchParams(createSearchParams({category: legendItem.text.toLowerCase()}))
    }

    // return the dataset for the given type (timestamp - score)
    const fetchChartData = ((type, start_time = null, end_time = null) => {
        // Reports filtered by type
        const reports = props.reports_scores.filter(report_score => report_score.tool.type === type)
            .filter((report_score) => (start_time ? dayjs(report_score.timestamp) > start_time : report_score))
            .filter((report_score) => (end_time ? dayjs(report_score.timestamp) < end_time : report_score))

        // scores
        const report_scores = reports.map(report => report.scores.map(score => score.score)).flat();
        // timestamps
        const report_timestamps = reports.map(report => report.timestamp);

        var dataset = [];

        if (report_scores.length === report_timestamps.length) {
            report_scores.forEach((score, index) => {
                dataset.push({
                    x: dayjs(report_timestamps[index]).utcOffset(dayjs().utcOffset()).format(),
                    y: score
                })
            });
        } else {
            console.error('Axis data are not of the same length.');
        }

        return dataset;
    })

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
    const updateDataRender = useCallback((start, end) => {
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
    // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [])
    
    // chart options
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
                onClick: filterCategory,
            },
        },
        scales: {
            x: {
                type: 'time',
                time: {
                    unit: 'week',
                    unitStepSize: 1,
                    displayFormats: {
                        hour: 'HH:mm',
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
    // update the time render of the chart
    const updateTimeRender = (filter_time, change_date) => {
        const new_date = dayjs(change_date);
        var time_between;
        if (filter_time === "start") {
            if (endDate && new_date > endDate) return;
            setStartDate(change_date);
            time_between = endDate ? Math.floor((endDate - new_date) / 1000) : null;
        }
        else if (filter_time === "end") {
            if (startDate && new_date < startDate) return;
            setEndDate(change_date);
            time_between = startDate ? Math.floor((new_date - startDate) / 1000) : null;
        }

        // Modify the chart option you want to change dynamically
        var time_format;

        if (time_between && time_between < secondsInDay * 2) {
            time_format = "hour";
        } else if (time_between && time_between < (secondsInWeek * 2)) {
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

    /* ----------------------------------------------------------- */

    // update data render filtering by start/end dates
    useMemo(() => {
        updateDataRender(startDate, endDate)
    }, [startDate, endDate, updateDataRender])

    // set filter category by search params
    useEffect(() => {
        const chart = chartRef.current;

        if (chart) {
            for (const legendItem of chart.legend.legendItems) {
                if (legendItem.text.toLowerCase() === searchParams.get("category")) {
                    filterCategory(null, legendItem);
                }
            }
        }
    // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [])

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