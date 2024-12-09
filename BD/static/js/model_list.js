
function getCsrfToken() {
  let match = document.cookie.split('csrftoken=')[1];
  if (match) return match;
  return null;
}
function makeEditable(element) {//при клике на ячейку она становится редактируемой
    if (user_group != "Пациенты")
    {
        const user_perm_arr_BD = user_perm.split(", ");
        const user_perm_arr = user_perm_arr_BD.map(item => item.split('.')[1]);
        model_dict = {
            "Участки":"neighborhood",
            "Пациенты":"patient",
            "Цели визита":"visit",
            "Врачи":"doctor",
            "Талоны":"ticket",
            "Диагнозы":"diagnosis"}
        if (user_perm.includes("change_"+model_dict[model]))
        {
            let list_fields = ["category","status"];
            last_data = element.innerText;
            field = element.getAttribute("Name");
            if (list_fields.includes(field))//Если ячейка имеет тип данных - перечисление
            {
                element.focus();
                dict_fields ={"category":["Первая","Вторая","Высшая"],"status":["Первичный","Вторичный"]};
                arr_fields = dict_fields[field];
                createDropdown(element,arr_fields);//то создаётся выпадающий список
                return
            }
            element.contentEditable = true;
            element.focus();
            enterIsPressed = false;//нужно т.к при вызове onkeydown вызывается сразу же onblur
            /*при потере фокуса, идёт поиск данной строки в БД,
            идёт попытка присвоить полю новое значение,
            если успешно то записывается,иначе возвращает ошибку
             */
            element.onkeydown = (event) => {if (event.key === 'Enter' && !enterIsPressed)  {enterIsPressed=true; requestTextUpdate(event, element);}}
            element.onblur = (event) => {if (!enterIsPressed) {requestTextUpdate(event, element)} enterIsPressed = false;}
        }
    }
}

function requestListUpdate (event,element,element_parent,text)
{
    children = element_parent.children;
    index = Array.prototype.indexOf.call(children, element);
    thead = document.querySelector('thead').firstElementChild;
    field_name = thead.children[index].innerText;
    let data = {
      "field":"list",
      "table_verbose_name_plural": model,
      "id": element.parentElement.firstElementChild.innerText,
      "field_name":field_name,
      "new_data":text,
    };
    sendData(data,element,"POST", "/change/",false);
}

function requestTextUpdate (event,element)
{
    element.contentEditable = false;
    children = element.parentElement.children;
    index = Array.prototype.indexOf.call(children, element);
    thead = document.querySelector('thead').firstElementChild;
    field_name = thead.children[index].innerText;
    let data = {
      "field":"text",
      "last_data":last_data,
      "table_verbose_name_plural": model,
      "id": element.parentElement.firstElementChild.innerText,
      "field_name":field_name,
      "new_data":element.innerText,
    };
    sendData(data,element,"POST", "/change/",false);
}

function sendData(data, element, method, dir, isReturn) {
    return new Promise((resolve, reject) => {
        csrfToken = getCsrfToken();
        let xhr = new XMLHttpRequest();
        xhr.open(method, dir, true);
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.setRequestHeader("X-CSRFToken", csrfToken);
        let jsonData = JSON.stringify(data);
        xhr.onload = function () {
            let response;
            if (xhr.status == 200 && isReturn) {
                response = JSON.parse(xhr.responseText);
                resolve(response); // Разрешаем промис с данными ответа
            } else {
                if (xhr.status != 304) {
                    response = JSON.parse(xhr.responseText);
                    showPopups(response.response);
                    element.classList.add('highlight-error');
                    element.innerText = last_data;
                    setTimeout(() => { element.classList.remove('highlight-error'); }, 1000);
                    reject(response); // Отклоняем промис с ошибкой
                }
            }
        };
        xhr.send(jsonData);
    });
}

function showPopup(text) {
    return new Promise((resolve) => {
        const errorsDiv = document.querySelector('.errors');
        const popup = document.createElement('div');
        popup.setAttribute('id', 'popup');
        popup.innerText = text;
        popup.style.display = "flex";
        popup.style.opacity = "1";
        errorsDiv.appendChild(popup);
        setTimeout(() => {
            popup.style.transition = "opacity 1s";
            popup.style.opacity = "0";
        }, 2000);
        setTimeout(() => {
            popup.remove();
            resolve();
        }, 3000);
    });
}

