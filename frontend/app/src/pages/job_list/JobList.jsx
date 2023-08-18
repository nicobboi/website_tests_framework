import useFetch from "react-fetch-hook";
import { useState, useMemo } from "react";
import styles from "./scheduleslist.module.scss";
import {
  Accordion, 
  AccordionSummary, 
  AccordionDetails, 
  Typography,
  ToggleButton,
  ToggleButtonGroup
} from "@mui/material";
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import dayjs from "dayjs";

import { useSearchParams, createSearchParams } from "react-router-dom";

import ScheduleElement from "../../components/schedule_element/ScheduleElement";


const JobList = () => {
    // search params handler
    const [searchParams, setSearchParams] = useSearchParams();

    const [jobType, setJobType] = useState(searchParams.get("job"));
    const handleJobSelection = (event, newJobType) => {
      setJobType(newJobType);
      setSearchParams((newJobType ? createSearchParams({ job: newJobType }) : createSearchParams({})))
    };

    var request_url = ""
    if (jobType === "schedule") request_url = "http://localhost/api/v1/schedule/get-all";
    const { isLoading, data, error } = useFetch(request_url);
    const [dataFetched, setDataFetched] = useState({});

    useMemo(() => {
      if (error) return;

      if (!isLoading) {
        // fetch the data to organize by URL
        const listByUrl = {};

        for (const schedule of data) {
          const { url, ...otherAttributes} = schedule;

          if (!listByUrl[url]) listByUrl[url] = [];

          listByUrl[url].push(otherAttributes);
        }

        setDataFetched(listByUrl);
      }
    }, [isLoading, data])
  
    if (request_url !== "" && error) {
        return (
        <div>
            <p>Code: {error.status}</p>
            <p>Message: {error.statusText}</p>
        </div>
        )
    }

    // delete the child schedule and rerender
    const deleteScheduleRender = (url, data_index) => {
      var tempData = {...dataFetched};
      delete tempData[url][data_index];
      setDataFetched(tempData);
    }

    return (
      <>
        {isLoading ? (
          <p className="text-center">Loading component...</p>
        ) : (
          <div className="container">
            <div className="container mt-3">
              <div className="row">
                <div className="col-md-12 mb-4">
                  <div className="d-flex justify-content-between align-items-center">
                    <ToggleButtonGroup
                      color="primary"
                      value={jobType}
                      exclusive
                      onChange={handleJobSelection}
                      aria-label="Platform"
                    >
                      <ToggleButton value="schedule">Schedules</ToggleButton>
                      <ToggleButton value="tasks">Tasks</ToggleButton>
                    </ToggleButtonGroup>
                    <div className=" d-flex align-items-center">
                      <div className="me-3">
                        <i className="fa-regular fa-clock"></i>
                        <span className="ms-2">
                          {dayjs(new Date()).format("DD/MM/YYYY HH:mm")}
                        </span>
                      </div>
                      <button className={`${styles.icons} ${styles.reload} btn`}>
                        <i className="fa-solid fa-rotate-left"></i>
                      </button>
                    </div>
                  </div>

                  {jobType === "schedule" ? (
                  Object.entries(dataFetched).map(
                    (accordion_data, url_index) => (
                      <div key={url_index}>
                        <Accordion
                          className="my-4"
                          expanded={
                            searchParams.get("url") === accordion_data[0]
                          }
                          onChange={() =>
                            searchParams.get("url") !== accordion_data[0] ? 
                            setSearchParams(
                              createSearchParams({ url: accordion_data[0] })
                            ) :
                            setSearchParams(createSearchParams({}))
                          }
                        >
                          <AccordionSummary
                            expandIcon={<ExpandMoreIcon />}
                            id="panel1a-content"
                          >
                            <Typography>
                              <strong>{accordion_data[0]}</strong>
                            </Typography>
                          </AccordionSummary>
                          <AccordionDetails>
                            {accordion_data[1].map(
                              (schedule_data, data_index) => (
                                <ScheduleElement
                                  key={data_index}
                                  schedule={schedule_data}
                                  ondelete={deleteScheduleRender}
                                  url={accordion_data[0]}
                                  data_index={data_index}
                                />
                              )
                            )}
                          </AccordionDetails>
                        </Accordion>
                      </div>
                    )
                  )
                  ) : null }
                </div>
              </div>
            </div>
          </div>
        )}
      </>
    );
}

export default JobList;