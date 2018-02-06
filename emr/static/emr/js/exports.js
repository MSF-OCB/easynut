var export_file_ready = {};

function export_ajax_check_file_ready(url, interval, max_execution_time, done, error) {
  export_file_ready.url = url;
  export_file_ready.interval = (interval || 10) * 1000;
  export_file_ready.done = done;
  export_file_ready.error = error;
  export_file_ready.max_execution_time = max_execution_time * 1000;
  export_file_ready.execution_time = 0;
  export_ajax_is_file_ready();
}

function export_ajax_is_file_ready() {
  $.get(export_file_ready.url, function (response) {
    if (response.ready) {
      export_file_ready.done(response);
    } else {
      export_file_ready.execution_time += export_file_ready.interval;
      if (export_file_ready.execution_time < export_file_ready.max_execution_time) {
        setTimeout(export_ajax_is_file_ready, export_file_ready.interval);
      } else {
        export_file_ready.error(export_file_ready.execution_time / 1000);
      }
    }
  });
}
