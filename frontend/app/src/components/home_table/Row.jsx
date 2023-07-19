import { Link } from "react-router-dom";

const Row = (props) => {
    var td_id = 0;

    return (
      <>
        <tbody>
          <tr>
            {/* must change the parameter with a slug */}
            <th scope="row"><Link to={`/sitehistory/${formatUrl(props.site)}`}>{props.site}</Link></th> 
            {
                Object.values(props.scores).map((score) => (
                    <td key={td_id+=1} style={{background: setColor(score)}}>{score}</td>
                ))
            }
          </tr>
        </tbody>
      </>
    );  
};

export default Row;

// JS FUNCTIONS

function setColor(score) {
    let color;

    if (score === null | score === undefined) 
        color = 'white'
    else if (score >= 90) 
        color = '#7FFF00'; // green
    else if (score >= 60) 
        color = '#FFD700'; // yellow
    else
        color = "#DC143C"; // red
    
    return color
}

// temporary
function formatUrl(str) {
    const withoutHttp = str.replace(/^(https?:\/\/)/, '');
    const withoutSlash = withoutHttp.replace(/\//g, '');
    return withoutSlash;
  }