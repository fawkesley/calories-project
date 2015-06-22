
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

var DayTitle = React.createClass({
  render: function() {
    return (
        <h2>2015-01-01 <span className="small highlight-green"> total calories: 1300</span></h2>
      );
  }
});

var MealRow = React.createClass({
  render: function() {
    return (
      <tr>
        <td>09:00</td>
        <td>Cheese burger and McFlurry</td>
        <td>800</td>
        <td><i className="fa fa-times"></i></td>
      </tr>
    );
  }
});

var MealsTable = React.createClass({
  render: function() {
    return (
      <table className="table">
        <tbody>
        <MealRow />

        </tbody>
      </table>
      );
  }
});

var DaySection = React.createClass({
  render: function() {
    return (
      <div className="row">

        <div className="col-md-12">
          <DayTitle />
          <MealsTable />

          <button type="button" className="btn btn-success pull-right"><i className="fa fa-plus"></i> Add</button>
        </div>
      </div>
      );
  }
});

var CalendarSection = React.createClass({
  render: function() {
    return (
      <div className="container">
        <DaySection />
        <DaySection />
      </div>
      );
  }
});


var CalorieCounterApp = React.createClass({
  render: function() {
    return (
    <div>
      <ConfigSection />
      <CalendarSection />
    </div>
    );
  }
});


React.render(
    <CalorieCounterApp />,
    document.getElementById('calorieCounterAppPlaceholder'));
