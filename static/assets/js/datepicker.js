function loadScript(src, callback) {
    const script = document.createElement('script');
    script.src = src;
    script.onload = callback;
    document.head.appendChild(script);
  }
  
  const link = document.createElement('link');
  link.rel = 'stylesheet';
  link.href = 'https://cdn.jsdelivr.net/npm/daterangepicker/daterangepicker.css';
  document.head.appendChild(link);
  
  loadScript('https://code.jquery.com/jquery-3.6.0.min.js', function () {
    loadScript('https://cdn.jsdelivr.net/npm/moment/min/moment.min.js', function () {
      loadScript('https://cdn.jsdelivr.net/npm/daterangepicker/daterangepicker.min.js', function () {
        $(document).ready(function () {
          $('#date-range').daterangepicker({
            locale: {
              format: 'DD/MM/YYYY',
              applyLabel: 'Áp dụng',
              cancelLabel: 'Hủy',
              customRangeLabel: 'Tùy chỉnh',
            },
            opens: 'center',
            autoUpdateInput: false,
          });
  
          $('#date-range').on('apply.daterangepicker', function (ev, picker) {
            $(this).val(picker.startDate.format('DD/MM/YYYY') + ' - ' + picker.endDate.format('DD/MM/YYYY'));
          });
  
          $('#date-range').on('cancel.daterangepicker', function (ev, picker) {
            $(this).val('');
          });
        });
      });
    });
  });
  