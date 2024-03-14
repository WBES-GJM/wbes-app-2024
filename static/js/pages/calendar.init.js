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
        var formEvent = $("#booking-form");
        var forms = $('.needs-validation');
        var selectedEvent = null;
        var newEventData = null;
        // var eventObject = null;

        /* initialize the calendar */
        // var date = new Date();
        // var d = date.getDate();
        // var m = date.getMonth();
        // var y = date.getFullYear();
        // var externalEventContainerEl = document.getElementById('external-events');

        // init dragable - modified 2/7/2024
        var Draggable = FullCalendarInteraction.Draggable;
        const initDraggable = (parentId, childClass) => {
            new Draggable(document.getElementById(parentId), {
                itemSelector: childClass,
                eventData: function (eventEl) {
                    console.log('here!!', eventEl)
                    // return {
                    //     // title: eventEl.innerText,
                    //     // className: $(eventEl).data('class')
                    // };
                }
            });
        }

        // initDraggable('calendar', '.fc-event');

        /* Bookings data [
            {
                id: 999,
                title: 'Repeating Event',
                start: new Date(y, m, d, 16, 0),
                end: new Date(y, m, d),
                allDay: false,
                url: 'http://google.com/',
                className: 'bg-info'
            }
        ]; */

        // Elements
        // var draggableEl = document.getElementById('external-events');
        var calendarEl = document.getElementById('calendar');


        function addNewEvent(info) {
            // preset codes
            addEvent.modal('show');
            formEvent.removeClass("was-validated");
            formEvent[0].reset();

            // not preset code
            openNewBookingModal(info.date);

            // preset codes
            $("#form-client-input").val();
            $('#event-category').val();
            modalTitle.text('Add Booking');
            newEventData = info;
        }

        var initialViewOnSession = sessionStorage.getItem("calendarDefaultView");
        if (!initialViewOnSession) {
            initialViewOnSession = "dayGridMonth";
        }
        var calendar = new FullCalendar.Calendar(calendarEl, {
            plugins: ['bootstrap', 'interaction', 'dayGrid', 'timeGrid'],
            editable: true,
            droppable: true,
            selectable: true,
            eventResizableFromStart: true,
            eventDurationEditable: true,
            displayEventTime: true,
            defaultView: initialViewOnSession,
            slotDuration: '01:00:00',
            minTime: String(BUSINESS_HOURS.start)+':00:00',
            maxTime: String(BUSINESS_HOURS.end)+':00:00',
            themeSystem: 'bootstrap',
            header: {
                left: 'prev,next today',
                center: 'title',
                right: 'dayGridMonth,timeGridWeek,timeGridDay,listMonth'
            },
            eventClick: function (info) {

                // preset codes
                addEvent.modal('show');
                formEvent[0].reset();
                selectedEvent = info.event;

                // not preset codes
                openBookingModal(selectedEvent);

                // preset codes
                newEventData = null;
                modalTitle.text('Edit Booking');
                newEventData = null;

                // not preset code
                // $(".btn-cancel").show();
            },
            dateClick: function (info) {
                addNewEvent(info);
            },
            // not preset code
            eventDrop: function (info) {
                selectedEvent = info.event;
                onDateChangeBooking(selectedEvent); // in ecommerce-booking.html template
            },
            eventResize: function (info) {
                selectedEvent = info.event;
                onDateChangeBooking(selectedEvent); // in ecommerce-booking.html template
            },
            datesRender: function (info) {
                var view = info.view;
                var events = this.getEvents();
                onViewChangeBooking(view, events); // in ecommerce-booking.html template
            },
            events: BOOKINGS, // defaultEvents,
        });
        calendar.render();

        /*Add new event*/
        // Form to add new event when save button is pressed, instead of when form is submitted
        // $(formEvent).on('submit', function (ev) {
        $('#btn-save-button').on('click', function () { 
            // ev.preventDefault();
            //  var inputs = $('#booking-form :input');
            var updatedTitle = $("#newbooking-client-input").val();
            var updatedCategory = $('#event-category').val();

            // validation
            if (forms[0].checkValidity() === false) {
                // event.preventDefault();
                // event.stopPropagation();
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
                formEvent.submit();
            }
        });

        // not preset code
        $("#btn-cancel-button").on('click', function () {
            $('#cancel-booking-modal').modal('show').focus();
        });

        $("#btn-cancel-booking").on('click', function (e) {
            if (selectedEvent) {
                selectedEvent.remove();
                selectedEvent = null;
                addEvent.modal('hide');

                // not preset code
                cancelBooking();
            }
        });

        $("#btn-new-booking").on('click', function (e) {
            // not preset code
            var tomorrowsDate = new Date();
            tomorrowsDate.setDate(tomorrowsDate.getDate() + 1);

            // preset code
            addNewEvent({
                date: tomorrowsDate, // not preset
                allDay: true,
            });
            // $("#btn-cancel-booking").hide();
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