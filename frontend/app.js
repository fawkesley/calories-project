
var ConfigSection = React.createClass({
  render: function() {
    return (
      <div className="container">
        <div className="row">
          <div className="col-md-12">
            <h2>Expected daily calories</h2>
            <form className="form-inline">
              <div className="form-group">
                <label className="sr-only" htmlFor="expectedDailyCalories">From date</label>
                <input type="number" className="form-control" id="expectedDailyCalories" value="2000"></input>
              </div>
            </form>
          </div>
        </div>
        <div className="row">
          <div className="col-md-6">
            <h2>Filter Date</h2>
            <form className="form-inline">
              <div className="form-group">
                <label className="sr-only" htmlFor="inputFromDate">From date</label>
                <input type="date" className="form-control" id="inputFromDate"></input>
              </div>
              <div className="form-group">
                <label className="sr-only" htmlFor="inputToDate">To date</label>
                <input type="date" className="form-control" id="inputToDate"></input>
              </div>
            </form>
          </div>
          <div className="col-md-6">
            <h2>Filter Time</h2>
            <form className="form-inline">
              <div className="form-group">
                <label className="sr-only" htmlFor="inputFromTime">From time</label>
                <input type="time" className="form-control" id="inputFromTime"></input>
              </div>
              <div className="form-group">
                <label className="sr-only" htmlFor="inputToTime">To time</label>
                <input type="time" className="form-control" id="inputToTime"></input>
              </div>
            </form>
          </div>
        </div>

      </div>
      );
  }
});


var CalorieCounterApp = React.createClass({
  render: function() {
    return (
    <div>
      <ConfigSection />

      <div className="container">
        <div className="row">
          <div className="col-md-12">
            <h2>2015-01-01 <span className="small highlight-green"> total calories: 1300</span></h2>

            <table className="table">
              <tbody>
              <tr>
                <td>09:00</td>
                <td>Cheese burger and McFlurry</td>
                <td>800</td>
                <td><i className="fa fa-times"></i></td>
              </tr>
              <tr>
                <td>14:00</td>
                <td>Chips and cheese</td>
                <td>500</td>
                <td><i className="fa fa-times"></i></td>
              </tr>
              <tr>
                <td>20:00</td>
                <td>Pizza</td>
                <td>800</td>
                <td><i className="fa fa-times"></i></td>
              </tr>
              </tbody>
            </table>
            <button type="button" className="btn btn-success pull-right"><i className="fa fa-plus"></i> Add</button>
          </div>
        </div>

        <div className="row">
          <div className="col-md-12">
            <h2>2015-01-01 <span className="small highlight-red"> total calories: 2100</span></h2>

            <table className="table">
              <tbody>
              <tr>
                <td>09:00</td>
                <td>Eggs on toast</td>
                <td>200</td>
                <td><i className="fa fa-times"></i></td>
              </tr>
              <tr>
                <td>13:30</td>
                <td>Ham sandwich</td>
                <td>300</td>
                <td><i className="fa fa-times"></i></td>
              </tr>
              <tr>
                <td>19:00</td>
                <td>Pizza</td>
                <td>800</td>
                <td><i className="fa fa-times"></i></td>
              </tr>
              </tbody>
            </table>
            <button type="button" className="btn btn-success pull-right"><i className="fa fa-plus"></i> Add</button>
          </div>
        </div>

      </div>
    </div>
    );
  }
});


React.render(
    <CalorieCounterApp />,
    document.getElementById('calorieCounterAppPlaceholder'));
