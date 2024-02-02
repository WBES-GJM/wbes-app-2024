/*
Template Name: Dason - Admin & Dashboard Template
Author: Themesdesign
Website: https://themesdesign.in/
Contact: themesdesign.in@gmail.com
File: Calendar init js
*/

! function ($) {
    "use strict";

    var CalendarPage = function () {};

    CalendarPage.prototype.init = function () {

            var addEvent = $("#event-modal");
            var modalTitle = $("#modal-title");
            var formEvent = $("#form-event");
            var forms = $('.needs-validation');
            var selectedEvent = null;
            var newEventData = null;
            var eventObject = null;
            /* initialize the calendar */

            var date = new Date();
            var d = date.getDate();
            var m = date.getMonth();
            var y = date.getFullYear();
            var Draggable = FullCalendarInteraction.Draggable;
            var externalEventContainerEl = document.getElementById('external-events');
            // init dragable
            new Draggable(externalEventContainerEl, {
                itemSelector: '.external-event',
                eventData: function (eventEl) {
                    return {
                        title: eventEl.innerText,
                        className: $(eventEl).data('class')
                    };
                }
            });

            // Bookings data
            // [
                // {
                //     id: 999,
                //     title: 'Repeating Event',
                //     start: new Date(y, m, d - 3, 16, 0),
                //     end: new Date(y, m, d - 2),
                //     allDay: false,
                //     url: 'http://google.com/',
                //     className: 'bg-info'
                // }
            // ];
            var fetchBookings = BOOKINGS ? JSON.parse(BOOKINGS) : [];
            var defaultEvents = [];
            var formatDate = (argsList) => {
                return new Date(
                    argsList[0],
                    argsList[1],
                    argsList[2],
                    argsList[3],
                    argsList[4],
                )
            }
            for (const bk of fetchBookings) {
                bk.start = formatDate(bk.start);
                bk.end = formatDate(bk.end);
                defaultEvents.push(bk);
            }

            // Elements
            // var draggableEl = document.getElementById('external-events');
            var calendarEl = document.getElementById('calendar');

            function addNewEvent(info) {
                // for date and time
                $('#newbooking-start-date-input').attr('min', new Date().toLocaleDateString('en-ca'));
                $('#newbooking-end-date-input').attr('min', new Date().toLocaleDateString('en-ca'));

                // preset codes
                addEvent.modal('show');
                formEvent.removeClass("was-validated");
                formEvent[0].reset();

                $("#form-client-input").val();
                $('#event-category').val();
                modalTitle.text('Add Event');
                newEventData = info;
            }


            var calendar = new FullCalendar.Calendar(calendarEl, {
                plugins: ['bootstrap', 'interaction', 'dayGrid', 'timeGrid'],
                editable: true,
                droppable: true,
                selectable: true,
                defaultView: 'dayGridMonth',
                themeSystem: 'bootstrap',
                header: {
                    left: 'prev,next today',
                    center: 'title',
                    right: 'dayGridMonth,timeGridWeek,timeGridDay,listMonth'
                },
                eventClick: function (info) {
                    // for date and time
                    $('#newbooking-start-date-input').attr('min', new Date().toLocaleDateString('en-ca'));
                    $('#newbooking-end-date-input').attr('min', new Date().toLocaleDateString('en-ca'));

                    // preset codes
                    addEvent.modal('show');
                    formEvent[0].reset();
                    selectedEvent = info.event;
                    $("#newbooking-client-input").val(selectedEvent.title); // except this
                    $('#event-category').val(selectedEvent.classNames[0]);
                    newEventData = null;
                    modalTitle.text('Edit Event');
                    newEventData = null;
                    $("#btn-delete-event").show();
                },
                dateClick: function (info) {
                    addNewEvent(info);
                },
                events: defaultEvents
            });
            calendar.render();

            /*Add new event*/
            // Form to add new event

            $(formEvent).on('submit', function (ev) {
                ev.preventDefault();
                var inputs = $('#form-event :input');
                var updatedTitle = $("#form-client-input").val();
                var updatedCategory = $('#event-category').val();

                // validation
                if (forms[0].checkValidity() === false) {
                    event.preventDefault();
                    event.stopPropagation();
                    forms[0].classList.add('was-validated');
                } else {
                    if (selectedEvent) {
                        selectedEvent.setProp("title", updatedTitle);
                        selectedEvent.setProp("classNames", [updatedCategory]);
                    } else {
                        var newEvent = {
                            title: updatedTitle,
                            start: newEventData.date,
                            allDay: newEventData.allDay,
                            className: updatedCategory
                        }
                        calendar.addEvent(newEvent);
                    }
                    addEvent.modal('hide');
                }
            });

            $("#btn-delete-event").on('click', function (e) {
                if (selectedEvent) {
                    selectedEvent.remove();
                    selectedEvent = null;
                    addEvent.modal('hide');
                }
            });

            $("#btn-new-event").on('click', function (e) {
                addNewEvent({
                    date: new Date(),
                    allDay: true,
                });
                $("#btn-delete-event").hide();
            });

        },
        //init
        $.CalendarPage = new CalendarPage, $.CalendarPage.Constructor = CalendarPage
}(window.jQuery),

//initializing 
function ($) {
    "use strict";
    $.CalendarPage.init()
}(window.jQuery);