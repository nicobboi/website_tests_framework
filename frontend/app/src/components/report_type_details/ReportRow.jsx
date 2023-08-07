import { Link } from "react-router-dom";

const ReportRow = (props) => {

    return (
      <>
          <tbody>
            <tr>
              {/* must change the parameter with a slug */}
              <th scope="row">
                1
              </th>
              <td>
                nome
              </td>
              <td>
                ieri
              </td>
              <td>
                note
              </td>
            </tr>
          </tbody>
      </>
    );
}

export default ReportRow;