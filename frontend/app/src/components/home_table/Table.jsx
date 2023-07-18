import Row from './Row'

const Table = (props) => {
    return (
      <>
        <div className="container">
          <table class="table table-bordered border-black">
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
                    <Row site={row_data.url} scores={row_data.scores} />
                ))
            }
          </table>
        </div>
      </>
    );
}

export default Table;
