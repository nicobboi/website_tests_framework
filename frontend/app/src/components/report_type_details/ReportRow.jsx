import { Link } from "react-router-dom";

const ReportRow = (props) => {

    return (
      <>
        <tbody>
          <tr>
            <th scope="row">{props.id}</th>
            <td>{props.tool}</td>
            <td>{props.end_time}</td>
            <td>{props.notes}</td>
          </tr>
        </tbody>
      </>
    );
}

export default ReportRow;