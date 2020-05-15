ready(function () {
    bulmaCalendar.attach('.bulmaCalendar');

    bulmaCalendar.attach('#booking_date', {
        labelFrom: 'Check-in',
        labelTo: 'Check-out',
        cancelLabel: 'Batal',
        validateLabel: 'Ok',
        todayLabel: 'Sekarang',
        displayMode: 'dialog'
    });
});