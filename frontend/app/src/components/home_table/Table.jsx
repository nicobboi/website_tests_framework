import Row from './Row'

const Table = (props) => {
    var row_id = 0;

    return (
      <>
        <div className="container">
          <table className="table table-bordered border-black">
            <thead>
              <tr>
                <th scope="col">Site</th>
                <th scope="col">Accessibility</th>
                <th scope="col">Performance</th>
                <th scope="col">Security</th>
                <th scope="col">SEO</th>
                <th scope="col">Validation</th>
              </tr>
            </thead>
            {   // iterate all the table's data 
                props.table_data.map((row_data) => (
                    <Row key={row_data.site_id} slug={row_data.site_id} site={row_data.url} scores={row_data.scores} />
                ))
            }
          </table>
        </div>
      </>
    );
}

export default Table;