async function showPopups(text) {await showPopup(text);}


function createDropdown(element,optionsArray) {
  new_td = document.createElement('td');
  select = document.createElement('select');
  select.setAttribute('class', 'js-example-basic-single');
  select.setAttribute('name', 'state');
  option_result = optionsArray.map((value) => {
        return {
            text: String(value),
            value: String(value),
            selected: false
        };
    });
  option_result.forEach(optionText => {
    const option = document.createElement('option');
    option.textContent = optionText.text;
    select.appendChild(option);
  });
  select.selectedIndex = -1;
  par_el = element.parentElement;
  element.replaceWith(new_td);
  new_td.appendChild(select);
    $(document).ready(function() {
        $('.js-example-basic-single').select2();
    });
  select.addEventListener('change', function(event) {
    options_arr = event.target.getElementsByTagName('option')
    for (let cur_option of options_arr)
    {
        if (cur_option.selected)
            {
            requestListUpdate(event,new_td,par_el,cur_option.text)
            break;
            }
    }
});
}

function MakeAddingRow(element){
    let tableBody = document.querySelector('table tbody');
    let newRow = document.createElement('tr');
    let columnCount = tableBody.rows[0] ? tableBody.rows[0].cells.length : 0;
    sendData({"table_verbose_name_plural":model},element,"POST", "/addEmpty/", true)//теперь есть новая пустая запись, с последним id
     .then(response => {
            //new_id = response.last_id; // Например, если сервер возвращает `last_id`
            new_id = response.id
            for (let i = 0; i < columnCount; i++) {
                let newCell = document.createElement('td');
                newCell.ondblclick = function() { FillRow(this); };
                if (i==0) {newCell.textContent=new_id} else newCell.textContent = '-';
                newRow.appendChild(newCell);
            }
            tableBody.insertBefore(newRow, tableBody.firstChild);
        })
        .catch(error => {
            console.error('Ошибка при добавлении строки:', error);
        });
}

function FillRow(element){//редактируем поля
    let list_fields = ["category","status"];
    last_data = element.innerText;
    field = element.getAttribute("Name");
    if (list_fields.includes(field))
    {
        element.focus();
        dict_fields ={"category":["Первая","Вторая","Высшая"],"status":["Первичный","Вторичный"]};
        arr_fields = dict_fields[field];
        createDropdown(element,arr_fields);
        return
    }
    element.contentEditable = true;
    element.focus();
    enterIsPressed = false;//нужно т.к при вызове onkeydown вызывается сразу же onblur
    /*
    Проверка валидности,если норм то оставляем в ячейке,
    иначе анимируем красным цветом, и оставляем пред-ее значение,
    если поле валидно, то проверяем все поля если все поля валидны то сораняем
    */
    element.onkeydown = (event) => {if (event.key === 'Enter' && !enterIsPressed)  {enterIsPressed=true; requestTextUpdate(event, element);}}
    element.onblur = (event) => {if (!enterIsPressed) {requestTextUpdate(event, element)} enterIsPressed = false;}
}

function requestUpdateText (event,element,element_parent,text)
{
    children = element_parent.children;
    index = Array.prototype.indexOf.call(children, element);
    thead = document.querySelector('thead').firstElementChild;
    field_name = thead.children[index].innerText;
    let data = {
      "field":"list",
      "table_verbose_name_plural": model,
      "id": element.parentElement.firstElementChild.innerText,
      "field_name":field_name,
      "new_data":text,
    };
    sendData(data,element,"POST", "/change/",false)
    .then(response => {
            new_id = response.id
            for (let i = 0; i < columnCount; i++) {
                let newCell = document.createElement('td');
                newCell.ondblclick = function() { FillRow(this); };
                if (i==0) {newCell.textContent=new_id} else newCell.textContent = '-';
                newRow.appendChild(newCell);
            }
            tableBody.insertBefore(newRow, tableBody.firstChild);
        })
}