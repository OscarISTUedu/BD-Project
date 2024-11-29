function makeEditable(element) {
            if (user_group != "Пациенты")
            {
            const user_perm_arr_BD = user_perm.split(", ");
            const user_perm_arr = user_perm_arr_BD.map(item => item.split('.')[1]);
            console.log(user_perm_arr);
            model_dict = {
                "Участки":"neighborhood",
                "Пациенты":"patient",
                "Цели визита":"visit",
                "Врачи":"doctor",
                "Талоны":"ticket",
                "Диагнозы":"diagnosis"}
            console.log("change_"+model_dict[model]);
            if (user_perm.includes("change_"+model_dict[model]))
            {
                element.contentEditable = true;  // Делаем элемент редактируемым
                element.focus();  // Сразу устанавливаем фокус на элементе
                // Добавляем обработчик для завершения редактирования при потере фокуса
                element.onblur = function() {
                    element.contentEditable = false;  // Отключаем редактирование
                    // Здесь можно добавить AJAX-запрос для сохранения изменений на сервере
                    //saveData(element.innerText);
                }
            }
            }
        }
