
var ConfigSection = React.createClass({

  handleChangeCalories: function(event) {
    console.log('handleCaloriesChange()');
    console.log('expectedDailyCalories input: ' + this.refs.expectedDailyCaloriesInput);

    this.props.updateExpectedDailyCalories(this.refs.expectedDailyCaloriesInput.getDOMNode().value);
  },

  render: function() {
    return (
      <div className="container">
        <div className="row">
          <div className="col-md-12">
            <h2>Expected daily calories</h2>
            <form className="form-inline">
              <div className="form-group">
                <label className="sr-only" htmlFor="expectedDailyCalories">From date</label>
                <input type="number" className="form-control" step={100}
                       id="expectedDailyCalories"
                       ref="expectedDailyCaloriesInput"
                       value={this.props.expectedDailyCalories}
                       onChange={this.handleChangeCalories} ></input>
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
                <input type="date" className="form-control" id="inputFromDate" value={this.props.fromDate}></input>
              </div>
              <div className="form-group">
                <label className="sr-only" htmlFor="inputToDate">To date</label>
                <input type="date" className="form-control" id="inputToDate" value={this.props.toDate}></input>
              </div>
            </form>
          </div>
          <div className="col-md-6">
            <h2>Filter Time</h2>
            <form className="form-inline">
              <div className="form-group">
                <label className="sr-only" htmlFor="inputFromTime">From time</label>
                <input type="time" className="form-control" id="inputFromTime" value={this.props.fromTime}></input>
              </div>
              <div className="form-group">
                <label className="sr-only" htmlFor="inputToTime">To time</label>
                <input type="time" className="form-control" id="inputToTime" value={this.props.toTime}></input>
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
    console.log('totalCalories ' + this.props.totalCalories + ' expectedDailyCalories ' + this.props.expectedDailyCalories);
    if(this.props.totalCalories <= this.props.expectedDailyCalories) {
      var colourClass = "highlight-green";
    }
    else {
      var colourClass = "highlight-red";
    }

    return (
        <h2>{this.props.date} <span className={"small " + colourClass}> total calories: {this.props.totalCalories}</span></h2>
      );
  }
});

var MealRow = React.createClass({
  render: function() {
    return (
      <tr>
        <td>{this.props.time}</td>
        <td>{this.props.description}</td>
        <td>{this.props.calories}</td>
        <td><i className="fa fa-times"></i></td>
      </tr>
    );
  }
});

var MealsTable = React.createClass({
  render: function() {
    var mealRows = [];
    this.props.meals.forEach(function(meal) {
      mealRows.push(<MealRow id={meal.id} time={meal.time} description={meal.description} calories={meal.calories} />);
    });
    return (
      <table className="table">
        <tbody>
          {mealRows}
        </tbody>
      </table>
      );
  }
});

var DaySection = React.createClass({
  render: function() {
    var totalCalories = 0;
    this.props.meals.forEach(function(meal) {
      totalCalories += meal.calories;
    });

    console.log(totalCalories);

    return (
      <div className="row">

        <div className="col-md-12">
          <DayTitle date={this.props.date}
                    totalCalories={totalCalories}
                    expectedDailyCalories={this.props.expectedDailyCalories} />
          <MealsTable meals={this.props.meals} />

          <button type="button" className="btn btn-success pull-right"><i className="fa fa-plus"></i> Add</button>
        </div>
      </div>
      );
  }
});

var CalendarSection = React.createClass({
  render: function() {
    var mealsByDate = {};

    this.props.meals.forEach(function(meal) {
      var date = meal['date'];
      (mealsByDate[date] = mealsByDate[date] || []).push(meal);
    }.bind(this));

    console.log(mealsByDate);

    var daySections = [];

    for(var date in mealsByDate) {
      if(!mealsByDate.hasOwnProperty(date)) {
        continue;
      }
      daySections.push(<DaySection date={date} meals={mealsByDate[date]} expectedDailyCalories={this.props.expectedDailyCalories} />);
    }

    return (
      <div className="container">
        {daySections}
      </div>
      );
  }
});


var CalorieCounterApp = React.createClass({
  getInitialState: function() {
    var dateNow = moment();
    var thirtyDaysAgo = moment(dateNow).subtract(30, 'days');

    return {
      token: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE0MzUwNjU4MzEsInVzZXJuYW1lIjoiYm9iIiwiZW1haWwiOiIiLCJ1c2VyX2lkIjoyfQ.8NyoDbtR-UqxqUP9M5BFFQlWrbImL37FuAv4nv2uFNw',
      username: 'bob',
      meals: [],
      expectedDailyCalories: 2000,
      fromDate: thirtyDaysAgo.format(DATE_FORMAT),
      toDate: dateNow.format(DATE_FORMAT),
      fromTime: '00:00',
      toTime: '23:59'
    }
  },

  componentDidMount: function() {
    this.requestMealsForUser();
  },

  requestMealsForUser: function() {

    var url = API + '/users/' + this.state.username + '/meals/?';
    url += $.param({
      to_date: this.state.toDate,
      from_date: this.state.fromDate,
      to_time: this.state.toTime,
      from_time: this.state.fromTime
   });

    console.log(url);

    $.ajax({
      url: url,
      beforeSend: function(xhr) {
        xhr.setRequestHeader("Authorization", "Bearer " + this.state.token);
      }.bind(this),
      dataType: 'json',
      cache: false,
      success: function(data) {
        this.setState({meals: data});
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },

  updateExpectedDailyCalories: function(newExpectedDailyCalories) {
    console.log('updateExpectedDailyCalories ' + newExpectedDailyCalories);
    this.setState({expectedDailyCalories: newExpectedDailyCalories});
  },

  render: function() {
    console.log('fromDate: ' + this.state.fromDate + ' toDate: ' + this.state.toDate);

    return (
    <div>
      <ConfigSection expectedDailyCalories={this.state.expectedDailyCalories}
                     fromDate={this.state.fromDate}
                     toDate={this.state.toDate}
                     fromTime={this.state.fromTime}
                     toTime={this.state.toTime}
                     updateExpectedDailyCalories={this.updateExpectedDailyCalories} />
      <CalendarSection meals={this.state.meals}
                       expectedDailyCalories={this.state.expectedDailyCalories}/>
    </div>
    );
  }
});


var API = 'http://localhost:8000';
var DATE_FORMAT = 'YYYY-MM-DD';

React.render(
    <CalorieCounterApp />,
    document.getElementById('calorieCounterAppPlaceholder'));
