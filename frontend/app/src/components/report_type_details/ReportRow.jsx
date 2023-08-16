import dayjs from 'dayjs';
import utc from 'dayjs-plugin-utc';
dayjs.extend(utc);

const ReportRow = (props) => {

    return (
      <>
        <tbody>
          <tr>
            <th scope="row">{props.id}</th>
            <td>{props.tool}</td>
            <td>{props.scores.map((score) => (`${score.name}: ${score.score}`))}</td>
            <td>{dayjs(props.end_time).utcOffset(dayjs().utcOffset()).format('DD/MM/YYYY HH:mm')}</td>
            <td>{props.notes}</td>
          </tr>
        </tbody>
      </>
    );
}

export default ReportRow;