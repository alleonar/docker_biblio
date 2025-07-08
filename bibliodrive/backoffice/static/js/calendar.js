document.addEventListener('DOMContentLoaded', function () {
    // Recup les données de reservation s'il y en a
    const titleResaData = document.getElementById('title_resa_data').dataset.titleresa;
    console.log(typeof titleResaData);

    let titleResa = [];
    if (titleResaData && titleResaData !== "null" && titleResaData !== "") {
        titleResa = JSON.parse(titleResaData);
    }
    console.log(titleResa);

    const options = {
        settings: {
            selection: {
                day: 'multiple-ranged',
            },
            range: {
                min: 'today',
                disabled: titleResa,
                disableGaps: true,
            },
        },
        actions: {
            clickDay(event, self) {
                console.log(self.selectedDates);

                if (self.selectedDates.length >= 2) {
                    const startDate = self.selectedDates[0];
                    const endDate = self.selectedDates[self.selectedDates.length - 1];

                    // Mettre à jour les champs de date de début et de fin
                    const startField = document.getElementById('start_date');
                    const endField = document.getElementById('end_date');

                    if (startField && endField) {
                        startField.value = startDate;  // Date de début
                        endField.value = endDate;      // Date de fin
                    } else {
                        console.error('Les champs de date de début ou de fin sont introuvables.');
                    }
                }
            },
        },
    };

    const calendar = new VanillaCalendar('#calendar', options);
    calendar.init();
});
