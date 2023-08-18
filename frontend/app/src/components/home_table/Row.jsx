import { Link } from "react-router-dom";

import { useNavigate, createSearchParams } from "react-router-dom";

const Row = (props) => {
    const navigate = useNavigate();

    const toChartFiltered = (type_index) => {
      var type;
      switch(type_index) {
        default: return;
        case 0: type="accessibility"; break;
        case 1: type="performance"; break;
        case 2: type="security"; break;
        case 3: type="seo"; break;
        case 4: type="validation"; break;
      }

      const params = { category: type }
      navigate({
        pathname: '/site-history/' + props.slug,
        search: `?${createSearchParams(params)}`
      })
    }

    return (
      <>
        <tbody>
          <tr>
            {/* must change the parameter with a slug */}
            <th scope="row">
              <Link to={`/site-history/${props.slug}`}>{props.site}</Link>
            </th>
            {Object.values(props.scores).map((score, index) => (
              <td
                key={index}
                onClick={() => toChartFiltered(index)}
                style={{ 
                  background: setColor(score), 
                  cursor: "pointer",
                }}
              >
                {score}
              </td>
            ))}
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
