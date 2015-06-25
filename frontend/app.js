"use strict";

var ConfigSection = React.createClass({

  handleChangeCalories: function(event) {
    this.props.updateExpectedDailyCalories(this.refs.expectedDailyCaloriesInput.getDOMNode().value);
  },

  handleChangeDateTime: function(event) {
    this.props.updateDateTimeFilters({
      fromDate: this.refs.fromDateInput.getDOMNode().value,
      toDate: this.refs.toDateInput.getDOMNode().value,
      fromTime: this.refs.fromTimeInput.getDOMNode().value,
      toTime: this.refs.toTimeInput.getDOMNode().value
    });
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
                <input type="number" className="form-control" step={DEFAULT_STEP}
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
                <label className="sr-only" htmlFor="fromDateInput">From date</label>
                <input type="date" className="form-control" id="fromDateInput"
                       ref="fromDateInput"
                       value={this.props.fromDate}
                       onChange={this.handleChangeDateTime} ></input>
              </div>
              <div className="form-group">
                <label className="sr-only" htmlFor="toDateInput">To date</label>
                <input type="date" className="form-control" id="toDateInput"
                       ref="toDateInput"
                       value={this.props.toDate}
                       onChange={this.handleChangeDateTime}></input>
              </div>
            </form>
          </div>
          <div className="col-md-6">
            <h2>Filter Time</h2>
            <form className="form-inline">
              <div className="form-group">
                <label className="sr-only" htmlFor="fromTimeInput">From time</label>
                <input type="time" className="form-control" id="fromTimeInput"
                       ref="fromTimeInput"
                       value={this.props.fromTime}
                       onChange={this.handleChangeDateTime} ></input>
              </div>
              <div className="form-group">
                <label className="sr-only" htmlFor="toTimeInput">To time</label>
                <input type="time" className="form-control" id="toTimeInput"
                       ref="toTimeInput"
                       value={this.props.toTime}
                       onChange={this.handleChangeDateTime}></input>
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
  handleClickDelete: function() {
    this.props.deleteMealId(this.props.id);
  },

  handleChange: function() {
    // Change locally, but don't update server until focus is lost on an
    // element (blur)

    this.props.updateMealId(this.props.id, this.getMealData(), false);
  },

  handleBlur: function() {
    this.props.updateMealId(this.props.id, this.getMealData(), true);
  },

  getMealData: function() {
    return {
      id: this.props.id,
      date: this.props.date,
      time: this.refs.mealTimeInput.getDOMNode().value,
      description: this.refs.mealDescriptionInput.getDOMNode().value,
      calories: parseInt(this.refs.mealCaloriesInput.getDOMNode().value)
    };
  },

  render: function() {
    return (
      <tr>
        <td>
          <input className="stealth-input"
                 type="time"
                 value={this.props.time}
                 onChange={this.handleChange}
                 onBlur={this.handleBlur}
                 ref='mealTimeInput' />
        </td>
        <td>
          <input className="stealth-input"
                 type="description"
                 value={this.props.description}
                 onChange={this.handleChange}
                 onBlur={this.handleBlur}
                 ref='mealDescriptionInput' />
        </td>
        <td>
          <input className="stealth-input"
                 type="number"
                 step={DEFAULT_STEP}
                 value={this.props.calories}
                 onChange={this.handleChange}
                 onBlur={this.handleBlur}
                 ref='mealCaloriesInput' />
        </td>

        <td><i className="fa fa-times" onClick={this.handleClickDelete}></i></td>
      </tr>
    );
  }
});

var MealsTable = React.createClass({
  render: function() {
    var mealRows = [];
    this.props.meals.forEach(function(meal) {
      mealRows.push(
        <MealRow id={meal.id}
                 date={meal.date}
                 time={meal.time}
                 description={meal.description}
                 calories={meal.calories}
                 deleteMealId={this.props.deleteMealId}
                 updateMealId={this.props.updateMealId} />);
    }.bind(this));
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

    return (
      <div className="row">

        <div className="col-md-12">
          <DayTitle date={this.props.date}
                    totalCalories={totalCalories}
                    expectedDailyCalories={this.props.expectedDailyCalories} />
          <MealsTable meals={this.props.meals}
                      deleteMealId={this.props.deleteMealId}
                      updateMealId={this.props.updateMealId} />
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

    var daySections = [];

    for(var date in mealsByDate) {
      if(!mealsByDate.hasOwnProperty(date)) {
        continue;
      }
      daySections.push(<DaySection date={date}
                                   meals={mealsByDate[date]}
                                   expectedDailyCalories={this.props.expectedDailyCalories}
                                   deleteMealId={this.props.deleteMealId}
                                   updateMealId={this.props.updateMealId} />);
    }

    return (
      <div className="container">
        {daySections}
      </div>
      );
  }
});


var AddMealSection = React.createClass({

  handleAddButton: function() {
    this.props.addMeal({
      date: this.refs.newMealDateInput.getDOMNode().value,
      time: this.refs.newMealTimeInput.getDOMNode().value,
      description: this.refs.newMealDescriptionInput.getDOMNode().value,
      calories: this.refs.newMealCaloriesInput.getDOMNode().value
    });
  },

  render: function() {
    return (
      <div className="container">
        <h3>Add a meal</h3>
        <form className="form-inline">
          <div className="form-group">
            <label className="sr-only" htmlFor="expectedDailyCalories">From date</label>
            <input type="date" className="form-control"
                   defaultValue={moment().format(DATE_FORMAT)}
                   id="newMealDateInput"
                   ref="newMealDateInput" />

            <input type="time" className="form-control"
                   defaultValue={moment().format('HH:[00]')}
                   id="newMealTimeInput"
                   ref="newMealTimeInput" />

            <input type="text" className="form-control"
                   placeholder="Enter description..."
                   id="newMealDescriptionInput"
                   ref="newMealDescriptionInput" />

            <input type="number" className="form-control"
                   defaultValue={DEFAULT_CALORIES}
                   step={DEFAULT_STEP}
                   id="newMealCaloriesInput"
                   ref="newMealCaloriesInput" />

            <a className="btn btn-success" onClick={this.handleAddButton} >
              <i className="fa fa-plus"></i> Add
            </a>
          </div>
        </form>
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
    this.loadUserConfig();
    this.requestMealsForUser(null);
  },

  loadUserConfig() {

    this.callApi({
        method: 'GET',
        partialUrl: '/users/' + this.state.username + '/',
        success: function(data) {
          this.setState({expectedDailyCalories: data['expected_daily_calories']})
        }.bind(this)
    });
  },

  requestMealsForUser: function(config) {

    if(null == config) {
      config = {
        fromDate: this.state.fromDate,
        toDate: this.state.toDate,
        fromTime: this.state.fromTime,
        toTime: this.state.toTime
      };
    }

    var url = '/users/' + this.state.username + '/meals/?';
    url += $.param({
      to_date: config.toDate,
      from_date: config.fromDate,
      to_time: config.toTime,
      from_time: config.fromTime
    });

    this.callApi({
        partialUrl: url,
        success: function(data) {
          this.setState({meals: data});
        }.bind(this)
    });
  },

  updateExpectedDailyCalories: function(newExpectedDailyCalories) {
    this.setState({expectedDailyCalories: newExpectedDailyCalories});

    var data = {
      'username': this.state.username,
      'expected_daily_calories': newExpectedDailyCalories
    }

    this.callApi({
        method: 'PUT',
        partialUrl: '/users/' + this.state.username + '/',
        data: data,
        success: function(data) {
          console.log('Successfully updated user expected_daily_calories');
          this.setState({expectedDailyCalories: data['expected_daily_calories']});
        }.bind(this)
    });
  },

  updateDateTimeFilters: function(config) {
    console.log('updateDateTimeFilters ' + config.fromDate + ' '
                + config.toDate + ' ' + config.fromTime + ' ' + config.toTime);

    this.setState({
      fromDate: config.fromDate,
      toDate: config.toDate,
      fromTime: config.fromTime,
      toTime: config.toTime
    });

    this.requestMealsForUser(config);
  },

  addMeal: function(mealData) {
    this.callApi({
        method: 'POST',
        partialUrl: '/users/' + this.state.username + '/meals/',
        data: mealData,
        success: function(data) {
          this.requestMealsForUser(null);
        }.bind(this)
    });
  },

  deleteMealId: function(mealId) {
    console.log('Delete meal ID ' + mealId);

    this.callApi({
        method: 'DELETE',
        partialUrl: '/users/' + this.state.username + '/meals/' + mealId + '/',
        success: function(data) {
          this.requestMealsForUser(null);
        }.bind(this)
    });
  },

  updateMealId: function(mealId, updatedMeal, saveToApi) {
    console.log('Update meal ID ' + mealId);
    console.log(updatedMeal);

    var newMeals = [];
    this.state.meals.forEach(function(meal) {
      if(mealId == meal.id) {
        newMeals.push(updatedMeal);
      } else {
        newMeals.push(meal);
      }
    });

    this.setState({meals: newMeals});

    if(saveToApi) {
      this.callApi({
        method: 'PUT',
        partialUrl: '/users/' + this.state.username + '/meals/' + mealId + '/',
        data: updatedMeal,
        success: function(data) {
          this.requestMealsForUser(null);
        }.bind(this)
      });
    }
  },

  callApi: function(settings) {
    settings.url = API + settings.partialUrl;

    settings.dataType = 'json',
    settings.cache = false;
    settings.error = function(xhr, status, err) {
      console.error(settings.url, status, err.toString());
    }.bind(this)

   settings.beforeSend = function(xhr) {
        xhr.setRequestHeader("Authorization", "Bearer " + this.state.token);
    }.bind(this),

    console.log(settings);
    $.ajax(settings);
  },

  render: function() {

    return (
    <div>
      <ConfigSection expectedDailyCalories={this.state.expectedDailyCalories}
                     fromDate={this.state.fromDate}
                     toDate={this.state.toDate}
                     fromTime={this.state.fromTime}
                     toTime={this.state.toTime}
                     updateExpectedDailyCalories={this.updateExpectedDailyCalories}
                     updateDateTimeFilters={this.updateDateTimeFilters} />
      <CalendarSection meals={this.state.meals}
                       expectedDailyCalories={this.state.expectedDailyCalories}
                       deleteMealId={this.deleteMealId}
                       updateMealId={this.updateMealId} />
      <AddMealSection addMeal={this.addMeal} />
    </div>
    );
  }
});


var API = 'http://localhost:8000';
var DATE_FORMAT = 'YYYY-MM-DD';
var DEFAULT_STEP = 100;
var DEFAULT_CALORIES = 500;

React.render(
    <CalorieCounterApp />,
    document.getElementById('calorieCounterAppPlaceholder'));
