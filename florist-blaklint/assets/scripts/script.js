let pageLang = document.getElementsByTagName('html')[0].getAttribute('lang');

let openhours = {
    "weekdays": {
        "open": 10,
        "close": 16
    },
    "saturday": {
        "open": 12,
        "close": 15
    },
    "sunday": {
        "open": "Closed",
        "close": "Closed"
    }
}
let closed_days;

if (pageLang == 'uk') {
    /* sort closed days relative to today */
    closed_days = [
        { title: 'Новий рік', month_worded: "січня", month: 1, day: 1 },
        { title: 'Тринадцятий день Різдва', month_worded: "січня", month: 1, day: 6 },
        { title: '1 травня', month_worded: "травня", month: 5, day: 1  },
        { title: 'Національний день Швеції', month_worded: "червня", month: 6, day: 6 },
        { title: 'Святвечір', month_worded: "грудня", month: 12, day: 24 },
        { title: 'Різдво', month_worded: "грудня", month: 12, day: 25 },
        { title: 'День подарунків Різдва', month_worded: "грудня", month: 12, day: 26 },
        { title: 'Переддень Нового року', month_worded: "грудня", month: 12, day: 31 }
    ];

    openhours_text = {
        "closed": "Сьогодні ми закриті",
        "closing_soon": "Ми скоро зачиняємося",
        "weekdayopenuntil": "Ми працюємо до 16:00",
        "weekdayopen": "Ми відкриваємось о 10:00",
        "weekdayclosed": "Ми відкриваємось о 10:00 завтра",
        "weekdayclosed2": "Ми відкриваємось о 12 ранку. завтра",
        "weekendopenuntil": "Ми працюємо до 15:00",
        "weekendopen": "Ми відкриваємось о 12:00",
        "weekendclosed": "Ми знову відкриваємось у понеділок о 10:00",
    }
}
else {
    /* sort closed days relative to today */
    closed_days = [
        { title: 'Nyårsdagen', month_worded: "Januari", month: 1, day: 1 },
        { title: 'Trettondedag jul', month_worded: "Januari", month: 1, day: 6 },
        { title: 'Första maj', month_worded: "Maj", month: 5, day: 1  },
        { title: 'Sveriges nationaldag', month_worded: "Juni", month: 6, day: 6 },
        { title: 'Julafton', month_worded: "December", month: 12, day: 24 },
        { title: 'Juldagen', month_worded: "December", month: 12, day: 25 },
        { title: 'Annandag jul', month_worded: "December", month: 12, day: 26 },
        { title: 'Nyårsafton', month_worded: "December", month: 12, day: 31 }
    ];

    openhours_text = {
        "closed": "Vi har stängt idag",
        "closing_soon": "Vi stänger snart",
        "weekdayopenuntil": "Vi har öppet till klockan 16 idag",
        "weekdayopen": "Vi öppnar klockan 10",
        "weekdayclosed": "Vi öppnar klockan 10 imorgon",
        "weekdayclosed2": "Vi öppnar klockan 12 imorgon",
        "weekendopenuntil": "Vi har öppet till klockan 15 idag",
        "weekendopen": "Vi öppnar klockan 12",
        "weekendclosed": "Vi öppnar igen på Måndag klockan 10",
    }
}


/* Sort closing days */
let closed_days_element = document.querySelector('.holidays');
closed_days_element.innerHTML = ''; // Clear inner table

let currentMonth = parseInt(current_date.getMonth() + 1); //get month returns a value between 0 and 11. setting +1 gets the real month number.
let currentDay = parseInt(current_date.getDate());

let dateArr = [];

let pastDates = [];
let futureDates = [];

for(let i = 0; i < closed_days.length; i++)
{
        if(closed_days[i].month <= currentMonth)
        {
            if(closed_days[i].day >= currentDay && closed_days[i].month == currentMonth)
            {
                dateArr.push(closed_days[i])
            }
            else 
            {
                pastDates.push(closed_days[i]);
            }
        }
        else 
        {
        dateArr.push(closed_days[i]);
        
        }
}
dateArr = dateArr.concat(pastDates);
for(let i = 0; i < dateArr.length; i++){
    closed_days_element.innerHTML += `
        <tr>
            <th>${dateArr[i].title}</th>
            <td></td>
            <td>${dateArr[i].day} ${dateArr[i].month_worded}</td>
        </tr>
    `
}