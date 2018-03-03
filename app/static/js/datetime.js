$('#timepicker').datetimepicker().on('show.timepicker', function(e) {
    console.log('The time is ' + e.time.value);
    console.log('The hour is ' + e.time.hours);
    console.log('The minute is ' + e.time.minutes);
    console.log('The meridian is ' + e.time.meridian);
  });

