import useFetch from "react-fetch-hook";
import { useState, useEffect } from "react";
import styles from "./scheduleslist.module.scss";
import {Accordion, AccordionSummary, AccordionDetails, Typography} from "@mui/material";
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';

import ScheduleElement from "../../components/schedule_element/ScheduleElement";

const SchedulesList = () => {
    const { isLoading, data, error } = useFetch("http://localhost/api/v1/schedule/get-all");
    const [dataFetched, setDataFetched] = useState({});

    useEffect(() => {
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
    }, [isLoading])
  
    if (error) {
        console.log(error)
        return (
        <div>
            <p>Code: {error.status}</p>
            <p>Message: {error.statusText}</p>
        </div>
        )
    }

    // get the current time in a formatted string like "dd/MM/YY hh:mm"
    const getCurrentDateFormatted = () => {
        const date = new Date();

        const day = String(date.getDate()).padStart(2, '0');
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const year = date.getFullYear();
        const hours = String(date.getHours()).padStart(2, '0');
        const minutes = String(date.getMinutes()).padStart(2, '0');

        const formattedString = `${day}/${month}/${year} ${hours}:${minutes}`;
        return formattedString;
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
            <h2 className="text-center mt-2">Schedules list</h2>

            <div className="container mt-3">
              <div className="row">
                <div className="col-md-12">
                  <div className="d-flex justify-content-between align-items-center activity">
                    <div>
                      <i className="fa-regular fa-clock"></i>
                      <span className="ms-2">{getCurrentDateFormatted()}</span>
                    </div>
                    <div className={styles.icons}>
                      <i className="fa fa-search"></i>
                      <i className="fa fa-ellipsis-h"></i>
                    </div>
                  </div>


                  {Object.entries(dataFetched).map(
                    (accordion_data, url_index) => (
                      <div key={url_index}>
                        <Accordion className="my-4">
                          <AccordionSummary
                            expandIcon={<ExpandMoreIcon />}
                            id="panel1a-content"
                          >
                            <Typography><strong>{accordion_data[0]}</strong></Typography>
                          </AccordionSummary>
                          <AccordionDetails>
                            {accordion_data[1].map((schedule_data, data_index) => (
                              <ScheduleElement key={data_index} schedule={schedule_data} ondelete={deleteScheduleRender} url={accordion_data[0]} data_index={data_index}/>
                            ))}
                          </AccordionDetails>
                        </Accordion>
                      </div>
                    )
                  )}
                </div>
              </div>
            </div>
          </div>
        )}
      </>
    );
}

export default SchedulesList;